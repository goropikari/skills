---
name: dependency-review
description: Review dependency changes for vulnerabilities, licensing, maintenance, transitive, and supply-chain risks.
---

# Dependency Review

追加・更新・削除された依存関係と、その推移依存をレビューする。既知の脆弱性だけでなく、更新可能性、ライセンス、供給網、実行時影響を確認する。

## Workflow

1. manifest、lockfile、build script、container image の変更を特定する。
2. direct/transitive dependency、取得元、固定バージョン、checksum を確認する。
3. 脆弱性、ライセンス、保守状況、リリース頻度、実績を確認する。
4. 権限、install script、runtime code、native code、ネットワークアクセスを評価する。
5. 不要な重複依存、過剰な依存、互換性やサイズへの影響を確認する。
6. scanner や advisory を実行していない場合は未確認として明示する。

## Output

```markdown
## Dependency Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Dependency:
- Evidence:
- Risk:
- Suggested action:
- Verification:

## Unverified Checks
```
