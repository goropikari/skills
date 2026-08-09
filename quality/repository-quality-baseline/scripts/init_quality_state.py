#!/usr/bin/env python3
"""Create a conservative, inspectable .quality baseline for a repository."""

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone


def command_checks(root: Path):
    checks = []
    package = root / "package.json"
    if package.exists():
        try:
            scripts = json.loads(package.read_text(encoding="utf-8")).get("scripts", {})
        except (OSError, json.JSONDecodeError):
            scripts = {}
        for name in (
            "build",
            "typecheck",
            "lint",
            "test",
            "test:unit",
            "test:integration",
        ):
            if name in scripts:
                checks.append(
                    {
                        "id": name,
                        "command": f"npm run {name}",
                        "required": name in {"build", "typecheck", "test"},
                        "when": "repository script exists",
                    }
                )
    if (
        (root / "pyproject.toml").exists()
        or (root / "pytest.ini").exists()
        or (root / "tests").is_dir()
    ):
        checks.append(
            {
                "id": "python-tests",
                "command": "python -m pytest",
                "required": True,
                "when": "Python tests are present",
            }
        )
    if (root / "go.mod").exists():
        checks.extend(
            [
                {
                    "id": "go-test",
                    "command": "go test ./...",
                    "required": True,
                    "when": "Go module",
                },
                {
                    "id": "go-vet",
                    "command": "go vet ./...",
                    "required": True,
                    "when": "Go module",
                },
            ]
        )
    if (root / "Cargo.toml").exists():
        checks.extend(
            [
                {
                    "id": "cargo-check",
                    "command": "cargo check",
                    "required": True,
                    "when": "Rust crate",
                },
                {
                    "id": "cargo-test",
                    "command": "cargo test",
                    "required": True,
                    "when": "Rust crate",
                },
            ]
        )
    if (root / "Makefile").exists():
        checks.append(
            {
                "id": "make-check",
                "command": "make check",
                "required": False,
                "when": "verify that the target exists",
            }
        )
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    quality = root / ".quality"
    quality.mkdir(exist_ok=True)
    baseline_path = quality / "baseline.json"
    state_path = quality / "state.json"
    if not args.force and (baseline_path.exists() or state_path.exists()):
        raise SystemExit(
            ".quality state already exists; review it or pass --force explicitly"
        )

    baseline = {
        "schema_version": 1,
        "baseline_version": "1.0.0",
        "repository": {"root": "."},
        "repository_tools": [],
        "analysis_skills": [
            {
                "name": name,
                "applied": False,
                "evidence": "Apply during repository analysis and record evidence.",
            }
            for name in (
                "requirements-review",
                "architecture-review",
                "change-impact-review",
                "security-review",
                "whitebox-risk-based-test",
            )
        ],
        "mechanical_checks": command_checks(root),
        "must_quality": [
            {
                "id": "requirements",
                "rule": "Requested behavior is satisfied and demonstrated by tests or evidence",
                "severity": "critical",
            },
            {
                "id": "regression",
                "rule": "Existing supported behavior is not unintentionally broken",
                "severity": "critical",
            },
            {
                "id": "repository-conventions",
                "rule": "Repository-local guidance and public contracts are respected",
                "severity": "major",
            },
            {
                "id": "security",
                "rule": "No critical security defect is introduced",
                "severity": "critical",
            },
        ],
        "performance_quality": [
            {
                "id": "simplicity",
                "rule": "Prefer the smallest understandable change",
                "severity": "non_blocking",
            },
            {
                "id": "maintainability",
                "rule": "Keep responsibilities, names, and tests easy to evolve",
                "severity": "non_blocking",
            },
        ],
        "critical_defects": [
            "Security compromise or secret exposure",
            "Data loss, corruption, or unsafe migration",
            "Required behavior missing or public API broken without approval",
        ],
        "assumptions": [
            "Discovered commands must be reviewed before the first gate run."
        ],
    }
    now = datetime.now(timezone.utc).isoformat()
    state = {
        "schema_version": 1,
        "baseline_version": "1.0.0",
        "run_id": None,
        "started_at": None,
        "finished_at": now,
        "result": "NOT_RUN",
        "checks": [],
        "findings": [],
        "changed_scope": [],
        "notes": ["Baseline initialized; no quality gate has run yet."],
    }
    baseline_path.write_text(
        json.dumps(baseline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    state_path.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    readme = quality / "README.md"
    readme.write_text(
        "# Repository quality state\n\n- `baseline.json` is the versioned quality contract.\n- `state.json` records the latest gate evidence.\n- Run `$coding-quality-gate` after implementation.\n",
        encoding="utf-8",
    )
    print(f"Initialized {quality}")


if __name__ == "__main__":
    main()
