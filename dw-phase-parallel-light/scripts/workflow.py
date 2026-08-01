#!/usr/bin/env python3
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

skills_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(skills_dir / "dw-phase-parallel" / "scripts"))
from common import main  # noqa: E402


def phase_design_reviewed(root: Path) -> bool:
    current = root / ".dev-workflow-phase" / "CURRENT_STEP.md"
    if not current.exists():
        return False
    text = current.read_text(encoding="utf-8")
    values = {
        key: match.group(1).strip()
        for key in ("Status", "Global Step")
        for match in [re.search(rf"^\s*-\s+\*\*{re.escape(key)}\*\*:\s*(.*?)\s*$", text, re.M)]
        if match
    }
    return values.get("Status") == "REVIEWED" and values.get("Global Step") == "1"


def main_with_design_gate(argv: list[str]) -> int:
    if phase_design_reviewed(Path.cwd()):
        return main(argv, True)

    dw_phase = skills_dir / "dw-phase" / "scripts" / "workflow.py"
    if not dw_phase.exists():
        raise RuntimeError(f"dw-phase の workflow.py が見つかりません: {dw_phase}")
    print("phase 設計が未完了のため、dw-phase を先に開始します。")
    return subprocess.run([sys.executable, str(dw_phase)], cwd=Path.cwd(), check=False).returncode


raise SystemExit(main_with_design_gate(sys.argv[1:]))
