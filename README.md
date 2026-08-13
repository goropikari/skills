# Agent Skills

Codex と Claude Code で利用できる Agent Skill のコレクションです。要件定義、開発フロー、テスト設計、実装、コードレビュー、リリース準備まで、開発ライフサイクルを支援します。

## 収録している skill

### 実装・開発フロー

| Skill                                                         | 用途                                                                     |
| ------------------------------------------------------------- | ------------------------------------------------------------------------ |
| [`implementation-orchestrator`](implementation-orchestrator/) | 変更内容・リスク・不確実性を分析し、適切な実装 workflow を選択・実行する |
| [`agent-workflow-evals`](agent-workflow-evals/)               | 凍結済みblack-box oracleでagent workflowの実装成果物を継続評価する       |

### 要件定義・計画

| Skill                                   | 用途                                                   |
| --------------------------------------- | ------------------------------------------------------ |
| [`grill-me`](grill-me/)                 | 計画や設計を一問ずつ掘り下げ、共通理解を作る           |
| [`prd-maker`](prd-maker/)               | 曖昧なアイデアから日本語の PRD を作成する              |
| [`prd-to-issue`](prd-to-issue/)         | 完成した PRD を GitHub issue に変換する                |
| [`session-learning`](session-learning/) | セッションやデバッグ履歴から再利用可能な教訓を抽出する |

### テスト設計

| Skill                                                   | 用途                                                                                 |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [`blackbox-risk-based-test`](blackbox-risk-based-test/) | 外部から観測できる振る舞い、要件、API、UI をもとにリスクベーステストを設計する       |
| [`whitebox-risk-based-test`](whitebox-risk-based-test/) | ソースコード、制御フロー、データフロー、依存関係をもとにリスクベーステストを設計する |

### バグ調査

| Skill                                                   | 用途                                                         |
| ------------------------------------------------------- | ------------------------------------------------------------ |
| [`reproduce-then-trace-bug`](reproduce-then-trace-bug/) | 不具合を再現、ログ・実行時証拠の確認、原因追跡の順に調査する |

### 品質管理

| Skill                                                                 | 用途                                                                   |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [`quality-modeling`](quality/quality-modeling/)                       | 品質特性から測定・証拠までを結ぶ、説明可能な品質モデルを設計する       |
| [`repository-quality-baseline`](quality/repository-quality-baseline/) | リポジトリ固有の品質モデル、閾値、必須チェックを定義・更新する         |
| [`quality-assessment`](quality/quality-assessment/)                   | 品質ベースラインに対し、テスト・観測・レビューの証拠から変更を評価する |
| [`coding-quality-gate`](quality/coding-quality-gate/)                 | 実装後の品質評価、必要な修正、出荷可否の判定を一貫して実行する         |

### エンジニアリング原則

| Skill                                         | 用途                                                                     |
| --------------------------------------------- | ------------------------------------------------------------------------ |
| [`engineering-compass`](engineering-compass/) | 可読性、理解しやすさ、テスト容易性、疎結合を重視する個人の設計・実装原則 |

### コードレビュー

直接呼び出せる公開 skill は次の 2 つです。

| 公開 skill                                    | 用途                                             |
| --------------------------------------------- | ------------------------------------------------ |
| [`review-orchestrator`](review-orchestrator/) | 変更内容とリスクに応じてレビューを選定・調整する |
| [`goreadable`](goreadable/)                   | Go の可読性レビューの優先対象を定量的に抽出する  |

#### `review-orchestrator` が選択する内部 reviewer

以下は `review-orchestrator` に同梱される内部 component です。単独では install・
起動せず、必要な観点だけを `review-orchestrator` が選択します。

| 内部 reviewer                                                                            | 用途                                                                                 |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [`api-compatibility-review`](review-orchestrator/skills/api-compatibility-review/)       | API、event、CLI、設定、schema の後方互換性を確認する                                 |
| [`architecture-review`](review-orchestrator/skills/architecture-review/)                 | 責務、境界、依存方向、結合、拡張性を確認する                                         |
| [`change-impact-review`](review-orchestrator/skills/change-impact-review/)               | 変更が呼び出し元、データ、API、運用に与える影響を追跡する                            |
| [`code-smell-review`](review-orchestrator/skills/code-smell-review/)                     | 設計、責務、結合、変更容易性、テスト容易性の問題を確認する                           |
| [`code-comment-review`](review-orchestrator/skills/code-comment-review/)                 | コメント、docstring、TODO の正確性と保守性を確認する                                 |
| [`comment-contract-reviewer`](review-orchestrator/skills/comment-contract-reviewer/)     | コメントが公開契約だけを説明しているか確認する                                       |
| [`comment-review-orchestrator`](review-orchestrator/skills/comment-review-orchestrator/) | コメントレビューを専門 reviewer と連携して統合する                                   |
| [`concurrency-review`](review-orchestrator/skills/concurrency-review/)                   | race、deadlock、leak、cancel、shutdown の問題を確認する                              |
| [`data-integrity-review`](review-orchestrator/skills/data-integrity-review/)             | DB、migration、永続化、復旧時のデータ整合性を確認する                                |
| [`dependency-review`](review-orchestrator/skills/dependency-review/)                     | 脆弱性、ライセンス、保守性、供給網リスクを確認する                                   |
| [`gocomment-contract-review`](review-orchestrator/skills/gocomment-contract-review/)     | git diff の Go コメントを抽出して契約レビューする                                    |
| [`engineering-compass-review`](review-orchestrator/skills/engineering-compass-review/)   | Engineering Compass 原則に基づき可読性、理解しやすさ、テスト容易性、疎結合を確認する |
| [`security-review`](review-orchestrator/skills/security-review/)                         | 認証・認可、入力、秘密情報、プライバシー、悪用経路を確認する                         |
| [`test-quality-review`](review-orchestrator/skills/test-quality-review/)                 | テストの検出力、脆さ、flakiness、順序依存を確認する                                  |
| [`ta-review`](review-orchestrator/skills/ta-review/)                                     | テスト分析の観点から要件、受け入れ条件、ユーザー価値を確認する                       |
| [`tta-review`](review-orchestrator/skills/tta-review/)                                   | 技術テスト分析の観点からテスト容易性と非機能リスクを確認する                         |
| [`review-finding-validator`](review-orchestrator/skills/review-finding-validator/)       | 既存のレビュー指摘をソース、テスト、仕様に照らして検証する                           |
| [`review-calibration`](review-orchestrator/skills/review-calibration/)                   | 複数 reviewer の指摘を正規化・重複排除・統合する                                     |
| [`coderabbit-review`](review-orchestrator/skills/coderabbit-review/)                     | CodeRabbit のレビューを複数回実行し、指摘の安定性を評価する                          |

#### 品質・運用の内部 reviewer

| 内部 reviewer                                                                          | 用途                                                               |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [`accessibility-review`](review-orchestrator/skills/accessibility-review/)             | キーボード、スクリーンリーダー、視覚、motion、入力の障壁を確認する |
| [`requirements-review`](review-orchestrator/skills/requirements-review/)               | 要件の曖昧さ、抜け、矛盾、検証可能性を確認する                     |
| [`performance-review`](review-orchestrator/skills/performance-review/)                 | latency、throughput、メモリ、I/O、DB、スケーラビリティを確認する   |
| [`migration-review`](review-orchestrator/skills/migration-review/)                     | 移行の互換性、安全性、冪等性、rollback を確認する                  |
| [`mutation-test-review`](review-orchestrator/skills/mutation-test-review/)             | テストが現実的なコード変更を検出できるか確認する                   |
| [`property-based-test-review`](review-orchestrator/skills/property-based-test-review/) | 不変条件、入力空間、組み合わせ、stateful test を確認する           |
| [`privacy-review`](review-orchestrator/skills/privacy-review/)                         | 個人データの収集、利用、保存、共有、削除を確認する                 |
| [`observability-review`](review-orchestrator/skills/observability-review/)             | ログ、metrics、trace、health check、障害切り分けを確認する         |
| [`incident-readiness-review`](review-orchestrator/skills/incident-readiness-review/)   | 検知、診断、封じ込め、復旧、runbook の準備状況を確認する           |
| [`release-readiness-review`](review-orchestrator/skills/release-readiness-review/)     | deploy、rollback、migration、監視、復旧の準備状況を確認する        |
| [`prd-acceptance-review`](review-orchestrator/skills/prd-acceptance-review/)           | 完成物が PRD の受け入れ条件を満たすか確認する                      |

公開 skill の発動条件、制約、成果物は、それぞれの `SKILL.md` を参照してください。
内部 reviewer の選択基準は `review-orchestrator` の `SKILL.md` にあります。

## インストール

リポジトリのルートで実行します。

```bash
make install
```

active skill が `~/.claude/skills` と `~/.agents/skills` にコピーされます。各コピー先の `.skills-install-state` に前回の管理対象を記録しているため、リポジトリから削除した skill は次回の `make install` でコピー先からも削除されます。状態ファイルに記録されていない既存パスは削除しません。シンボリックリンクで利用する場合は次を実行します。既存のパスは上書きされません。

```bash
make link
```

インストール対象は `deprecated/` を除く、トップレベルと `quality/` 直下の `SKILL.md` から自動的に決まります。`implementation-orchestrator/skills/` と `review-orchestrator/skills/` は bundle 内部 component であり、個別にはインストールしません。

コミット時にフォーマットを確認する hook を有効にするには、次を一度実行します。

```bash
make install-hooks
```

## 使い方

インストール後、対象プロジェクトのルートで skill を呼び出します。Codex では `$`、Claude Code では `/` を使います。

```text
$implementation-orchestrator
$review-orchestrator
```

`implementation-orchestrator` は変更の大きさ・外部契約・リスクに応じて、direct、staged、parallel、comparative の実行方法と必要なreviewを選びます。作業の根拠と最終証拠は対象プロジェクトの `.implementation-orchestrator/` に保存されます。

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
├── <skill-name>/SKILL.md       # 共通系 skill
├── implementation-orchestrator/ # 実装方法を選択する orchestrator と内部 skill 群
├── quality/<skill-name>/        # repository品質モデルとquality gate
├── review-orchestrator/         # review の公開 entry point
│   └── skills/<review-name>/   # orchestrator が選択する内部 reviewer
├── <skill-name>/agents/        # agent 用メタデータ（必要な skill のみ）
├── <skill-name>/scripts/       # 実行ロジック（必要な skill のみ）
├── tests/                      # skill / workflow のテスト
└── Makefile                    # install、link、fmt、lint
```

## ライセンス

このリポジトリの利用条件は、リポジトリのライセンス設定を確認してください。
