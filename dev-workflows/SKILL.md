---
name: dw
description: >-
  ユーザーが Codex で $dw / $dw next / $dw review / $dw approve、
  または Claude Code で /dw / /dw next / /dw review / /dw approve を入力したときに
  このスキルを有効化し、同じディレクトリにある workflow.py を実行します。
---

# Dev Workflow Skill

このスキルは、Git worktree 環境で人間のレビューを挟みながら厳格に段階的開発（6ステップ）を進めるための agent skill です。

## 使い方 (Usage)

ユーザーが以下のコマンドを入力した際、本スキルに同封されている `workflow.py` を実行し、その出力をそのままユーザーに表示してください。

`workflow.py` はこの `SKILL.md` と同じディレクトリにあります。スキルのインストール場所に合わせて絶対パスを解決し、以下の形で実行してください。

1. **`$dw` / `/dw` (引数なし)**
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/workflow.py"`

2. **`$dw next` / `/dw next` (引数 `next` あり)**
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/workflow.py" next`

3. **`$dw approve` / `/dw approve` (引数 `approve` あり)**
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/workflow.py" approve`

4. **`$dw review` / `/dw review` (引数 `review` あり)**
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/workflow.py" review`

## 制約事項 (Constraints)

- 状態管理およびステップ 1〜3 の設計成果物は、現在開いている作業ディレクトリ直下の `.dev-workflow/` ディレクトリに隔離されます。ステップ 4 以降のテストコード・実装コードは、対象プロジェクトの既存構成に合う場所へ作成・修正してください。
- `CURRENT_STEP.md` に記載されている現在のステップおよび制約を厳守し、指示されたステップ以外の開発（ファイルの生成や修正）を行わないでください。
- 各ステップの作業が完了したら、生成・更新した成果物のパスと内容または要約をユーザーに出力し、その後 AI 自身で `python3 "<このスキルディレクトリ>/workflow.py" review` を実行してレビュー待ち状態に移行してください。
- ステップ 1「実装の要件定義」では、必ず `grill-me` スキルの進め方に従ってください。ユーザーに一問ずつ質問し、各質問に AI の推奨回答を添え、コードベースから判断できることは質問せずに調査してください。合意した内容を `.dev-workflow/01_requirements.md` に要件定義書としてまとめてください。
- ステップ 2「Gherkin定義」では、`.dev-workflow/01_requirements.md` を入力として `.dev-workflow/02_features/spec.feature` を自動生成してください。ユーザーへ追加質問せず、判断できない内容はコメントまたは未決事項として明記してください。
- ステップ 3「テスト分析・設計」では、`.dev-workflow/01_requirements.md` と `.dev-workflow/02_features/spec.feature` を入力として `.dev-workflow/03_test_design.md` を自動生成してください。ユーザーへ追加質問せず、判断できない内容は未決事項またはテストリスクとして明記してください。
