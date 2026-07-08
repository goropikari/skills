import sys

# Linter presets
PRESETS = {
    "basic": ["govet", "staticcheck"],
    "standard": ["govet", "staticcheck", "unused", "errcheck", "ineffassign"],
    "strict": ["govet", "staticcheck", "unused", "errcheck", "ineffassign", "revive", "goconst", "misspell", "bodyclose"],
}

def write_golangci_yml(preset_name):
    linters = PRESETS.get(preset_name, PRESETS["standard"])

    # Build the linters list for YAML
    linters_yaml = "\n".join([f"    - {l}" for l in linters])

    # Basic structure for golangci-lint v2.
    content = f"""version: "2"

run:
  timeout: 5m

linters:
  default: none
  enable:
{linters_yaml}
  settings:
    govet:
      enable:
        - shadow
    revive:
      rules:
        - name: package-comments
          disabled: true
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
        print(f"Error: Invalid preset '{preset}'. Available: {', '.join(PRESETS.keys())}")
        sys.exit(1)

    print(f"Setting up Go project with '{preset}' preset...")
    write_golangci_yml(preset)
    write_makefile()
    print("\nSetup complete! Run 'make fmt' to modernize your project and 'make lint' to check it.")

if __name__ == "__main__":
    main()
