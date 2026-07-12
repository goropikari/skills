from importlib.machinery import SourceFileLoader
import importlib.util
from pathlib import Path
import sys


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "bin" / "ai-auto-dev-worker"
).resolve()
loader = SourceFileLoader("ai_auto_dev_worker", str(MODULE_PATH))
spec = importlib.util.spec_from_loader(loader.name, loader)
worker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = worker
spec.loader.exec_module(worker)


def test_build_prompt_includes_resume_mode(monkeypatch):
    monkeypatch.setenv("AI_AUTO_DEV_REPO_ROOT", "/tmp/repo")
    monkeypatch.setenv(
        "AI_AUTO_DEV_WORKTREE_ROOT", "/tmp/repo/.worktrees/issue-42-fix-login-flow"
    )
    monkeypatch.setenv("AI_AUTO_DEV_REPO_NAME", "example/repo")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_NUMBER", "42")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_TITLE", "Fix login flow")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_BODY", "Handle stale sessions")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_URL", "https://example.invalid/issues/42")
    monkeypatch.setenv("AI_AUTO_DEV_BRANCH_NAME", "issue-42-fix-login-flow")
    monkeypatch.setenv("AI_AUTO_DEV_SLUG", "fix-login-flow")
    monkeypatch.setenv("AI_AUTO_DEV_RESUME_MODE", "pr")

    prompt = worker.build_prompt()

    assert "Worktree root: /tmp/repo/.worktrees/issue-42-fix-login-flow" in prompt
    assert (
        "Open or update exactly one PR for this issue yourself before you finish."
        in prompt
    )
    assert "Implementation is already done." in prompt
    assert "Required review suite at every completed phase:" in prompt
    assert "`ta-review`" in prompt
    assert "`tta-review`" in prompt
    assert "`jr`" in prompt
    assert "`comment-review-orchestrator`" in prompt
    assert (
        "Do not treat a phase as complete until the review suite has been run for that phase or subphase."
        in prompt
    )
    assert "only after the current phase or subphase is fully complete" in prompt
    assert (
        "Do not run the review suite after intermediate steps inside a phase or subphase."
        in prompt
    )
    assert "treat it as implementation input and move to code changes" in prompt
    assert (
        "Do not stop at PRD improvement when code changes are still required." in prompt
    )


def test_build_prompt_includes_pr_comment_mode(monkeypatch):
    monkeypatch.setenv("AI_AUTO_DEV_PR_COMMENT_MODE", "1")
    monkeypatch.setenv("AI_AUTO_DEV_REPO_ROOT", "/tmp/repo")
    monkeypatch.setenv(
        "AI_AUTO_DEV_WORKTREE_ROOT", "/tmp/repo/.worktrees/issue-42-fix-login-flow"
    )
    monkeypatch.setenv("AI_AUTO_DEV_REPO_NAME", "example/repo")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_NUMBER", "42")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_TITLE", "Fix login flow")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_BODY", "Handle stale sessions")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_URL", "https://example.invalid/issues/42")
    monkeypatch.setenv("AI_AUTO_DEV_BRANCH_NAME", "issue-42-fix-login-flow")
    monkeypatch.setenv("AI_AUTO_DEV_SLUG", "fix-login-flow")
    monkeypatch.setenv("AI_AUTO_DEV_PR_NUMBER", "11")
    monkeypatch.setenv("AI_AUTO_DEV_PR_URL", "https://example.invalid/pr/11")
    monkeypatch.setenv(
        "AI_AUTO_DEV_PR_NEW_COMMENTS",
        '[{"id":101,"author_login":"reviewer","body":"Please clarify this","created_at":"2026-07-12T12:00:00Z","kind":"issue"}]',
    )

    prompt = worker.build_prompt()

    assert "You are the PR comment response worker for ai-auto-dev." in prompt
    assert (
        "Always make it clear that your reply is from AI by prefixing comments with `AI からの返信:`."
        in prompt
    )
    assert "PR number: 11" in prompt
    assert "https://example.invalid/pr/11" in prompt
    assert "Please clarify this" in prompt
    assert "Human judgment" not in prompt


def test_main_posts_pr_comment_from_codex_stdout(monkeypatch, tmp_path):
    monkeypatch.setenv("AI_AUTO_DEV_PR_COMMENT_MODE", "1")
    monkeypatch.setenv("AI_AUTO_DEV_REPO_ROOT", str(tmp_path))
    monkeypatch.setenv("AI_AUTO_DEV_WORKTREE_ROOT", str(tmp_path))
    monkeypatch.setenv("AI_AUTO_DEV_REPO_NAME", "example/repo")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_NUMBER", "42")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_TITLE", "Fix login flow")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_BODY", "Handle stale sessions")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_URL", "https://example.invalid/issues/42")
    monkeypatch.setenv("AI_AUTO_DEV_BRANCH_NAME", "issue-42-fix-login-flow")
    monkeypatch.setenv("AI_AUTO_DEV_SLUG", "fix-login-flow")
    monkeypatch.setenv("AI_AUTO_DEV_PR_NUMBER", "11")
    monkeypatch.setenv("AI_AUTO_DEV_PR_URL", "https://example.invalid/pr/11")
    monkeypatch.setenv("AI_AUTO_DEV_CODEX_BIN", "codex")
    monkeypatch.setenv("AI_AUTO_DEV_CODEX_ARGS", "")

    calls = []

    class FakeCompleted:
        def __init__(self, stdout="", returncode=0):
            self.stdout = stdout
            self.returncode = returncode

    def fake_run(cmd, **kwargs):
        calls.append((cmd, kwargs))
        if cmd[:3] == ["gh", "pr", "comment"]:
            return FakeCompleted(returncode=0)
        return FakeCompleted(stdout="Please update the docs.")

    monkeypatch.setattr(worker.subprocess, "run", fake_run)

    assert worker.main() == 0
    assert calls[0][0][:2] == ["codex", "exec"]
    assert calls[0][1]["capture_output"] is True
    assert calls[1][0] == [
        "gh",
        "pr",
        "comment",
        "11",
        "--body",
        "AI からの返信:\nPlease update the docs.",
    ]


def test_normalize_pr_comment_body_adds_ai_prefix():
    assert (
        worker.normalize_pr_comment_body("Need human review")
        == "AI からの返信:\nNeed human review"
    )
    assert (
        worker.normalize_pr_comment_body("")
        == "AI からの返信: コメント応答を生成できませんでした。人間の判断が必要です。"
    )


def test_build_command_uses_codex_exec_and_stdin(monkeypatch):
    monkeypatch.setenv("AI_AUTO_DEV_REPO_ROOT", "/tmp/repo")
    monkeypatch.setenv(
        "AI_AUTO_DEV_WORKTREE_ROOT", "/tmp/repo/.worktrees/issue-42-fix-login-flow"
    )
    monkeypatch.setenv("AI_AUTO_DEV_CODEX_BIN", "codex")
    monkeypatch.delenv("AI_AUTO_DEV_BYPASS_APPROVALS", raising=False)
    monkeypatch.setenv("AI_AUTO_DEV_CODEX_ARGS", "--ignore-rules")

    cmd = worker.build_command()

    assert cmd[:4] == [
        "codex",
        "exec",
        "--cd",
        "/tmp/repo/.worktrees/issue-42-fix-login-flow",
    ]
    assert "--model" not in cmd
    assert "--ignore-rules" in cmd
    assert cmd[-1] == "-"
