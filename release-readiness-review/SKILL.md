---
name: release-readiness-review
description: Assess rollout, migration, rollback, configuration, monitoring, and post-deploy readiness for a change.
---

# Release Readiness Review

リリース単位で、安全に deploy、監視、rollback、復旧できるかをレビューする。コード品質の一般論は扱わない。

## Workflow

1. 変更の release unit、依存サービス、migration、config、secret、feature flag を特定する。
2. deploy order と新旧 version の同時稼働を確認する。
3. pre-deploy checks、backup、migration guard、canary/gradual rollout を確認する。
4. post-deploy verification、metrics、logs、alerts、停止条件を確認する。
5. rollback が可能か、不可なら forward-fix とデータ復旧手順があるか確認する。
6. runbook、owner、連絡経路、保守時間帯、顧客通知の不足を評価する。

## Decision Rules

根拠のないチェックリスト不足は報告しない。rollback 不可は影響と代替復旧策を確認してから評価する。未確定の運用情報は質問として分離する。

## Output

```markdown
## Release Readiness Summary

## Blocking Findings

### [Severity: Critical/High/Medium/Low] Title

- Evidence:
- Release risk:
- Failure / rollback consequence:
- Required action:
- Verification / owner:

## Rollout Plan Gaps

## Post-Deploy Verification

## Open Questions

## Final Recommendation

- Ready
- Ready with conditions
- Not ready
```
