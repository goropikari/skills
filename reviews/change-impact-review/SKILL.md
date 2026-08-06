---
name: change-impact-review
description: Trace changed behavior across callers, data, APIs, configuration, and operations. Use for diffs, PRs, migrations, and implementation plans when regression or hidden dependency risk matters.
---

# Change Impact Review

変更による影響範囲をレビューする。ソースコードを変更せず、明確な根拠のある影響だけを報告する。

## Workflow

1. 変更の目的、変更された契約、変更された状態を特定する。
2. 呼び出し元、設定、環境変数、feature flag、DB schema、migration、fixture を検索する。
3. API、イベント、キュー、キャッシュ、ファイル形式、CLI、外部サービスの利用者を確認する。
4. エラー、retry、timeout、transaction、権限、ログ、metrics、alert、deploy order への影響を確認する。
5. 影響先ごとに互換性、回帰、ロールバック可否を判断する。
6. 利用者や仕様が確認できない推測は未検証として扱う。

## Focus

- 直接・間接の consumer
- 入出力、schema、状態遷移、default 値
- 入れ替え中の新旧バージョン
- migration、cache invalidation、非同期処理
- テスト、ドキュメント、運用手順の追随漏れ

## Output

```markdown
## Change Impact Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Evidence:
- Affected components:
- Risk:
- Compatibility / rollback:
- Suggested action:

## Unchecked Impact Areas

## Final Recommendation
```

影響がなければ「確認できる影響はない」と明記し、検索範囲と制約を書く。
