---
name: architecture-review
description: Review architecture and design changes for responsibility boundaries, dependency direction, coupling, extensibility, and operational consequences.
---

# Architecture Review

変更がシステムの境界、責務、依存関係をどう変えるかを確認し、将来の変更容易性と運用可能性を損なう具体的な設計リスクを報告する。

## Workflow

1. 変更対象と、その呼び出し元・依存先・データ境界を整理する。
2. 各責務の所有者、依存方向、公開境界、ライフサイクルを確認する。
3. 高凝集・低結合、変更理由の分離、循環依存、隠れた共有状態を評価する。
4. エラー、トランザクション、設定、並行性、観測性の境界を確認する。
5. 既存の拡張点を壊さず、変更の影響範囲が局所化されているか確認する。

## Exclusions

単なる好みやパターン名の違いは報告しない。具体的な変更シナリオ、障害、または保守コストに結びつける。

## Output

```markdown
## Architecture Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Location:
- Evidence:
- Failure or change scenario:
- Impact:
- Suggested design direction:

## Dependency and Boundary Notes

## Assumptions
```
