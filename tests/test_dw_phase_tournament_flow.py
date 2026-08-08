import json
import importlib.util
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "dw-phase-tournament-flow"
    / "scripts"
    / "workflow.py"
)
SPEC = importlib.util.spec_from_file_location(
    "dw_phase_tournament_flow_workflow", SCRIPT
)
assert SPEC and SPEC.loader
workflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflow)


def test_initializes_own_state_and_does_not_delegate(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert workflow.main([]) == 0

    assert (tmp_path / ".dev-workflow-tournament" / "state.json").exists()
    assert (tmp_path / ".dev-workflow-tournament" / "CURRENT_STEP.md").exists()
    assert not (tmp_path / ".dev-workflow-phase").exists()
    state = json.loads(
        (tmp_path / ".dev-workflow-tournament" / "state.json").read_text()
    )
    assert state == {"status": "ACTIVE", "stage_index": 0, "gate": "WORK"}


def test_requires_review_approval_before_advancing(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert workflow.main(["next"]) == 2
    assert workflow.main(["review"]) == 0
    assert workflow.main(["approve"]) == 0
    assert workflow.main(["next"]) == 0

    state = json.loads(
        (tmp_path / ".dev-workflow-tournament" / "state.json").read_text()
    )
    assert state["stage_index"] == 1
    assert state["gate"] == "WORK"


def test_phase_artifact_tree_exists_before_implementation_stage(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    workflow.main([])

    for _ in range(2):
        assert workflow.main(["review"]) == 0
        assert workflow.main(["approve"]) == 0
        assert workflow.main(["next"]) == 0

    (tmp_path / ".dev-workflow-tournament" / "02_phase_design.md").write_text(
        """## Phase 1: Search

### Acceptance Criteria

- **AC-P1-001**: Search returns matching records.
  - Expected Result: matching records are shown.
  - Evidence: API response.
""",
        encoding="utf-8",
    )
    assert workflow.main(["review"]) == 0
    assert workflow.main(["approve"]) == 0
    assert workflow.main(["next"]) == 0

    state = json.loads(
        (tmp_path / ".dev-workflow-tournament" / "state.json").read_text()
    )
    assert state["stage_index"] == 3
    assert (tmp_path / ".dev-workflow-tournament" / "phases").is_dir()
    assert (tmp_path / ".dev-workflow-tournament" / "reports").is_dir()


def test_phase_design_requires_acceptance_criteria_per_phase(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    workflow.main([])
    for _ in range(2):
        assert workflow.main(["review"]) == 0
        assert workflow.main(["approve"]) == 0
        assert workflow.main(["next"]) == 0

    design = tmp_path / ".dev-workflow-tournament" / "02_phase_design.md"
    design.write_text("## Phase 1: Search\n\n### Scope\n", encoding="utf-8")
    assert workflow.main(["review"]) == 0
    assert workflow.main(["approve"]) == 2

    design.write_text(
        """## Phase 1: Search

### Acceptance Criteria

- **AC-P1-001**: Search returns matching records.
  - Expected Result: matching records are shown.
  - Evidence: API response and UI screenshot.
""",
        encoding="utf-8",
    )
    assert workflow.main(["approve"]) == 0


def test_rejects_unknown_commands(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    assert workflow.main(["bogus"]) == 2
    assert "Usage:" in capsys.readouterr().err


def test_scheduler_runs_independent_phases_and_waits_for_dependencies(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    workflow.ROOT.mkdir()
    (workflow.ROOT / "01_acceptance_contract.md").write_text(
        "## Goal\nDeliver it.\n", encoding="utf-8"
    )
    (workflow.ROOT / "02_phase_design.md").write_text(
        "## Phase 1: Base A\n\n## Phase 2: Base B\n\n## Phase 3: Feature\n",
        encoding="utf-8",
    )
    phases = {
        "phase1": {
            "id": "phase1",
            "number": 1,
            "name": "Base A",
            "depends_on": [],
            "status": "READY",
            "worktree": "",
            "branch": "",
            "request_file": "",
            "completion_file": "",
        },
        "phase2": {
            "id": "phase2",
            "number": 2,
            "name": "Base B",
            "depends_on": [],
            "status": "READY",
            "worktree": "",
            "branch": "",
            "request_file": "",
            "completion_file": "",
        },
        "phase3": {
            "id": "phase3",
            "number": 3,
            "name": "Feature",
            "depends_on": ["phase1"],
            "status": "READY",
            "worktree": "",
            "branch": "",
            "request_file": "",
            "completion_file": "",
        },
    }
    monkeypatch.setattr(
        workflow,
        "phase_worktree",
        lambda phase: (
            tmp_path / ".worktrees" / phase["id"],
            f"tournament/{phase['id']}",
        ),
    )
    state = {"phases": phases, "max_parallel": 3}

    workflow.schedule_phases(state)

    assert state["phases"]["phase1"]["status"] == "RUNNING"
    assert state["phases"]["phase2"]["status"] == "RUNNING"
    assert state["phases"]["phase3"]["status"] == "READY"
    assert len(list((workflow.ROOT / "requests").glob("*.md"))) == 2
