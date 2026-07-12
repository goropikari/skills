# ai-auto-dev の bin スクリプト

このディレクトリには、issue 監督フロー用の実行ファイルを置いています。

## スクリプト

- `ai-auto-dev-supervisor`: GitHub issue を監視し、1 件ずつ claim して worker を監督します。
- `ai-auto-dev-worker`: supervisor から渡された issue 情報を使って `codex exec` を実行し、PR まで作成します。
- `ai-auto-dev-worker-light`: `dw-phase-light` を使う worker 版です。各 phase の完了時のみレビューを挟みます。
- 新規 issue の worktree は最新の `origin/main` を起点に作成します。
- PR 作成だけ失敗した場合は `resume_mode=pr` で worker を再起動し、実装済みの worktree から PR だけを作り直します。
- 各 phase 完了時には worker が `ta-review`、`tta-review`、`jr`、`comment-review-orchestrator` を実行してから次の phase に進みます。
- 作成済み PR にコメントが付いたら、worker がそのコメントに応答し、必要なら `AI からの返信:` を含むコメントを返します。
- 人間の判断が必要な場合は、AI がその旨を PR コメントに明記します。

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

- `AI_AUTO_DEV_SUPERVISOR_STATE_DIR`: supervisor の状態を保存するディレクトリ。既定値: `/tmp`
- `--reset-state`: この repo の cached state を消してから選定し直します。

Worker 側:

- `AI_AUTO_DEV_CODEX_BIN`: 実行する Codex バイナリ。既定値: `codex`
- `AI_AUTO_DEV_CODEX_COLOR`: Codex に渡す色設定。既定値: `auto`
- `AI_AUTO_DEV_CODEX_ARGS`: `codex exec` に追加する引数
- `AI_AUTO_DEV_BYPASS_APPROVALS`: `1` を設定すると `--dangerously-bypass-approvals-and-sandbox` を Codex に渡します

PR は worker が作成し、supervisor は `Closes #<issue-number>` を含む PR だけを完了扱いにします。
PR が見つからない状態で worker が終わったときは、supervisor が PR-only mode に切り替えて再試行します。
`git config --get github.user` に設定された login と一致する PR だけを監視対象にします。
worker が変更を入れたあと、supervisor は該当 branch を `git push` して remote に反映します。
PR コメント対応モードでは worker が Codex の応答を `gh pr comment` で投稿します。
issue の情報が少なすぎる場合は、supervisor が issue comment で確認質問を返して保留します。

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
