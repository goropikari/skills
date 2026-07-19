---
name: test-quality-review
description: Assess whether tests detect failures without brittle implementation coupling, false positives, flakiness, or hidden order dependence.
---

# Test Quality Review

テストの有無ではなく、失敗を検出する能力と保守性をレビューする。プロダクトコードの新規欠陥を広く探す skill ではない。

## Workflow

1. テスト対象の observable behavior とリスクを特定する。
2. assertion が本当に期待結果を検証しているか確認する。
3. 正常系、境界値、異常系、状態遷移、回帰ケースの不足を評価する。
4. mock、fixture、time、randomness、network、filesystem、DB の制御を確認する。
5. テスト間の順序依存、共有状態、flaky 条件、並列実行時の問題を確認する。
6. 実装詳細への過剰な結合と、実装を壊しても通る false positive を探す。
7. 最小限の追加テストまたはテスト設計を提案する。

## Exclusions

単に coverage が低い、テストが長い、mock が嫌い、といった好みだけでは報告しない。対象リスクと検出能力の関係を示す。

## Output

```markdown
## Test Quality Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Test:
- Evidence:
- Escaped failure:
- Why the test misses it:
- Suggested improvement:

## Missing Test Conditions

## Flakiness / Isolation Risks

## Suggested Verification
```
