import json
import subprocess
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
HARNESS_VALIDATOR = (
    REPOSITORY_ROOT / "implementation-orchestrator/scripts/validate_harness.py"
)
EVIDENCE_VALIDATOR = (
    REPOSITORY_ROOT / "implementation-orchestrator/scripts/validate_evidence.py"
)
EVAL_VALIDATOR = (
    REPOSITORY_ROOT / "agent-workflow-evals/scripts/validate_eval_manifest.py"
)
ORCHESTRATOR_SKILL = REPOSITORY_ROOT / "implementation-orchestrator/SKILL.md"
PLAN_TEMPLATE = (
    REPOSITORY_ROOT
    / "implementation-orchestrator/references/implementation-plan-template.md"
)
ACCEPTANCE_CONTRACT = (
    REPOSITORY_ROOT
    / "implementation-orchestrator/skills/implementation-acceptance-contract/SKILL.md"
)
VERIFICATION_GATE = (
    REPOSITORY_ROOT
    / "implementation-orchestrator/skills/implementation-verification-gate/SKILL.md"
)


def run_validator(script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


def write_json(path: Path, data: dict) -> Path:
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_harness_validator_rejects_missing_destructive_rejection_case(
    tmp_path: Path,
) -> None:
    manifest = write_json(
        tmp_path / "manifest.json",
        {
            "version": 1,
            "goal": "Delete a branch safely.",
            "consumer_entry": "git tool delete",
            "risks": ["destructive"],
            "immutable_paths": ["manifest.json"],
            "criteria": [
                {
                    "id": "AC-001",
                    "required": True,
                    "tags": ["consumer-entry"],
                    "command": "tool delete branch",
                    "expected": "branch is deleted",
                }
            ],
        },
    )

    result = run_validator(
        HARNESS_VALIDATOR,
        "--repo-root",
        str(tmp_path),
        "--stage",
        "plan",
        str(manifest),
    )

    assert result.returncode == 1
    assert "rejection-no-side-effect" in result.stdout


def test_harness_validator_accepts_frozen_manifest(tmp_path: Path) -> None:
    test_path = tmp_path / "tests" / "acceptance" / "consumer_test.py"
    test_path.parent.mkdir(parents=True)
    test_path.write_text("pass\n", encoding="utf-8")
    manifest_path = tmp_path / "manifest.json"
    manifest = {
        "version": 1,
        "goal": "Delete a branch safely.",
        "consumer_entry": "git tool delete",
        "risks": ["destructive"],
        "immutable_paths": ["manifest.json", "tests/acceptance/consumer_test.py"],
        "criteria": [
            {
                "id": "AC-001",
                "required": True,
                "tags": ["rejection-no-side-effect"],
                "command": "tool delete --invalid",
                "expected": "no branch changes",
                "test_path": "tests/acceptance/consumer_test.py",
            }
        ],
    }
    write_json(manifest_path, manifest)

    result = run_validator(
        HARNESS_VALIDATOR,
        "--repo-root",
        str(tmp_path),
        "--stage",
        "frozen",
        str(manifest_path),
    )

    assert result.returncode == 0, result.stdout


def test_harness_validator_detects_frozen_file_changes(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"], cwd=tmp_path, check=True
    )
    manifest = {
        "version": 1,
        "goal": "Check a public command.",
        "consumer_entry": "tool check",
        "risks": [],
        "immutable_paths": ["manifest.json"],
        "criteria": [
            {
                "id": "AC-001",
                "required": True,
                "tags": [],
                "command": "tool check",
                "expected": "success",
            }
        ],
    }
    manifest_path = write_json(tmp_path / "manifest.json", manifest)
    subprocess.run(["git", "add", "manifest.json"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "freeze harness"], cwd=tmp_path, check=True)
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    manifest["goal"] = "Changed after freeze."
    write_json(manifest_path, manifest)

    result = run_validator(
        HARNESS_VALIDATOR,
        "--repo-root",
        str(tmp_path),
        "--stage",
        "frozen",
        "--base",
        base,
        str(manifest_path),
    )

    assert result.returncode == 1
    assert "immutable paths changed" in result.stdout


def test_evidence_validator_requires_final_results(tmp_path: Path) -> None:
    evidence = write_json(
        tmp_path / "evidence.json",
        {
            "version": 1,
            "acceptance_criteria": [{"id": "AC-001", "required": True}],
            "risks": [{"id": "RISK-API-001"}],
            "selected_checks": [
                {"id": "CHECK-001", "risk_ids": ["RISK-API-001"], "required": True}
            ],
            "results": [{"id": "AC-001", "status": "PASS", "evidence": ["pytest"]}],
            "residual_risks": [],
        },
    )

    result = run_validator(EVIDENCE_VALIDATOR, "--stage", "final", str(evidence))

    assert result.returncode == 1
    assert "missing final result for CHECK-001" in result.stdout


def test_evidence_validator_rejects_results_during_planning(tmp_path: Path) -> None:
    evidence = write_json(
        tmp_path / "evidence.json",
        {
            "version": 1,
            "acceptance_criteria": [{"id": "AC-001", "required": True}],
            "risks": [],
            "selected_checks": [],
            "results": [{"id": "AC-001", "status": "PASS", "evidence": ["pytest"]}],
        },
    )

    result = run_validator(EVIDENCE_VALIDATOR, "--stage", "plan", str(evidence))

    assert result.returncode == 1
    assert "results must be empty" in result.stdout


def test_evidence_validator_accepts_complete_final_evidence(tmp_path: Path) -> None:
    evidence = write_json(
        tmp_path / "evidence.json",
        {
            "version": 1,
            "acceptance_criteria": [{"id": "AC-001", "required": True}],
            "risks": [{"id": "RISK-API-001"}],
            "selected_checks": [
                {"id": "CHECK-001", "risk_ids": ["RISK-API-001"], "required": True}
            ],
            "results": [
                {"id": "AC-001", "status": "PASS", "evidence": ["pytest"]},
                {"id": "CHECK-001", "status": "PASS", "evidence": ["review report"]},
            ],
            "residual_risks": [],
        },
    )

    result = run_validator(EVIDENCE_VALIDATOR, "--stage", "final", str(evidence))

    assert result.returncode == 0, result.stdout


def test_orchestrator_requires_documented_example_and_specific_evidence() -> None:
    skill = ORCHESTRATOR_SKILL.read_text(encoding="utf-8")
    template = PLAN_TEMPLATE.read_text(encoding="utf-8")
    contract = ACCEPTANCE_CONTRACT.read_text(encoding="utf-8")
    verification = VERIFICATION_GATE.read_text(encoding="utf-8")

    assert "## Required route decision" in template
    assert "exactly as documented" in skill
    assert "regression-only harness" in skill
    assert "exactly as documented" in contract
    assert "exit status" in verification


def test_eval_manifest_validator_requires_harnesses(tmp_path: Path) -> None:
    manifest = write_json(
        tmp_path / "evals.json",
        {
            "version": 1,
            "workflows": [
                {"id": "WF-ORCHESTRATOR", "skill": "implementation-orchestrator"}
            ],
            "tasks": [{"id": "TASK-API-001"}],
        },
    )

    result = run_validator(EVAL_VALIDATOR, str(manifest))

    assert result.returncode == 1
    assert "harness" in result.stdout


def test_eval_manifest_validator_accepts_workflow_and_task(tmp_path: Path) -> None:
    manifest = write_json(
        tmp_path / "evals.json",
        {
            "version": 1,
            "workflows": [
                {"id": "WF-ORCHESTRATOR", "skill": "implementation-orchestrator"}
            ],
            "tasks": [
                {
                    "id": "TASK-API-001",
                    "harness": "tasks/api/acceptance-harness/manifest.json",
                }
            ],
        },
    )

    result = run_validator(EVAL_VALIDATOR, str(manifest))

    assert result.returncode == 0, result.stdout
