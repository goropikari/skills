---
name: security-review
description: Review changed code for concrete authentication, authorization, input handling, secret, privacy, and abuse risks.
---

# Security Review

差分に起因する具体的なセキュリティ・プライバシーリスクをレビューする。攻撃経路と影響をコード上の根拠で示す。

## Workflow

1. 信頼境界、資産、攻撃者の権限、入力源、出力先を特定する。
2. 認証、認可、tenant/resource boundary、session、CSRF、rate limit を確認する。
3. 入力検証、query/command/template、path、URL、redirect、serialization を追跡する。
4. secret、PII、token、error、log、metrics、backup への露出を確認する。
5. retry、replay、競合、権限昇格、SSRF、path traversal、injection の条件を確認する。
6. middleware、validation、permission helper が全経路を覆うか検証する。

## Rules

- 脆弱性名だけで finding にしない。入力から影響までの経路を示す。
- 脅威モデルや仕様が不明なら、前提を明示して未検証にする。
- 秘密情報や攻撃手順を不要に出力へ再掲しない。
- scanner 未実行の結果を検出済みと表現しない。

## Output

```markdown
## Security Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Attack precondition:
- Evidence:
- Impact:
- Exploitability:
- Suggested mitigation:
- Verification:

## Assumptions and Unverified Risks

## Security Checks Not Run
```
