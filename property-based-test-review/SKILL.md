---
name: property-based-test-review
description: Review test designs for properties, generators, invariants, boundary coverage, and stateful or combinatorial behavior that example tests may miss.
---

# Property-Based Test Review

例示ベースのテストだけでは漏れやすい入力空間・状態遷移・不変条件を特定し、property-based testing が有効な箇所と設計をレビューする。

## Workflow

1. 対象の observable behavior、不変条件、保存則、可逆性、単調性を特定する。
2. 入力の型、制約、境界、組み合わせ、縮小可能な失敗例を整理する。
3. generator が有効値・無効値・重要な境界ケースを生成できるか確認する。
4. stateful workflow、sequence、並行イベント、時間、再試行の性質を評価する。
5. property が実装の再記述になっていないか、false positive にならないか確認する。
6. seed、shrinking、再現性、実行時間、既存テストとの役割分担を確認する。

## Output

```markdown
## Property-Based Test Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Behavior or invariant:
- Missing input/state space:
- Evidence:
- Escaped failure:
- Suggested property and generator:

## Candidate Properties

## Generator and Reproducibility Risks
```
