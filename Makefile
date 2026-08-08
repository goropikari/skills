SKILL_DIRS := $(sort $(filter-out deprecated/%,$(patsubst %/SKILL.md,%,$(wildcard */SKILL.md) $(wildcard implementation/*/SKILL.md) $(wildcard reviews/*/SKILL.md))))
TARGET_SKILL_ROOTS := $(HOME)/.claude/skills $(HOME)/.agents/skills
PYTHON_FILES := $(shell find . -path './.git' -prune -o -path './deprecated' -prune -o -name '*.py' -print)

.PHONY: default install link copy install-hooks fmt lint

default: copy

install: copy

install-hooks:
	@git config core.hooksPath .githooks
	@printf 'git hooks enabled from .githooks\n'

link:
	@set -eu; \
	repo_dir=$$(pwd); \
	for target_root in $(TARGET_SKILL_ROOTS); do \
		mkdir -p "$$target_root"; \
		for skill in $(SKILL_DIRS); do \
			skill_name=$$(basename $$skill); \
			link_path="$$target_root/$$skill_name"; \
			source_path="$$repo_dir/$$skill"; \
			if [ -e "$$link_path" ] || [ -L "$$link_path" ]; then \
				printf 'skip %s\n' "$$link_path"; \
			else \
				ln -s "$$source_path" "$$link_path"; \
				printf 'link %s -> %s\n' "$$link_path" "$$source_path"; \
			fi; \
		done; \
	done

copy:
	@python3 scripts/install.py

fmt:
	dprint fmt
	@if [ -n "$(PYTHON_FILES)" ]; then \
		ruff format $(PYTHON_FILES); \
	fi

lint: fmt
	gitleaks detect --no-banner --redact --source .
