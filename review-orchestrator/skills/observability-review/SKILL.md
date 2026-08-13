---
name: observability-review
description: Review logging, metrics, tracing, alerts, health checks, and diagnosability for changed production behavior.
---

# Observability Review

変更された本番挙動を、検知・切り分け・復旧できるかレビューする。ログを増やすこと自体を目的にしない。

## Workflow

1. 変更された重要な workflow、failure mode、SLO、利用者影響を特定する。
2. success/failure、latency、retry、queue、resource、dependency の signal を確認する。
3. trace/correlation の伝播と、ログから個別リクエストを追えるか確認する。
4. alert の条件、threshold、cardinality、actionability、noise を評価する。
5. health/readiness、graceful degradation、startup/shutdown、feature flag を確認する。
6. PII、secret、token、payload のログ漏洩と retention を確認する。

## Rules

- ログが少ないではなく、障害時に答えられない具体的な問いを示す。
- metric の高 cardinality や alert storm も対象にする。
- 既存の dashboard/alert が存在するか確認し、推測で不足としない。

## Output

```markdown
## Observability Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Failure or operational question:
- Evidence:
- Detection gap:
- Diagnosis / recovery impact:
- Suggested signal or action:

## Signal Coverage

## Privacy / Noise Concerns

## Verification After Deploy
```
