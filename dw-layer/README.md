# dw-layer

`dw-layer` は、AI agent での開発を「全体要件定義」「レイヤー設計」「各レイヤーごとの 6 ステップ」に分け、人間のレビューを挟みながら進めるための agent skill です。

## Commands

- Codex: `$dw-layer`, `$dw-layer next`, `$dw-layer review`, `$dw-layer approve`
- Claude Code: `/dw-layer`, `/dw-layer next`, `/dw-layer review`, `/dw-layer approve`

各コマンドは `scripts/workflow.py` を実行します。

Codex と Claude Code のどちらで使っても、同じ対象プロジェクトのルートで実行すれば同じ `.dev-workflow-layer/` の状態を共有します。別ディレクトリで実行すると別の状態ディレクトリが作られるため、併用時は実行場所を揃えてください。

## State

対象プロジェクト直下の `.dev-workflow-layer/` に状態と成果物を保存します。

状態ファイル:

```text
.dev-workflow-layer/CURRENT_STEP.md
```

状態ファイルには `Step`, `Step Name`, `Target`, `Status`, `Layers` が記録されます。

## Workflow

初期ステップ:

| Step | Name                       | Target                                           |
| ---: | -------------------------- | ------------------------------------------------ |
|    0 | プロジェクト全体の要件定義 | `.dev-workflow-layer/00_project_requirements.md` |
|    1 | レイヤー設計               | `.dev-workflow-layer/01_layer_design.md`         |

レイヤー設計書には次のメタデータを必ず記載します。

```markdown
- **Layers**: 3
```

`Layers` は 1 以上 20 以下の整数です。ステップ 1 承認後の `next` で読み取られ、各レイヤーごとの 6 ステップが動的に生成されます。

各レイヤーのステップ:

1. `layerN/01_requirements.md`
2. `layerN/02_features/spec.feature`
3. `layerN/03_test_design.md`
4. 実プロジェクト内の適切なソースファイル
5. 実プロジェクト内の適切なテストファイル
6. 実プロジェクト内の適切なソースファイル
