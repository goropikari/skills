from pathlib import Path
import importlib.util
import sys


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "poll.py"
spec = importlib.util.spec_from_file_location("ai_auto_dev_poll", MODULE_PATH)
poll = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = poll
spec.loader.exec_module(poll)


def test_derive_slug_prefers_short_ascii_words():
    assert poll.derive_slug("Add OAuth login flow for the admin console!") == (
        "add-oauth-login-flow-admin"
    )


def test_branch_name_for_uses_issue_number_and_slug():
    assert poll.branch_name_for(42, "Fix login flow", "") == "issue-42-fix-login-flow"


def test_issue_state_helpers_detect_processing_and_failed_markers():
    assert poll.is_processing_issue(["hello", poll.PROCESSING_MARKER])
    assert poll.is_failed_issue(["hello", poll.FAILED_MARKER])
    assert not poll.is_processing_issue(["hello"])
    assert not poll.is_failed_issue(["hello"])


def test_select_candidate_skips_processing_and_failed_issues(monkeypatch, tmp_path):
    monkeypatch.setattr(
        poll,
        "list_open_issues",
        lambda: [
            poll.Issue(1, "First issue", "body", "https://example.invalid/1"),
            poll.Issue(2, "Second issue", "body", "https://example.invalid/2"),
            poll.Issue(3, "Third issue", "body", "https://example.invalid/3"),
        ],
    )
    monkeypatch.setattr(
        poll,
        "list_open_pull_requests",
        lambda: [
            poll.PullRequest(
                10,
                "Implement second issue",
                "Closes #2",
                "https://example.invalid/pr/10",
            )
        ],
    )
    comments = {
        1: [poll.PROCESSING_MARKER],
        2: [],
        3: [poll.FAILED_MARKER],
    }
    monkeypatch.setattr(poll, "load_issue_comments", lambda number: comments[number])
    monkeypatch.setattr(
        poll,
        "list_local_branches",
        lambda repo_root: ["issue-2-second-issue", "main"],
    )

    candidate = poll.select_candidate(tmp_path)

    assert candidate is not None
    assert candidate.issue.number == 2
    assert candidate.branch_name == "issue-2-second-issue"
    assert candidate.existing_branch == "issue-2-second-issue"
    assert candidate.existing_pr_url == "https://example.invalid/pr/10"

