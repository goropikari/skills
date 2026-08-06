---
name: privacy-review
description: Review changes involving personal data for collection, purpose, minimization, access, retention, logging, sharing, deletion, and privacy risk.
---

# Privacy Review

個人情報・識別子・行動データを含む変更について、データのライフサイクルと利用目的に照らして具体的なプライバシーリスクを確認する。法的適合性は管轄と組織方針を前提に判断し、断定しない。

## Workflow

1. データ項目、本人、収集元、利用目的、保存先、共有先を特定する。
2. 最小収集、目的外利用、アクセス制御、tenant 境界、暗号化を確認する。
3. log、metrics、trace、error、analytics、backup への漏えいを追跡する。
4. retention、削除、訂正、エクスポート、匿名化、バックアップ残存を確認する。
5. 同意、通知、地域移転、委託先、管理者アクセスなどの前提を確認する。
6. `security-review` と重なる場合は、攻撃経路ではなくデータ保護の観点を報告する。

## Output

```markdown
## Privacy Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Data:
- Lifecycle location:
- Evidence:
- Privacy impact:
- Suggested control:
- Verification:

## Data Flow and Retention Gaps

## Legal or Policy Assumptions
```
