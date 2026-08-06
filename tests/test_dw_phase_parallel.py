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


def test_prompt_includes_contract_and_only_selected_phase_design(
    tmp_path: Path,
) -> None:
    state = {"step": 1}
    phase = {
        "id": "phase1",
        "number": 1,
        "name": "Base",
        "phase_type": "layer",
        "depends_on": [],
    }
    context = tmp_path / ".dev-workflow-phase"
    context.mkdir()
    (context / "00_project_requirements.md").write_text(
        "全体PRDの対象外要件: 決済できること", encoding="utf-8"
    )
    (context / "acceptance-contract.md").write_text(
        """## Goal
検索機能を提供する。
## Non-goals
決済は対象外。
## Phase Scope
### Search scope
- **Phase**: phase1
## Acceptance Criteria
### AC-001: 検索できる
- **Phase**: phase1
- Expected Result: 検索結果が返る。
### AC-002: 決済できる
- **Phase**: phase2
- Expected Result: 決済が完了する。
## Constraints and Compatibility
既存 API を維持する。
## Prioritized Risks
### RISK-001: 検索不能
- **Phase**: phase1
## Validation Matrix
### VM-001: 検索テスト
- **Phase**: phase1
- Command: python3 -m pytest
### VM-002: 決済テスト
- **Phase**: phase2
- Command: python3 -m pytest
## Assumptions and Open Questions
なし。
""",
        encoding="utf-8",
    )
    (context / "01_phase_design.md").write_text(
        """- **Phases**: 2

## Phase 1: Base
- **Phase Type**: layer
- **Depends On**: none
- 責務: 検索基盤

## Phase 2: Payment
- **Phase Type**: feature
- **Depends On**: none
- 責務: 決済
""",
        encoding="utf-8",
    )

    request = common.prompt(tmp_path, state, phase, True)

    assert "AC-001: 検索できる" in request
    assert "AC-002: 決済できる" not in request
    assert "Phase 1: Base" in request
    assert "責務: 検索基盤" in request
    assert "Phase 2: Payment" not in request
    assert "全体PRDの対象外要件" not in request


def test_prompt_fails_closed_without_acceptance_contract(tmp_path: Path) -> None:
    context = tmp_path / ".dev-workflow-phase"
    context.mkdir()
    (context / "01_phase_design.md").write_text(
        "## Phase 1: Base\n- **Phase Type**: layer\n",
        encoding="utf-8",
    )
    phase = {
        "id": "phase1",
        "number": 1,
        "name": "Base",
        "phase_type": "layer",
        "depends_on": [],
    }

    with pytest.raises(RuntimeError, match="acceptance-contract.md"):
        common.prompt(tmp_path, {}, phase, True)


def test_phase_worktree_slug_is_ascii(tmp_path: Path) -> None:
    assert common.phase_slug({"id": "phase1", "name": "日本語 API 実装"}) == "api"


def test_phase_worktree_uses_phase_id_for_non_ascii_name(tmp_path: Path) -> None:
    assert common.phase_slug({"id": "phase2", "name": "日本語のみ"}) == "phase2"
