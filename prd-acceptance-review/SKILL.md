---
name: prd-acceptance-review
description: Verify that a completed implementation, pull request, release candidate, or other final deliverable satisfies every testable acceptance criterion in a PRD. Use when checking implementation completion, release readiness against a PRD, or whether acceptance criteria are proven by code, tests, and observable behavior.
---

# PRD Acceptance Review

## Mission

判定済みの成果物が PRD の受け入れ条件を満たすかを、実装・テスト・実行結果・設定・画面や API の観測可能な挙動で検証する。実装が「それらしく見える」ことだけでは合格にせず、各条件に追跡可能な証拠を付ける。

## Workflow

1. **Test basis を確定する**
   - PRD の場所を特定する。候補はユーザー指定のファイル、`docs/prd.md`、`prd.md`、関連する issue/spec である。
   - 受け入れ条件を原文のまま番号付きで抽出する。機能要件、非機能要件、制約、リリース条件に埋もれた検証可能な条件も拾う。
   - 対象成果物を確定する。差分、実装ファイル、設定・migration、テスト、実行中のサービス、生成物を確認し、対象外の既存変更を混ぜない。

2. **各条件を検証可能な単位に分解する**
   - Given/When/Then、入力、前提状態、期待結果、観測方法に変換する。
   - 正常系だけでなく、境界値、空値・不正値、権限、状態遷移、失敗・再試行、既存機能への回帰を必要に応じて含める。
   - 条件が曖昧、矛盾、または観測不能なら、勝手に補完せず `BLOCKED` として不足を記録する。

3. **証拠を集める**
   - まず既存の focused test、integration/E2E test、lint/type check、build、migration check を実行する。
   - 必要なら API/UI を実際に操作し、入力と出力、HTTP status、画面状態、ログ、DB/生成物など観測可能な結果を確認する。
   - 実行不能な場合は、原因（依存サービス、認証、環境変数、fixture、ツール不足など）を明記する。未実行を成功扱いにしない。
   - コード読解は補助証拠として使い、ユーザーから見える条件は可能な限り実行結果で裏付ける。

4. **判定する**
   - `PASS`: 条件を満たし、再現可能で十分な証拠がある。
   - `FAIL`: 検証した結果、期待結果を満たさない、または明確な実装欠陥がある。
   - `BLOCKED`: 条件または環境の不足により、合否を信頼できる形で判定できない。
   - `N/A`: PRD と成果物の関係を確認したうえで、明示的に対象外と判断できる。理由を必ず書く。
   - 重要な条件が一つでも `FAIL` または `BLOCKED` なら、全体を `NOT ACCEPTED` とする。全条件が `PASS`（または根拠付き `N/A`）のときだけ `ACCEPTED` とする。

5. **回帰と未記載のリスクを確認する**
   - 変更された共有 API、データ形式、権限、設定、依存サービス、既存ユーザーフローへの影響を確認する。
   - PRD にない重大な挙動差分があれば、受け入れ条件の判定とは分けて「追加リスク」として報告する。

## Evidence Rules

- 各条件に、確認したファイル・テスト名・コマンドと結果、または実行時の観測結果を紐付ける。
- 「テストがある」だけでは不十分。テストが対象条件の期待結果を実際にアサートしているか確認する。
- 弱いモック、常に成功するスタブ、実装詳細だけを確認するテスト、曖昧な snapshot は単独でユーザー向け条件の証拠にしない。
- 失敗を隠すためにテストを変更・削除したり、検証を通すだけの実装変更をしたりしない。ユーザーが修正を依頼していない限り、レビューと修正提案に留める。
- PRD に明確な受け入れ条件がない場合は、合格判定を推測せず、`BLOCKED` として不足を報告する。

## Output

レビュー結果は、ユーザー指定の出力先がなければ `docs/reviews/prd-acceptance-review.md` に保存する。既存ファイルを更新する場合は、今回の対象と実行日時を明記し、無関係なレビュー内容を壊さない。

```markdown
# PRD Acceptance Review

- PRD:
- Deliverable:
- Overall: ACCEPTED / NOT ACCEPTED
- Reviewed at:

## Acceptance Criteria Matrix

| ID   | Acceptance criterion | Status                | Evidence                                | Notes |
| ---- | -------------------- | --------------------- | --------------------------------------- | ----- |
| AC-1 | ...                  | PASS/FAIL/BLOCKED/N/A | command, test, file, or observed result | ...   |

## Blocking Findings

### [FAIL/BLOCKED] AC-...

- Expected:
- Actual or missing evidence:
- Risk:
- Required action:

## Additional Risks

## Executed Checks

## Assumptions and Open Questions

## Recommendation

ACCEPTED / NOT ACCEPTED — one-sentence rationale.
```

## Review Style

判定と証拠を分離し、推測・確認済み事実・環境起因の未確認を明確に区別する。指摘は受け入れ条件の ID、期待結果、実際の結果、再現手順、影響、必要な対応を具体的に書く。コード品質や設計の指摘は、受け入れ条件や観測可能なリスクに関係する場合だけ追加する。
