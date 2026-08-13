---
name: performance-review
description: Review code and designs for concrete latency, throughput, memory, I/O, database, and scalability risks.
---

# Performance Review

性能要件と実行経路を確認し、入力規模や同時実行数の増加で顕在化する具体的なボトルネックを探す。測定なしの印象論は finding にしない。

## Workflow

1. latency、throughput、memory、CPU、startup、容量などの対象指標と許容値を特定する。
2. 主要経路の計算量、ループ内 I/O、N+1、不要なコピー、シリアライズを追跡する。
3. DB の query、index、pagination、lock、transaction、connection pool を確認する。
4. キャッシュ、retry、queue、batch、並行性が負荷を増幅しないか確認する。
5. 大入力、同時実行、長時間運転、コールドスタートでの劣化を評価する。
6. 必要な benchmark、profiling、load test と成功基準を提案する。

## Output

```markdown
## Performance Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Workload:
- Evidence:
- Bottleneck:
- Impact:
- Suggested mitigation:
- Measurement:

## Unmeasured Risks

## Verification Plan
```
