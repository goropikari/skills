# Agent Skills

Codex と Claude Code で利用できる Agent Skill のコレクションです。要件定義、開発フロー、テスト設計、実装、コードレビュー、リリース準備まで、開発ライフサイクルを支援します。

## 収録している skill

### 開発フロー・要件定義

| Skill                                                                                           | 用途                                                                            |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [`acceptance-driven-app`](acceptance-driven-app/)                                               | Web/API アプリを受け入れ条件駆動で実装し、PR の証跡まで管理する                 |
| [`dw-phase`](dw-phase/)                                                                         | phase/subphase ツリーを使って機能やレイヤーを段階的に開発する                   |
| [`dw-phase-parallel`](dw-phase-parallel/)                                                       | 依存関係のない phase を別 worktree・別 agent で並列実装し、各段階でレビューする |
| [`dw-phase-parallel-light`](dw-phase-parallel-light/)                                           | phase を並列に一括実装し、自己レビューとテストまで実行する                      |
| [`dw-phase-tournament-flow`](dw-phase-tournament-flow/)                                         | リスクベーステスト、並列実装、実装トーナメント、レビュー、最終検証を統合する    |
| [`grill-me`](grill-me/)                                                                         | 計画や設計を一問ずつ掘り下げ、共通理解を作る                                    |
| [`prd-maker`](prd-maker/)                                                                       | 曖昧なアイデアから日本語の PRD を作成する                                       |
| [`prd-to-issue`](prd-to-issue/)                                                                 | 完成した PRD を GitHub issue に変換する                                         |
| [`iterative-multi-agent-tournament-development`](iterative-multi-agent-tournament-development/) | 複数 agent の実装を比較し、複数ラウンドで改善する                               |
| [`multi-agent-tounament-development`](multi-agent-tounament-development/)                       | 複数 agent の実装を worktree 上で比較し、採用案を検証する                       |
| [`session-learning`](session-learning/)                                                         | セッションやデバッグ履歴から再利用可能な教訓を抽出する                          |

### テスト設計

| Skill                                                   | 用途                                                                                 |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [`blackbox-risk-based-test`](blackbox-risk-based-test/) | 外部から観測できる振る舞い、要件、API、UI をもとにリスクベーステストを設計する       |
| [`whitebox-risk-based-test`](whitebox-risk-based-test/) | ソースコード、制御フロー、データフロー、依存関係をもとにリスクベーステストを設計する |

### コードレビュー

| Skill                                                                 | 用途                                                           |
| --------------------------------------------------------------------- | -------------------------------------------------------------- |
| [`review-orchestrator`](reviews/review-orchestrator/)                 | 変更内容とリスクに応じて、実行すべきレビューを選定・調整する   |
| [`api-compatibility-review`](reviews/api-compatibility-review/)       | API、event、CLI、設定、schema の後方互換性を確認する           |
| [`architecture-review`](reviews/architecture-review/)                 | 責務、境界、依存方向、結合、拡張性を確認する                   |
| [`change-impact-review`](reviews/change-impact-review/)               | 変更が呼び出し元、データ、API、運用に与える影響を追跡する      |
| [`code-smell-review`](reviews/code-smell-review/)                     | 設計、責務、結合、変更容易性、テスト容易性の問題を確認する     |
| [`code-comment-review`](reviews/code-comment-review/)                 | コメント、docstring、TODO の正確性と保守性を確認する           |
| [`comment-contract-reviewer`](reviews/comment-contract-reviewer/)     | コメントが公開契約だけを説明しているか確認する                 |
| [`comment-review-orchestrator`](reviews/comment-review-orchestrator/) | コメントレビューを専門 reviewer と連携して統合する             |
| [`concurrency-review`](reviews/concurrency-review/)                   | race、deadlock、leak、cancel、shutdown の問題を確認する        |
| [`data-integrity-review`](reviews/data-integrity-review/)             | DB、migration、永続化、復旧時のデータ整合性を確認する          |
| [`dependency-review`](reviews/dependency-review/)                     | 脆弱性、ライセンス、保守性、供給網リスクを確認する             |
| [`gocomment-contract-review`](reviews/gocomment-contract-review/)     | git diff の Go コメントを抽出して契約レビューする              |
| [`jr`](reviews/jr/)                                                   | 可読性、理解しやすさ、テスト容易性、疎結合を確認する           |
| [`security-review`](reviews/security-review/)                         | 認証・認可、入力、秘密情報、プライバシー、悪用経路を確認する   |
| [`test-quality-review`](reviews/test-quality-review/)                 | テストの検出力、脆さ、flakiness、順序依存を確認する            |
| [`ta-review`](reviews/ta-review/)                                     | テスト分析の観点から要件、受け入れ条件、ユーザー価値を確認する |
| [`tta-review`](reviews/tta-review/)                                   | 技術テスト分析の観点からテスト容易性と非機能リスクを確認する   |
| [`review-finding-validator`](reviews/review-finding-validator/)       | 既存のレビュー指摘をソース、テスト、仕様に照らして検証する     |
| [`review-calibration`](reviews/review-calibration/)                   | 複数 reviewer の指摘を正規化・重複排除・統合する               |
| [`coderabbit-review`](reviews/coderabbit-review/)                     | CodeRabbit のレビューを複数回実行し、指摘の安定性を評価する    |

### 品質・運用レビュー

| Skill                                                               | 用途                                                               |
| ------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [`accessibility-review`](reviews/accessibility-review/)             | キーボード、スクリーンリーダー、視覚、motion、入力の障壁を確認する |
| [`requirements-review`](reviews/requirements-review/)               | 要件の曖昧さ、抜け、矛盾、検証可能性を確認する                     |
| [`performance-review`](reviews/performance-review/)                 | latency、throughput、メモリ、I/O、DB、スケーラビリティを確認する   |
| [`migration-review`](reviews/migration-review/)                     | 移行の互換性、安全性、冪等性、rollback を確認する                  |
| [`mutation-test-review`](reviews/mutation-test-review/)             | テストが現実的なコード変更を検出できるか確認する                   |
| [`property-based-test-review`](reviews/property-based-test-review/) | 不変条件、入力空間、組み合わせ、stateful test を確認する           |
| [`privacy-review`](reviews/privacy-review/)                         | 個人データの収集、利用、保存、共有、削除を確認する                 |
| [`observability-review`](reviews/observability-review/)             | ログ、metrics、trace、health check、障害切り分けを確認する         |
| [`incident-readiness-review`](reviews/incident-readiness-review/)   | 検知、診断、封じ込め、復旧、runbook の準備状況を確認する           |
| [`release-readiness-review`](reviews/release-readiness-review/)     | deploy、rollback、migration、監視、復旧の準備状況を確認する        |
| [`prd-acceptance-review`](reviews/prd-acceptance-review/)           | 完成物が PRD の受け入れ条件を満たすか確認する                      |

各 skill の発動条件、制約、成果物は、それぞれの `SKILL.md` を参照してください。

## インストール

リポジトリのルートで実行します。

```bash
make install
```

active skill が `~/.claude/skills` と `~/.agents/skills` にコピーされます。シンボリックリンクで利用する場合は次を実行します。既存のパスは上書きされません。

```bash
make link
```

インストール対象は `deprecated/` を除く、各ディレクトリの `SKILL.md` から自動的に決まります。

コミット時にフォーマットを確認する hook を有効にするには、次を一度実行します。

```bash
make install-hooks
```

## 使い方

インストール後、対象プロジェクトのルートで skill を呼び出します。Codex では `$`、Claude Code では `/` を使います。

```text
$dw-phase
$dw-phase next
$security-review
$review-orchestrator
```

`dw-phase` の設計レビュー後は、依存関係のない phase を並列実装できます。

```text
$dw-phase-parallel
$dw-phase-parallel next --agent-cmd '<agent command>'
$dw-phase-parallel status

# 途中レビューを省略して一括実装へ切り替える場合
$dw-phase-parallel switch light
```

`dw-phase-parallel-light` は native subagent を使うため、agent command の指定は不要です。並列系の skill は agent に commit、push、PR 作成をさせず、ユーザーが Git 操作を行った後に `status` で状態を同期します。

開発フローの状態と成果物は、対象プロジェクトの `.dev-workflow*` ディレクトリに保存されます。Codex と Claude Code で状態を共有する場合は、同じプロジェクトルートから実行してください。

## 開発・検証

```bash
python3 -m pytest
make fmt
make lint
```

`make fmt` は Markdown/configuration を dprint で、Python を Ruff で整形します。`make lint` は整形後に gitleaks で秘密情報を検査します。

## ディレクトリ構成

```text
.
├── <skill-name>/SKILL.md       # 開発フロー・テスト設計などの skill
├── reviews/<skill-name>/       # コードレビュー系 skill
├── <skill-name>/agents/        # agent 用メタデータ（必要な skill のみ）
├── <skill-name>/scripts/       # 実行ロジック（必要な skill のみ）
├── tests/                      # skill / workflow のテスト
└── Makefile                    # install、link、fmt、lint
```

## ライセンス

このリポジトリの利用条件は、リポジトリのライセンス設定を確認してください。
