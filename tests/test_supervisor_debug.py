from importlib.machinery import SourceFileLoader
import importlib.util
from pathlib import Path
import sys


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "bin" / "ai-auto-dev-supervisor"
).resolve()
loader = SourceFileLoader("ai_auto_dev_supervisor_debug", str(MODULE_PATH))
spec = importlib.util.spec_from_loader(loader.name, loader)
supervisor = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = supervisor
spec.loader.exec_module(supervisor)


def test_select_candidate_debug_reports_fresh_processing_lock(
    monkeypatch, capsys, tmp_path
):
    monkeypatch.setattr(
        supervisor,
        "list_open_issues",
        lambda label_name: [
            supervisor.Issue(
                3,
                "Fix login flow",
                "\n".join(
                    [
                        "The login button on the settings page stops working after a session timeout.",
                        "Repro:",
                        "1. Sign in.",
                        "2. Wait until the session expires.",
                        "3. Open settings and click login again.",
                    ]
                ),
                "https://example.invalid/3",
            ),
        ],
    )
    monkeypatch.setattr(supervisor, "list_open_pull_requests", lambda: [])
    monkeypatch.setattr(supervisor, "list_local_branches", lambda repo_root: [])
    monkeypatch.setattr(
        supervisor,
        "load_issue_comments",
        lambda repo_name, number: [
            {
                "body": "\n".join(
                    [
                        supervisor.PROCESSING_MARKER,
                        "claimed_at: 2026-07-12T12:00:00Z",
                    ]
                ),
                "created_at": "2026-07-12T12:00:00Z",
            }
        ],
    )
    monkeypatch.setattr(
        supervisor,
        "utc_now",
        lambda: supervisor.dt.datetime(
            2026, 7, 12, 12, 10, tzinfo=supervisor.dt.timezone.utc
        ),
    )

    candidate = supervisor.select_candidate(
        tmp_path,
        "example/target",
        supervisor.SupervisorState(),
        label_name=supervisor.LABEL_NAME,
        stale_after_seconds=1800,
        debug=True,
    )

    captured = capsys.readouterr()

    assert candidate is None
    assert "found 1 open issue(s) with label auto-implement" in captured.err
    assert "skipping issue #3: processing lock is fresh" in captured.err
    assert "matched processing comment id=" in captured.err
    assert "no eligible issue found" in captured.err


def test_reset_state_deletes_cached_state(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text('{"completed_issue_numbers":[3]}')

    supervisor.reset_state(state_file)

    assert not state_file.exists()


def test_select_candidate_asks_for_clarification_once(monkeypatch, tmp_path):
    monkeypatch.setattr(
        supervisor,
        "list_open_issues",
        lambda label_name: [
            supervisor.Issue(
                3, "Fix login flow", "Need help", "https://example.invalid/3"
            ),
        ],
    )
    monkeypatch.setattr(supervisor, "list_open_pull_requests", lambda: [])
    monkeypatch.setattr(supervisor, "list_local_branches", lambda repo_root: [])
    monkeypatch.setattr(supervisor, "load_issue_comments", lambda repo_name, number: [])
    comments = []
    monkeypatch.setattr(
        supervisor,
        "issue_comment",
        lambda repo_name, number, body: comments.append((repo_name, number, body)),
    )

    candidate = supervisor.select_candidate(
        tmp_path,
        "example/target",
        supervisor.SupervisorState(),
        label_name=supervisor.LABEL_NAME,
        stale_after_seconds=1800,
        debug=False,
    )

    assert candidate is None
    assert comments == [
        (
            "example/target",
            3,
            supervisor.make_clarification_comment(
                supervisor.Issue(
                    3, "Fix login flow", "Need help", "https://example.invalid/3"
                )
            ),
        )
    ]


def test_select_candidate_does_not_repeat_pending_clarification(monkeypatch, tmp_path):
    monkeypatch.setattr(
        supervisor,
        "list_open_issues",
        lambda label_name: [
            supervisor.Issue(
                3, "Fix login flow", "Need help", "https://example.invalid/3"
            ),
        ],
    )
    monkeypatch.setattr(supervisor, "list_open_pull_requests", lambda: [])
    monkeypatch.setattr(supervisor, "list_local_branches", lambda repo_root: [])
    monkeypatch.setattr(
        supervisor,
        "load_issue_comments",
        lambda repo_name, number: [
            {
                "body": supervisor.make_clarification_comment(
                    supervisor.Issue(
                        3, "Fix login flow", "Need help", "https://example.invalid/3"
                    )
                ),
                "created_at": "2026-07-12T12:00:00Z",
            }
        ],
    )
    posted = []
    monkeypatch.setattr(
        supervisor,
        "issue_comment",
        lambda *args, **kwargs: posted.append((args, kwargs)),
    )

    candidate = supervisor.select_candidate(
        tmp_path,
        "example/target",
        supervisor.SupervisorState(),
        label_name=supervisor.LABEL_NAME,
        stale_after_seconds=1800,
        debug=False,
    )

    assert candidate is None
    assert posted == []


def test_select_candidate_resumes_after_clarification_response(monkeypatch, tmp_path):
    monkeypatch.setattr(
        supervisor,
        "list_open_issues",
        lambda label_name: [
            supervisor.Issue(
                3, "Fix login flow", "Need help", "https://example.invalid/3"
            ),
        ],
    )
    monkeypatch.setattr(supervisor, "list_open_pull_requests", lambda: [])
    monkeypatch.setattr(supervisor, "list_local_branches", lambda repo_root: [])
    monkeypatch.setattr(
        supervisor,
        "load_issue_comments",
        lambda repo_name, number: [
            {
                "body": supervisor.make_clarification_comment(
                    supervisor.Issue(
                        3, "Fix login flow", "Need help", "https://example.invalid/3"
                    )
                ),
                "created_at": "2026-07-12T12:00:00Z",
            },
            {
                "body": "Use the existing login settings screen and preserve session timeout.",
                "created_at": "2026-07-12T12:10:00Z",
            },
        ],
    )
    monkeypatch.setattr(supervisor, "issue_comment", lambda *args, **kwargs: None)

    candidate = supervisor.select_candidate(
        tmp_path,
        "example/target",
        supervisor.SupervisorState(),
        label_name=supervisor.LABEL_NAME,
        stale_after_seconds=1800,
        debug=False,
    )

    assert candidate is not None
    assert candidate.issue.number == 3


def test_pr_only_mode_gives_up_after_two_failures(monkeypatch, tmp_path):
    candidate = supervisor.Candidate(
        issue=supervisor.Issue(
            3, "golang で hello world", "body", "https://example.invalid/3"
        ),
        slug="golang-hello-world",
        branch_name="issue-3-golang-hello-world",
        existing_branch="issue-3-golang-hello-world",
        existing_pr_url=None,
        stale_processing_lock=False,
    )
    state = supervisor.SupervisorState(resume_mode="pr", pr_resume_failures=1)
    state_path = tmp_path / "state.json"
    launches = []

    monkeypatch.setattr(
        supervisor, "ensure_issue_worktree", lambda repo_root, candidate: tmp_path
    )
    monkeypatch.setattr(supervisor, "issue_comment", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        supervisor, "verify_pull_request", lambda repo_root, issue: None
    )

    class FakeWorker:
        pid = 123

        def wait(self, timeout=None):
            return 0

    monkeypatch.setattr(
        supervisor.subprocess,
        "Popen",
        lambda *args, **kwargs: launches.append((args, kwargs)) or FakeWorker(),
    )

    return_code = supervisor.supervise_worker(
        tmp_path,
        "example/target",
        candidate,
        state_path,
        state,
        ["ai-auto-dev-worker"],
        max_restarts=2,
        retry_delay_seconds=1,
    )

    assert return_code == 1
    assert state.failed_issue_numbers == {3}
    assert state.resume_mode is None
    assert state.pr_resume_failures >= 2


def test_supervise_worker_tracks_open_pr_after_success(monkeypatch, tmp_path):
    candidate = supervisor.Candidate(
        issue=supervisor.Issue(
            3,
            "Fix login flow",
            "Handle stale sessions",
            "https://example.invalid/issues/3",
        ),
        slug="fix-login-flow",
        branch_name="issue-3-fix-login-flow",
        existing_branch="issue-3-fix-login-flow",
        existing_pr_url=None,
        stale_processing_lock=False,
    )
    state = supervisor.SupervisorState()
    state_path = tmp_path / "state.json"

    monkeypatch.setattr(
        supervisor, "ensure_issue_worktree", lambda repo_root, candidate: tmp_path
    )
    monkeypatch.setattr(supervisor, "issue_comment", lambda *args, **kwargs: None)
    pushed = []
    monkeypatch.setattr(
        supervisor,
        "push_worktree_branch",
        lambda worktree_root, branch_name: pushed.append((worktree_root, branch_name)),
    )
    monkeypatch.setattr(
        supervisor,
        "verify_pull_request",
        lambda repo_root, issue: supervisor.PullRequest(
            11, "Fix login flow", "Closes #3", "https://example.invalid/pr/11"
        ),
    )
    monkeypatch.setattr(
        supervisor,
        "load_pull_request_comments",
        lambda repo_name, number: [
            {
                "id": 99,
                "author_login": "reviewer",
                "body": "Looks good",
                "created_at": "2026-07-12T12:00:00Z",
                "kind": "issue",
            }
        ],
    )

    class FakeWorker:
        pid = 123

        def wait(self, timeout=None):
            return 0

    monkeypatch.setattr(
        supervisor.subprocess,
        "Popen",
        lambda *args, **kwargs: FakeWorker(),
    )

    return_code = supervisor.supervise_worker(
        tmp_path,
        "example/target",
        candidate,
        state_path,
        state,
        ["ai-auto-dev-worker"],
        max_restarts=2,
        retry_delay_seconds=1,
    )

    assert return_code == 0
    assert pushed == [(tmp_path, "issue-3-fix-login-flow")]
    assert state.tracking_issue_number == 3
    assert state.tracking_pr_number == 11
    assert state.tracking_pr_comment_ids == [99]
    assert 3 not in state.completed_issue_numbers


def test_monitor_tracked_pull_request_launches_comment_worker(monkeypatch, tmp_path):
    state = supervisor.SupervisorState(
        tracking_issue_number=3,
        tracking_issue_title="Fix login flow",
        tracking_issue_body="Handle stale sessions",
        tracking_issue_url="https://example.invalid/issues/3",
        tracking_pr_number=11,
        tracking_pr_url="https://example.invalid/pr/11",
        tracking_branch_name="issue-3-fix-login-flow",
        tracking_pr_comment_ids=[1],
        active_slug="fix-login-flow",
    )
    state_path = tmp_path / "state.json"
    captured_env: dict[str, str] = {}
    pushed = []

    monkeypatch.setattr(supervisor, "configured_github_user", lambda: None)
    monkeypatch.setattr(
        supervisor,
        "load_pull_request",
        lambda repo_name, number: {"state": "open", "merged_at": None},
    )
    monkeypatch.setattr(
        supervisor,
        "load_pull_request_comments",
        lambda repo_name, number: [
            {
                "id": 1,
                "author_login": "reviewer",
                "body": "Old comment",
                "created_at": "2026-07-12T12:00:00Z",
                "kind": "issue",
            },
            {
                "id": 2,
                "author_login": "reviewer",
                "body": "Please clarify this",
                "created_at": "2026-07-12T12:05:00Z",
                "kind": "review",
            },
        ],
    )
    monkeypatch.setattr(supervisor, "worktree_exists", lambda path: True)
    monkeypatch.setattr(
        supervisor,
        "push_worktree_branch",
        lambda worktree_root, branch_name: pushed.append((worktree_root, branch_name)),
    )

    class FakeWorker:
        pid = 456

        def wait(self, timeout=None):
            return 0

    def fake_popen(*args, **kwargs):
        captured_env.update(kwargs.get("env", {}))
        return FakeWorker()

    monkeypatch.setattr(supervisor.subprocess, "Popen", fake_popen)

    return_code = supervisor.monitor_tracked_pull_request(
        tmp_path,
        "example/target",
        state_path,
        state,
        ["ai-auto-dev-worker"],
        retry_delay_seconds=1,
    )

    assert return_code == 0
    assert captured_env["AI_AUTO_DEV_PR_COMMENT_MODE"] == "1"
    assert captured_env["AI_AUTO_DEV_PR_NUMBER"] == "11"
    assert "Please clarify this" in captured_env["AI_AUTO_DEV_PR_NEW_COMMENTS"]
    assert state.tracking_pr_comment_ids == [1, 2]
    assert pushed == [
        (tmp_path / ".worktrees" / "issue-3-fix-login-flow", "issue-3-fix-login-flow")
    ]


def test_monitor_tracked_pull_request_ignores_comments_before_tracking_started(
    monkeypatch, tmp_path
):
    state = supervisor.SupervisorState(
        tracking_issue_number=3,
        tracking_issue_title="Fix login flow",
        tracking_issue_body="Handle stale sessions",
        tracking_issue_url="https://example.invalid/issues/3",
        tracking_pr_number=11,
        tracking_pr_url="https://example.invalid/pr/11",
        tracking_branch_name="issue-3-fix-login-flow",
        tracking_started_at="2026-07-12T12:00:30Z",
        tracking_pr_comment_ids=[],
        active_slug="fix-login-flow",
    )
    state_path = tmp_path / "state.json"
    captured_env: dict[str, str] = {}

    monkeypatch.setattr(supervisor, "configured_github_user", lambda: None)
    monkeypatch.setattr(
        supervisor,
        "load_pull_request",
        lambda repo_name, number: {"state": "open", "merged_at": None},
    )
    monkeypatch.setattr(
        supervisor,
        "load_pull_request_comments",
        lambda repo_name, number: [
            {
                "id": 1,
                "author_login": "reviewer",
                "body": "Comment before tracking started",
                "created_at": "2026-07-12T12:00:10Z",
                "kind": "review",
            },
            {
                "id": 2,
                "author_login": "reviewer",
                "body": "Comment after tracking started",
                "created_at": "2026-07-12T12:00:40Z",
                "kind": "review",
            },
        ],
    )
    monkeypatch.setattr(supervisor, "worktree_exists", lambda path: True)
    monkeypatch.setattr(
        supervisor, "push_worktree_branch", lambda *args, **kwargs: None
    )

    class FakeWorker:
        pid = 456

        def wait(self, timeout=None):
            return 0

    def fake_popen(*args, **kwargs):
        captured_env.update(kwargs.get("env", {}))
        return FakeWorker()

    monkeypatch.setattr(supervisor.subprocess, "Popen", fake_popen)

    return_code = supervisor.monitor_tracked_pull_request(
        tmp_path,
        "example/target",
        state_path,
        state,
        ["ai-auto-dev-worker"],
        retry_delay_seconds=1,
    )

    assert return_code == 0
    assert (
        "Comment after tracking started" in captured_env["AI_AUTO_DEV_PR_NEW_COMMENTS"]
    )
    assert (
        "Comment before tracking started"
        not in captured_env["AI_AUTO_DEV_PR_NEW_COMMENTS"]
    )


def test_monitor_tracked_pull_request_keeps_comments_while_worker_runs(
    monkeypatch, tmp_path
):
    state = supervisor.SupervisorState(
        tracking_issue_number=3,
        tracking_issue_title="Fix login flow",
        tracking_issue_body="Handle stale sessions",
        tracking_issue_url="https://example.invalid/issues/3",
        tracking_pr_number=11,
        tracking_pr_url="https://example.invalid/pr/11",
        tracking_branch_name="issue-3-fix-login-flow",
        tracking_pr_comment_ids=[1],
        active_slug="fix-login-flow",
    )
    state_path = tmp_path / "state.json"
    call_count = {"value": 0}
    captured_env: dict[str, str] = {}

    monkeypatch.setattr(supervisor, "configured_github_user", lambda: None)
    monkeypatch.setattr(
        supervisor,
        "load_pull_request",
        lambda repo_name, number: {"state": "open", "merged_at": None},
    )

    def fake_load_pull_request_comments(repo_name, number):
        call_count["value"] += 1
        if call_count["value"] == 1:
            return [
                {
                    "id": 1,
                    "author_login": "reviewer",
                    "body": "Old comment",
                    "created_at": "2026-07-12T12:00:00Z",
                    "kind": "issue",
                },
                {
                    "id": 2,
                    "author_login": "reviewer",
                    "body": "First follow-up",
                    "created_at": "2026-07-12T12:05:00Z",
                    "kind": "review",
                },
            ]
        return [
            {
                "id": 1,
                "author_login": "reviewer",
                "body": "Old comment",
                "created_at": "2026-07-12T12:00:00Z",
                "kind": "issue",
            },
            {
                "id": 2,
                "author_login": "reviewer",
                "body": "First follow-up",
                "created_at": "2026-07-12T12:05:00Z",
                "kind": "review",
            },
            {
                "id": 3,
                "author_login": "reviewer",
                "body": "Second follow-up while worker was running",
                "created_at": "2026-07-12T12:10:00Z",
                "kind": "review",
            },
        ]

    monkeypatch.setattr(
        supervisor, "load_pull_request_comments", fake_load_pull_request_comments
    )
    monkeypatch.setattr(supervisor, "worktree_exists", lambda path: True)
    monkeypatch.setattr(
        supervisor, "push_worktree_branch", lambda *args, **kwargs: None
    )

    class FakeWorker:
        pid = 456

        def wait(self, timeout=None):
            return 0

    def fake_popen(*args, **kwargs):
        captured_env.update(kwargs.get("env", {}))
        return FakeWorker()

    monkeypatch.setattr(supervisor.subprocess, "Popen", fake_popen)

    return_code = supervisor.monitor_tracked_pull_request(
        tmp_path,
        "example/target",
        state_path,
        state,
        ["ai-auto-dev-worker"],
        retry_delay_seconds=1,
    )
    assert return_code == 0
    assert state.tracking_pr_comment_ids == [1, 2]
    assert "First follow-up" in captured_env["AI_AUTO_DEV_PR_NEW_COMMENTS"]

    captured_env.clear()
    return_code = supervisor.monitor_tracked_pull_request(
        tmp_path,
        "example/target",
        state_path,
        state,
        ["ai-auto-dev-worker"],
        retry_delay_seconds=1,
    )
    assert return_code == 0
    assert (
        "Second follow-up while worker was running"
        in captured_env["AI_AUTO_DEV_PR_NEW_COMMENTS"]
    )


def test_monitor_tracked_pull_request_ignores_comments_from_configured_user(
    monkeypatch, tmp_path
):
    state = supervisor.SupervisorState(
        tracking_issue_number=3,
        tracking_issue_title="Fix login flow",
        tracking_issue_body="Handle stale sessions",
        tracking_issue_url="https://example.invalid/issues/3",
        tracking_pr_number=11,
        tracking_pr_url="https://example.invalid/pr/11",
        tracking_branch_name="issue-3-fix-login-flow",
        tracking_pr_comment_ids=[1],
        active_slug="fix-login-flow",
    )
    state_path = tmp_path / "state.json"
    monkeypatch.setattr(supervisor, "configured_github_user", lambda: "alice")
    monkeypatch.setattr(
        supervisor,
        "load_pull_request",
        lambda repo_name, number: {
            "state": "open",
            "merged_at": None,
            "author": {"login": "alice"},
        },
    )
    monkeypatch.setattr(
        supervisor,
        "load_pull_request_comments",
        lambda repo_name, number: [
            {
                "id": 1,
                "author_login": "alice",
                "body": "AI からの返信: working on it",
                "created_at": "2026-07-12T12:00:00Z",
                "kind": "issue",
            },
            {
                "id": 2,
                "author_login": "reviewer",
                "body": "Please clarify this",
                "created_at": "2026-07-12T12:05:00Z",
                "kind": "review",
            },
        ],
    )
    monkeypatch.setattr(supervisor, "worktree_exists", lambda path: True)
    monkeypatch.setattr(
        supervisor, "push_worktree_branch", lambda *args, **kwargs: None
    )

    class FakeWorker:
        pid = 456

        def wait(self, timeout=None):
            return 0

    captured_env: dict[str, str] = {}

    def fake_popen(*args, **kwargs):
        captured_env.update(kwargs.get("env", {}))
        return FakeWorker()

    monkeypatch.setattr(supervisor.subprocess, "Popen", fake_popen)

    return_code = supervisor.monitor_tracked_pull_request(
        tmp_path,
        "example/target",
        state_path,
        state,
        ["ai-auto-dev-worker"],
        retry_delay_seconds=1,
    )

    assert return_code == 0
    assert "Please clarify this" in captured_env["AI_AUTO_DEV_PR_NEW_COMMENTS"]
    assert "working on it" not in captured_env["AI_AUTO_DEV_PR_NEW_COMMENTS"]


def test_monitor_tracked_pull_request_ignores_other_users_pr(monkeypatch, tmp_path):
    state = supervisor.SupervisorState(
        tracking_issue_number=3,
        tracking_issue_title="Fix login flow",
        tracking_issue_body="Handle stale sessions",
        tracking_issue_url="https://example.invalid/issues/3",
        tracking_pr_number=11,
        tracking_pr_url="https://example.invalid/pr/11",
        tracking_branch_name="issue-3-fix-login-flow",
        tracking_pr_comment_ids=[1],
        active_slug="fix-login-flow",
    )
    state_path = tmp_path / "state.json"
    monkeypatch.setattr(supervisor, "configured_github_user", lambda: "alice")
    monkeypatch.setattr(
        supervisor,
        "load_pull_request",
        lambda repo_name, number: {
            "state": "open",
            "merged_at": None,
            "author": {"login": "bob"},
        },
    )

    return_code = supervisor.monitor_tracked_pull_request(
        tmp_path,
        "example/target",
        state_path,
        state,
        ["ai-auto-dev-worker"],
        retry_delay_seconds=1,
    )

    assert return_code == 0
    assert state.tracking_issue_number is None
    assert state.tracking_pr_number is None
    assert state.tracking_pr_comment_ids == []
