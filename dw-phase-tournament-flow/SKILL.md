---
name: dw-phase-tournament-flow
description: >-
  要件、受入条件、blackbox リスクテスト設計、phase 分割、依存関係、
  並列実装、必要な tournament、検証、統合までを単独で管理する delivery
  workflow。既存 workflow skill は使わず、review 系 skill だけを必要に応じて
  呼び出す。既存 phase 設計をこの flow の成果物へ移行するときにも使う。
---

# DW Phase Tournament Flow

この skill が workflow、設計、blackbox test design、状態遷移、成果物管理を
一貫して担当します。既存の workflow / test-design skill は呼び出さず、
必要な場合のみ review 系 skill を独立 reviewer として使います。

## Canonical state and commands

状態と成果物は対象リポジトリ直下の `.dev-workflow-tournament/` に保存します。
`dw-phase` の `.dev-workflow-phase/` は作成・更新しません。

```text
$dw-phase-tournament-flow          # 初期化または状態表示
$dw-phase-tournament-flow review   # 現在の成果物をレビュー待ちにする
$dw-phase-tournament-flow approve  # 現在の gate を承認する
$dw-phase-tournament-flow next     # 承認済み gate を次へ進める
$dw-phase-tournament-flow status   # completion marker を回収し ready phase を起動する
$dw-phase-tournament-flow complete phaseN  # 統合確認済み phase を完了にする
```

router はこの skill の `scripts/workflow.py` 自身を実行します。別 skill の
workflow script へ委譲してはいけません。

## Artifact layout

実装を開始する前に、phase ごとの設計成果物を必ず作成・レビュー・承認します。
phase が `phase1`、`phase2` のように確定したら、次を作成します。

```text
.dev-workflow-tournament/
├── CURRENT_STEP.md
├── state.json
├── 00_context.md
├── 01_acceptance_contract.md
├── 02_phase_design.md
├── 03_traceability.md
├── phases/
│   └── phaseN/
│       ├── 01_definition.md
│       ├── 02_blackbox_test_design.md
│       ├── 03_risk_assessment.md
│       └── 04_validation_plan.md
└── reports/
    ├── phaseN-review.md
    └── final-report.md
├── requests/                 # phase ごとの native subagent 依頼
└── completion/               # subagent の終了 marker
```

`02_blackbox_test_design.md` はこの skill が作成する正式な成果物です。各リスク
には `RISK-*`、テスト条件には `TC-*`、受入条件には `AC-*`、検証条件には
`VM-*` の安定した ID を付けます。最低限、次を記録します。

- 受入条件との対応、Impact、Likelihood、Uncertainty、Base Risk、Priority
- 前提データ、操作・シナリオ、期待される外部観測結果、test oracle
- 回帰範囲、手動確認、未実行 (`NOT RUN`) の理由、残余リスク

実装後に初めて test design を作ってはいけません。実装後の blackbox review は
既存設計を実装結果に照合し、`03_traceability.md` と phase report の PASS /
FAIL / NOT RUN を更新します。

## State machine

次の順序を崩しません。

```text
context
  -> acceptance-contract
  -> phase-design
  -> per-phase design (definition + blackbox + risk + validation)
  -> design approval
  -> implementation wave
  -> verification and review
  -> integration
  -> final approval
```

各段階は `WORK -> REVIEW -> APPROVED` の gate を持ちます。`approve` なしに
次の段階へ進めません。設計 gate が未承認なら、実装 agent、worktree、candidate
を起動してはいけません。

### Design gates

1. `00_context.md` に repository root、branch、HEAD、dirty files、依頼範囲、
   制約を記録する。
2. `01_acceptance_contract.md` に Goal、Non-goals、Scope、`AC-*`、互換性、
   優先リスク、`VM-*`、前提と未解決事項を記録する。
3. `02_phase_design.md` に phase ごとの責務、Phase Type、依存、完了条件、
   Impact、Likelihood、Uncertainty、Blast Radius、Reversibility、Validation
   Confidence、Implementation Mode を記録する。各 `## Phase N:` セクションには
   必ず phase 固有の `### Acceptance Criteria` を置き、`AC-PN-*`、Expected
   Result、Evidence を記載する。phase の受入条件を global contract にだけ
   書いて済ませてはいけない。
4. phase ごとに4つの設計成果物を作成し、`03_traceability.md` で global の
   `AC-*`、phase 固有の `AC-PN-*`、`VM-*` を phase、test condition、evidence
   に結び付ける。

### Contract and delivery boundary

仕様が標準、公開インターフェース、形式、互換性などの**明示的な外部契約**を
指定する場合、受入契約にはその契約を満たす実装上の根拠と、境界・不正入力を
扱う `AC-*` / `TC-*` を記載します。見かけ上動作する、より広い解釈を契約準拠と
みなしてはいけません。破壊的操作では、拒否時に副作用を起こさないことまで
oracle に含めます。

配布可能な CLI、ライブラリ、プラグイン、サービスの phase では、成果物名、公開
module/package 名、install/build target、利用者が通る入口を acceptance contract と
traceability に含めます。単体の内部 API が動くだけでは配布要件を満たしません。

phase の設計が曖昧、oracle が定義不能、または acceptance criterion が検証
不能な場合は実装に進まず、`Assumptions and Open Questions` に記録して人間の
判断を求めます。

### Implementation and tournament

承認済みで依存が解決した phase だけを実装します。ready phase は最大3件まで
同時に起動し、依存関係のない phase は同じ implementation wave で並列に進めます。
各 phase は専用 worktree で作業し、caller root を変更しません。実装 agent には full PRD ではなく、
対象 phase の definition、blackbox 条件、validation plan、制約、completion
marker を渡します。

- routine phase は単独実装し、自己レビューと共通 validation を行う。
- Impact が High、Uncertainty が High、外部・永続化・認証・決済・migration
  などを含む phase、または設計候補が複数ある phase は tournament にする。
- tournament は独立 candidate を比較し、実行済み evidence、受入条件、回帰
  リスク、変更範囲で winner を選ぶ。比較には、外部契約の境界条件、実際の
  配布入口を通る critical flow、関連する異常状態と部分失敗を含める。
  candidate 比較は
  `reports/phaseN-review.md` に残す。
- 実装 agent は commit、push、PR 作成を行わない。統合前に branch、worktree、
  diff、tracked/untracked、validation、caller-root boundary を確認する。
- `status` は completion marker を回収し、成功した phase を `READY_TO_COMMIT`
  にします。統合と検証後、`complete phaseN` を実行すると、その phase に依存
  する次の ready phase が自動的に起動します。

### Review boundary

既存 skill を呼び出せるのは review 目的だけです。変更内容に応じて次を
独立 reviewer として使えます。

- `security-review`, `privacy-review`
- `migration-review`, `data-integrity-review`, `concurrency-review`
- `performance-review`, `observability-review`, `accessibility-review`
- `test-quality-review`, `architecture-review`, `change-impact-review`,
  `review-finding-validator`

これらは設計・実装を進める owner ではありません。reviewer の指摘は
`phaseN-review.md` に記録し、修正は実装 role で行ってから該当 validation と
review を再実行します。blackbox の設計と acceptance traceability の更新は
この skill 自身が行います。

## Completion gate

phase 完了には次をすべて満たします。

- 全 applicable `AC-*` が PASS、または明示的な `NOT RUN` と残余リスクを持つ。
- P0/P1 の blackbox 条件に実行済み evidence がある。
- 外部に配布・起動される成果物では、install/build 済みの成果物を利用者と同じ
  入口から起動する critical-flow E2E evidence がある。内部 API / help / version
  だけの確認は代替にしない。
- 外部契約と破壊的操作では、境界条件や拒否時の安全性を示す evidence がある。
  例外的な実行状態の扱いも仕様・evidence のどちらかで明示する。
- 実装、テスト、検証、review finding が criterion ID に追跡できる。
- 依存 phase の完了、統合後の回帰テスト、caller-root boundary を確認する。
- 未実行 command は成功扱いにせず、理由を残す。

全体完了時は `reports/final-report.md` に requirements、設計、phase 別の mode と
risk、blackbox/whitebox coverage、branch/worktree/commit、validation 結果、
review finding、残余リスク、最終判定 (`PASS` / `PASS WITH RISKS` / `FAIL`) を
記録します。
