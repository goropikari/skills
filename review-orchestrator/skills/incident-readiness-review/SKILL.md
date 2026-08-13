---
name: incident-readiness-review
description: Review production changes for failure detection, diagnosis, containment, recovery, runbook, and learning readiness.
---

# Incident Readiness Review

本番障害が起きることを前提に、検知・切り分け・封じ込め・復旧・再発防止の準備をレビューする。一般的な運用論ではなく、変更に固有の失敗モードを根拠にする。

## Workflow

1. 変更による失敗モード、影響範囲、最初に壊れる境界を列挙する。
2. health check、log、metric、trace、alert が失敗を検知・識別できるか確認する。
3. feature flag、kill switch、rate limit、rollback、forward-fix の有無を確認する。
4. owner、severity、連絡経路、runbook、判断基準、復旧手順を確認する。
5. 部分障害、依存先障害、データ不整合、再起動、負荷急増時の復旧を評価する。
6. `observability-review` と `release-readiness-review` と連携し、重複を避ける。

## Output

```markdown
## Incident Readiness Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Failure mode:
- Evidence:
- Detection or recovery gap:
- Impact:
- Suggested control:
- Verification:

## Missing Alerts, Runbooks, or Owners

## Unverified Operational Assumptions
```
