from pathlib import Path
import importlib.util
import sys


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "workflow.py"
spec = importlib.util.spec_from_file_location("workflow", MODULE_PATH)
workflow = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = workflow
spec.loader.exec_module(workflow)


def test_generate_workflow_steps_zero_returns_initial_steps_only():
    steps = workflow.generate_workflow_steps(0)

    assert len(steps) == 2
    assert steps[0].target == ".dev-workflow-layer/00_project_requirements.md"
    assert steps[1].target == ".dev-workflow-layer/01_layer_design.md"


def test_generate_workflow_steps_two_layers_returns_fourteen_steps():
    steps = workflow.generate_workflow_steps(2)

    assert len(steps) == 14
    assert steps[2].target == ".dev-workflow-layer/layer1/01_requirements.md"
    assert steps[7].target == "実プロジェクト内の適切なソースファイル"
    assert steps[8].target == ".dev-workflow-layer/layer2/01_requirements.md"
    assert steps[13].name == "Layer 2: 内部ロジック実装"


def test_parse_layers_from_text_valid_metadata():
    text = "# Layer Design\n\n- **Layers**: 3\n"

    assert workflow.parse_layers_from_text(text) == 3


def test_parse_layers_from_text_rejects_missing_zero_too_large_and_non_numeric():
    assert workflow.parse_layers_from_text("# Layer Design\n") is None
    assert workflow.parse_layers_from_text("- **Layers**: 0\n") is None
    assert workflow.parse_layers_from_text("- **Layers**: 21\n") is None
    assert workflow.parse_layers_from_text("- **Layers**: three\n") is None


def test_review_approve_and_next_update_current_step(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(workflow.sys, "argv", ["workflow.py"])

    workflow.init_environment(tmp_path)
    assert workflow.main() == 0
    content = (tmp_path / ".dev-workflow-layer" / "CURRENT_STEP.md").read_text(
        encoding="utf-8"
    )
    assert "- **Step**: 0" in content
    assert "- **Status**: IN_PROGRESS" in content
    assert "- **Layers**: 0" in content

    monkeypatch.setattr(workflow.sys, "argv", ["workflow.py", "review"])
    assert workflow.main() == 0
    content = (tmp_path / ".dev-workflow-layer" / "CURRENT_STEP.md").read_text(
        encoding="utf-8"
    )
    assert "- **Status**: REVIEW_PENDING" in content

    monkeypatch.setattr(workflow.sys, "argv", ["workflow.py", "approve"])
    assert workflow.main() == 0
    content = (tmp_path / ".dev-workflow-layer" / "CURRENT_STEP.md").read_text(
        encoding="utf-8"
    )
    assert "- **Status**: REVIEWED" in content

    monkeypatch.setattr(workflow.sys, "argv", ["workflow.py", "next"])
    assert workflow.main() == 0
    content = (tmp_path / ".dev-workflow-layer" / "CURRENT_STEP.md").read_text(
        encoding="utf-8"
    )
    assert "- **Step**: 1" in content
    assert "- **Status**: IN_PROGRESS" in content


def test_invalid_layers_do_not_advance_from_step_one(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    workflow.write_status(tmp_path, 1, "REVIEWED", 0)
    design = tmp_path / ".dev-workflow-layer" / "01_layer_design.md"
    design.write_text("- **Layers**: 21\n", encoding="utf-8")

    monkeypatch.setattr(workflow.sys, "argv", ["workflow.py", "next"])
    assert workflow.main() == 1

    content = (tmp_path / ".dev-workflow-layer" / "CURRENT_STEP.md").read_text(
        encoding="utf-8"
    )
    assert "- **Step**: 1" in content
    assert "- **Status**: IN_PROGRESS" in content
    assert "- **Layers**: 0" in content


def test_valid_layers_advance_from_step_one_and_persist_layers(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow.init_environment(tmp_path)
    workflow.write_status(tmp_path, 1, "REVIEWED", 0)
    design = tmp_path / ".dev-workflow-layer" / "01_layer_design.md"
    design.write_text("- **Layers**: 2\n", encoding="utf-8")

    monkeypatch.setattr(workflow.sys, "argv", ["workflow.py", "next"])
    assert workflow.main() == 0

    content = (tmp_path / ".dev-workflow-layer" / "CURRENT_STEP.md").read_text(
        encoding="utf-8"
    )
    assert "- **Step**: 2" in content
    assert "- **Target**: .dev-workflow-layer/layer1/01_requirements.md" in content
    assert "- **Status**: IN_PROGRESS" in content
    assert "- **Layers**: 2" in content
