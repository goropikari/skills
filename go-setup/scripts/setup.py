import sys

DEFAULT_LINTER_SET = "standard"
DEFAULT_ENABLED_LINTERS = [
    "asciicheck",
    "bodyclose",
    "cyclop",
    "dupl",
    "errcheck",
    "gocritic",
    "gosec",
    "ineffassign",
    "testifylint",
    "testpackage",
    "wsl_v5",
    "usetesting",
    "revive",
]
DEFAULT_FORMATTERS = [
    "gofumpt",
    "goimports",
]

# Linter presets
PRESETS = {
    "basic": {
        "disable": ["errcheck", "ineffassign", "unused"],
        "enable": DEFAULT_ENABLED_LINTERS,
    },
    "standard": {
        "disable": [],
        "enable": DEFAULT_ENABLED_LINTERS,
    },
    "strict": {
        "disable": [],
        "enable": [*DEFAULT_ENABLED_LINTERS, "goconst", "misspell"],
    },
}

EXCLUSION_PATHS = [
    "third_party$",
    "builtin$",
    "examples$",
    '"^sample/"',
]


def write_golangci_yml(preset_name):
    preset = PRESETS.get(preset_name, PRESETS["standard"])

    disabled_linters = preset["disable"]
    enabled_linters = [l for l in preset["enable"] if l not in disabled_linters]
    enable_yaml = "\n".join([f"    - {l}" for l in enabled_linters])
    disable_yaml = "\n".join([f"    - {l}" for l in disabled_linters])
    exclusion_paths_yaml = "\n".join([f"      - {path}" for path in EXCLUSION_PATHS])
    formatter_yaml = "\n".join(
        [f"    - {formatter}" for formatter in DEFAULT_FORMATTERS]
    )

    # Minimal golangci-lint v2 structure with the common exclusions used by the skill.
    content = f"""version: "2"

linters:
  default: {DEFAULT_LINTER_SET}
"""
    if enabled_linters:
        content += f"""  enable:
{enable_yaml}
"""
    if disabled_linters:
        content += f"""  disable:
{disable_yaml}
"""
    content += f"""  settings:
    revive:
      rules:
        - name: package-comments
          disabled: true
        - name: redundant-import-alias
          disabled: false
  exclusions:
    generated: lax
    presets:
      - comments
      - common-false-positives
      - legacy
      - std-error-handling
    paths:
{exclusion_paths_yaml}

formatters:
  enable:
{formatter_yaml}
  exclusions:
    generated: lax
    paths:
{exclusion_paths_yaml}
"""
    with open(".golangci.yml", "w") as f:
        f.write(content)
    print("Created .golangci.yml")


def write_makefile():
    content = r""".PHONY: fmt lint

fmt:
	goimports -w .
	go fix
	golangci-lint run --fix

lint:
	golangci-lint run
"""
    with open("Makefile", "w") as f:
        f.write(content)
    print("Created Makefile")


def write_agents_md():
    content = """# 開発ガイドライン

## テスト

- テストは AAA pattern（Arrange・Act・Assert）で記述する。テスト対象の準備、実行、結果の検証を分け、各段階が読み取れる構成にする。
- アサーションには `github.com/stretchr/testify` を使う。`assert` や `require` で、失敗時に意図が分かる検証を書く。
- テスト関数名にはテスト対象の関数名を含める。たとえば `CalculateTotal` のテストは `TestCalculateTotal` とする。
- 複数のケースを検証する場合は `t.Run` を使う。
- `t.Run` の説明には、そのケースの前提条件と期待値を書く。入力値だけでなく、どの条件で何が起きるべきかが分かる名前にする。

```go
import "github.com/stretchr/testify/assert"

func TestCalculateTotal(t *testing.T) {
\ttests := []struct {
\t\tname string
\t\tinput []int
\t\twant int
\t}{
\t\t{
\t\t\tname:  "商品が2件あるとき合計金額が返る",
\t\t\tinput: []int{100, 200},
\t\t\twant:  300,
\t\t},
\t}

\tfor _, tt := range tests {
\t\tt.Run(tt.name, func(t *testing.T) {
\t\t\t// Arrange
\t\t\tinput := tt.input

\t\t\t// Act
\t\t\tgot := CalculateTotal(input)

\t\t\t// Assert
\t\t\tassert.Equal(t, tt.want, got)
\t\t})
\t}
}
```
"""
    with open("AGENTS.md", "w") as f:
        f.write(content)
    print("Created AGENTS.md")


def main():
    preset = "standard"
    if len(sys.argv) > 1:
        preset = sys.argv[1].lower()

    if preset not in PRESETS:
        print(
            f"Error: Invalid preset '{preset}'. Available: {', '.join(PRESETS.keys())}"
        )
        sys.exit(1)

    print(f"Setting up Go project with '{preset}' preset...")
    write_golangci_yml(preset)
    write_makefile()
    write_agents_md()
    print(
        "\nSetup complete! Run 'make fmt' to modernize your project and 'make lint' to check it."
    )


if __name__ == "__main__":
    main()
