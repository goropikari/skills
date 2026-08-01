---
name: dw-phase-parallel-light
description: >-
  dw-phase のレビュー済み phase 設計を入力に、依存関係のない phase を別 worktree・別 agent で並列に一括実装し、自己レビューとテスト後に PR 準備状態にします。
---

# DW Phase Parallel Light

`.gitignore` は変更しません。worktree や状態ディレクトリの作成に伴う ignore 設定が必要な場合も、ユーザーの明示的な指示なしには追加・更新しないでください。

`dw-phase-parallel` と同じ共有 state・worktree・依存グラフを使います。phase ごとの途中レビューは行わず、agent が設計・実装・テスト・自己レビューを一括で実行します。

実行前に `.dev-workflow-phase/CURRENT_STEP.md` を確認し、`Global Step: 1` かつ `Status: REVIEWED` でない場合は、parallel state を初期化せず `dw-phase` を先に開始します。phase 設計のレビュー・承認が完了してから、同じコマンドを再実行してください。

## Commands

- `$dw-phase-parallel-light`: 初期化済みなら状態表示、未初期化なら検証して初期化
- `$dw-phase-parallel-light next`: ready phase を最大3件まで起動
- `$dw-phase-parallel-light status`: agent の完了を確認し、次の ready phase を起動
- `$dw-phase-parallel-light switch parallel`: 安全な境界でレビュー型へ変更

light mode は native subagent を使用します。`next` / `status` が作成した `.dev-workflow-phase-parallel/requests/*.md` を読み、そこに記載された worktree で通常の subagent を起動してください。subagent は作業完了時に、依頼ファイルに記載された completion marker に `0` を書き込みます。`codex exec` や別の CLI agent は起動しません。

agent は commit、push、PR 作成を行いません。完了後は `READY_TO_COMMIT` となり、ユーザーが Git 操作を行います。
