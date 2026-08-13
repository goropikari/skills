# implementation-orchestrator

変更内容を分析し、必要な既存 skill を組み合わせて実装計画を作成・実行する skill です。

## 使い方

skill をインストールした対象リポジトリのルートで実行します。

Codex:

```text
$implementation-orchestrator
```

Claude Code:

```text
/implementation-orchestrator
```

通常の依頼と一緒に使うこともできます。

```text
$implementation-orchestrator
ユーザー認証を追加してください。
```

計画だけ作成する場合は、実装しないことを明示してください。

```text
$implementation-orchestrator
このターンでは実装せず、分析と実装計画の作成だけ行ってください。
```

## 動作

orchestrator は、実装前に次を確認します。

1. `AGENTS.md`、contribution guide、package-local rules などの repository 規約
2. 現在の worktree、既存の変更、active workflow state
3. 既存の実装パターン、テスト、build/lint コマンド
4. 変更範囲、外部から観測できる振る舞い、リスク、依存関係
5. 変更量と影響する call site

分析結果をもとに、direct、staged、parallel、comparative の実行方式を選び、
`.implementation-orchestrator/implementation-plan.md` を作成します。

計画には、利用する skill、利用順、各 skill の成果物、受入条件、検証コマンド、
decision gate、実装手順を記録します。

## 利用する skill

必要なものだけを選びます。すべての reviewer を常に実行するわけではありません。
review 系の観点が必要な場合は、公開 entry point である
`review-orchestrator` を選びます。個別 reviewer はその内部 component として
選定されます。

- 要件・計画: `prd-maker`、`grill-me`、`review-orchestrator`
- テスト設計: `blackbox-risk-based-test`、`whitebox-risk-based-test`
- 設計・影響・リスク・運用レビュー: `review-orchestrator`

外部 API、CLI、library、service、破壊的変更、候補実装の比較では、内部 component
`implementation-acceptance-harness` を使い、実装前に black-box の受入条件を凍結します。

## 制約

インストール済みの公開 skill だけを選び、review は
`review-orchestrator` を通して依頼します。orchestrator 自身が計画に沿って実装します。

repository 固有の規約は、この skill の既定ルールより優先されます。

変更量の目安は次のとおりです。

- 機械的変更以外: 変更行数 800 行未満
- 複雑なロジック変更: 変更行数 500 行未満

上限を超える場合は、実際の diff、依存関係、影響する call site を確認し、
最小の reviewable stage に分割します。後続 branch/PR との依存関係も計画に記録し、
原則として最初の stage だけを実装します。

## インストール

skill repository のルートで実行します。

```bash
make install
```

`implementation-orchestrator` は内部 component skill 群を含む bundle として、
`~/.claude/skills` と `~/.agents/skills` にコピーされます。
