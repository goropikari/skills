#!/usr/bin/env python3
"""Small, deterministic state machine for acceptance-driven-app."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PHASES = [
    "bootstrap",
    "acceptance-contract",
    "design",
    "implement-loop",
    "verification",
    "pr-ready",
]
ROOT = Path(".acceptance-driven-app")
STATE = ROOT / "state.json"
CURRENT = ROOT / "CURRENT_STEP.md"


def load() -> dict:
    if not STATE.exists():
        return {"status": "ACTIVE", "phase_index": 0, "gate": "WORK"}
    return json.loads(STATE.read_text())


def save(state: dict) -> None:
    ROOT.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    phase = PHASES[state["phase_index"]]
    CURRENT.write_text(
        f"# Acceptance-Driven App Workflow\n\n"
        f"- **Phase**: {phase}\n"
        f"- **Gate**: {state['gate']}\n"
        f"- **Status**: {state['status']}\n"
        f"- **Mode**: {state.get('mode', 'manual')}\n"
    )


def show(state: dict) -> None:
    phase = PHASES[state["phase_index"]]
    print(f"PHASE: {phase}")
    print(f"GATE: {state['gate']}")
    print(f"STATUS: {state['status']}")
    print(f"MODE: {state.get('mode', 'manual')}")


def transition(command: str) -> int:
    state = load()
    if command == "status":
        show(state)
        return 0
    if state["status"] == "BLOCKED":
        print("BLOCKED: resolve the recorded blocker before continuing")
        return 2
    if command == "review":
        state["gate"] = "REVIEW"
    elif command == "approve":
        if state["gate"] != "REVIEW":
            print("ERROR: approve requires REVIEW gate")
            return 2
        state["gate"] = "WORK"
        if state["phase_index"] == len(PHASES) - 1:
            state["status"] = "COMPLETED"
    elif command in {"next", "auto"}:
        state["mode"] = "auto" if command == "auto" else "manual"
        if state["gate"] == "REVIEW" and command == "next":
            print("ERROR: approve or auto is required at a REVIEW gate")
            return 2
        if state["gate"] == "REVIEW":
            state["gate"] = "WORK"
        if command == "next" and state["phase_index"] == len(PHASES) - 1:
            state["status"] = "COMPLETED"
        elif command == "auto":
            state["phase_index"] = min(state["phase_index"] + 1, len(PHASES) - 1)
            state["gate"] = "REVIEW"
        else:
            state["phase_index"] = min(state["phase_index"] + 1, len(PHASES) - 1)
    else:
        print("ERROR: use next, review, approve, status, or auto")
        return 2
    save(state)
    show(state)
    return 0


def main(argv: list[str]) -> int:
    ROOT.mkdir(exist_ok=True)
    command = argv[1] if len(argv) > 1 else "status"
    return transition(command)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
