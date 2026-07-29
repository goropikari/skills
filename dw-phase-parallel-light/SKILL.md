---
name: dw-phase-parallel-light
description: >-
  dw-phase のレビュー済み phase 設計を入力に、依存関係のない phase を別 worktree・別 agent で並列に一括実装し、自己レビューとテスト後に PR 準備状態にします。
---

# DW Phase Parallel Light

`dw-phase-parallel` と同じ共有 state・worktree・依存グラフを使います。phase ごとの途中レビューは行わず、agent が設計・実装・テスト・自己レビューを一括で実行します。

## Commands

- `$dw-phase-parallel-light`: 初期化済みなら状態表示、未初期化なら検証して初期化
- `$dw-phase-parallel-light next`: ready phase を最大3件まで起動
- `$dw-phase-parallel-light status`: agent の完了を確認し、次の ready phase を起動
- `$dw-phase-parallel-light switch parallel`: 安全な境界でレビュー型へ変更

agent コマンドは `--agent-cmd` または `DW_PHASE_PARALLEL_AGENT_CMD` で指定します。agent は commit、push、PR 作成を行いません。完了後は `READY_TO_COMMIT` となり、ユーザーが Git 操作を行います。
