#!/usr/bin/env python3
"""Poll GitHub issues and emit the next auto-implement candidate as JSON."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


LABEL_NAME = "auto-implement"
PROCESSING_MARKER = "[ai-auto-dev] processing"
FAILED_MARKER = "[ai-auto-dev] failed"
DEFAULT_INTERVAL_SECONDS = 300
MAX_SLUG_WORDS = 5


@dataclass(frozen=True)
class Issue:
    number: int
    title: str
    body: str
    url: str


@dataclass(frozen=True)
class PullRequest:
    number: int
    title: str
    body: str
    url: str


@dataclass(frozen=True)
class Candidate:
    issue: Issue
    slug: str
    branch_name: str
    existing_branch: str | None
    existing_pr_url: str | None

    def to_json(self) -> dict[str, object]:
        return {
            "issue_number": self.issue.number,
            "issue_title": self.issue.title,
            "issue_body": self.issue.body,
            "issue_url": self.issue.url,
            "slug": self.slug,
            "branch_name": self.branch_name,
            "worktree_name": self.branch_name,
            "existing_branch": self.existing_branch,
            "existing_pr_url": self.existing_pr_url,
        }


def run_json_command(args: list[str], *, cwd: Path | None = None) -> object:
    result = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def list_open_issues() -> list[Issue]:
    raw = run_json_command(
        [
            "gh",
            "issue",
            "list",
            "--state",
            "open",
            "--label",
            LABEL_NAME,
            "--limit",
            "100",
            "--json",
            "number,title,body,url",
        ]
    )
    issues = [Issue(**item) for item in raw]
    return sorted(issues, key=lambda issue: issue.number)


def list_open_pull_requests() -> list[PullRequest]:
    raw = run_json_command(
        [
            "gh",
            "pr",
            "list",
            "--state",
            "open",
            "--limit",
            "100",
            "--json",
            "number,title,body,url",
        ]
    )
    return [PullRequest(**item) for item in raw]


def load_issue_comments(number: int) -> list[str]:
    raw = run_json_command(
        [
            "gh",
            "issue",
            "view",
            str(number),
            "--json",
            "comments",
        ]
    )
    comments = raw.get("comments", [])
    bodies: list[str] = []
    for comment in comments:
        body = comment.get("body", "")
        if isinstance(body, str):
            bodies.append(body)
    return bodies


def is_processing_issue(comment_bodies: Iterable[str]) -> bool:
    return any(PROCESSING_MARKER in body for body in comment_bodies)


def is_failed_issue(comment_bodies: Iterable[str]) -> bool:
    return any(FAILED_MARKER in body for body in comment_bodies)


def derive_slug(text: str, max_words: int = MAX_SLUG_WORDS) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    words = re.findall(r"[a-z0-9]+", normalized.lower())
    filtered = [word for word in words if word not in {"the", "and", "or", "to", "for", "a", "an", "of", "in", "on"}]
    if not filtered:
        return "issue"
    return "-".join(filtered[:max_words])


def branch_name_for(issue_number: int, title: str, body: str) -> str:
    source = f"{title.strip()} {body.strip()}".strip() or f"issue {issue_number}"
    return f"issue-{issue_number}-{derive_slug(source)}"


def list_local_branches(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "for-each-ref", "refs/heads", "--format=%(refname:short)"],
        cwd=str(repo_root),
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def find_existing_branch(branches: Iterable[str], issue_number: int) -> str | None:
    prefix = f"issue-{issue_number}-"
    for branch in branches:
        if branch.startswith(prefix):
            return branch
    return None


def find_existing_pr(issue: Issue, prs: Iterable[PullRequest]) -> PullRequest | None:
    needle = f"Closes #{issue.number}"
    fallback = f"#{issue.number}"
    for pr in prs:
        body = pr.body or ""
        title = pr.title or ""
        if needle in body or fallback in body or fallback in title:
            return pr
    return None


def select_candidate(repo_root: Path) -> Candidate | None:
    issues = list_open_issues()
    prs = list_open_pull_requests()
    local_branches = list_local_branches(repo_root)

    for issue in issues:
        comment_bodies = load_issue_comments(issue.number)
        if is_processing_issue(comment_bodies):
            continue
        if is_failed_issue(comment_bodies):
            continue

        slug = derive_slug(f"{issue.title} {issue.body}".strip() or f"issue {issue.number}")
        branch_name = find_existing_branch(local_branches, issue.number)
        if branch_name is None:
            branch_name = branch_name_for(issue.number, issue.title, issue.body)

        existing_pr = find_existing_pr(issue, prs)
        return Candidate(
            issue=issue,
            slug=slug,
            branch_name=branch_name,
            existing_branch=find_existing_branch(local_branches, issue.number),
            existing_pr_url=existing_pr.url if existing_pr else None,
        )

    return None


def poll_forever(interval_seconds: int, repo_root: Path) -> Candidate:
    while True:
        try:
            candidate = select_candidate(repo_root)
        except subprocess.CalledProcessError as exc:
            print(f"poll failed: {exc}", file=sys.stderr)
            time.sleep(interval_seconds)
            continue

        if candidate is not None:
            return candidate

        print(
            f"[ai-auto-dev] no eligible issue found; sleeping {interval_seconds}s",
            file=sys.stderr,
        )
        time.sleep(interval_seconds)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL_SECONDS,
        help="Polling interval in seconds. Default: 300.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Check once and exit with status 1 if no issue is ready.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = Path.cwd()

    if args.once:
        candidate = select_candidate(repo_root)
        if candidate is None:
            return 1
    else:
        candidate = poll_forever(args.interval, repo_root)

    json.dump(candidate.to_json(), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
