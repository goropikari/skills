#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


STATE_DIR = ".dev-workflow-phase-light"
STATE_FILE = "CURRENT_STEP.md"
MIN_PHASES = 1
MAX_PHASES = 20
PHASE_TYPES = {"feature", "layer"}
DW_NEXT_COMMAND = "$dw-phase-light next (Claude Code: /dw-phase-light next)"
DW_REVIEW_COMMAND = "$dw-phase-light review (Claude Code: /dw-phase-light review)"
DW_APPROVE_COMMAND = "$dw-phase-light approve (Claude Code: /dw-phase-light approve)"

supports_color = (
    sys.stdout.isatty()
    and os.environ.get("TERM") != "dumb"
    and not os.environ.get("NO_COLOR")
)

BOLD = "\033[1m" if supports_color else ""
GREEN = "\033[32m" if supports_color else ""
YELLOW = "\033[33m" if supports_color else ""
BLUE = "\033[34m" if supports_color else ""
CYAN = "\033[36m" if supports_color else ""
RED = "\033[31m" if supports_color else ""
RESET = "\033[0m" if supports_color else ""


@dataclass(frozen=True)
class WorkflowState:
    status: str
    global_step: int | None = None
    current_path: str = ""
    current_name: str = ""
    phase_type: str = ""
    local_step: int = 0
    local_stage: str = ""


@dataclass(frozen=True)
class ChildPhase:
    number: int
    name: str
    phase_type: str
    status: str
    path: str


@dataclass(frozen=True)
class StepInfo:
    name: str
    target: str
    description: str


def init_environment(base_dir: Path) -> None:
    workflow_dir = base_dir / STATE_DIR
    workflow_dir.mkdir(exist_ok=True)

    gitignore_path = base_dir / ".gitignore"
    ignore_entry = f"{STATE_DIR}/"
    lines = []
    if gitignore_path.exists():
        lines = gitignore_path.read_text(encoding="utf-8").splitlines()
    if ignore_entry not in [line.strip() for line in lines] and STATE_DIR not in [
        line.strip() for line in lines
    ]:
        with gitignore_path.open("a", encoding="utf-8") as f:
            if gitignore_path.exists() and gitignore_path.stat().st_size > 0:
                f.write("\n")
            f.write(f"{ignore_entry}\n")


def state_path(base_dir: Path) -> Path:
    return base_dir / STATE_DIR / STATE_FILE


def parse_metadata(text: str, key: str) -> str | None:
    match = re.search(
        rf"^\s*-\s+\*\*{re.escape(key)}\*\*:\s*(.*?)\s*$",
        text,
        re.MULTILINE,
    )
    if not match:
        return None
    return match.group(1).strip()


def parse_int_metadata(text: str, key: str) -> int | None:
    value = parse_metadata(text, key)
    if value is None or not re.fullmatch(r"\d+", value):
        return None
    number = int(value)
    if number < MIN_PHASES or number > MAX_PHASES:
        return None
    return number


def parse_phase_type_from_text(text: str) -> str | None:
    value = parse_metadata(text, "Phase Type")
    if value not in PHASE_TYPES:
        return None
    return value


def parse_split_from_text(text: str) -> str | None:
    value = parse_metadata(text, "Split")
    if value not in {"yes", "no"}:
        return None
    return value


def read_state(base_dir: Path) -> WorkflowState:
    path = state_path(base_dir)
    if not path.exists():
        state = WorkflowState(status="IN_PROGRESS", global_step=0)
        write_state(base_dir, state)
        return state

    content = path.read_text(encoding="utf-8")
    status = parse_metadata(content, "Status") or "IN_PROGRESS"
    global_step_value = parse_metadata(content, "Global Step")
    current_path = parse_metadata(content, "Current Path") or ""
    current_name = parse_metadata(content, "Current Name") or ""
    phase_type = parse_metadata(content, "Phase Type") or ""
    local_step_value = parse_metadata(content, "Local Step") or "0"
    local_stage = parse_metadata(content, "Local Stage") or ""

    global_step = None
    if global_step_value and re.fullmatch(r"\d+", global_step_value):
        global_step = int(global_step_value)

    local_step = int(local_step_value) if re.fullmatch(r"\d+", local_step_value) else 0
    return WorkflowState(
        status=status,
        global_step=global_step,
        current_path=current_path,
        current_name=current_name,
        phase_type=phase_type,
        local_step=local_step,
        local_stage=local_stage,
    )


def current_requirements_path(base_dir: Path) -> Path:
    return base_dir / STATE_DIR / "00_project_requirements.md"


def current_phase_design_path(base_dir: Path) -> Path:
    return base_dir / STATE_DIR / "01_phase_design.md"


def current_definition_path(base_dir: Path, state: WorkflowState) -> Path:
    return base_dir / STATE_DIR / state.current_path / "01_definition.md"


def current_gherkin_path(base_dir: Path, state: WorkflowState) -> Path:
    return base_dir / STATE_DIR / state.current_path / "02_gherkin" / "spec.feature"


def current_contract_path(base_dir: Path, state: WorkflowState) -> Path:
    return base_dir / STATE_DIR / state.current_path / "02_contract_design.md"


def current_test_design_path(base_dir: Path, state: WorkflowState) -> Path:
    return base_dir / STATE_DIR / state.current_path / "03_test_design.md"


def current_split_design_path(base_dir: Path, state: WorkflowState) -> Path:
    return base_dir / STATE_DIR / state.current_path / "04_split_design.md"


def write_state(base_dir: Path, state: WorkflowState) -> None:
    path = state_path(base_dir)
    step = current_step_info(state)
    content = f"""# DW Phase Light Workflow State

- **Global Step**: {state.global_step if state.global_step is not None else ""}
- **Current Path**: {state.current_path}
- **Current Name**: {state.current_name}
- **Phase Type**: {state.phase_type}
- **Local Step**: {state.local_step}
- **Local Stage**: {state.local_stage}
- **Step Name**: {step.name}
- **Target**: {step.target}
- **Status**: {state.status}

## 説明
{step.description}

{step_notes(state)}
## 進捗サマリ / Progress Summary
<!-- AI が現在の作業状況を随時記録し、phase 完了時のみ {DW_REVIEW_COMMAND} を実行してください -->
- [ ] ターゲット範囲の作成・初期定義
- [ ] 詳細な内容の実装・調整
- [ ] 動作確認 / 自己テスト合格

## AI Agent Constraint / 制約事項
次へ進む指示（`$dw-phase-light next` コマンド、Claude Code では `/dw-phase-light next` の実行）があるまで、絶対にこれ以降のステップのファイルを生成・変更してはいけない。
Do NOT create or modify files for subsequent steps until explicitly instructed to proceed via `$dw-phase-light next` or `/dw-phase-light next`.
"""
    path.write_text(content, encoding="utf-8")


def current_step_info(state: WorkflowState) -> StepInfo:
    if state.global_step == 0:
        return StepInfo(
            "0. プロジェクト全体の要件定義",
            f"{STATE_DIR}/00_project_requirements.md",
            "プロジェクト全体の目的、対象ユーザー、スコープ、非スコープ、主要ユースケース、制約、受け入れ条件を定義する。",
        )
    if state.global_step == 1:
        return StepInfo(
            "1. フェーズ設計",
            f"{STATE_DIR}/01_phase_design.md",
            "トップレベル phase の責務、依存方向、完了条件、実装順、Phase Type を定義する。",
        )

    path = f"{STATE_DIR}/{state.current_path}" if state.current_path else STATE_DIR
    prefix = f"{state.current_path}: " if state.current_path else ""
    if state.local_stage == "definition":
        return StepInfo(
            f"{prefix}定義",
            f"{path}/01_definition.md",
            "この作業単位の目的、責務、境界、受け入れ条件、Phase Type を定義する。",
        )
    if state.local_stage == "gherkin":
        return StepInfo(
            f"{prefix}Gherkin定義",
            f"{path}/02_gherkin/spec.feature",
            "feature phase の期待される振る舞いを Given/When/Then で定義する。",
        )
    if state.local_stage == "contract":
        return StepInfo(
            f"{prefix}契約・依存設計",
            f"{path}/02_contract_design.md",
            "layer phase の契約、依存方向、外部境界、呼び出し関係を設計する。",
        )
    if state.local_stage == "test-design":
        return StepInfo(
            f"{prefix}テスト分析・設計",
            f"{path}/03_test_design.md",
            "テスト観点、条件、ケース、境界値、リスクを設計し、Split yes/no を判断する。",
        )
    if state.local_stage == "split-design":
        return StepInfo(
            f"{prefix}分割設計",
            f"{path}/04_split_design.md",
            "子 phase の数、名前、Phase Type、責務、順序、完了条件を設計する。",
        )
    if state.local_stage == "interface":
        return StepInfo(
            f"{prefix}関数定義・コメント作成",
            "実プロジェクト内の適切なソースファイル",
            "末端 phase として、既存構成に合う場所へシグネチャ、docstring、スタブのみを実装する。",
        )
    if state.local_stage == "tests":
        return StepInfo(
            f"{prefix}テスト実装",
            "実プロジェクト内の適切なテストファイル",
            "末端 phase として、自動テストを実装する。",
        )
    if state.local_stage == "implementation":
        return StepInfo(
            f"{prefix}内部ロジック実装",
            "実プロジェクト内の適切なソースファイル",
            "末端 phase として、内部ロジックを実装する。phase 完了後だけレビューを行う。",
        )
    return StepInfo("完了", STATE_DIR, "すべてのステップが完了しています。")


def step_notes(state: WorkflowState) -> str:
    if state.global_step == 0:
        return f"""## 進め方
- コードベースから判断できることは調査し、ユーザーに不要な質問をしない。
- 目的、対象ユーザー、スコープ、非スコープ、主要ユースケース、入出力、制約、受け入れ条件、未決事項を合意する。
- 合意内容を `{STATE_DIR}/00_project_requirements.md` にまとめる。
"""
    if state.global_step == 1:
        return f"""## 進め方
- `{STATE_DIR}/00_project_requirements.md` を読み、トップレベル phase を設計する。
- 必須メタデータ `- **Phases**: N` を書く。N は {MIN_PHASES} 以上 {MAX_PHASES} 以下の整数。
- 各 `## Phase N: 名前` セクションに `- **Phase Type**: feature|layer` を書く。
"""
    if state.local_stage == "definition":
        return """## 進め方
- 親の設計書を読み、この作業単位の目的、責務、境界、入出力、受け入れ条件を定義する。
- 必須メタデータ `- **Phase Type**: feature|layer` を書く。
"""
    if state.local_stage == "gherkin":
        return """## 進め方
- `01_definition.md` を読み、ユーザー視点の期待される振る舞いを Gherkin 形式で定義する。
- 要件だけでは判断できない内容は推測せず、未決事項として明記する。
"""
    if state.local_stage == "contract":
        return """## 進め方
- `01_definition.md` を読み、layer の公開契約、依存方向、境界、エラー方針を設計する。
- 判断できない内容は未決事項または設計リスクとして明記する。
"""
    if state.local_stage == "test-design":
        return """## 進め方
- `01_definition.md` と step 2 の成果物を読み、テスト観点、条件、ケース、境界値、リスクを設計する。
- 必須メタデータ `- **Split**: yes|no` を書く。
- `yes` の場合は分割理由と分割観点を明記する。子 phase の詳細は次の `04_split_design.md` に書く。
"""
    if state.local_stage == "split-design":
        return f"""## 進め方
- テスト分析・設計を読み、子 phase への分割を設計する。
- 必須メタデータ `- **Subphases**: N` を書く。N は {MIN_PHASES} 以上 {MAX_PHASES} 以下の整数。
- 各 `## Subphase N: 名前` セクションに `- **Phase Type**: feature|layer` を書く。
"""
    if state.local_stage == "interface":
        return """## 進め方
- この phase は `Split: no` の末端 phase として扱う。
- 対象プロジェクトの既存構成に合う場所へ、関数や型のシグネチャ、docstring、スタブのみを実装する。
- 内部ロジックはまだ実装しない。
"""
    if state.local_stage == "tests":
        return """## 進め方
- テスト分析・設計と関数定義に従い、対象プロジェクトのテスト構成に合う場所へ自動テストを実装する。
- この段階ではテストが失敗してもよいが、失敗理由が未実装ロジックに対応していることを確認する。
"""
    return """## 進め方
- 対象プロジェクトのソースファイルに内部ロジックを実装し、phase の完了後にのみレビューを行う。
"""


def parse_children_from_text(text: str, parent_path: str) -> list[ChildPhase] | None:
    count = parse_int_metadata(text, "Subphases" if parent_path else "Phases")
    if count is None:
        return None

    label = "Subphase" if parent_path else "Phase"
    pattern = re.compile(
        rf"^##\s+{label}\s+(\d+):\s*(.*?)\s*$([\s\S]*?)(?=^##\s+{label}\s+\d+:|\Z)",
        re.MULTILINE,
    )
    sections = {
        int(m.group(1)): (m.group(2).strip(), m.group(3))
        for m in pattern.finditer(text)
    }
    children: list[ChildPhase] = []
    for number in range(1, count + 1):
        if number not in sections:
            return None
        name, body = sections[number]
        phase_type = parse_phase_type_from_text(body)
        if phase_type is None:
            return None
        status = parse_metadata(body, "Status") or "NOT_STARTED"
        path = f"{parent_path}/subphase{number}" if parent_path else f"phase{number}"
        children.append(ChildPhase(number, name, phase_type, status, path))
    return children


def children_design_path(base_dir: Path, parent_path: str) -> Path:
    if not parent_path:
        return base_dir / STATE_DIR / "01_phase_design.md"
    return base_dir / STATE_DIR / parent_path / "04_split_design.md"


def read_children(base_dir: Path, parent_path: str) -> list[ChildPhase] | None:
    path = children_design_path(base_dir, parent_path)
    try:
        return parse_children_from_text(path.read_text(encoding="utf-8"), parent_path)
    except FileNotFoundError:
        return None


def update_child_status(
    base_dir: Path, parent_path: str, child_number: int, status: str
) -> None:
    path = children_design_path(base_dir, parent_path)
    text = path.read_text(encoding="utf-8")
    label = "Subphase" if parent_path else "Phase"
    section_pattern = re.compile(
        rf"(^##\s+{label}\s+{child_number}:\s*.*?$)([\s\S]*?)(?=^##\s+{label}\s+\d+:|\Z)",
        re.MULTILINE,
    )
    match = section_pattern.search(text)
    if not match:
        return

    header, body = match.group(1), match.group(2)
    if re.search(r"^\s*-\s+\*\*Status\*\*:", body, re.MULTILINE):
        body = re.sub(
            r"^\s*-\s+\*\*Status\*\*:\s*.*$",
            f"- **Status**: {status}",
            body,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        phase_type_match = re.search(
            r"^\s*-\s+\*\*Phase Type\*\*:\s*.*$",
            body,
            re.MULTILINE,
        )
        if phase_type_match:
            insert_at = phase_type_match.end()
            body = body[:insert_at] + f"\n- **Status**: {status}" + body[insert_at:]
        else:
            body = f"\n- **Status**: {status}" + body

    text = text[: match.start()] + header + body + text[match.end() :]
    path.write_text(text, encoding="utf-8")


def parent_path_of(path: str) -> str:
    if "/" not in path:
        return ""
    return path.rsplit("/", 1)[0]


def child_number_from_path(path: str) -> int:
    leaf = path.rsplit("/", 1)[-1]
    match = re.search(r"(\d+)$", leaf)
    return int(match.group(1)) if match else 0


def initial_state_for_child(child: ChildPhase) -> WorkflowState:
    return WorkflowState(
        status="IN_PROGRESS",
        current_path=child.path,
        current_name=child.name,
        phase_type=child.phase_type,
        local_step=1,
        local_stage="definition",
    )


def next_uncompleted_child(base_dir: Path, parent_path: str) -> ChildPhase | None:
    children = read_children(base_dir, parent_path)
    if children is None:
        return None
    for child in children:
        if child.status != "COMPLETED":
            return child
    return None


def complete_node_and_find_next(base_dir: Path, path: str) -> WorkflowState | None:
    current = path
    while current:
        parent = parent_path_of(current)
        update_child_status(
            base_dir, parent, child_number_from_path(current), "COMPLETED"
        )
        sibling = next_uncompleted_child(base_dir, parent)
        if sibling is not None:
            update_child_status(base_dir, parent, sibling.number, "IN_PROGRESS")
            return initial_state_for_child(sibling)
        current = parent

    sibling = next_uncompleted_child(base_dir, "")
    if sibling is not None:
        update_child_status(base_dir, "", sibling.number, "IN_PROGRESS")
        return initial_state_for_child(sibling)
    return None


def definition_path(base_dir: Path, state: WorkflowState) -> Path:
    return base_dir / STATE_DIR / state.current_path / "01_definition.md"


def test_design_path(base_dir: Path, state: WorkflowState) -> Path:
    return base_dir / STATE_DIR / state.current_path / "03_test_design.md"


def invalid(message: str, state: WorkflowState, base_dir: Path) -> int:
    write_state(base_dir, WorkflowState(**{**state.__dict__, "status": "IN_PROGRESS"}))
    print_header(RED, "DW-PHASE-LIGHT: INVALID WORKFLOW METADATA")
    print(message)
    print(
        "対象成果物を修正し、必要な場合のみ phase 完了時の review / approve をやり直してください。"
    )
    print(
        f"通常手順: `{DW_REVIEW_COMMAND}` -> `{DW_APPROVE_COMMAND}` -> `{DW_NEXT_COMMAND}`"
    )
    print(f"{RED}{BOLD}========================================={RESET}")
    return 1


def transition_from_next(base_dir: Path, state: WorkflowState) -> int:
    if state.global_step == 0:
        requirements = current_requirements_path(base_dir)
        if (
            not requirements.exists()
            or not requirements.read_text(encoding="utf-8").strip()
        ):
            return invalid(
                f"`{STATE_DIR}/00_project_requirements.md` を作成してから次へ進んでください。",
                state,
                base_dir,
            )
        new_state = WorkflowState(status="IN_PROGRESS", global_step=1)
        write_state(base_dir, new_state)
        print_transition(state, new_state)
        return 0

    if state.global_step == 1:
        children = read_children(base_dir, "")
        if children is None:
            return invalid(
                f"`{STATE_DIR}/01_phase_design.md` に有効な `- **Phases**: N` と各 Phase の `- **Phase Type**: feature|layer` が必要です。",
                state,
                base_dir,
            )
        first = children[0]
        update_child_status(base_dir, "", first.number, "IN_PROGRESS")
        new_state = initial_state_for_child(first)
        write_state(base_dir, new_state)
        print_transition(state, new_state)
        return 0

    if state.local_stage == "definition":
        phase_type = parse_phase_type_from_text(
            definition_path(base_dir, state).read_text(encoding="utf-8")
        )
        if phase_type is None:
            return invalid(
                "`01_definition.md` に `- **Phase Type**: feature|layer` が必要です。",
                state,
                base_dir,
            )
        new_state = WorkflowState(
            status="IN_PROGRESS",
            current_path=state.current_path,
            current_name=state.current_name,
            phase_type=phase_type,
            local_step=2,
            local_stage="gherkin" if phase_type == "feature" else "contract",
        )
        write_state(base_dir, new_state)
        print_transition(state, new_state)
        return 0

    if state.local_stage in {"gherkin", "contract"}:
        target_path = (
            current_gherkin_path(base_dir, state)
            if state.local_stage == "gherkin"
            else current_contract_path(base_dir, state)
        )
        if not target_path.exists():
            return invalid(
                f"`{target_path.relative_to(base_dir)}` を作成してから次へ進んでください。",
                state,
                base_dir,
            )
        new_state = WorkflowState(
            status="IN_PROGRESS",
            current_path=state.current_path,
            current_name=state.current_name,
            phase_type=state.phase_type,
            local_step=3,
            local_stage="test-design",
        )
        write_state(base_dir, new_state)
        print_transition(state, new_state)
        return 0

    if state.local_stage == "test-design":
        split = parse_split_from_text(
            test_design_path(base_dir, state).read_text(encoding="utf-8")
        )
        if split is None:
            return invalid(
                "`03_test_design.md` に `- **Split**: yes|no` が必要です。",
                state,
                base_dir,
            )
        local_stage = "split-design" if split == "yes" else "interface"
        new_state = WorkflowState(
            status="IN_PROGRESS",
            current_path=state.current_path,
            current_name=state.current_name,
            phase_type=state.phase_type,
            local_step=4,
            local_stage=local_stage,
        )
        write_state(base_dir, new_state)
        print_transition(state, new_state)
        return 0

    if state.local_stage == "split-design":
        children = read_children(base_dir, state.current_path)
        if children is None:
            return invalid(
                "`04_split_design.md` に有効な `- **Subphases**: N` と各 Subphase の `- **Phase Type**: feature|layer` が必要です。",
                state,
                base_dir,
            )
        first = children[0]
        update_child_status(base_dir, state.current_path, first.number, "IN_PROGRESS")
        new_state = initial_state_for_child(first)
        write_state(base_dir, new_state)
        print_transition(state, new_state)
        return 0

    if state.local_stage == "interface":
        new_state = WorkflowState(
            status="IN_PROGRESS",
            current_path=state.current_path,
            current_name=state.current_name,
            phase_type=state.phase_type,
            local_step=5,
            local_stage="tests",
        )
        write_state(base_dir, new_state)
        print_transition(state, new_state)
        return 0

    if state.local_stage == "tests":
        new_state = WorkflowState(
            status="IN_PROGRESS",
            current_path=state.current_path,
            current_name=state.current_name,
            phase_type=state.phase_type,
            local_step=6,
            local_stage="implementation",
        )
        write_state(base_dir, new_state)
        print_transition(state, new_state)
        return 0

    if state.local_stage == "implementation":
        if state.status == "REVIEW_PENDING":
            print_header(CYAN, "DW-PHASE-LIGHT: REVIEW PENDING")
            print("現在の phase は人間のレビュー確認待ちです。")
            print(
                "承認指示を受け取ったら、AI 自身で approve を実行してから next を再実行してください。"
            )
            print(
                f"直接実行: `python3 {Path(__file__).resolve()} approve` -> `python3 {Path(__file__).resolve()} next`"
            )
            print(f"{CYAN}{BOLD}========================================={RESET}")
            return 0
        if state.status != "REVIEWED":
            print_header(YELLOW, "DW-PHASE-LIGHT: PHASE COMPLETE, REVIEW REQUIRED")
            print(
                "この phase の実装は完了しています。次は review でレビュー待ちに移行してください。"
            )
            print(f"実行: `{DW_REVIEW_COMMAND}`")
            print(f"{YELLOW}{BOLD}========================================={RESET}")
            return 0
        new_state = complete_node_and_find_next(base_dir, state.current_path)
        if new_state is None:
            write_state(base_dir, WorkflowState(status="COMPLETED"))
            print_header(GREEN, "DW-PHASE-LIGHT ALL STEPS COMPLETED")
            print("すべてのトップレベル phase が完了しています。")
            print(f"{GREEN}{BOLD}========================================={RESET}")
            return 0
        write_state(base_dir, new_state)
        print_transition(state, new_state)
        return 0

    write_state(base_dir, WorkflowState(status="COMPLETED"))
    print_header(GREEN, "DW-PHASE-LIGHT ALL STEPS COMPLETED")
    print("すべてのステップが完了しています。")
    print(f"{GREEN}{BOLD}========================================={RESET}")
    return 0


def print_header(color: str, title: str) -> None:
    print(f"{color}{BOLD}========================================={RESET}")
    print(f"{color}{BOLD}{title}{RESET}")
    print(f"{color}{BOLD}========================================={RESET}")


def print_agent_instruction(
    state: WorkflowState, script_path: Path, continuing: bool = False
) -> None:
    step = current_step_info(state)
    action = "作成・更新" if continuing else "作成"
    print(f"1. ターゲット `{CYAN}{step.target}{RESET}` を{action}してください。")
    print(
        "2. 現在のステップの範囲だけを扱い、後続ステップのファイルは作成・変更しないでください。"
    )
    print(f"3. `{STATE_DIR}/{STATE_FILE}` の進捗サマリを随時更新してください。")
    print(
        "4. phase の内部ステップは next で連続進行し、実装完了時のみ review -> approve -> next の順で進めてください。"
    )
    if state.local_stage == "implementation":
        print(
            f"5. phase の作業が完了したら、成果物のパスと内容または要約をユーザーに出力し、その後 AI 自身で `{CYAN}python3 {script_path} review{RESET}` を実行してください。"
        )
    if state.global_step == 1:
        print(
            f"5. フェーズ設計書には `- **Phases**: N` と各 Phase の `- **Phase Type**: feature|layer` を記載してください。"
        )
    if state.local_stage == "definition":
        print(
            "5. 定義ファイルには `- **Phase Type**: feature|layer` を記載してください。"
        )
    if state.local_stage == "test-design":
        print("5. テスト設計には `- **Split**: yes|no` を記載してください。")
    if state.local_stage == "split-design":
        print(
            "5. 分割設計には `- **Subphases**: N` と各 Subphase の `- **Phase Type**: feature|layer` を記載してください。"
        )


def print_current(state: WorkflowState, script_path: Path) -> None:
    step = current_step_info(state)
    title = "DW-PHASE-LIGHT"
    if state.global_step is not None:
        title = f"DW-PHASE-LIGHT (Global Step {state.global_step})"
    elif state.current_path:
        title = f"DW-PHASE-LIGHT ({state.current_path} / Local Step {state.local_step})"
    print_header(BLUE, title)
    print(f"現在のステップ: {BOLD}{step.name}{RESET}")
    print(f"ターゲット: {CYAN}{step.target}{RESET}")
    if state.current_path:
        print(f"現在の phase: {BOLD}{state.current_name}{RESET}")
        print(f"Phase Type: {BOLD}{state.phase_type}{RESET}")
    print(f"現在のステータス: {YELLOW}{BOLD}{state.status}{RESET}")
    print(f"\n{BOLD}説明:{RESET}")
    print(step.description)
    print(f"\n{YELLOW}{BOLD}AI Agent への指示:{RESET}")
    print_agent_instruction(state, script_path, continuing=True)
    print(f"\n{RED}{BOLD}制約事項:{RESET}")
    print(
        "次へ進む指示があるまで、絶対にこれ以降のステップのファイルを生成・変更しないでください。"
    )
    print(f"{BLUE}{BOLD}========================================={RESET}")


def print_transition(old_state: WorkflowState, new_state: WorkflowState) -> None:
    new = current_step_info(new_state)
    print_header(CYAN, "DW-PHASE-LIGHT STEP TRANSITION")
    print("現在のステップが正常に進みました。")
    print(f"新しいステップ: {BOLD}{new.name}{RESET}")
    print(f"ターゲット: {CYAN}{new.target}{RESET}")
    if new_state.current_path:
        print(f"現在の phase: {BOLD}{new_state.current_name}{RESET}")
        print(f"Phase Type: {BOLD}{new_state.phase_type}{RESET}")
    print(f"現在のステータス: {YELLOW}{BOLD}IN_PROGRESS{RESET}")
    print(f"\n{BOLD}説明:{RESET}")
    print(new.description)
    print(f"{CYAN}{BOLD}========================================={RESET}")


def main() -> int:
    base_dir = Path.cwd()
    script_path = Path(__file__).resolve()
    init_environment(base_dir)

    command = sys.argv[1] if len(sys.argv) > 1 else ""
    is_next = command == "next"
    is_review = command in {"review", "submit", "review-pending", "review_pending"}
    is_approve = command in {"approve", "reviewed"}

    state = read_state(base_dir)

    if is_review:
        if state.local_stage != "implementation" or state.global_step in {0, 1}:
            return invalid(
                "review は phase の内部実装が完了した時だけ実行してください。",
                state,
                base_dir,
            )
        new_state = WorkflowState(**{**state.__dict__, "status": "REVIEW_PENDING"})
        write_state(base_dir, new_state)
        print_header(CYAN, "DW-PHASE-LIGHT STATUS UPDATED TO REVIEW_PENDING")
        print(f"現在のステップ: {BOLD}{current_step_info(new_state).name}{RESET}")
        print("ステータスを REVIEW_PENDING に更新しました。")
        print(
            f"承認が得られたら、AI自身で {GREEN}{DW_APPROVE_COMMAND}{RESET} を実行してください。"
        )
        print(f"{CYAN}{BOLD}========================================={RESET}")
        return 0

    if is_approve:
        if state.local_stage != "implementation" or state.status != "REVIEW_PENDING":
            return invalid(
                "approve は phase 完了後の REVIEW_PENDING 状態でのみ実行してください。",
                state,
                base_dir,
            )
        new_state = WorkflowState(**{**state.__dict__, "status": "REVIEWED"})
        write_state(base_dir, new_state)
        print_header(GREEN, "DW-PHASE-LIGHT STATUS UPDATED TO REVIEWED")
        print(f"現在のステップ: {BOLD}{current_step_info(new_state).name}{RESET}")
        print("ステータスを REVIEWED に更新しました。")
        print(
            f"次のステップに進むには、{CYAN}{BOLD}{DW_NEXT_COMMAND}{RESET} を実行してください。"
        )
        print(f"{GREEN}{BOLD}========================================={RESET}")
        return 0

    if not is_next:
        print_current(state, script_path)
        return 0

    if state.status == "REVIEW_PENDING":
        print_header(CYAN, "DW-PHASE-LIGHT: REVIEW PENDING")
        print("現在の phase は人間のレビュー確認待ちです。")
        print(
            "承認指示を受け取ったら、AI自身で approve を実行してから next を再実行してください。"
        )
        print(
            f"直接実行: `python3 {script_path} approve` -> `python3 {script_path} next`"
        )
        print(f"{CYAN}{BOLD}========================================={RESET}")
        return 0

    if state.status == "COMPLETED":
        print_header(GREEN, "DW-PHASE-LIGHT ALL STEPS COMPLETED")
        print("すべてのステップが完了しています。")
        print(f"{GREEN}{BOLD}========================================={RESET}")
        return 0

    return transition_from_next(base_dir, state)


if __name__ == "__main__":
    raise SystemExit(main())
