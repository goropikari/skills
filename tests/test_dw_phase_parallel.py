from pathlib import Path
import sys

import pytest

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / "dw-phase-parallel" / "scripts")
)
import common


def write_design(tmp_path: Path, body: str) -> None:
    design = tmp_path / ".dev-workflow-phase"
    design.mkdir()
    (design / "01_phase_design.md").write_text(body, encoding="utf-8")


def test_load_design_reads_dependencies(tmp_path: Path) -> None:
    write_design(
        tmp_path,
        """- **Phases**: 2

## Phase 1: Base
- **Phase Type**: layer
- **Depends On**: none

## Phase 2: Feature
- **Phase Type**: feature
- **Depends On**: phase1
""",
    )
    phases = common.load_design(tmp_path)
    assert phases[1]["depends_on"] == ["phase1"]


def test_load_design_rejects_unknown_dependency(tmp_path: Path) -> None:
    write_design(
        tmp_path,
        """- **Phases**: 1

## Phase 1: Base
- **Phase Type**: layer
- **Depends On**: phase2
""",
    )
    with pytest.raises(ValueError):
        common.load_design(tmp_path)


def test_light_defaults_to_native_subagent() -> None:
    args = type("Args", (), {"agent_cmd": None, "light": True})()
    assert common.command_from_args(args) == "native-subagent"


def test_reviewed_mode_requires_agent_command() -> None:
    args = type("Args", (), {"agent_cmd": None, "light": False})()
    assert common.command_from_args(args) == ""


def test_prompt_includes_requirements_and_phase_design(tmp_path: Path) -> None:
    state = {"step": 1}
    phase = {
        "id": "phase1",
        "name": "Base",
        "phase_type": "layer",
        "depends_on": [],
    }
    context = tmp_path / ".dev-workflow-phase"
    context.mkdir()
    (context / "00_project_requirements.md").write_text(
        "受け入れ条件: 検索できること", encoding="utf-8"
    )
    (context / "01_phase_design.md").write_text(
        "Phase 1 の責務: 検索基盤", encoding="utf-8"
    )

    request = common.prompt(tmp_path, state, phase, True)

    assert "受け入れ条件: 検索できること" in request
    assert "Phase 1 の責務: 検索基盤" in request


def test_phase_worktree_slug_is_ascii(tmp_path: Path) -> None:
    assert common.phase_slug({"id": "phase1", "name": "日本語 API 実装"}) == "api"


def test_phase_worktree_uses_phase_id_for_non_ascii_name(tmp_path: Path) -> None:
    assert common.phase_slug({"id": "phase2", "name": "日本語のみ"}) == "phase2"
