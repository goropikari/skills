from pathlib import Path
import importlib.util
import sys


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "workflow.py"
spec = importlib.util.spec_from_file_location("workflow", MODULE_PATH)
workflow = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = workflow
spec.loader.exec_module(workflow)


def run_command(monkeypatch, *args):
    monkeypatch.setattr(workflow.sys, "argv", ["workflow.py", *args])
    return workflow.main()


def approve_and_next(monkeypatch):
    assert run_command(monkeypatch, "review") == 0
    assert run_command(monkeypatch, "approve") == 0
    assert run_command(monkeypatch, "next") == 0


def current_state(tmp_path):
    return (tmp_path / ".dev-workflow-phase" / "CURRENT_STEP.md").read_text(
        encoding="utf-8"
    )


def test_parse_children_requires_count_sections_and_phase_type():
    text = """- **Phases**: 2

## Phase 1: Search
- **Phase Type**: feature

## Phase 2: Application
- **Phase Type**: layer
"""

    children = workflow.parse_children_from_text(text, "")

    assert children is not None
    assert [child.path for child in children] == ["phase1", "phase2"]
    assert [child.name for child in children] == ["Search", "Application"]
    assert [child.phase_type for child in children] == ["feature", "layer"]


def test_parse_children_rejects_missing_phase_type():
    text = """- **Phases**: 1

## Phase 1: Search
"""

    assert workflow.parse_children_from_text(text, "") is None


def test_phase_design_advances_to_first_phase_definition(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    assert run_command(monkeypatch) == 0
    approve_and_next(monkeypatch)

    design = tmp_path / ".dev-workflow-phase" / "01_phase_design.md"
    design.write_text(
        """- **Phases**: 1

## Phase 1: Search
- **Phase Type**: feature
""",
        encoding="utf-8",
    )

    approve_and_next(monkeypatch)

    content = current_state(tmp_path)
    assert "- **Current Path**: phase1" in content
    assert "- **Current Name**: Search" in content
    assert "- **Phase Type**: feature" in content
    assert "- **Local Step**: 1" in content
    assert "- **Local Stage**: definition" in content
    assert "- **Status**: IN_PROGRESS" in content

    design_content = design.read_text(encoding="utf-8")
    assert "- **Status**: IN_PROGRESS" in design_content


def test_definition_phase_type_controls_step_two(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    workflow.write_state(
        tmp_path,
        workflow.WorkflowState(
            status="REVIEWED",
            current_path="phase1",
            current_name="Application",
            phase_type="layer",
            local_step=1,
            local_stage="definition",
        ),
    )
    definition = tmp_path / ".dev-workflow-phase" / "phase1" / "01_definition.md"
    definition.parent.mkdir(parents=True)
    definition.write_text("- **Phase Type**: layer\n", encoding="utf-8")

    assert run_command(monkeypatch, "next") == 0

    content = current_state(tmp_path)
    assert "- **Local Step**: 2" in content
    assert "- **Local Stage**: contract" in content
    assert ".dev-workflow-phase/phase1/02_contract_design.md" in content


def test_test_design_split_no_advances_to_leaf_implementation_steps(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    workflow.write_state(
        tmp_path,
        workflow.WorkflowState(
            status="REVIEWED",
            current_path="phase1",
            current_name="Search",
            phase_type="feature",
            local_step=3,
            local_stage="test-design",
        ),
    )
    test_design = tmp_path / ".dev-workflow-phase" / "phase1" / "03_test_design.md"
    test_design.parent.mkdir(parents=True)
    test_design.write_text("- **Split**: no\n", encoding="utf-8")

    assert run_command(monkeypatch, "next") == 0
    assert "- **Local Stage**: interface" in current_state(tmp_path)

    approve_and_next(monkeypatch)
    assert "- **Local Stage**: tests" in current_state(tmp_path)

    approve_and_next(monkeypatch)
    assert "- **Local Stage**: implementation" in current_state(tmp_path)


def test_split_yes_enters_subphase_and_completes_parent_depth_first(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    phase_design = tmp_path / ".dev-workflow-phase" / "01_phase_design.md"
    phase_design.write_text(
        """- **Phases**: 2

## Phase 1: Search
- **Phase Type**: feature

## Phase 2: Admin
- **Phase Type**: feature
""",
        encoding="utf-8",
    )
    workflow.write_state(
        tmp_path,
        workflow.WorkflowState(
            status="REVIEWED",
            current_path="phase1",
            current_name="Search",
            phase_type="feature",
            local_step=3,
            local_stage="test-design",
        ),
    )
    test_design = tmp_path / ".dev-workflow-phase" / "phase1" / "03_test_design.md"
    test_design.parent.mkdir(parents=True)
    test_design.write_text("- **Split**: yes\n", encoding="utf-8")

    assert run_command(monkeypatch, "next") == 0
    assert "- **Local Stage**: split-design" in current_state(tmp_path)

    split_design = tmp_path / ".dev-workflow-phase" / "phase1" / "04_split_design.md"
    split_design.write_text(
        """- **Subphases**: 1

## Subphase 1: Application Service
- **Phase Type**: layer
""",
        encoding="utf-8",
    )
    approve_and_next(monkeypatch)

    content = current_state(tmp_path)
    assert "- **Current Path**: phase1/subphase1" in content
    assert "- **Current Name**: Application Service" in content
    assert "- **Local Stage**: definition" in content

    workflow.write_state(
        tmp_path,
        workflow.WorkflowState(
            status="REVIEWED",
            current_path="phase1/subphase1",
            current_name="Application Service",
            phase_type="layer",
            local_step=6,
            local_stage="implementation",
        ),
    )
    assert run_command(monkeypatch, "next") == 0

    content = current_state(tmp_path)
    assert "- **Current Path**: phase2" in content
    assert "- **Current Name**: Admin" in content
    assert "- **Local Stage**: definition" in content

    phase_design_content = phase_design.read_text(encoding="utf-8")
    assert (
        "## Phase 1: Search\n- **Phase Type**: feature\n- **Status**: COMPLETED"
        in phase_design_content
    )
    split_design_content = split_design.read_text(encoding="utf-8")
    assert "- **Status**: COMPLETED" in split_design_content


def test_last_leaf_completion_marks_workflow_completed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    phase_design = tmp_path / ".dev-workflow-phase" / "01_phase_design.md"
    phase_design.write_text(
        """- **Phases**: 1

## Phase 1: Search
- **Phase Type**: feature
- **Status**: IN_PROGRESS
""",
        encoding="utf-8",
    )
    workflow.write_state(
        tmp_path,
        workflow.WorkflowState(
            status="REVIEWED",
            current_path="phase1",
            current_name="Search",
            phase_type="feature",
            local_step=6,
            local_stage="implementation",
        ),
    )

    assert run_command(monkeypatch, "next") == 0

    content = current_state(tmp_path)
    assert "- **Status**: COMPLETED" in content
