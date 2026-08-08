import json
import subprocess
import sys
from pathlib import Path


SCRIPT = (
    Path(__file__).parents[1]
    / "implementation"
    / "acceptance-driven-app"
    / "scripts"
    / "workflow.py"
)


def run(tmp_path, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )


def state(tmp_path):
    return json.loads((tmp_path / ".acceptance-driven-app/state.json").read_text())


def test_auto_stops_at_next_phase_review_gate(tmp_path):
    result = run(tmp_path, "auto")

    assert result.returncode == 0
    assert state(tmp_path) == {
        "status": "ACTIVE",
        "phase_index": 1,
        "phase": "acceptance-contract",
        "phase_description": "受け入れ条件を実行可能な契約にする",
        "gate": "REVIEW",
        "mode": "auto",
    }
    assert "acceptance-contract" in result.stdout

    result = run(tmp_path, "auto")
    assert result.returncode == 0
    assert state(tmp_path)["phase_index"] == 2
    assert state(tmp_path)["phase"] == "design"
    assert (
        state(tmp_path)["phase_description"]
        == "アーキテクチャ、インターフェース、リスク、テスト戦略を設計する"
    )
    assert state(tmp_path)["gate"] == "REVIEW"


def test_initial_state_includes_human_readable_phase(tmp_path):
    result = run(tmp_path, "next")
    assert result.returncode == 0
    assert state(tmp_path)["phase"] == "acceptance-contract"
    assert state(tmp_path)["phase_description"] == "受け入れ条件を実行可能な契約にする"


def test_approve_requires_review(tmp_path):
    result = run(tmp_path, "approve")

    assert result.returncode == 2
    assert "requires REVIEW" in result.stdout


def test_manual_review_approve_next_sequence(tmp_path):
    assert run(tmp_path, "review").returncode == 0
    assert run(tmp_path, "approve").returncode == 0
    result = run(tmp_path, "next")

    assert result.returncode == 0
    assert state(tmp_path)["phase_index"] == 1
    assert state(tmp_path)["gate"] == "WORK"
