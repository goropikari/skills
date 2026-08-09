#!/usr/bin/env python3
"""Build a bounded context packet from quality state and the current diff."""

import argparse
import json
import subprocess
from pathlib import Path


def git_diff(root, limit):
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "diff", "HEAD", "--", "."],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return result.stdout[-limit:]
    except (OSError, subprocess.SubprocessError):
        return "(git diff unavailable)"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-diff-chars", type=int, default=12000)
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    quality = root / ".quality"
    baseline = json.loads((quality / "baseline.json").read_text(encoding="utf-8"))
    state_path = quality / "state.json"
    state = (
        json.loads(state_path.read_text(encoding="utf-8"))
        if state_path.exists()
        else {}
    )
    print("# Quality context packet")
    print(
        f"Baseline: {baseline.get('baseline_version')} | Last gate: {state.get('result', 'NOT_RUN')}"
    )
    print("\n## Applied analysis skills")
    for skill in baseline.get("analysis_skills", []):
        print(
            f"- {skill.get('name')}: {'applied' if skill.get('applied') else 'not recorded'}"
        )
    print("\n## Required mechanical checks")
    for check in baseline.get("mechanical_checks", []):
        print(
            f"- {check.get('id')}: `{check.get('command')}` (required={check.get('required', True)})"
        )
    print("\n## Latest check failures or blocks")
    failures = [
        check
        for check in state.get("checks", [])
        if check.get("status") in {"FAIL", "BLOCKED"}
    ]
    print(
        "- none recorded"
        if not failures
        else "\n".join(
            f"- {check.get('id')}: {check.get('status')} — {check.get('evidence', '')[:500]}"
            for check in failures
        )
    )
    print("\n## Changed scope")
    for path in state.get("changed_scope", []):
        print(f"- {path}")
    print("\n## Must Quality")
    for rule in baseline.get("must_quality", []):
        print(f"- [{rule.get('severity')}] {rule.get('id')}: {rule.get('rule')}")
    print("\n## Bounded diff")
    print("```diff")
    print(git_diff(root, args.max_diff_chars))
    print("```")


if __name__ == "__main__":
    main()
