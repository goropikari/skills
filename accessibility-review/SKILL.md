---
name: accessibility-review
description: Review user interfaces and interaction changes for keyboard, screen reader, visual, motion, input, and assistive-technology accessibility barriers.
---

# Accessibility Review

UI 変更を、障害のある利用者を含む実際の操作経路からレビューする。規格適合の断定は、対象規格・環境・実測結果がある場合に限る。

## Workflow

1. 対象画面、主要タスク、利用者、対応ブラウザ、支援技術を特定する。
2. キーボード順序、focus、操作可能な要素、ショートカット、drag/drop を確認する。
3. semantic HTML、名前・役割・状態、label、error、live region を確認する。
4. 色だけに依存しない情報、コントラスト、拡大、reflow、レスポンシブ表示を確認する。
5. 動き、点滅、時間制限、入力方式、音声・画像の代替を確認する。
6. 自動検査と手動検査を区別し、再現手順と検証環境を記録する。

## Output

```markdown
## Accessibility Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- User task:
- Barrier:
- Evidence:
- Affected users:
- Suggested fix:
- Verification method:

## Manual Checks Not Run

## Assumptions
```
