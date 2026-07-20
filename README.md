# Agent Skills

Codex と Claude Code で使える Agent Skill のコレクションです。
要件定義から実装・テスト・レビューまでの開発フローを段階的に進める skill と、変更内容を専門領域ごとにレビューする skill を提供します。

## 収録している skill

### 開発フロー

| Skill | 用途 |
| --- | --- |
| [`dw`](dw/) | 要件定義、Gherkin、テスト設計、実装を 6 ステップで進める基本フロー |
| [`dw-layer`](dw-layer/) | 全体要件とレイヤー設計の後、レイヤー単位で開発するフロー |
| [`dw-phase`](dw-phase/) | phase/subphase ツリーを使って機能・レイヤーを段階的に開発するフロー |
| [`dw-phase-light`](dw-phase-light/) | phase 完了時だけ人間レビューを挟む軽量版フロー |
| [`grill-me`](grill-me/) | 計画や設計を一問ずつ掘り下げ、共通理解を作るインタビュー |
| [`prd-maker`](prd-maker/) | 曖昧なアイデアから日本語の PRD を作成するインタビュー |
| [`prd-to-issue`](prd-to-issue/) | 完成した PRD を GitHub issue に変換する |
| [`go-setup`](go-setup/) | 新規 Go プロジェクトに formatter/linter 設定を導入する |

### コードレビュー

| Skill | 用途 |
| --- | --- |
| [`review-orchestrator`](review-orchestrator/) | 変更内容に応じて必要なレビュー skill を選定・実行する |
| [`api-compatibility-review`](api-compatibility-review/) | API、CLI、設定、schema などの後方互換性を確認する |
| [`change-impact-review`](change-impact-review/) | 変更が呼び出し元、データ、運用へ与える影響を追跡する |
| [`security-review`](security-review/) | 認証・認可、入力、秘密情報、プライバシー、悪用経路を確認する |
| [`data-integrity-review`](data-integrity-review/) | DB、migration、永続化、復旧時のデータ整合性を確認する |
| [`concurrency-review`](concurrency-review/) | race、deadlock、leak、cancel、shutdown の問題を確認する |
| [`observability-review`](observability-review/) | ログ、metrics、trace、health check、障害切り分けを確認する |
| [`release-readiness-review`](release-readiness-review/) | deploy、rollback、migration、監視、復旧の準備状況を確認する |
| [`test-quality-review`](test-quality-review/) | テストの検出力、脆さ、flakiness、順序依存を確認する |
| [`ta-review`](ta-review/) | テスト分析の観点から要件、受け入れ条件、ユーザー価値を確認する |
| [`tta-review`](tta-review/) | 技術テスト分析の観点からテスト容易性と非機能リスクを確認する |
| [`jr`](jr/) | 可読性、理解しやすさ、テスト容易性、疎結合を確認する |
| [`code-smell-review`](code-smell-review/) | 設計、責務、結合、変更容易性などのコードスメルを確認する |
| [`code-comment-review`](code-comment-review/) | コメント、docstring、TODO の正確性と保守性を確認する |
| [`comment-contract-reviewer`](comment-contract-reviewer/) | コメントが公開契約だけを説明しているか確認する |
| [`comment-review-orchestrator`](comment-review-orchestrator/) | コメントレビューを言語別 reviewer と連携して統合する |
| [`golang-godoc-reviewer`](golang-godoc-reviewer/) | GoDoc と Effective Go の規約を確認する |
| [`gocomment-contract-review`](gocomment-contract-review/) | git diff の Go コメントを抽出して契約レビューする |
| [`review-finding-validator`](review-finding-validator/) | 既存のレビュー指摘をソース、テスト、仕様に照らして検証する |
| [`review-calibration`](review-calibration/) | 複数 reviewer の指摘を重複排除・統合する |
| [`coderabbit-review`](coderabbit-review/) | CodeRabbit のレビューを複数回実行し、指摘の安定性を評価する |

各 skill の詳細な発動条件、制約、成果物は、それぞれの `SKILL.md` を参照してください。

## インストール

このリポジトリのルートで次を実行します。

```bash
make install
```

各 skill が `~/.claude/skills` と `~/.agents/skills` にコピーされます。既存のインストールをシンボリックリンクにしたい場合は、次を使います。

```bash
make link
```

`make link` は既存のパスを上書きせず、`make install` は対象 skill のコピーを更新します。

## 使い方

インストール後、対象プロジェクトのルートで skill のコマンドを入力します。Codex では `$`、Claude Code では `/` を使います。

```text
$dw
$dw next
$dw review
$dw approve
```

レビューを実行する場合は、目的に合う skill を指定します。

```text
$security-review
$test-quality-review
$review-orchestrator
```

開発フローの状態と成果物は、対象プロジェクトの `.dev-workflow*` ディレクトリに保存されます。Codex と Claude Code で同じ状態を共有する場合は、同じプロジェクトルートから実行してください。

## AI Auto Dev

`bin/` には GitHub issue を監督し、worker に実装と PR 作成を委譲するスクリプトがあります。詳細なオプションと環境変数は [`bin/README.md`](bin/README.md) を参照してください。

```bash
ai-auto-dev-supervisor --worker-cmd ai-auto-dev-worker
ai-auto-dev-supervisor --worker-cmd ai-auto-dev-worker-light
```

## 開発・検証

Python のテストを実行します。

```bash
python3 -m pytest
```

フォーマットと lint は次で実行できます。

```bash
make fmt
make lint
```

## ディレクトリ構成

```text
.
├── <skill-name>/SKILL.md   # Agent Skill の定義
├── <skill-name>/agents/    # agent 用メタデータ（必要な skill のみ）
├── <skill-name>/scripts/   # 実行ロジック（必要な skill のみ）
├── bin/                     # AI Auto Dev の実行スクリプト
├── tests/                   # worker/supervisor のテスト
└── Makefile                 # install、link、fmt、lint
```

## ライセンス

このリポジトリの利用条件は、リポジトリのライセンス設定を確認してください。
