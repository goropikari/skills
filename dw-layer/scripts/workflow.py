#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


STATE_DIR = ".dev-workflow-layer"
STATE_FILE = "CURRENT_STEP.md"
MIN_LAYERS = 1
MAX_LAYERS = 20
DW_NEXT_COMMAND = "$dw-layer next (Claude Code: /dw-layer next)"
DW_REVIEW_COMMAND = "$dw-layer review (Claude Code: /dw-layer review)"
DW_APPROVE_COMMAND = "$dw-layer approve (Claude Code: /dw-layer approve)"

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
class Step:
    index: int
    name: str
    target: str
    description: str
    layer: int | None = None
    phase: str | None = None


def generate_workflow_steps(layers: int) -> list[Step]:
    if layers < 0:
        raise ValueError("layers must be >= 0")

    steps = [
        Step(
            0,
            "0. プロジェクト全体の要件定義",
            f"{STATE_DIR}/00_project_requirements.md",
            "プロジェクト全体の目的、対象ユーザー、スコープ、非スコープ、主要ユースケース、制約、受け入れ条件を定義する。",
        ),
        Step(
            1,
            "1. レイヤー設計",
            f"{STATE_DIR}/01_layer_design.md",
            "プロジェクトを実装レイヤーへ分割し、各レイヤーの責務、依存方向、完了条件、実装順を定義する。",
        ),
    ]

    for layer in range(1, layers + 1):
        prefix = f"{STATE_DIR}/layer{layer}"
        layer_steps = [
            (
                f"Layer {layer}: 要件定義",
                f"{prefix}/01_requirements.md",
                f"レイヤー {layer} の責務、入出力、境界、受け入れ条件を定義する。",
                "requirements",
            ),
            (
                f"Layer {layer}: Gherkin定義",
                f"{prefix}/02_features/spec.feature",
                f"レイヤー {layer} の期待される振る舞いを Given/When/Then で定義する。",
                "gherkin",
            ),
            (
                f"Layer {layer}: テスト分析・設計",
                f"{prefix}/03_test_design.md",
                f"レイヤー {layer} のテスト観点、条件、ケース、リスクを設計する。",
                "test-design",
            ),
            (
                f"Layer {layer}: 関数定義・コメント作成",
                "実プロジェクト内の適切なソースファイル",
                f"レイヤー {layer} の設計に合う場所へ、シグネチャ、docstring、スタブのみを実装する。",
                "interface",
            ),
            (
                f"Layer {layer}: テスト実装",
                "実プロジェクト内の適切なテストファイル",
                f"レイヤー {layer} のテスト構成に合う場所へ自動テストを実装する。",
                "tests",
            ),
            (
                f"Layer {layer}: 内部ロジック実装",
                "実プロジェクト内の適切なソースファイル",
                f"レイヤー {layer} の内部ロジックを実装し、対象テストをパスさせる。",
                "implementation",
            ),
        ]
        for name, target, description, phase in layer_steps:
            steps.append(Step(len(steps), name, target, description, layer, phase))

    return steps


def parse_layers_from_text(text: str) -> int | None:
    match = re.search(r"^\s*-\s+\*\*Layers\*\*:\s*(\S+)\s*$", text, re.MULTILINE)
    if not match:
        return None

    value = match.group(1)
    if not re.fullmatch(r"\d+", value):
        return None

    layers = int(value)
    if layers < MIN_LAYERS or layers > MAX_LAYERS:
        return None
    return layers


def extract_layers_from_design(base_dir: Path) -> int | None:
    design_path = base_dir / STATE_DIR / "01_layer_design.md"
    try:
        return parse_layers_from_text(design_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None


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


def read_status(base_dir: Path) -> tuple[int, str, int]:
    path = state_path(base_dir)
    if not path.exists():
        write_status(base_dir, 0, "IN_PROGRESS", 0)
        return 0, "IN_PROGRESS", 0

    content = path.read_text(encoding="utf-8")
    step = 0
    status = "IN_PROGRESS"
    layers = 0

    step_match = re.search(r"-\s+\*\*Step\*\*:\s*(\d+)", content)
    if step_match:
        step = int(step_match.group(1))

    status_match = re.search(r"-\s+\*\*Status\*\*:\s*([A-Z_]+)", content)
    if status_match:
        status = status_match.group(1)

    layers_match = re.search(r"-\s+\*\*Layers\*\*:\s*(\d+)", content)
    if layers_match:
        layers = int(layers_match.group(1))

    max_step = len(generate_workflow_steps(layers)) - 1
    if step < 0 or step > max_step:
        step = 0
    return step, status, layers


def step_notes(step: Step) -> str:
    if step.index == 0:
        return f"""## 進め方
- コードベースから判断できることは調査し、ユーザーに不要な質問をしない。
- 目的、対象ユーザー、スコープ、非スコープ、主要ユースケース、入出力、制約、受け入れ条件、未決事項を合意する。
- 合意内容を `{STATE_DIR}/00_project_requirements.md` にまとめる。
"""
    if step.index == 1:
        return f"""## 進め方
- `{STATE_DIR}/00_project_requirements.md` を読み、実装レイヤーを設計する。
- レイヤーごとの責務、依存方向、成果物、完了条件、実装順を明記する。
- 必須メタデータ `- **Layers**: N` を書く。N は {MIN_LAYERS} 以上 {MAX_LAYERS} 以下の整数。
"""
    if step.phase == "requirements":
        return f"""## 進め方
- 全体要件とレイヤー設計を読み、レイヤー {step.layer} の要件だけを定義する。
- 他レイヤーとの境界、依存、入出力、受け入れ条件、未決事項を明記する。
"""
    if step.phase == "gherkin":
        return f"""## 進め方
- `layer{step.layer}/01_requirements.md` を読み、Gherkin 形式で期待される振る舞いを定義する。
- 要件だけでは判断できない内容は推測せず、コメントまたは未決事項として明記する。
"""
    if step.phase == "test-design":
        return f"""## 進め方
- `layer{step.layer}/01_requirements.md` と `layer{step.layer}/02_features/spec.feature` を読み、テスト観点、条件、ケース、境界値、リスクを設計する。
- 判断できない内容は未決事項またはテストリスクとして明記する。
"""
    if step.phase == "interface":
        return """## 進め方
- 対象プロジェクトの既存構成に合う場所へ、関数や型のシグネチャ、docstring、スタブのみを実装する。
- 内部ロジックはまだ実装しない。
"""
    if step.phase == "tests":
        return """## 進め方
- テスト分析・設計と関数定義に従い、対象プロジェクトのテスト構成に合う場所へ自動テストを実装する。
- この段階ではテストが失敗してもよいが、失敗理由が未実装ロジックに対応していることを確認する。
"""
    return """## 進め方
- 対象プロジェクトのソースファイルに内部ロジックを実装し、対象テストをパスさせる。
"""


def write_status(base_dir: Path, step_num: int, status: str, layers: int) -> None:
    path = state_path(base_dir)
    steps = generate_workflow_steps(layers)
    step = steps[step_num]

    if path.exists():
        content = path.read_text(encoding="utf-8")
        current_step = re.search(r"-\s+\*\*Step\*\*:\s*(\d+)", content)
        if current_step and int(current_step.group(1)) == step_num:
            content = re.sub(
                r"-\s+\*\*Step Name\*\*:\s*.*",
                f"- **Step Name**: {step.name}",
                content,
            )
            content = re.sub(
                r"-\s+\*\*Target\*\*:\s*.*",
                f"- **Target**: {step.target}",
                content,
            )
            content = re.sub(
                r"-\s+\*\*Status\*\*:\s*[A-Z_]+",
                f"- **Status**: {status}",
                content,
            )
            content = re.sub(
                r"-\s+\*\*Layers\*\*:\s*\d+",
                f"- **Layers**: {layers}",
                content,
            )
            path.write_text(content, encoding="utf-8")
            return

    content = f"""# DW Layer Workflow State

- **Step**: {step_num}
- **Step Name**: {step.name}
- **Target**: {step.target}
- **Status**: {status}
- **Layers**: {layers}

## 説明
{step.description}

{step_notes(step)}
## 進捗サマリ / Progress Summary
<!-- AI が現在の作業状況を随時記録し、完了したら {DW_REVIEW_COMMAND} を実行してください -->
- [ ] ターゲット範囲の作成・初期定義
- [ ] 詳細な内容の実装・調整
- [ ] 動作確認 / 自己テスト合格

## AI Agent Constraint / 制約事項
次へ進む指示（`$dw-layer next` コマンド、Claude Code では `/dw-layer next` の実行）があるまで、絶対にこれ以降のステップのファイルを生成・変更してはいけない。
Do NOT create or modify files for subsequent steps until explicitly instructed to proceed via `$dw-layer next` or `/dw-layer next`.
"""
    path.write_text(content, encoding="utf-8")


def print_agent_instruction(
    step: Step, script_path: Path, continuing: bool = False
) -> None:
    action = "作成・更新" if continuing else "作成"
    print(f"1. ターゲット `{CYAN}{step.target}{RESET}` を{action}してください。")
    print(
        "2. 現在のステップの範囲だけを扱い、後続ステップのファイルは作成・変更しないでください。"
    )
    print(f"3. `{STATE_DIR}/{STATE_FILE}` の進捗サマリを随時更新してください。")
    print(
        "4. ステップの作業が完了したら、成果物のパスと内容または要約をユーザーに出力してください。"
    )
    print(
        f"5. 成果物の出力後、AI自身で `{CYAN}python3 {script_path} review{RESET}` を実行してください。"
    )
    if step.index == 1:
        print(
            f"6. レイヤー設計書には必ず `- **Layers**: N` を記載してください（{MIN_LAYERS}〜{MAX_LAYERS}）。"
        )


def print_header(color: str, title: str) -> None:
    print(f"{color}{BOLD}========================================={RESET}")
    print(f"{color}{BOLD}{title}{RESET}")
    print(f"{color}{BOLD}========================================={RESET}")


def print_current(
    step: Step, status: str, layers: int, total: int, script_path: Path
) -> None:
    print_header(BLUE, f"DW-LAYER (Step {step.index}/{total - 1})")
    print(f"現在のステップ: {BOLD}{step.name}{RESET}")
    print(f"ターゲット: {CYAN}{step.target}{RESET}")
    print(f"現在のステータス: {YELLOW}{BOLD}{status}{RESET}")
    print(f"Layers: {BOLD}{layers}{RESET}")
    print(f"\n{BOLD}説明:{RESET}")
    print(step.description)
    print(f"\n{YELLOW}{BOLD}AI Agent への指示:{RESET}")
    print_agent_instruction(step, script_path, continuing=True)
    print(f"\n{RED}{BOLD}制約事項:{RESET}")
    print(
        "次へ進む指示があるまで、絶対にこれ以降のステップのファイルを生成・変更しないでください。"
    )
    print(f"{BLUE}{BOLD}========================================={RESET}")


def print_invalid_layers(script_path: Path) -> None:
    print_header(RED, "DW-LAYER: INVALID LAYERS")
    print(
        f"`{STATE_DIR}/01_layer_design.md` から有効な `- **Layers**: N` を読み取れませんでした。"
    )
    print(f"N は {MIN_LAYERS} 以上 {MAX_LAYERS} 以下の整数である必要があります。")
    print(
        "ステップ 1 からは進みません。レイヤー設計書を修正し、レビューと承認をやり直してください。"
    )
    print(
        f"修正後の通常手順: `{DW_REVIEW_COMMAND}` -> `{DW_APPROVE_COMMAND}` -> `{DW_NEXT_COMMAND}`"
    )
    print(
        f"スクリプト直接実行: `python3 {script_path} review` -> `python3 {script_path} approve` -> `python3 {script_path} next`"
    )
    print(f"{RED}{BOLD}========================================={RESET}")


def main() -> int:
    base_dir = Path.cwd()
    script_path = Path(__file__).resolve()
    init_environment(base_dir)

    command = sys.argv[1] if len(sys.argv) > 1 else ""
    is_next = command == "next"
    is_review = command in {"review", "submit", "review-pending", "review_pending"}
    is_approve = command in {"approve", "reviewed"}

    step_num, status, layers = read_status(base_dir)
    steps = generate_workflow_steps(layers)
    step = steps[step_num]

    if is_review:
        write_status(base_dir, step_num, "REVIEW_PENDING", layers)
        print_header(CYAN, "DW-LAYER STATUS UPDATED TO REVIEW_PENDING")
        print(f"現在のステップ: {BOLD}{step.name}{RESET}")
        print("ステータスを REVIEW_PENDING に更新しました。")
        print(
            f"承認が得られたら、AI自身で {GREEN}{DW_APPROVE_COMMAND}{RESET} を実行してください。"
        )
        print(f"{CYAN}{BOLD}========================================={RESET}")
        return 0

    if is_approve:
        write_status(base_dir, step_num, "REVIEWED", layers)
        print_header(GREEN, "DW-LAYER STATUS UPDATED TO REVIEWED")
        print(f"現在のステップ: {BOLD}{step.name}{RESET}")
        print("ステータスを REVIEWED に更新しました。")
        print(
            f"次のステップに進むには、{CYAN}{BOLD}{DW_NEXT_COMMAND}{RESET} を実行してください。"
        )
        print(f"{GREEN}{BOLD}========================================={RESET}")
        return 0

    if not is_next:
        print_current(step, status, layers, len(steps), script_path)
        return 0

    if status == "IN_PROGRESS":
        print_header(YELLOW, "DW-LAYER: CURRENT STEP IN PROGRESS")
        print("現在のステップの作業はまだ完了していません。")
        print(f"ターゲット: {CYAN}{step.target}{RESET}")
        print(f"現在のステータス: {YELLOW}{BOLD}IN_PROGRESS{RESET}")
        print(f"\n{YELLOW}{BOLD}AI Agent への指示:{RESET}")
        print_agent_instruction(step, script_path, continuing=True)
        print(f"{YELLOW}{BOLD}========================================={RESET}")
        return 0

    if status == "REVIEW_PENDING":
        print_header(CYAN, "DW-LAYER: REVIEW PENDING")
        print("現在のステップは人間のレビュー確認待ちです。")
        print(f"ターゲット: {CYAN}{step.target}{RESET}")
        print(
            "承認指示を受け取ったら、AI自身で approve を実行してから next を再実行してください。"
        )
        print(
            f"直接実行: `python3 {script_path} approve` -> `python3 {script_path} next`"
        )
        print(f"{CYAN}{BOLD}========================================={RESET}")
        return 0

    if step_num == 1:
        parsed_layers = extract_layers_from_design(base_dir)
        if parsed_layers is None:
            write_status(base_dir, 1, "IN_PROGRESS", layers)
            print_invalid_layers(script_path)
            return 1
        layers = parsed_layers
        steps = generate_workflow_steps(layers)

    if step_num >= len(steps) - 1:
        write_status(base_dir, step_num, "COMPLETED", layers)
        print_header(GREEN, "DW-LAYER ALL STEPS COMPLETED")
        print(f"すべてのステップ（0〜{len(steps) - 1}）が完了しています。")
        print(f"Layers: {BOLD}{layers}{RESET}")
        print(f"{GREEN}{BOLD}========================================={RESET}")
        return 0

    new_step = step_num + 1
    write_status(base_dir, new_step, "IN_PROGRESS", layers)
    new = generate_workflow_steps(layers)[new_step]
    print_header(CYAN, f"DW-LAYER STEP TRANSITION ({step_num} -> {new_step})")
    print("現在のステップが正常に進みました。")
    print(f"新しいステップ: {BOLD}{new.name}{RESET}")
    print(f"ターゲット: {CYAN}{new.target}{RESET}")
    print(f"現在のステータス: {YELLOW}{BOLD}IN_PROGRESS{RESET}")
    print(f"Layers: {BOLD}{layers}{RESET}")
    print(f"\n{BOLD}説明:{RESET}")
    print(new.description)
    print(f"\n{YELLOW}{BOLD}AI Agent への指示:{RESET}")
    print_agent_instruction(new, script_path)
    print(
        f"{RED}{BOLD}それ以外のステップのファイルは絶対に編集・作成しないでください。{RESET}"
    )
    print(f"{CYAN}{BOLD}========================================={RESET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
