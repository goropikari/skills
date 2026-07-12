# ai-auto-dev の bin スクリプト

このディレクトリには、issue 監督フロー用の実行ファイルを置いています。

## スクリプト

- `ai-auto-dev-supervisor`: GitHub issue のコメントを source of truth にして、1 件ずつ claim して worker を監督します。
- `ai-auto-dev-worker`: supervisor から渡された issue 情報を使って `codex exec` を実行し、PR まで作成します。PR body は Markdown として読みやすい形に整え、リポジトリに PR template があればそれを雛形として使います。
- `ai-auto-dev-worker-light`: `dw-phase-light` を使う worker 版です。各 phase の完了時のみレビューを挟みます。PR body の整形ルールと PR template の扱いは通常 worker と同じです。
- 新規 issue の worktree は最新の `origin/main` を起点に作成します。
- PR 作成だけ失敗した場合は `resume_mode=pr` で worker を再起動し、実装済みの worktree から PR だけを作り直します。
- 各 phase 完了時には worker が `ta-review`、`tta-review`、`jr`、`comment-review-orchestrator` を実行してから次の phase に進みます。
- これらの review が生成する `docs/reviews/` 配下の Markdown は診断用の一時成果物として扱い、PR や commit に含めません。
- 作成済み PR にコメントが付いたら、worker がそのコメントに応答し、必要なら `AI からの返信:` を含むコメントを返します。
- 人間の判断が必要な場合は、AI がその旨を PR コメントに明記します。
- `AI_AUTO_DEV_SUPERVISOR_STATE_DIR` の state file は制御用ではなく、現在の issue / PR 状態を人間が読み取るためのスナップショットとして扱います。

## 使い方

このディレクトリを `PATH` に通してから、次のように実行します。

```bash
ai-auto-dev-supervisor --worker-cmd ai-auto-dev-worker
ai-auto-dev-supervisor --worker-cmd ai-auto-dev-worker-light
```

よく使うオプション:

```bash
ai-auto-dev-supervisor --interval 120 --stale-after 1800 --max-restarts 2 --worker-cmd ai-auto-dev-worker
ai-auto-dev-supervisor --interval 120 --stale-after 1800 --max-restarts 2 --worker-cmd ai-auto-dev-worker-light
ai-auto-dev-supervisor --once
```

## 環境変数

Supervisor 側:

- `AI_AUTO_DEV_SUPERVISOR_STATE_DIR`: supervisor のスナップショットを保存するディレクトリ。既定値: `/tmp`
- `--reset-state`: この repo の cached state を消してから選定し直します。

Worker 側:

- `AI_AUTO_DEV_CODEX_BIN`: 実行する Codex バイナリ。既定値: `codex`
- `AI_AUTO_DEV_CODEX_COLOR`: Codex に渡す色設定。既定値: `auto`
- `AI_AUTO_DEV_CODEX_ARGS`: `codex exec` に追加する引数
- `AI_AUTO_DEV_BYPASS_APPROVALS`: `1` を設定すると `--dangerously-bypass-approvals-and-sandbox` を Codex に渡します

PR は worker が作成し、supervisor は issue コメントの `"[ai-auto-dev] pr ready: ..."` を見て PR tracking に切り替えます。
`git config --get github.user` に設定された login と一致する PR だけを監視対象にします。
worker が変更を入れたあと、supervisor は該当 branch を `git push` して remote に反映します。
PR コメント対応モードでは worker が Codex の応答を `gh pr comment` で投稿します。
issue の情報が少なすぎる場合は、supervisor が issue comment で確認質問を返して保留します。
PR template は `.github/pull_request_template.md`、`.github/PULL_REQUEST_TEMPLATE.md`、または `.github/PULL_REQUEST_TEMPLATE/` 配下の最初のテンプレートを優先して使います。
PR body は escaped `\n` をそのまま出さず、見出し・箇条書き・空行を使った Markdown として書くよう worker に指示します。

supervisor は次の環境変数で issue コンテキストも worker に渡します。

- `AI_AUTO_DEV_REPO_ROOT`
- `AI_AUTO_DEV_REPO_NAME`
- `AI_AUTO_DEV_ISSUE_NUMBER`
- `AI_AUTO_DEV_ISSUE_TITLE`
- `AI_AUTO_DEV_ISSUE_BODY`
- `AI_AUTO_DEV_ISSUE_URL`
- `AI_AUTO_DEV_BRANCH_NAME`
- `AI_AUTO_DEV_SLUG`
- `AI_AUTO_DEV_EXISTING_BRANCH`
- `AI_AUTO_DEV_EXISTING_PR_URL`
