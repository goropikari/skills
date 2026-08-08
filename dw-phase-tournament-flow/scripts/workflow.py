#!/usr/bin/env python3
"""Own the tournament-flow state without delegating to another workflow skill."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(".dev-workflow-tournament")
STATE = ROOT / "state.json"
CURRENT = ROOT / "CURRENT_STEP.md"
STAGES = [
    ("context", "00_context.md", "記録", "リポジトリ状態と依頼範囲を記録する"),
    (
        "acceptance-contract",
        "01_acceptance_contract.md",
        "設計",
        "受入条件と検証条件を定義する",
    ),
    (
        "phase-design",
        "02_phase_design.md",
        "設計",
        "phase、依存、実装 mode、リスクを定義する",
    ),
    (
        "phase-artifacts",
        "phases/",
        "設計",
        "phase ごとの test design と validation plan を作成する",
    ),
    ("implementation", "worktree", "実装", "承認済み phase を実装し、証跡を収集する"),
    ("verification", "reports/", "検証", "review、受入確認、統合を行う"),
    ("complete", "reports/final-report.md", "完了", "最終 report を確定する"),
]
MAX_PARALLEL_DEFAULT = 3


def load() -> dict:
    if not STATE.exists():
        return {"status": "ACTIVE", "stage_index": 0, "gate": "WORK"}
    return json.loads(STATE.read_text(encoding="utf-8"))


def save(state: dict) -> None:
    ROOT.mkdir(exist_ok=True)
    STATE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    stage, target, label, description = STAGES[state["stage_index"]]
    CURRENT.write_text(
        "# DW Phase Tournament Flow\n\n"
        f"- **Stage**: {stage}\n"
        f"- **Target**: {ROOT / target}\n"
        f"- **Label**: {label}\n"
        f"- **Gate**: {state['gate']}\n"
        f"- **Status**: {state['status']}\n"
        f"- **Instruction**: {description}\n",
        encoding="utf-8",
    )


def ensure_artifact_tree() -> None:
    (ROOT / "phases").mkdir(parents=True, exist_ok=True)
    (ROOT / "reports").mkdir(parents=True, exist_ok=True)


def metadata(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*-\s+\*\*{re.escape(key)}\*\*:\s*(.*?)\s*$", text, re.M)
    return match.group(1).strip() if match else None


def load_phases() -> dict[str, dict]:
    text = (ROOT / "02_phase_design.md").read_text(encoding="utf-8")
    sections = list(
        re.finditer(
            r"^##\s+Phase\s+(\d+):\s*(.*?)\s*$([\s\S]*?)(?=^##\s+Phase\s+\d+:|\Z)",
            text,
            re.M,
        )
    )
    phases: dict[str, dict] = {}
    for match in sections:
        number = int(match.group(1))
        body = match.group(3)
        depends = metadata(body, "Depends On") or "none"
        dependencies = (
            []
            if depends.lower() == "none"
            else [item.strip() for item in depends.split(",")]
        )
        phase_id = f"phase{number}"
        phases[phase_id] = {
            "id": phase_id,
            "number": number,
            "name": match.group(2).strip(),
            "depends_on": dependencies,
            "status": "READY",
            "worktree": "",
            "branch": "",
            "request_file": "",
            "completion_file": "",
        }
    ids = set(phases)
    for phase in phases.values():
        if any(dep not in ids or dep == phase["id"] for dep in phase["depends_on"]):
            raise ValueError(f"{phase['id']} の Depends On が不正です")
    return dict(sorted(phases.items(), key=lambda item: item[1]["number"]))


def phase_slug(phase: dict) -> str:
    return (
        re.sub(r"[^a-z0-9]+", "-", phase["name"].lower()).strip("-")[:48] or phase["id"]
    )


def phase_worktree(phase: dict) -> tuple[Path, str]:
    slug = phase_slug(phase)
    branch = f"tournament/{phase['id']}-{slug}"
    path = Path.cwd() / ".worktrees" / "tournament" / f"{phase['id']}-{slug}"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        subprocess.run(
            ["git", "worktree", "add", "-b", branch, str(path), "HEAD"], check=True
        )
    return path, branch


def phase_design_section(phase: dict) -> str:
    text = (ROOT / "02_phase_design.md").read_text(encoding="utf-8")
    match = re.search(
        rf"^##\s+Phase\s+{phase['number']}:.*?(?=^##\s+Phase\s+\d+:|\Z)",
        text,
        re.M | re.S,
    )
    return match.group(0).strip() if match else ""


def ready_phases(state: dict) -> list[dict]:
    phases = state.get("phases", {})
    return [
        phase
        for phase in phases.values()
        if phase["status"] == "READY"
        and all(phases[dep]["status"] == "COMPLETED" for dep in phase["depends_on"])
    ]


def poll_phases(state: dict) -> None:
    for phase in state.get("phases", {}).values():
        if phase["status"] != "RUNNING" or not phase["completion_file"]:
            continue
        marker = Path(phase["completion_file"])
        if not marker.exists():
            continue
        try:
            result = int(marker.read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            continue
        phase["status"] = "READY_TO_COMMIT" if result == 0 else "BLOCKED"


def schedule_phases(state: dict) -> None:
    running = sum(
        phase["status"] == "RUNNING" for phase in state.get("phases", {}).values()
    )
    for phase in ready_phases(state):
        if running >= state.get("max_parallel", MAX_PARALLEL_DEFAULT):
            break
        worktree, branch = phase_worktree(phase)
        stamp = int(time.time() * 1000)
        request = ROOT / "requests" / f"{phase['id']}-{stamp}.md"
        completion = ROOT / "completion" / f"{phase['id']}-{stamp}.exit"
        request.parent.mkdir(parents=True, exist_ok=True)
        completion.parent.mkdir(parents=True, exist_ok=True)
        request.write_text(
            f"""# Phase implementation request

対象 phase: {phase["id"]} {phase["name"]}
依存: {", ".join(phase["depends_on"]) or "none"}
Worktree: {worktree}
Branch: {branch}

この worktree だけで設計に従って実装、テスト、自己レビューを行ってください。
commit、push、PR 作成は禁止です。caller root は変更しないでください。

--- phase design ---
{phase_design_section(phase)}
--- phase design end ---

--- acceptance contract ---
{(ROOT / "01_acceptance_contract.md").read_text(encoding="utf-8")}
--- acceptance contract end ---

完了時に {completion} へ成功なら `0`、失敗なら `1` だけを書き込んでください。
""",
            encoding="utf-8",
        )
        phase.update(
            {
                "status": "RUNNING",
                "worktree": str(worktree),
                "branch": branch,
                "request_file": str(request),
                "completion_file": str(completion),
            }
        )
        running += 1
        print(f"{phase['id']}: request={request} worktree={worktree}")


def complete_phase(state: dict, phase_id: str) -> int:
    phase = state.get("phases", {}).get(phase_id)
    if phase is None:
        print(f"ERROR: unknown phase: {phase_id}", file=sys.stderr)
        return 2
    if phase["status"] != "READY_TO_COMMIT":
        print(f"ERROR: {phase_id} is not ready to commit", file=sys.stderr)
        return 2
    phase["status"] = "COMPLETED"
    schedule_phases(state)
    save(state)
    show(state)
    return 0


def initialize_phases(state: dict) -> None:
    state["phases"] = load_phases()
    state["max_parallel"] = MAX_PARALLEL_DEFAULT


def phase_design_error() -> str | None:
    path = ROOT / "02_phase_design.md"
    if not path.exists():
        return f"missing required artifact: {path}"
    text = path.read_text(encoding="utf-8")
    headings = list(re.finditer(r"^## Phase (\d+):.+$", text, re.MULTILINE))
    if not headings:
        return "02_phase_design.md must contain one or more '## Phase N:' sections"
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section = text[heading.start() : end]
        phase_number = heading.group(1)
        if not re.search(r"^### Acceptance Criteria\s*$", section, re.MULTILINE):
            return f"Phase {phase_number} is missing '### Acceptance Criteria'"
        if not re.search(rf"AC-P{phase_number}-\d+", section):
            return f"Phase {phase_number} needs at least one AC-P{phase_number}-* criterion"
        if not re.search(r"Expected Result|期待結果", section, re.IGNORECASE):
            return f"Phase {phase_number} acceptance criteria need Expected Result"
        if not re.search(r"Evidence|証跡", section, re.IGNORECASE):
            return f"Phase {phase_number} acceptance criteria need Evidence"
    return None


def show(state: dict) -> None:
    stage, target, label, description = STAGES[state["stage_index"]]
    print(f"STAGE: {stage}")
    print(f"TARGET: {ROOT / target}")
    print(f"GATE: {state['gate']}")
    print(f"STATUS: {state['status']}")
    print(f"INSTRUCTION: {description}")


def transition(command: str) -> int:
    state = load()
    ensure_artifact_tree()

    if command in {"", "status"}:
        poll_phases(state)
        if state.get("stage_index") == 4:
            schedule_phases(state)
        save(state)
        show(state)
        for phase in state.get("phases", {}).values():
            print(f"{phase['id']}: {phase['status']} (branch={phase['branch'] or '-'})")
        return 0
    if state["status"] == "COMPLETED":
        print("ERROR: workflow is already completed", file=sys.stderr)
        return 2
    if command == "review":
        if state["gate"] != "WORK":
            print("ERROR: review requires WORK gate", file=sys.stderr)
            return 2
        state["gate"] = "REVIEW"
    elif command == "approve":
        if state["gate"] != "REVIEW":
            print("ERROR: approve requires REVIEW gate", file=sys.stderr)
            return 2
        if state["stage_index"] == 2:
            error = phase_design_error()
            if error:
                print(f"ERROR: {error}", file=sys.stderr)
                return 2
        state["gate"] = "APPROVED"
    elif command == "next":
        if state["gate"] != "APPROVED":
            print("ERROR: next requires APPROVED gate", file=sys.stderr)
            return 2
        if state["stage_index"] == len(STAGES) - 1:
            state["status"] = "COMPLETED"
        else:
            state["stage_index"] += 1
            state["gate"] = "WORK"
            if state["stage_index"] == 3:
                initialize_phases(state)
            if state["stage_index"] == 3:
                ensure_artifact_tree()
            if state["stage_index"] == 4:
                schedule_phases(state)
    elif command.startswith("complete "):
        return complete_phase(state, command.split(maxsplit=1)[1])
    else:
        print(
            "Usage: workflow.py [review|approve|next|status|complete phaseN]",
            file=sys.stderr,
        )
        return 2

    save(state)
    show(state)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) > 2 or (args and args[0] == "complete" and len(args) != 2):
        print(
            "Usage: workflow.py [review|approve|next|status|complete phaseN]",
            file=sys.stderr,
        )
        return 2
    command = (
        " ".join(args) if args and args[0] == "complete" else (args[0] if args else "")
    )
    return transition(command)


if __name__ == "__main__":
    raise SystemExit(main())
