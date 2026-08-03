---
name: migration-review
description: Review database, schema, data-format, configuration, and rollout migrations for compatibility, safety, idempotency, and rollback risks.
---

# Migration Review

既存利用者や旧バージョンが残る期間を前提に、データ・schema・設定の移行が安全に進み、失敗時に復旧できるかを確認する。永続化の詳細な整合性は `data-integrity-review` と連携する。

## Workflow

1. 移行前後の schema、データ、設定、コードの互換性を整理する。
2. expand/contract、dual read/write、バックフィル、段階 rollout の順序を確認する。
3. lock、transaction、所要時間、負荷、オンライン実行時の影響を確認する。
4. 部分実行、再実行、並行実行、中断時の idempotency を確認する。
5. validation、checkpoint、監視、停止条件、rollback または forward-fix を確認する。
6. 旧クライアント・旧 worker・複数リージョンの共存期間を確認する。

## Output

```markdown
## Migration Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Migration step:
- Evidence:
- Failure scenario:
- Impact:
- Mitigation or rollout change:
- Verification:

## Compatibility Matrix

## Rollback and Recovery Gaps
```
