---
name: dw-phase-light
description: >-
  ユーザーが Codex で $dw-phase-light / $dw-phase-light next / $dw-phase-light review / $dw-phase-light approve、
  または Claude Code で /dw-phase-light / /dw-phase-light next / /dw-phase-light review / /dw-phase-light approve を入力したときに
  このスキルを有効化し、scripts/workflow.py を実行します。
---

# DW Phase Light Workflow Skill

このスキルは、全体要件定義、フェーズ設計、phase/subphase ツリーによる段階的な設計と実装を進めるための agent skill です。\
人間のレビューは各 phase の完了時だけに挟み、途中の設計・実装ステップではレビューを要求しません。

## 使い方

ユーザーが以下のコマンドを入力した際、本スキルに同封されている `scripts/workflow.py` を実行し、その出力をそのままユーザーに表示してください。

`scripts/workflow.py` はこの `SKILL.md` から見た相対パスです。スキルのインストール場所に合わせて絶対パスを解決し、以下の形で実行してください。

Codex と Claude Code のどちらで実行しても、同じ対象プロジェクトの作業ディレクトリで実行する限り、同じ `.dev-workflow-phase-light/` の状態を共有します。Codex では `$dw-phase-light`、Claude Code では `/dw-phase-light` を同じ操作の別名として扱ってください。

1. `$dw-phase-light` / `/dw-phase-light`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/workflow.py"`

2. `$dw-phase-light next` / `/dw-phase-light next`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/workflow.py" next`

3. `$dw-phase-light review` / `/dw-phase-light review`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/workflow.py" review`

4. `$dw-phase-light approve` / `/dw-phase-light approve`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/workflow.py" approve`

## 制約事項

- 状態管理と設計成果物は、現在開いている作業ディレクトリ直下の `.dev-workflow-phase-light/` に保存されます。
- Codex と Claude Code を併用する場合、必ず同じ対象プロジェクトのルートでコマンドを実行してください。異なるディレクトリで実行すると、それぞれ別の `.dev-workflow-phase-light/` が作られます。
- `CURRENT_STEP.md` に記載されている現在のステップ、現在の phase パス、Phase Type、Local Step、制約を厳守し、指示されたステップ以外の開発を行わないでください。
- 全体ステップは次の 2 つです。
  - `0. プロジェクト全体の要件定義`: `.dev-workflow-phase-light/00_project_requirements.md`
  - `1. フェーズ設計`: `.dev-workflow-phase-light/01_phase_design.md`
- フェーズ設計書には必ず `- **Phases**: N` を記載してください。`N` は 1 以上 20 以下の整数です。
- フェーズ設計書には `## Phase N: 名前` を N 個記載し、各セクションに必ず `- **Phase Type**: feature|layer` を記載してください。
- ステップ 1 が完了した状態で `$dw-phase-light next` を実行すると、フェーズ設計書からトップレベル phase を読み取り、記載順に深さ優先で進行します。不正な場合はステップ 1 から進みません。
- 各 phase/subphase は最初に `.dev-workflow-phase-light/<phase-path>/01_definition.md` を作成します。このファイルにも必ず `- **Phase Type**: feature|layer` を記載してください。承認後、以後の step 構成を Phase Type で確定します。
- `feature` phase は次の順に進めます。
  - `01_definition.md`
  - `02_gherkin/spec.feature`
  - `03_test_design.md`
  - `04_interface` 相当の関数定義・コメント作成
  - `05_tests` 相当のテスト実装
  - `06_implementation` 相当の内部ロジック実装
- `layer` phase は次の順に進めます。
  - `01_definition.md`
  - `02_contract_design.md`
  - `03_test_design.md`
  - `04_interface` 相当のインターフェース/スタブ作成
  - `05_tests` 相当のテスト実装
  - `06_implementation` 相当の内部ロジック実装
- `03_test_design.md` には必ず `- **Split**: yes|no` を記載してください。
- `Split: yes` の場合、`03_test_design.md` 完了後の `$dw-phase-light next` は同じ phase/subphase 直下の `.dev-workflow-phase-light/<phase-path>/04_split_design.md` 作成 step に進みます。
- `04_split_design.md` には必ず `- **Subphases**: N` を記載し、`## Subphase N: 名前` を N 個記載し、各セクションに `- **Phase Type**: feature|layer` を記載してください。
- `Split: no` の場合のみ、その phase/subphase を末端 phase として関数定義・コメント作成、テスト実装、内部ロジック実装へ進めます。
- 子 phase は分割設計書の記載順に深さ優先で進みます。子 phase 群がすべて完了したら親 phase は自動的に完了扱いになります。
- 全トップレベル phase が完了したらワークフロー全体も `COMPLETED` になります。
- 各 phase の内部ステップは `next` で連続進行し、レビューはその phase の内部実装が完了した時点だけに行います。レビュー待ちに入ったら、AI 自身で `python3 "<このスキルディレクトリ>/scripts/workflow.py" review` を実行してください。
