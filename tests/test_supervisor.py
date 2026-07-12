from importlib.machinery import SourceFileLoader
import importlib.util
from pathlib import Path
import sys


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "bin" / "ai-auto-dev-supervisor"
).resolve()
loader = SourceFileLoader("ai_auto_dev_supervisor", str(MODULE_PATH))
spec = importlib.util.spec_from_loader(loader.name, loader)
supervisor = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = supervisor
spec.loader.exec_module(supervisor)


def test_reset_state_deletes_cached_state(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text('{"completed_issue_numbers":[3]}')

    supervisor.reset_state(state_file)

    assert not state_file.exists()


def test_verify_pull_request_requires_closes_body(monkeypatch):
    issue = supervisor.Issue(7, "Add thing", "body", "https://example.invalid/7")

    monkeypatch.setattr(supervisor, "configured_github_user", lambda: None)
    monkeypatch.setattr(
        supervisor,
        "list_open_pull_requests",
        lambda: [
            supervisor.PullRequest(
                11, "Add thing", "Fixes #7", "https://example.invalid/pr/11"
            ),
        ],
    )

    assert supervisor.verify_pull_request(Path("/tmp"), issue) is None

    monkeypatch.setattr(
        supervisor,
        "list_open_pull_requests",
        lambda: [
            supervisor.PullRequest(
                11, "Add thing", "Closes #7", "https://example.invalid/pr/11"
            ),
        ],
    )

    assert (
        supervisor.verify_pull_request(Path("/tmp"), issue).url
        == "https://example.invalid/pr/11"
    )


def test_verify_pull_request_ignores_other_users_pull_requests(monkeypatch):
    issue = supervisor.Issue(7, "Add thing", "body", "https://example.invalid/7")

    monkeypatch.setattr(supervisor, "configured_github_user", lambda: "alice")
    monkeypatch.setattr(
        supervisor,
        "list_open_pull_requests",
        lambda: [
            supervisor.PullRequest(
                11,
                "Add thing",
                "Closes #7",
                "https://example.invalid/pr/11",
                author_login="bob",
            ),
            supervisor.PullRequest(
                12,
                "Add thing",
                "Closes #7",
                "https://example.invalid/pr/12",
                author_login="alice",
            ),
        ],
    )

    pr = supervisor.verify_pull_request(Path("/tmp"), issue)

    assert pr is not None
    assert pr.url == "https://example.invalid/pr/12"
