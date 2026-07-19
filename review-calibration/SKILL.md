---
name: review-calibration
description: Normalize, deduplicate, and quality-check findings from multiple reviewers without performing a new broad review.
---

# Review Calibration

複数 reviewer の findings を統合し、重複・矛盾・根拠不足・severity のばらつきを整理する。新しいコードレビューを行わない。

## Workflow

1. 各 finding に stable ID を付け、元 reviewer、location、claim、severity、evidence を保持する。
2. 同じ root cause、failure mode、同じ修正で解消される finding を候補として束ねる。
3. source location と証拠を照合し、存在しない箇所や矛盾する記述を指摘する。
4. validity と severity を別々に評価する。根拠が弱い finding を severity だけで残さない。
5. 同じ問題は最も具体的で証拠の強い finding を retained finding とする。
6. reviewer 間で結論が異なる場合、勝手に平均せず、差分と追加確認方法を示す。
7. 新たな問題は検証結果と分離した New observations に置く。

## Normalization Rules

- path、line、symbol の表記を統一する。
- severity は Critical/High/Medium/Low に正規化する。
- Evidence、Impact、Action を分離する。
- 原文の意味を変えず、要約した場合は要約であることを示す。
- 重複削除で元の finding ID と reviewer を失わない。

## Output

```markdown
# Review Calibration

## Summary

- Input findings:
- Retained:
- Duplicates:
- Conflicts:
- Unsupported or incomplete:

## Calibrated Findings

### [R-1] [Severity: High] Title

- Retained from:
- Duplicate findings:
- Evidence:
- Impact:
- Recommended action:
- Confidence:

## Conflicts Requiring Decision

## Rejected / Insufficient Findings

## New Observations
```

入力 finding がなければ統合を開始せず、必要な入力を明記する。
