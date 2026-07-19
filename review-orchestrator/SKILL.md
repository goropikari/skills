---
name: review-orchestrator
description: Select and coordinate the smallest effective set of review skills based on a change's files, behavior, architecture, risk, and available evidence. Use for PRs, diffs, design reviews, release reviews, or requests to decide which reviews should run.
---

# Review Orchestrator

変更の文脈に応じて必要な review skill だけを選び、実行順序・省略理由・統合方法を管理する。自分で全領域をレビューしない。

## Default Mode: Adversarial Review

明示的な指定がない限り、すべての review を敵対的レビューとして実行する。これは作者や設計者を攻撃することではなく、変更が失敗すると仮定して反例を探すレビューである。

- 仕様、入力、権限、データ、外部サービス、時刻、並行実行、deploy 状態を信頼せずに検証する。
- 正常系の確認より先に、境界値、異常系、悪意ある入力、部分失敗、retry、timeout、旧版との混在を調べる。
- 「通常は起きない」「呼び出し側が正しく使う」「運用で防ぐ」という前提には、成立条件と破綻時の影響を求める。
- 各 reviewer は最低1つの反例候補または、反例が成立しない根拠を確認する。
- 根拠がない安全宣言をしない。検証できない領域は安全ではなく未検証として報告する。
- 作者の意図ではなく、実際に成立する実行経路・契約・影響を評価する。

## Operating Rules

- ユーザーが明示した review は、不要に見えても実行対象に含める。
- それ以外は、変更の証拠から必要性を判断する。全 skill を機械的に実行しない。
- 変更が小さくても、データ、認証、並行処理、公開契約に関係する場合は専門 review を優先する。
- リスクが確認できない領域は、実行しない理由を記録する。未確認と無関係を混同しない。
- 各 reviewer には対象範囲と担当外の観点を明示する。
- reviewer の結果を勝手に補完しない。複数結果は review-calibration で統合し、既存 finding がある場合は review-finding-validator で妥当性を検証する。
- reviewer には「この変更が失敗するとしたら、どの前提が破綻するか」を必ず確認させる。

## Routing Workflow

1. 入力を分類する: diff/PR、設計、要件、テスト、migration、release plan、既存 review findings。
2. 変更対象を特定する: UI、API、DB、認証、非同期処理、設定、監視、deploy、テストなど。
3. 変更の影響とリスクを短く記録する。
4. 下表から必須候補を選ぶ。
5. 依存順に reviewer を実行する。
6. 2つ以上の reviewer 結果があれば review-calibration を実行する。
7. 既存 findings の妥当性確認が目的なら review-finding-validator を実行する。
8. 実行した skill、見送った skill、見送り理由を最終出力に残す。

各 reviewer の依頼には、次の敵対的レビュー指示を付ける。

1. 変更が壊れる最小の条件を探す。
2. その条件を満たす具体的な入力、状態、実行順序、consumer、deploy sequence を示す。
3. 既存の防御、テスト、契約が反例を防ぐか確認する。
4. 防げない場合は影響と severity を報告する。
5. 反例が成立しない場合は、その根拠と残る不確実性を報告する。

## Routing Matrix

| 条件                                                                     | 実行する review             |
| ------------------------------------------------------------------------ | --------------------------- |
| 既存の review report / findings が入力された                             | review-finding-validator    |
| 複数 reviewer の結果を統合する                                           | review-calibration          |
| 呼び出し元、依存サービス、設定、cache、event に影響する差分              | change-impact-review        |
| schema、migration、repository、永続化、backfill、data conversion         | data-integrity-review       |
| login、permission、tenant boundary、secret、PII、外部入力                | security-review             |
| goroutine、thread、async、queue、lock、atomic、callback、shared state    | concurrency-review          |
| HTTP/RPC、event、message、CLI、config、schema の consumer-facing change  | api-compatibility-review    |
| テストコード、fixture、mock、assertion、flaky 対策を変更                 | test-quality-review         |
| metrics、logs、tracing、health check、alert、SLO、dashboard              | observability-review        |
| deploy、rollback、feature flag、migration rollout、runbook、release plan | release-readiness-review    |
| プロダクト挙動・要件・受入条件の検証が中心                               | ta-review                   |
| 技術リスク・テスト戦略・非機能リスクが中心                               | tta-review                  |
| 設計、責務、結合、変更容易性、テスト容易性が中心                         | code-smell-review または jr |
| コメント・docstring・GoDoc が変更対象                                    | comment-review-orchestrator |

## Selection Details

### Always consider

差分やPRではまず change-impact-review の必要性を判定する。consumer、設定、永続化、外部境界がなければ、単純な局所変更として見送ってよい。

### Risk overrides

次の条件では、該当ファイル数が少なくても専門 review を選ぶ。

- 認可、個人情報、秘密情報: security-review
- データ削除、型変更、migration: data-integrity-review
- 共有状態、非同期 lifecycle、retry: concurrency-review
- 公開 API、イベント、設定契約: api-compatibility-review
- production signal や deploy 手順の変更: observability-review または release-readiness-review

### Avoiding overlap

- ta-review は利用者・要件・機能挙動に限定する。
- tta-review は技術的テストリスクと非機能リスクに限定する。
- code-smell-review / jr は設計・保守性に限定する。
- test-quality-review はテストコードの検出力・隔離性に限定する。
- セキュリティ、データ整合性、互換性の finding を一般的な smell として重複報告しない。
- コメント関連は comment-review-orchestrator に委譲する。

## Execution Order

依存関係がある場合は次の順序を基本とする。

1. change-impact-review
2. 専門 review（security / data-integrity / concurrency / api-compatibility）
3. 挙動・テスト review（ta / tta / test-quality）
4. 運用 review（observability / release-readiness）
5. review-calibration
6. review-finding-validator（既存 findings の検証、または統合後の最終確認）

独立した reviewer は並列実行してよい。専門 review の結果を受けて追加 review が必要になった場合は、追加理由を記録する。

## Output

```markdown
# Review Orchestration

## Context

- Change type:
- Scope:
- Risk signals:
- Available evidence:

## Selected Reviews

| Review | Reason | Scope | Order |
| ------ | ------ | ----- | ----- |

## Skipped Reviews

| Review | Why it was not selected |
| ------ | ----------------------- |

## Results

各 reviewer の findings を、元の severity・location・evidence を保持して掲載する。

## Calibration / Validation

- Calibration result:
- Finding validation result:
- Remaining uncertainty:

## Final Recommendation

- Approve
- Approve with comments
- Request changes
- Blocked pending evidence
```

最終 recommendation は、finding がないことではなく、敵対的に調べた範囲と未検証の前提を考慮して決める。未検証の重大な前提が残る場合は Approve ではなく Blocked pending evidence または Request changes を選ぶ。

入力が不足している場合は、確認できた範囲だけを選定し、必要な追加入力を Available evidence と Remaining uncertainty に明記する。
