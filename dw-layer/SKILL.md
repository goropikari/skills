---
name: dw-layer
description: >-
  ユーザーが Codex で $dw-layer / $dw-layer next / $dw-layer review / $dw-layer approve、
  または Claude Code で /dw-layer / /dw-layer next / /dw-layer review / /dw-layer approve を入力したときに
  このスキルを有効化し、scripts/workflow.py を実行します。
---

# DW Layer Workflow Skill

このスキルは、全体要件定義、レイヤー設計、各レイヤーごとの 6 ステップ開発を、人間のレビューを挟みながら進めるための agent skill です。

## 使い方

ユーザーが以下のコマンドを入力した際、本スキルに同封されている `scripts/workflow.py` を実行し、その出力をそのままユーザーに表示してください。

`scripts/workflow.py` はこの `SKILL.md` から見た相対パスです。スキルのインストール場所に合わせて絶対パスを解決し、以下の形で実行してください。

Codex と Claude Code のどちらで実行しても、同じ対象プロジェクトの作業ディレクトリで実行する限り、同じ `.dev-workflow-layer/` の状態を共有します。Codex では `$dw-layer`、Claude Code では `/dw-layer` を同じ操作の別名として扱ってください。

1. `$dw-layer` / `/dw-layer`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/workflow.py"`

2. `$dw-layer next` / `/dw-layer next`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/workflow.py" next`

3. `$dw-layer review` / `/dw-layer review`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/workflow.py" review`

4. `$dw-layer approve` / `/dw-layer approve`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/workflow.py" approve`

## 制約事項

- 状態管理と設計成果物は、現在開いている作業ディレクトリ直下の `.dev-workflow-layer/` に保存されます。
- Codex と Claude Code を併用する場合、必ず同じ対象プロジェクトのルートでコマンドを実行してください。異なるディレクトリで実行すると、それぞれ別の `.dev-workflow-layer/` が作られます。
- `CURRENT_STEP.md` に記載されている現在のステップと制約を厳守し、指示されたステップ以外の開発を行わないでください。
- 全体ステップは次の 2 つです。
  - `0. プロジェクト全体の要件定義`: `.dev-workflow-layer/00_project_requirements.md`
  - `1. レイヤー設計`: `.dev-workflow-layer/01_layer_design.md`
- レイヤー設計書には必ず `- **Layers**: N` を記載してください。`N` は 1 以上 20 以下の整数です。
- ステップ 1 が `REVIEWED` の状態で `$dw-layer next` を実行すると、レイヤー設計書から `N` を読み取り、以後のステップを動的に生成します。`N` が不正な場合はステップ 1 から進みません。
- 各レイヤーでは、要件定義、Gherkin 定義、テスト分析・設計、関数定義・コメント作成、テスト実装、内部ロジック実装の順に進めます。
- 各ステップの作業が完了したら、生成・更新した成果物のパスと内容または要約をユーザーに出力し、その後 AI 自身で `python3 "<このスキルディレクトリ>/scripts/workflow.py" review` を実行してレビュー待ち状態にしてください。
