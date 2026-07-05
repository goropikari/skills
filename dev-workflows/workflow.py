#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re

# Check if color is supported
supports_color = sys.stdout.isatty() and os.environ.get("TERM") != "dumb" and not os.environ.get("NO_COLOR")

BOLD = "\033[1m" if supports_color else ""
GREEN = "\033[32m" if supports_color else ""
YELLOW = "\033[33m" if supports_color else ""
BLUE = "\033[34m" if supports_color else ""
CYAN = "\033[36m" if supports_color else ""
RED = "\033[31m" if supports_color else ""
RESET = "\033[0m" if supports_color else ""
DW_NEXT_COMMAND = "$dw next (Claude Code: /dw next)"
DW_REVIEW_COMMAND = "$dw review (Claude Code: /dw review)"
DW_APPROVE_COMMAND = "$dw approve (Claude Code: /dw approve)"

STEPS = [
    {
        "index": 0,
        "name": "1. 実装の要件定義",
        "file": ".dev-workflow/01_requirements.md",
        "description": "grill-me で要件を一問ずつ深掘りし、合意内容を要件定義書として記述する。"
    },
    {
        "index": 1,
        "name": "2. Gherkin定義",
        "file": ".dev-workflow/02_features/spec.feature",
        "description": "Gherkin (Given/When/Then) 形式で期待される振る舞いを定義する。"
    },
    {
        "index": 2,
        "name": "3. テスト分析・設計",
        "file": ".dev-workflow/03_test_design.md",
        "description": "要件定義書とGherkin定義を入力として、テスト観点、テストケース一覧を自動的に設計する。"
    },
    {
        "index": 3,
        "name": "4. テスト実装",
        "file": "実プロジェクト内の適切なテストファイル",
        "description": "テスト分析・設計に従い、対象プロジェクトのテスト構成に合う場所へ自動テストを実装する。"
    },
    {
        "index": 4,
        "name": "5. 関数定義・コメント作成（ロジック空）",
        "file": "実プロジェクト内の適切なソースファイル",
        "description": "対象プロジェクトの設計に合う場所へ、関数のシグネチャ、docstring、スタブのみを実装する。"
    },
    {
        "index": 5,
        "name": "6. 内部ロジック実装",
        "file": "実プロジェクト内の適切なソースファイル",
        "description": "対象プロジェクトのソースファイルに内部ロジックを実装し、テストをすべてパスさせる。"
    }
]

def get_step_workflow_notes(step_num):
    if step_num == 0:
        return """## 🔥 要件定義フェーズの進め方 / Requirements Workflow
- `grill-me` スキルを必ず使用し、ユーザーに一問ずつ質問して要件を詰める。
- 各質問では AI の推奨回答を添える。
- コードベースを確認すれば答えられることは、ユーザーに聞かずに調査する。
- 目的、対象ユーザー、スコープ、非スコープ、主要ユースケース、入出力、制約、受け入れ条件、未決事項を合意する。
- 合意した内容だけを `.dev-workflow/01_requirements.md` に要件定義書としてまとめる。
"""
    if step_num == 1:
        return """## 🥒 Gherkin定義フェーズの進め方 / Gherkin Workflow
- `.dev-workflow/01_requirements.md` を必ず読み、要件定義書の内容から期待される振る舞いをGherkin形式で定義する。
- Feature、Scenario、Given/When/Then を使い、主要ユースケース、受け入れ条件、正常系・異常系を表現する。
- 要件定義書だけでは判断できない内容は推測で埋めず、コメントまたは未決事項として `.dev-workflow/02_features/spec.feature` に明記する。
"""
    if step_num == 2:
        return """## 🧪 テスト分析・設計フェーズの進め方 / Test Analysis Workflow
- `.dev-workflow/01_requirements.md` を必ず読み、要件定義書の内容から自動的にテスト分析・設計を作成する。
- `.dev-workflow/02_features/spec.feature` を必ず読み、Gherkin定義と要件定義書の対応を確認する。
- ユーザーへ追加質問せず、要件定義書とGherkin定義から判断できる範囲でテスト観点、テスト条件、正常系・異常系・境界値、リスク、受け入れ条件との対応を整理する。
- 要件定義書とGherkin定義だけでは判断できない内容は推測で埋めず、未決事項またはテストリスクとして `.dev-workflow/03_test_design.md` に明記する。
"""
    return ""

def print_agent_instruction(step_num, script_path=None, continuing=False):
    step = STEPS[step_num]
    if step_num == 0:
        action = "作成・更新" if continuing else "作成"
        print(f"1. `grill-me` スキルを使用して、要件を一問ずつ深掘りしてください。")
        print("   - 各質問には AI の推奨回答を添えてください。")
        print("   - コードベースを確認すれば答えられることは、ユーザーに聞かずに調査してください。")
        print("2. 目的、対象ユーザー、スコープ、非スコープ、主要ユースケース、入出力、制約、受け入れ条件、未決事項を合意してください。")
        print(f"3. 合意後、ターゲットファイル `{CYAN}{step['file']}{RESET}` に要件定義書を{action}してください。")
        print("4. 今何が終わっていて、次に何が残っているのかのサマリ（完了したこと、残タスク）を")
        print("   `.dev-workflow/CURRENT_STEP.md` の「進捗サマリ」セクションに随時記録・更新してください。")
        print("5. ステップの作業が完了したら、生成・更新した成果物のパスと内容または要約をユーザーに出力してください。")
        if script_path:
            print(f"6. 成果物の出力後、AI自身でコマンド `{CYAN}python3 {script_path} review{RESET}` を実行してレビュー待ち状態にしてください。")
        return

    if step_num == 1:
        print(f"1. 入力元 `{CYAN}.dev-workflow/01_requirements.md{RESET}` を必ず読み、要件定義書からGherkin定義を作成してください。")
        print(f"2. ターゲットファイル `{CYAN}{step['file']}{RESET}` に、Feature、Scenario、Given/When/Then 形式で期待される振る舞いを記述してください。")
        print("3. ユーザーへ追加質問せず、判断できない内容はコメントまたは未決事項として明記してください。")
        print("4. 今何が終わっていて、次に何が残っているのかのサマリ（完了したこと、残タスク）を")
        print("   `.dev-workflow/CURRENT_STEP.md` の「進捗サマリ」セクションに随時記録・更新してください。")
        print("5. ステップの作業が完了したら、生成・更新した成果物のパスと内容または要約をユーザーに出力してください。")
        if script_path:
            print(f"6. 成果物の出力後、AI自身でコマンド `{CYAN}python3 {script_path} review{RESET}` を実行してレビュー待ち状態にしてください。")
        return

    if step_num == 2:
        print(f"1. 入力元 `{CYAN}.dev-workflow/01_requirements.md{RESET}` と `{CYAN}.dev-workflow/02_features/spec.feature{RESET}` を必ず読み、テスト分析・設計を自動生成してください。")
        print(f"2. ターゲットファイル `{CYAN}{step['file']}{RESET}` に、テスト観点、テスト条件、正常系・異常系・境界値、リスク、受け入れ条件との対応を記述してください。")
        print("3. ユーザーへ追加質問せず、判断できない内容は未決事項またはテストリスクとして明記してください。")
        print("4. 今何が終わっていて、次に何が残っているのかのサマリ（完了したこと、残タスク）を")
        print("   `.dev-workflow/CURRENT_STEP.md` の「進捗サマリ」セクションに随時記録・更新してください。")
        print("5. ステップの作業が完了したら、生成・更新した成果物のパスと内容または要約をユーザーに出力してください。")
        if script_path:
            print(f"6. 成果物の出力後、AI自身でコマンド `{CYAN}python3 {script_path} review{RESET}` を実行してレビュー待ち状態にしてください。")
        return

    if step_num >= 3:
        print(f"1. ターゲット範囲 `{CYAN}{step['file']}{RESET}` で、対象プロジェクトの既存構成に合う場所を選んで実装してください。")
    else:
        print(f"1. ターゲットファイル `{CYAN}{step['file']}{RESET}` に対する実装・作成作業を進めてください。")
    print("2. 今何が終わっていて、次に何が残っているのかのサマリ（完了したこと、残タスク）を")
    print("   `.dev-workflow/CURRENT_STEP.md` の「進捗サマリ」セクションに随時記録・更新してください。")
    print("3. ステップの作業が完了したら、生成・更新した成果物のパスと内容または要約をユーザーに出力してください。")
    if script_path:
        print(f"4. 成果物の出力後、AI自身でコマンド `{CYAN}python3 {script_path} review{RESET}` を実行してレビュー待ち状態にしてください。")

def init_environment(base_dir):
    dev_workflow_dir = os.path.join(base_dir, ".dev-workflow")
    subdirs = ["02_features"]
    
    # Create main directory
    if not os.path.exists(dev_workflow_dir):
        os.makedirs(dev_workflow_dir, exist_ok=True)
        
    # Create subdirectories
    for subdir in subdirs:
        os.makedirs(os.path.join(dev_workflow_dir, subdir), exist_ok=True)
        
    # Handle .gitignore
    gitignore_path = os.path.join(base_dir, ".gitignore")
    ignore_entry = ".dev-workflow/"
    
    needs_append = True
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            stripped = line.strip()
            if stripped == ignore_entry or stripped == ".dev-workflow":
                needs_append = False
                break
    
    if needs_append:
        has_newline = True
        if os.path.exists(gitignore_path) and os.path.getsize(gitignore_path) > 0:
            try:
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    f.seek(0, os.SEEK_END)
                    pos = max(0, f.tell() - 1)
                    f.seek(pos)
                    last_char = f.read(1)
                    has_newline = (last_char == '\n')
            except Exception:
                has_newline = True
        
        with open(gitignore_path, "a", encoding="utf-8") as f:
            if not has_newline:
                f.write("\n")
            f.write(f"{ignore_entry}\n")

def read_status(base_dir):
    current_step_path = os.path.join(base_dir, ".dev-workflow", "CURRENT_STEP.md")
    if not os.path.exists(current_step_path):
        write_status(base_dir, 0, "IN_PROGRESS")
        return 0, "IN_PROGRESS"
    
    step_num = 0
    status = "IN_PROGRESS"
    
    try:
        with open(current_step_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        step_match = re.search(r"-\s+\*\*Step\*\*:\s*(\d+)", content)
        if step_match:
            step_num = int(step_match.group(1))
            if step_num < 0 or step_num >= len(STEPS):
                step_num = 0
            
        status_match = re.search(r"-\s+\*\*Status\*\*:\s*([A-Z_]+)", content)
        if status_match:
            status = status_match.group(1)
    except Exception:
        pass
        
    return step_num, status

def write_status(base_dir, step_num, status):
    current_step_path = os.path.join(base_dir, ".dev-workflow", "CURRENT_STEP.md")
    
    # If the file exists and we are just changing status on the same step, preserve other contents (like progress summary)
    if os.path.exists(current_step_path):
        try:
            with open(current_step_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            step_match = re.search(r"-\s+\*\*Step\*\*:\s*(\d+)", content)
            if step_match and int(step_match.group(1)) == step_num:
                # Replace the status line
                updated_content = re.sub(
                    r"-\s+\*\*Status\*\*:\s*[A-Z_]+",
                    f"- **Status**: {status}",
                    content
                )
                with open(current_step_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                return
        except Exception:
            pass  # Fall back to overwriting if anything goes wrong
            
    step = STEPS[step_num]
    
    content = f"""# Dev Workflow State

- **Step**: {step_num}
- **Step Name**: {step["name"]}
- **Target**: {step["file"]}
- **Status**: {status}

## 📝 説明 / Description
{step["description"]}

{get_step_workflow_notes(step_num)}
## 📋 進捗サマリ / Progress Summary
<!-- AIが現在の作業状況（完了したこと・残タスク・進捗のサマリ）をここに随時記録し、完了したら {DW_REVIEW_COMMAND} を実行してください -->
- [ ] ターゲット範囲の作成・初期定義
- [ ] 詳細なロジック/テストの実装・調整
- [ ] 動作確認 / 自己テスト合格

## ⚠️ AI Agent Constraint / 制約事項
次へ進む指示（`$dw next` コマンド、Claude Code では `/dw next` の実行）があるまで、絶対にこれ以降のステップのファイルを生成・変更してはいけない。
Do NOT create or modify files for subsequent steps until explicitly instructed to proceed (via `$dw next`, or `/dw next` in Claude Code).
"""
    with open(current_step_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    base_dir = os.getcwd()
    script_path = os.path.abspath(__file__)
    
    # Initialize environment
    init_environment(base_dir)
    
    # Check arguments
    is_next = len(sys.argv) > 1 and sys.argv[1] == "next"
    is_approve = len(sys.argv) > 1 and sys.argv[1] in ("approve", "reviewed")
    is_review = len(sys.argv) > 1 and sys.argv[1] in ("review", "submit", "review-pending", "review_pending")
    
    step_num, status = read_status(base_dir)
    
    if is_review:
        write_status(base_dir, step_num, "REVIEW_PENDING")
        print(f"{CYAN}{BOLD}========================================={RESET}")
        print(f"{CYAN}{BOLD}✉️  DEV-WORKFLOW STATUS UPDATED TO REVIEW_PENDING{RESET}")
        print(f"{CYAN}{BOLD}========================================={RESET}")
        print(f"現在のステップ: {BOLD}{STEPS[step_num]['name']}{RESET}")
        print("ステータスを REVIEW_PENDING に更新しました（レビュー待ち状態）。")
        print("人間（ユーザー）によるレビュー・確認を待機します。")
        print(f"承認が得られたら、AI自身で {GREEN}{DW_APPROVE_COMMAND}{RESET} を実行してください。")
        print(f"{CYAN}{BOLD}========================================={RESET}")
        sys.exit(0)
        
    if is_approve:
        write_status(base_dir, step_num, "REVIEWED")
        print(f"{GREEN}{BOLD}========================================={RESET}")
        print(f"{GREEN}{BOLD}✅  DEV-WORKFLOW STATUS UPDATED TO REVIEWED{RESET}")
        print(f"{GREEN}{BOLD}========================================={RESET}")
        print(f"現在のステップ: {BOLD}{STEPS[step_num]['name']}{RESET}")
        print("ステータスを REVIEWED に更新しました。")
        print(f"次のステップに進むには、{CYAN}{BOLD}{DW_NEXT_COMMAND}{RESET} を実行してください。")
        print(f"{GREEN}{BOLD}========================================={RESET}")
        sys.exit(0)
        
    if is_next:
        if status == "IN_PROGRESS":
            print(f"{YELLOW}{BOLD}========================================={RESET}")
            print(f"{YELLOW}{BOLD}⚠️  DEV-WORKFLOW: CURRENT STEP IN PROGRESS / 作業継続指示{RESET}")
            print(f"{YELLOW}{BOLD}========================================={RESET}")
            print("現在のステップの開発・作業はまだ完了していません。")
            print(f"ターゲット: {CYAN}{STEPS[step_num]['file']}{RESET}")
            print(f"現在のステータス: {YELLOW}{BOLD}IN_PROGRESS{RESET}")
            print(f"\n{BOLD}📝 説明:{RESET}")
            print(STEPS[step_num]['description'])
            print(f"\n{YELLOW}{BOLD}👉 AI Agent への指示:{RESET}")
            print_agent_instruction(step_num, script_path=script_path, continuing=True)
            print(f"{YELLOW}{BOLD}========================================={RESET}")
            sys.exit(0)
            
        if status == "REVIEW_PENDING":
            print(f"{CYAN}{BOLD}========================================={RESET}")
            print(f"{CYAN}{BOLD}⏳  DEV-WORKFLOW: REVIEW PENDING / レビュー確認待ち{RESET}")
            print(f"{CYAN}{BOLD}========================================={RESET}")
            print("現在のステップは人間のレビュー確認待ち（REVIEW_PENDING）です。")
            print(f"ターゲット: {CYAN}{STEPS[step_num]['file']}{RESET}")
            print(f"\n{BOLD}👉 AI Agent への指示:{RESET}")
            print("1. 人間（ユーザー）からのレビュー確認または「OK」「進めて」などの指示を待ってください。")
            print("2. 承認指示を受け取ったら、AI自身でステータスを承認済みに更新してください：")
            print(f"   - コマンド `{CYAN}python3 {script_path} approve{RESET}` を実行する")
            print(f"3. 承認更新後、再度 `{CYAN}{DW_NEXT_COMMAND}{RESET}` コマンドを実行して次のステップへ進んでください。")
            print(f"{CYAN}{BOLD}========================================={RESET}")
            sys.exit(0)
            
        if step_num >= len(STEPS) - 1:
            write_status(base_dir, step_num, "COMPLETED")
            print(f"{GREEN}{BOLD}========================================={RESET}")
            print(f"{GREEN}{BOLD}🎉  DEV-WORKFLOW ALL STEPS COMPLETED{RESET}")
            print(f"{GREEN}{BOLD}========================================={RESET}")
            print(f"すべての開発ステップ（ステップ 1〜{len(STEPS)}）が完了しています！")
            print(f"最後のターゲット: {CYAN}{STEPS[step_num]['file']}{RESET}")
            print(f"現在のステータス: {GREEN}{BOLD}COMPLETED{RESET}")
            print(f"{GREEN}{BOLD}========================================={RESET}")
        else:
            old_step = step_num
            new_step = step_num + 1
            write_status(base_dir, new_step, "IN_PROGRESS")
            
            print(f"{CYAN}{BOLD}========================================={RESET}")
            print(f"{CYAN}{BOLD}➡️  DEV-WORKFLOW STEP TRANSITION (Step {old_step+1}/{len(STEPS)} -> {new_step+1}/{len(STEPS)}){RESET}")
            print(f"{CYAN}{BOLD}========================================={RESET}")
            print("現在のステップが正常に進みました！")
            print(f"新しいステップ: {BOLD}{STEPS[new_step]['name']}{RESET}")
            print(f"ターゲット: {CYAN}{STEPS[new_step]['file']}{RESET}")
            print(f"現在のステータス: {YELLOW}{BOLD}IN_PROGRESS{RESET}")
            print(f"\n{BOLD}📝 説明:{RESET}")
            print(STEPS[new_step]['description'])
            print(f"\n{YELLOW}{BOLD}👉 AI Agent への指示:{RESET}")
            print_agent_instruction(new_step, script_path=script_path)
            print(f"{RED}{BOLD}それ以外のステップのファイルは絶対に編集・作成しないでください。{RESET}")
            print(f"{CYAN}{BOLD}========================================={RESET}")
    else:
        # Show current step status
        print(f"{BLUE}{BOLD}========================================={RESET}")
        print(f"{BLUE}{BOLD}🛠️  DEV-WORKFLOW (Step {step_num+1}/{len(STEPS)}){RESET}")
        print(f"{BLUE}{BOLD}========================================={RESET}")
        print(f"現在のステップ: {BOLD}{STEPS[step_num]['name']}{RESET}")
        print(f"ターゲット: {CYAN}{STEPS[step_num]['file']}{RESET}")
        print(f"現在のステータス: {YELLOW}{BOLD}{status}{RESET}")
        print(f"\n{BOLD}📝 説明:{RESET}")
        print(STEPS[step_num]['description'])
        print(f"\n{YELLOW}{BOLD}👉 AI Agent への指示:{RESET}")
        print_agent_instruction(step_num, script_path=script_path, continuing=True)
        print(f"\n{RED}{BOLD}⚠️ 制約事項:{RESET}")
        print(f"{RED}次へ進む指示があるまで、絶対にこれ以降のステップのファイルを生成・変更しないでください。{RESET}")
        print(f"{BLUE}{BOLD}========================================={RESET}")

if __name__ == "__main__":
    main()
