---
name: go-setup
description: >-
  新規の Go プロジェクトに linter (golangci-lint) と formatter (go fix) の設定を導入します。
  /go-setup [basic|standard|strict] で設定レベルを選択できます。
---

# Go Project Setup Skill

このスキルは、Go プロジェクトに `golangci-lint` の設定ファイルと、コードの近代化およびフォーマットを自動化する `Makefile` を導入します。

## 使い方

ユーザーが以下のコマンドを入力した際、本スキルに同封されている `scripts/setup.py` を実行してください。

1. `/go-setup` または `/go-setup standard`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/setup.py" standard`
   - 標準的な設定（推奨）を導入します。

2. `/go-setup basic`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/setup.py" basic`
   - 最小限のノイズに抑えた設定を導入します。

3. `/go-setup strict`
   - 実行するコマンド: `python3 "<このスキルディレクトリ>/scripts/setup.py" strict`
   - 厳格なスタイルチェックと正当性チェックを導入します。

## 生成される成果物

- `.golangci.yml`: 選択したプリセットに基づいた `golangci-lint` v2 形式の linter 設定ファイル。
  - `linters.default` は `standard` を基準にし、標準 preset では `asciicheck`, `bodyclose`, `cyclop`, `dupl`, `errcheck`, `gocritic`, `gosec`, `ineffassign`, `testifylint`, `testpackage`, `wsl_v5`, `usetesting`, `revive` を有効化します。
  - `basic` は一部の標準 linter を外し、`strict` は追加 linter を有効化します。
  - formatter は `gofumpt` と `goimports` を有効化します。
- `Makefile`: `make fmt` と `make lint` コマンドを提供します。
  - `make fmt` は `go fix` と `golangci-lint run --fix` を順番に実行します。
  - `make lint` は `golangci-lint run` を実行します。
- `AGENTS.md`: 開発時のテストガイドラインを提供します。
  - AAA pattern（Arrange・Act・Assert）でテストを構成します。
  - アサーションには `github.com/stretchr/testify` を使います。
  - テスト関数名にはテスト対象の関数名を含めます。
  - 複数ケースのテストには `t.Run` を使い、その説明に前提条件と期待値を書きます。

## 前提条件

- `go` ツールチェーンがインストールされていること。
- `golangci-lint` がインストールされていること。
