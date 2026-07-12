import sys

DEFAULT_LINTER_SET = "standard"

# Linter presets
PRESETS = {
    "basic": {
        "disable": ["errcheck", "ineffassign", "unused"],
        "enable": [],
    },
    "standard": {
        "disable": [],
        "enable": [],
    },
    "strict": {
        "disable": [],
        "enable": ["bodyclose", "goconst", "misspell", "revive"],
    },
}

EXCLUSION_PATHS = [
    "third_party$",
    "builtin$",
    "examples$",
]


def write_golangci_yml(preset_name):
    preset = PRESETS.get(preset_name, PRESETS["standard"])

    enabled_linters = preset["enable"]
    disabled_linters = preset["disable"]
    enable_yaml = "\n".join([f"    - {l}" for l in enabled_linters])
    disable_yaml = "\n".join([f"    - {l}" for l in disabled_linters])
    exclusion_paths_yaml = "\n".join([f"      - {path}" for path in EXCLUSION_PATHS])

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
    print(
        "\nSetup complete! Run 'make fmt' to modernize your project and 'make lint' to check it."
    )


if __name__ == "__main__":
    main()
