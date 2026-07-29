---
name: dw-phase-parallel
description: >-
  dw-phase のレビュー済み phase 設計を入力に、依存関係のない phase を別 worktree・別 agent で並列実装し、phase ごとのレビューと PR 準備を管理します。
---

# DW Phase Parallel

`dw-phase` の Global Step 1 が `REVIEWED` になった後に使用する、phase 単位の並列実装オーケストレーターです。`dw-phase` の state は変更せず、`.dev-workflow-phase-parallel/` に独自 state を保存します。

## Commands

- `$dw-phase-parallel`: 初期化済みなら状態表示、未初期化なら依存グラフを検証して初期化
- `$dw-phase-parallel next`: ready phase を最大3件（`--max-parallel` で変更可）まで起動
- `$dw-phase-parallel status`: agent の完了を確認し、次の ready phase を起動
- `$dw-phase-parallel review` / `approve`: 現在のレビュー待ち状態を管理
- `$dw-phase-parallel switch light|parallel`: agent 停止中かつ安全な境界で mode を変更

agent コマンドは `--agent-cmd` または `DW_PHASE_PARALLEL_AGENT_CMD` で指定します。agent は commit、push、PR 作成を行いません。ユーザーが Git 操作を行った後、`status` / `next` が branch と PR 状態を同期します。

phase branch は `phase/<phase-id>-<slug>`、worktree は `.worktrees/phase/<phase-id>-<slug>` です。tracked の未 commit 変更が親 worktree にある場合は開始しません。
