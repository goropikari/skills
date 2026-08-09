#!/usr/bin/env python3
"""Run baseline mechanical checks and record compact, auditable evidence."""

import argparse
import json
import re
import shlex
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

SHELL_META = set(";&|<>`$()")
SECRET = re.compile(r"(?i)(api[_-]?key|token|secret|password)(\s*[:=]\s*)[^\s,;]+")


def now():
    return datetime.now(timezone.utc).isoformat()


def safe(text, limit=4000):
    text = SECRET.sub(r"\1\2[REDACTED]", text or "")
    return text[-limit:]


def git_files(root):
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--short"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    return [
        line[3:] if len(line) > 3 else line
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def run_check(root, check, timeout):
    command = check.get("command", "")
    result = {
        "id": check.get("id"),
        "status": "BLOCKED",
        "command": command,
        "exit_code": None,
        "evidence": "",
    }
    if not command or any(char in command for char in SHELL_META):
        result["evidence"] = (
            "Command is empty or uses shell syntax; run it manually and record evidence."
        )
        return result
    try:
        completed = subprocess.run(
            shlex.split(command),
            cwd=root,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        result["exit_code"] = completed.returncode
        result["status"] = "PASS" if completed.returncode == 0 else "FAIL"
        result["evidence"] = safe((completed.stdout + "\n" + completed.stderr).strip())
    except FileNotFoundError as exc:
        result["evidence"] = f"Executable unavailable: {exc.filename}"
    except subprocess.TimeoutExpired as exc:
        result["evidence"] = f"Timed out after {timeout}s.\n{safe(exc.stderr or '')}"
    except (OSError, ValueError) as exc:
        result["evidence"] = f"Could not execute command: {exc}"
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument(
        "--check-id", action="append", help="Run only this check id; repeatable"
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    quality = root / ".quality"
    baseline_path = quality / "baseline.json"
    state_path = quality / "state.json"
    if not baseline_path.exists():
        raise SystemExit(
            "Missing .quality/baseline.json; initialize the repository baseline first"
        )
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    checks = baseline.get("mechanical_checks", [])
    if args.check_id:
        checks = [check for check in checks if check.get("id") in set(args.check_id)]
    started = now()
    results = (
        []
        if args.dry_run
        else [run_check(root, check, args.timeout) for check in checks]
    )
    required_by_id = {check.get("id"): check.get("required", True) for check in checks}
    required_failures = [
        r
        for r in results
        if required_by_id.get(r["id"], True) and r["status"] == "FAIL"
    ]
    required_blocks = [
        r
        for r in results
        if required_by_id.get(r["id"], True) and r["status"] == "BLOCKED"
    ]
    optional_failures = [
        r
        for r in results
        if not required_by_id.get(r["id"], True) and r["status"] == "FAIL"
    ]
    if args.dry_run:
        gate = "NOT_RUN"
    elif required_failures:
        gate = "FAIL"
    elif required_blocks:
        gate = "BLOCKED"
    elif optional_failures or not results:
        gate = "PASS_WITH_NOTES"
    else:
        gate = "PASS"
    state = {
        "schema_version": 1,
        "baseline_version": baseline.get("baseline_version"),
        "run_id": str(uuid.uuid4()),
        "started_at": started,
        "finished_at": now(),
        "result": gate,
        "checks": results,
        "findings": [],
        "changed_scope": git_files(root),
        "notes": ["Mechanical result only; semantic review is still required."]
        if not args.dry_run
        else ["Dry run; no commands executed."],
    }
    if not args.dry_run:
        quality.mkdir(exist_ok=True)
        state_path.write_text(
            json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    print(json.dumps(state, indent=2, ensure_ascii=False))
    raise SystemExit(1 if gate in {"FAIL", "BLOCKED"} else 0)


if __name__ == "__main__":
    main()
