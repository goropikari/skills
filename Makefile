SKILL_DIRS := $(sort $(filter-out deprecated/%,$(patsubst %/SKILL.md,%,$(wildcard */SKILL.md) $(wildcard implementation/*/SKILL.md) $(wildcard quality/*/SKILL.md) $(wildcard reviews/*/SKILL.md))))
TARGET_SKILL_ROOTS := $(HOME)/.claude/skills $(HOME)/.agents/skills
PYTHON_FILES := $(shell find . -path './.git' -prune -o -path './deprecated' -prune -o -name '*.py' -print)

.PHONY: default install copy install-hooks fmt lint

default: copy

install: copy

install-hooks:
	@git config core.hooksPath .githooks
	@printf 'git hooks enabled from .githooks\n'

copy:
	@python3 scripts/install.py

fmt:
	dprint fmt
	@if [ -n "$(PYTHON_FILES)" ]; then \
		ruff format $(PYTHON_FILES); \
	fi

lint: fmt
	gitleaks detect --no-banner --redact --source .
