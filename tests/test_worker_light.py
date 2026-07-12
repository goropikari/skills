from importlib.machinery import SourceFileLoader
import importlib.util
from pathlib import Path
import sys


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "bin" / "ai-auto-dev-worker-light"
).resolve()
loader = SourceFileLoader("ai_auto_dev_worker_light", str(MODULE_PATH))
spec = importlib.util.spec_from_loader(loader.name, loader)
worker_light = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = worker_light
spec.loader.exec_module(worker_light)


def test_build_prompt_uses_dw_phase_light(monkeypatch):
    repo_root = Path("/tmp/repo-worker-light")
    template_path = repo_root / ".github" / "pull_request_template.md"
    template_path.parent.mkdir(parents=True, exist_ok=True)
    template_path.write_text(
        "## Summary\n\n- What changed\n- Why it changed\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("AI_AUTO_DEV_REPO_ROOT", str(repo_root))
    monkeypatch.setenv(
        "AI_AUTO_DEV_WORKTREE_ROOT",
        "/tmp/repo-worker-light/.worktrees/issue-42-fix-login-flow",
    )
    monkeypatch.setenv("AI_AUTO_DEV_REPO_NAME", "example/repo")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_NUMBER", "42")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_TITLE", "Fix login flow")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_BODY", "Handle stale sessions")
    monkeypatch.setenv("AI_AUTO_DEV_ISSUE_URL", "https://example.invalid/issues/42")
    monkeypatch.setenv("AI_AUTO_DEV_BRANCH_NAME", "issue-42-fix-login-flow")
    monkeypatch.setenv("AI_AUTO_DEV_SLUG", "fix-login-flow")
    monkeypatch.setenv("AI_AUTO_DEV_RESUME_MODE", "pr")

    prompt = worker_light.build_prompt()

    assert (
        "Use the repo's existing `dw-phase-light` workflow for implementation work."
        in prompt
    )
    assert (
        "Then run `dw-phase-light` and follow the current `CURRENT_STEP.md` exactly."
        in prompt
    )
    assert "Use the existing dw-phase-light state in the worktree" in prompt
    assert (
        "Do not commit, stage, or include files under `docs/reviews/` in the PR."
        in prompt
    )
    assert "Write the PR body as Markdown with real line breaks" in prompt
    assert "Repository pull request template:" in prompt
    assert (
        "Template path: /tmp/repo-worker-light/.github/pull_request_template.md"
        in prompt
    )
    assert "## Summary" in prompt
    assert "dw-phase` workflow" not in prompt
