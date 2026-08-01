#!/usr/bin/env python3
"""Shared scheduler for dw-phase-parallel and dw-phase-parallel-light."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import time
import re
from pathlib import Path

STATE_DIR = ".dev-workflow-phase-parallel"
STATE_FILE = "STATE.json"
MAX_PARALLEL_DEFAULT = 3


def metadata(text: str, key: str) -> str | None:
    import re
    match = re.search(rf"^\s*-\s+\*\*{re.escape(key)}\*\*:\s*(.*?)\s*$", text, re.M)
    return match.group(1).strip() if match else None


def load_design(root: Path) -> list[dict]:
    import re
    path = root / ".dev-workflow-phase" / "01_phase_design.md"
    text = path.read_text(encoding="utf-8")
    count = int(metadata(text, "Phases") or "0")
    sections = list(re.finditer(r"^##\s+Phase\s+(\d+):\s*(.*?)\s*$([\s\S]*?)(?=^##\s+Phase\s+\d+:|\Z)", text, re.M))
    by_number = {int(m.group(1)): m for m in sections}
    if count < 1 or len(by_number) != count:
        raise ValueError("01_phase_design.md の phase 定義が不正です")
    phases = []
    for number in range(1, count + 1):
        match = by_number.get(number)
        if not match:
            raise ValueError(f"phase{number} がありません")
        body = match.group(3)
        depends = metadata(body, "Depends On") or "none"
        dependencies = [] if depends.lower() == "none" else [item.strip() for item in depends.split(",")]
        if any(not item.startswith("phase") or not item[5:].isdigit() for item in dependencies):
            raise ValueError(f"phase{number} の Depends On が不正です")
        phases.append({
            "id": f"phase{number}", "number": number, "name": match.group(2).strip(),
            "phase_type": metadata(body, "Phase Type") or "", "depends_on": dependencies,
        })
    ids = {phase["id"] for phase in phases}
    for phase in phases:
        if any(dep not in ids or dep == phase["id"] for dep in phase["depends_on"]):
            raise ValueError(f"{phase['id']} の依存先が不正です")
    return phases


def root_clean(root: Path) -> bool:
    result = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True, check=True)
    return not result.stdout.strip()


def read_state(root: Path) -> dict | None:
    path = root / STATE_DIR / STATE_FILE
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def write_state(root: Path, state: dict) -> None:
    directory = root / STATE_DIR
    directory.mkdir(exist_ok=True)
    (directory / STATE_FILE).write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def init(root: Path, mode: str, max_parallel: int) -> dict:
    if not root_clean(root):
        raise RuntimeError("親 worktree に tracked の未 commit 変更があります")
    current = root / ".dev-workflow-phase" / "CURRENT_STEP.md"
    if not current.exists() or metadata(current.read_text(encoding="utf-8"), "Status") != "REVIEWED" or metadata(current.read_text(encoding="utf-8"), "Global Step") != "1":
        raise RuntimeError("dw-phase の Global Step 1 が REVIEWED である必要があります")
    phases = load_design(root)
    state = {"version": 1, "mode": mode, "max_parallel": max_parallel, "base": str(subprocess.run(["git", "branch", "--show-current"], cwd=root, capture_output=True, text=True, check=True).stdout.strip()), "phases": {}}
    for phase in phases:
        state["phases"][phase["id"]] = {**phase, "status": "READY", "step": 1, "attempts": 0, "worktree": "", "branch": "", "pid": None, "pr": None}
    write_state(root, state)
    return state


def command_from_args(args: argparse.Namespace) -> str:
    configured = args.agent_cmd or os.environ.get("DW_PHASE_PARALLEL_AGENT_CMD", "")
    # Native subagents are owned by the calling Codex session; they cannot be
    # started from a shell command. Light mode uses request files for this
    # backend so it never falls back to `codex exec`.
    return configured or ("native-subagent" if args.light else "")


def ready_phases(state: dict) -> list[dict]:
    active = {phase["id"] for phase in state["phases"].values() if phase["status"] in {"RUNNING", "REVIEW_PENDING", "READY_TO_COMMIT", "PR_OPEN"}}
    result = []
    for phase in state["phases"].values():
        if phase["status"] != "READY":
            continue
        if all(state["phases"][dep]["status"] in {"MERGED", "COMPLETED"} for dep in phase["depends_on"]):
            result.append(phase)
    return [phase for phase in result if phase["id"] not in active]


def phase_slug(phase: dict) -> str:
    # Keep branch and worktree names portable: phase names may contain
    # Japanese or other non-ASCII characters, which must not leak into paths.
    return re.sub(r"[^a-z0-9]+", "-", phase["name"].lower()).strip("-")[:48].strip("-") or phase["id"]


def phase_worktree(root: Path, phase: dict) -> tuple[Path, str]:
    slug = phase_slug(phase)
    branch = f"phase/{phase['id']}-{slug}"
    path = root / ".worktrees" / "phase" / f"{phase['id']}-{slug}"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        subprocess.run(["git", "worktree", "add", "-b", branch, str(path), "HEAD"], cwd=root, check=True)
    return path, branch


def prompt(state: dict, phase: dict, light: bool) -> str:
    mode = "一括実装" if light else "ステップ単位のレビュー型"
    return f"""あなたは phase 実装 agent です。対象 phase: {phase['id']} {phase['name']}\nPhase Type: {phase['phase_type']}\n依存: {', '.join(phase['depends_on']) or 'none'}\nモード: {mode}\nこの worktree だけで作業してください。commit、push、PR 作成は禁止です。\n{'設計・実装・テスト・自己レビューまで一気に行い、対象テストと全体テストを実行してください。' if light else f'現在は step {phase["step"]} です。指定された成果物だけを作成し、後続 step を変更しないでください。完了後、対象テストを実行してください。'}\n完了内容とテスト結果を標準出力に報告してください。"""


def spawn(root: Path, state: dict, phase: dict, args: argparse.Namespace) -> None:
    worktree, branch = phase_worktree(root, phase)
    command = command_from_args(args)
    if not command:
        raise RuntimeError("--agent-cmd または DW_PHASE_PARALLEL_AGENT_CMD が必要です")
    if args.light and "codex exec" in command:
        raise RuntimeError("light mode は codex exec を起動しません。native subagent を使用してください")
    log = root / STATE_DIR / "logs" / f"{phase['id']}-{int(time.time())}.log"
    exit_file = root / STATE_DIR / "logs" / f"{phase['id']}-{int(time.time())}.exit"
    log.parent.mkdir(parents=True, exist_ok=True)
    if command == "native-subagent":
        request_file = root / STATE_DIR / "requests" / f"{phase['id']}-{int(time.time())}.md"
        request_file.parent.mkdir(parents=True, exist_ok=True)
        request_file.write_text(
            prompt(state, phase, args.light)
            + f"\n\n親 agent への完了通知: 作業終了時に {exit_file} に `0`（失敗時は `1`）だけを書き込んでください。\n",
            encoding="utf-8",
        )
        phase.update({
            "status": "RUNNING",
            "worktree": str(worktree),
            "branch": branch,
            "pid": None,
            "request_file": str(request_file),
            "completion_file": str(exit_file),
            "attempts": phase.get("attempts", 0) + 1,
        })
        print(f"{phase['id']}: native subagent request -> {request_file} (worktree={worktree})")
        return
    handle = log.open("w", encoding="utf-8")
    wrapped = f"{shlex.join(shlex.split(command))}; printf '%s' $? > {shlex.quote(str(exit_file))}"
    process = subprocess.Popen(["sh", "-c", wrapped], cwd=worktree, stdin=subprocess.PIPE, stdout=handle, stderr=subprocess.STDOUT, text=True)
    process.stdin.write(prompt(state, phase, args.light))
    process.stdin.close()
    phase.update({"status": "RUNNING", "worktree": str(worktree), "branch": branch, "pid": process.pid, "log": str(log), "exit_file": str(exit_file), "attempts": phase.get("attempts", 0) + 1})


def poll(root: Path, state: dict, args: argparse.Namespace) -> None:
    for phase in state["phases"].values():
        pid = phase.get("pid")
        if phase["status"] != "RUNNING":
            continue
        exit_file = Path(phase.get("exit_file") or phase.get("completion_file", ""))
        # A native subagent signals completion by writing the same exit marker
        # used by the shell backend: 0 means success, any other value failure.
        if not exit_file.exists():
            continue
        try:
            exit_code = int(exit_file.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if exit_code != 0:
            phase["status"] = "BLOCKED"
            continue
        changes = subprocess.run(["git", "status", "--porcelain"], cwd=phase["worktree"], capture_output=True, text=True, check=True).stdout.strip()
        if not changes:
            phase["status"] = "BLOCKED"
        elif args.light:
            phase["status"] = "READY_TO_COMMIT"
        else:
            phase["status"] = "REVIEW_PENDING"
        phase["pid"] = None
    for phase in state["phases"].values():
        if not phase.get("branch") or phase["status"] not in {"READY_TO_COMMIT", "PR_OPEN", "EXTERNAL_CHECK_PENDING"}:
            continue
        try:
            result = subprocess.run(["gh", "pr", "list", "--head", phase["branch"], "--json", "url,state,mergedAt"], cwd=root, capture_output=True, text=True, check=True)
            prs = json.loads(result.stdout or "[]")
        except (OSError, subprocess.CalledProcessError, json.JSONDecodeError):
            phase["status"] = "EXTERNAL_CHECK_PENDING"
            continue
        if prs:
            pr = prs[0]
            phase["pr"] = pr
            phase["status"] = "MERGED" if pr.get("mergedAt") else "PR_OPEN"


def status(root: Path, state: dict, args: argparse.Namespace) -> None:
    poll(root, state, args)
    running = sum(phase["status"] == "RUNNING" for phase in state["phases"].values())
    for phase in ready_phases(state):
        if running >= state["max_parallel"]:
            break
        spawn(root, state, phase, args)
        running += 1
    write_state(root, state)
    for phase in state["phases"].values():
        print(f"{phase['id']}: {phase['status']} (branch={phase['branch'] or '-'})")


def main(argv: list[str], light: bool) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", choices=["next", "status", "review", "approve", "switch"])
    parser.add_argument("mode", nargs="?")
    parser.add_argument("--agent-cmd")
    parser.add_argument("--max-parallel", type=int, default=MAX_PARALLEL_DEFAULT)
    args = parser.parse_args(argv)
    args.light = light
    root = Path.cwd()
    state = read_state(root)
    if state is None:
        state = init(root, "light" if light else "reviewed", args.max_parallel)
        print("parallel state initialized; run next to start ready phases")
        if not args.command:
            return 0
    args.light = state.get("mode") == "light"
    if args.command == "switch":
        if args.mode not in {"parallel", "light"}:
            raise RuntimeError("switch の mode は parallel または light です")
        if any(phase["status"] == "RUNNING" for phase in state["phases"].values()):
            raise RuntimeError("agent 実行中は mode を切り替えられません")
        state["mode"] = "light" if args.mode == "light" else "reviewed"
        write_state(root, state)
        print(f"mode switched to {args.mode}")
        return 0
    if args.command == "review":
        for phase in state["phases"].values():
            if phase["status"] == "REVIEWED":
                phase["status"] = "REVIEW_PENDING"
        write_state(root, state)
        return 0
    if args.command == "approve":
        for phase in state["phases"].values():
            if phase["status"] == "REVIEW_PENDING":
                phase["status"] = "REVIEWED"
        write_state(root, state)
        return 0
    if args.command == "next":
        for phase in state["phases"].values():
            if phase["status"] == "BLOCKED":
                phase["status"] = "READY"
            elif phase["status"] == "REVIEWED":
                if phase["step"] >= 6:
                    phase["status"] = "READY_TO_COMMIT"
                else:
                    phase["step"] += 1
                    phase["status"] = "READY"
    status(root, state, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:], False))
