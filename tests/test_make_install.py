import os
import subprocess
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
STATE_FILE = ".skills-install-state"


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
    stale_skill = managed_root / "removed-skill"
    unmanaged_skill = managed_root / "user-skill"
    stale_skill.mkdir()
    unmanaged_skill.mkdir()
    (managed_root / STATE_FILE).write_text(
        (managed_root / STATE_FILE).read_text() + "removed-skill\n",
        encoding="utf-8",
    )

    run_make_install(tmp_path)

    assert not stale_skill.exists()
    assert unmanaged_skill.is_dir()
    assert (managed_root / "implementation-orchestrator").is_dir()
    state_names = (managed_root / STATE_FILE).read_text(encoding="utf-8").splitlines()
    assert "removed-skill" not in state_names
    assert "implementation-orchestrator" in state_names


def test_install_does_not_remove_existing_paths_without_state(tmp_path: Path) -> None:
    managed_root = tmp_path / ".agents" / "skills"
    managed_root.mkdir(parents=True)
    existing_skill = managed_root / "old-skill"
    existing_skill.mkdir()

    run_make_install(tmp_path)

    assert existing_skill.is_dir()
