#!/usr/bin/env python3
"""Validate an acceptance-harness manifest and optional Git immutability."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

CRITERION_ID = re.compile(r"AC-[A-Z0-9][A-Z0-9-]*$")
REQUIRED_ARTIFACT_FIELDS = ("kind", "build_command", "consumer_command")


def load_manifest(path: str) -> tuple[dict[str, Any], Path | None]:
    if path == "-":
        raw = sys.stdin.read()
        source = None
    else:
        source = Path(path).resolve()
        raw = source.read_text(encoding="utf-8")

    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")

    return data, source


def require_string(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")


def require_relative_path(value: Any, label: str, errors: list[str]) -> None:
    require_string(value, label, errors)
    if not isinstance(value, str):
        return

    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{label} must be a repository-relative path")


def validate(data: dict[str, Any], frozen: bool, repo_root: Path) -> list[str]:
    errors: list[str] = []
    if data.get("version") != 1:
        errors.append("version must equal 1")

    artifact = data.get("artifact")
    if not isinstance(artifact, dict):
        errors.append("artifact must be an object")
    else:
        for field in REQUIRED_ARTIFACT_FIELDS:
            require_string(artifact.get(field), f"artifact.{field}", errors)

    risks = data.get("risks", [])
    if not isinstance(risks, list) or not all(isinstance(risk, str) for risk in risks):
        errors.append("risks must be a list of strings")
        risks = []

    immutable_paths = data.get("immutable_paths")
    if not isinstance(immutable_paths, list) or not immutable_paths:
        errors.append("immutable_paths must be a non-empty list")
        immutable_paths = []

    for index, path in enumerate(immutable_paths):
        require_relative_path(path, f"immutable_paths[{index}]", errors)
        if frozen and isinstance(path, str) and not (repo_root / path).is_file():
            errors.append(f"immutable path does not exist: {path}")

    criteria = data.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        errors.append("criteria must be a non-empty list")
        criteria = []

    ids: set[str] = set()
    tags: set[str] = set()
    immutable = set(path for path in immutable_paths if isinstance(path, str))
    for index, criterion in enumerate(criteria):
        prefix = f"criteria[{index}]"
        if not isinstance(criterion, dict):
            errors.append(f"{prefix} must be an object")
            continue

        criterion_id = criterion.get("id")
        if not isinstance(criterion_id, str) or not CRITERION_ID.fullmatch(
            criterion_id
        ):
            errors.append(f"{prefix}.id must match AC-*")
        elif criterion_id in ids:
            errors.append(f"duplicate criterion id: {criterion_id}")
        else:
            ids.add(criterion_id)

        if criterion.get("required") is not True:
            errors.append(f"{prefix}.required must be true")
        for field in ("scenario", "command", "oracle"):
            require_string(criterion.get(field), f"{prefix}.{field}", errors)
        test_path = criterion.get("test_path")
        require_relative_path(test_path, f"{prefix}.test_path", errors)
        if isinstance(test_path, str):
            if test_path not in immutable:
                errors.append(f"{prefix}.test_path must appear in immutable_paths")
            if frozen and not (repo_root / test_path).is_file():
                errors.append(f"test file does not exist: {test_path}")

        criterion_tags = criterion.get("tags", [])
        if not isinstance(criterion_tags, list) or not all(
            isinstance(tag, str) for tag in criterion_tags
        ):
            errors.append(f"{prefix}.tags must be a list of strings")
        else:
            tags.update(criterion_tags)

    required_tags = {
        "destructive": "rejection-no-side-effect",
        "external-artifact": "consumer-entry",
        "module-identity": "module-identity",
    }
    for risk, required_tag in required_tags.items():
        if risk in risks and required_tag not in tags:
            errors.append(f"risk {risk!r} requires a criterion tagged {required_tag!r}")

    return errors


def changed_paths(repo_root: Path, base: str, paths: list[str]) -> list[str]:
    commands = [
        ["git", "diff", "--name-only", base, "--", *paths],
        ["git", "diff", "--name-only", "--", *paths],
    ]
    changed: set[str] = set()
    for command in commands:
        result = subprocess.run(
            command, cwd=repo_root, capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            raise ValueError(
                result.stderr.strip() or f"failed to run {' '.join(command)}"
            )
        changed.update(line for line in result.stdout.splitlines() if line)

    return sorted(changed)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="manifest JSON path, or - for stdin")
    parser.add_argument("--stage", choices=("plan", "frozen"), required=True)
    parser.add_argument(
        "--repo-root", default=".", help="repository root for --stage frozen"
    )
    parser.add_argument(
        "--base", help="frozen Git base revision used to detect harness edits"
    )
    args = parser.parse_args()

    try:
        data, _ = load_manifest(args.manifest)
        repo_root = Path(args.repo_root).resolve()
        errors = validate(data, args.stage == "frozen", repo_root)
        immutable_paths = [
            path for path in data.get("immutable_paths", []) if isinstance(path, str)
        ]
        if args.base:
            if args.stage != "frozen":
                errors.append("--base requires --stage frozen")
            elif not errors:
                changed = changed_paths(repo_root, args.base, immutable_paths)
                if changed:
                    errors.append("immutable paths changed: " + ", ".join(changed))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"PASS: acceptance harness manifest is valid for stage {args.stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
