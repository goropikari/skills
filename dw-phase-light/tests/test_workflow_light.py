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


def current_state(tmp_path):
    return (tmp_path / ".dev-workflow-phase-light" / "CURRENT_STEP.md").read_text(
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


def test_global_steps_advance_without_human_review(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    workflow.write_state(
        tmp_path,
        workflow.WorkflowState(status="IN_PROGRESS", global_step=0),
    )

    requirements = tmp_path / ".dev-workflow-phase-light" / "00_project_requirements.md"
    requirements.write_text("requirements", encoding="utf-8")
    assert run_command(monkeypatch, "next") == 0
    assert "- **Global Step**: 1" in current_state(tmp_path)

    design = tmp_path / ".dev-workflow-phase-light" / "01_phase_design.md"
    design.write_text(
        """- **Phases**: 1

## Phase 1: Search
- **Phase Type**: feature
""",
        encoding="utf-8",
    )
    assert run_command(monkeypatch, "next") == 0

    content = current_state(tmp_path)
    assert "- **Current Path**: phase1" in content
    assert "- **Current Name**: Search" in content
    assert "- **Phase Type**: feature" in content
    assert "- **Local Step**: 1" in content
    assert "- **Local Stage**: definition" in content


def test_phase_internal_steps_progress_without_review(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    workflow.write_state(
        tmp_path,
        workflow.WorkflowState(
            status="IN_PROGRESS",
            current_path="phase1",
            current_name="Search",
            phase_type="feature",
            local_step=1,
            local_stage="definition",
        ),
    )

    definition = tmp_path / ".dev-workflow-phase-light" / "phase1" / "01_definition.md"
    definition.parent.mkdir(parents=True)
    definition.write_text("- **Phase Type**: feature\n", encoding="utf-8")
    assert run_command(monkeypatch, "next") == 0
    assert "- **Local Stage**: gherkin" in current_state(tmp_path)

    gherkin = (
        tmp_path
        / ".dev-workflow-phase-light"
        / "phase1"
        / "02_gherkin"
        / "spec.feature"
    )
    gherkin.parent.mkdir(parents=True)
    gherkin.write_text("Feature: Search\n", encoding="utf-8")
    assert run_command(monkeypatch, "next") == 0
    assert "- **Local Stage**: test-design" in current_state(tmp_path)

    test_design = (
        tmp_path / ".dev-workflow-phase-light" / "phase1" / "03_test_design.md"
    )
    test_design.write_text("- **Split**: no\n", encoding="utf-8")
    assert run_command(monkeypatch, "next") == 0
    assert "- **Local Stage**: interface" in current_state(tmp_path)


def test_leaf_phase_requires_review_only_at_implementation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    phase_design = tmp_path / ".dev-workflow-phase-light" / "01_phase_design.md"
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
            status="IN_PROGRESS",
            current_path="phase1",
            current_name="Search",
            phase_type="feature",
            local_step=6,
            local_stage="implementation",
        ),
    )

    assert run_command(monkeypatch, "next") == 0
    assert "- **Local Stage**: implementation" in current_state(tmp_path)
    assert "- **Status**: IN_PROGRESS" in current_state(tmp_path)

    assert run_command(monkeypatch, "review") == 0
    assert "- **Status**: REVIEW_PENDING" in current_state(tmp_path)

    assert run_command(monkeypatch, "approve") == 0
    assert "- **Status**: REVIEWED" in current_state(tmp_path)

    assert run_command(monkeypatch, "next") == 0
    content = current_state(tmp_path)
    assert "- **Current Path**: phase2" in content
    assert "- **Current Name**: Admin" in content
    assert "- **Local Stage**: definition" in content

    phase_design_content = phase_design.read_text(encoding="utf-8")
    assert "## Phase 1: Search" in phase_design_content
    assert "- **Status**: COMPLETED" in phase_design_content


def test_review_is_rejected_before_implementation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    workflow.write_state(
        tmp_path,
        workflow.WorkflowState(
            status="IN_PROGRESS",
            current_path="phase1",
            current_name="Search",
            phase_type="feature",
            local_step=3,
            local_stage="test-design",
        ),
    )

    assert run_command(monkeypatch, "review") == 1
