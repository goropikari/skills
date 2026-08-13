import os
import re
import subprocess
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
STATE_FILE = ".skills-install-state"


def active_skill_directories() -> list[Path]:
    candidates = (
        *REPOSITORY_ROOT.glob("*/SKILL.md"),
        *REPOSITORY_ROOT.glob("quality/*/SKILL.md"),
    )
    return sorted(
        {
            skill_file.parent.relative_to(REPOSITORY_ROOT)
            for skill_file in candidates
            if "deprecated" not in skill_file.relative_to(REPOSITORY_ROOT).parts
        }
    )


def run_make_install(home: Path) -> None:
    environment = os.environ.copy()
    environment["HOME"] = str(home)
    subprocess.run(
        ["make", "install"],
        cwd=REPOSITORY_ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )


def test_install_removes_only_stale_managed_skills(tmp_path: Path) -> None:
    run_make_install(tmp_path)

    managed_root = tmp_path / ".agents" / "skills"
    stale_skill = managed_root / "security-review"
    stale_quality_assessment = managed_root / "quality-assessment"
    unmanaged_skill = managed_root / "user-skill"
    stale_skill.mkdir()
    stale_quality_assessment.mkdir()
    unmanaged_skill.mkdir()
    (managed_root / STATE_FILE).write_text(
        (managed_root / STATE_FILE).read_text()
        + "security-review\nquality-assessment\n",
        encoding="utf-8",
    )

    run_make_install(tmp_path)

    assert not stale_skill.exists()
    assert not stale_quality_assessment.exists()
    assert unmanaged_skill.is_dir()
    assert (managed_root / "implementation-orchestrator").is_dir()
    assert (managed_root / "coding-quality-gate").is_dir()
    assert (managed_root / "repository-quality-baseline").is_dir()
    for skill_directory in active_skill_directories():
        installed_skill = managed_root / skill_directory.name
        version = (installed_skill / "VERSION").read_text(encoding="utf-8").strip()
        assert re.fullmatch(r"\d+\.\d+\.\d+", version)
    state_names = (managed_root / STATE_FILE).read_text(encoding="utf-8").splitlines()
    assert "security-review" not in state_names
    assert "quality-assessment" not in state_names
    assert "implementation-orchestrator" in state_names
    assert "coding-quality-gate" in state_names
    assert "repository-quality-baseline" in state_names
    assert "acceptance-harness" not in state_names
    assert "acceptance-driven-app" not in state_names
    assert "review-orchestrator" in state_names
    assert "security-review" not in state_names
    assert (
        managed_root / "review-orchestrator" / "skills" / "security-review"
    ).is_dir()
    assert (managed_root / "review-orchestrator" / "skills" / "jr-review").is_dir()
    assert (
        managed_root / "coding-quality-gate" / "skills" / "quality-assessment"
    ).is_dir()


def test_install_does_not_remove_existing_paths_without_state(tmp_path: Path) -> None:
    managed_root = tmp_path / ".agents" / "skills"
    managed_root.mkdir(parents=True)
    existing_skill = managed_root / "old-skill"
    existing_skill.mkdir()

    run_make_install(tmp_path)

    assert existing_skill.is_dir()
