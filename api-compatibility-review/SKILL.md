---
name: api-compatibility-review
description: Check API, event, CLI, configuration, and schema changes for backward compatibility and contract risks.
---

# API Compatibility Review

HTTP/RPC API、event、message、CLI、設定、schema の利用者向け契約をレビューする。内部実装の好みは扱わない。

## Workflow

1. 変更前後の request、response、error、event、CLI、config の契約を抽出する。
2. producer/consumer、SDK、fixture、schema、documentation の利用箇所を検索する。
3. field の追加・削除・型変更、required 化、default、ordering、pagination、error code を確認する。
4. 新旧 client/server の同時稼働と rollout 順序を検討する。
5. versioning、deprecation、feature negotiation、migration、rollback を評価する。
6. 破壊的変更は具体的な既存 consumer と失敗形を示す。

## Checkpoints

- backward / forward compatibility
- unknown field と tolerant reader
- nullable、enum、precision、timezone
- idempotency、retry、ordering
- auth scope、rate limit、error semantics
- CLI exit code、config default、環境変数

## Output

```markdown
## Compatibility Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Contract change:
- Affected consumer:
- Evidence:
- Failure mode:
- Rollout / versioning risk:
- Suggested action:

## Compatibility Matrix

## Required Consumer Verification
```

consumer が確認できない場合は、破壊的と断定せず未検証として記載する。
