---
name: data-integrity-review
description: Review database, migration, persistence, and recovery changes for data loss, corruption, compatibility, and idempotency risks.
---

# Data Integrity Review

DB、migration、永続化、データ変換の変更を、データの正確性・完全性・復旧可能性の観点だけでレビューする。

## Workflow

1. 変更前後の schema、制約、型、default、index、enum、nullable を比較する。
2. 既存データ、新規データ、古いアプリと新しいアプリの組み合わせを確認する。
3. transaction 境界、部分失敗、retry、重複実行、並行更新、ordering を追跡する。
4. migration の実行時間、ロック、backfill、再実行性、rollback または forward-fix を評価する。
5. 読み書きコード、repository、cache、event、fixture、backup/restore への影響を調べる。
6. データ損失・破損の具体的な条件がある場合だけ finding にする。

## Checkpoints

- destructive change と保存期間
- null/default と既存行
- unique / foreign key / check 制約
- idempotency と重複イベント
- atomicity と整合性
- rollback 時の新旧 schema 互換性
- backfill の検証、監視、停止条件
- timezone、精度、丸め、文字コード、順序

## Output

```markdown
## Data Integrity Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Evidence:
- Failure condition:
- Integrity impact:
- Recovery / rollback impact:
- Suggested test or action:

## Migration and Compatibility Matrix

## Missing Verification
```

不明な仕様は欠陥と断定せず、必要な確認事項として分離する。
