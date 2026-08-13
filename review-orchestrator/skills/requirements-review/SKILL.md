---
name: requirements-review
description: Review requirements, user stories, acceptance criteria, and proposed behavior for ambiguity, omissions, contradictions, and unverifiable outcomes.
---

# Requirements Review

実装前または変更差分に対して、要求された価値と期待動作が明確で検証可能かを確認する。実装の好みではなく、要件の欠陥による手戻りや誤実装を報告する。

## Workflow

1. 対象ユーザー、目的、スコープ、非スコープを特定する。
2. 正常系、異常系、境界値、権限、状態遷移、失敗時の振る舞いを確認する。
3. 用語、前提、入力、出力、制約、受け入れ条件の曖昧さを探す。
4. 要件間の矛盾、既存仕様との不整合、未定義の互換性を確認する。
5. 各受け入れ条件が観測可能で、テスト可能か評価する。

## Output

```markdown
## Requirements Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Requirement:
- Evidence:
- Risk:
- Clarification or acceptance criterion:

## Missing Scenarios

## Assumptions and Open Questions
```
