---
name: mutation-test-review
description: Assess whether a test suite would kill realistic code mutations and identify weak assertions, untested branches, and misleading coverage.
---

# Mutation Test Review

テストが実装を通過させるかではなく、期待動作を壊す変更を検出できるかを確認する。mutation tool の実行結果がある場合はそれを優先し、ない場合も差分から代表的な mutation を推定する。

## Workflow

1. 変更された条件、境界、戻り値、エラー、side effect を列挙する。
2. 演算子反転、条件削除、境界変更、戻り値変更、呼び出し削除の mutation を想定する。
3. 各 mutation をどの assertion が検出するか確認する。
4. 見逃される mutation を、仕様上重要な順に分類する。
5. 実装詳細に結合せず、observable behavior を検証する追加テストを提案する。
6. mutation score を単独の品質基準にせず、除外理由と blind spot を明示する。

## Output

```markdown
## Mutation Testing Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Mutation:
- Expected behavior:
- Existing test:
- Why it survives:
- Suggested assertion or test:

## Uncovered Mutation Classes

## Tool Results and Limitations
```
