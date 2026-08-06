SKILL_DIRS := $(sort $(filter-out deprecated/%,$(patsubst %/SKILL.md,%,$(wildcard */SKILL.md) $(wildcard reviews/*/SKILL.md))))
TARGET_SKILL_ROOTS := $(HOME)/.claude/skills $(HOME)/.agents/skills
PYTHON_FILES := $(shell git ls-files '*.py')

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
	@set -eu; \
	repo_dir=$$(pwd); \
	for target_root in $(TARGET_SKILL_ROOTS); do \
		mkdir -p "$$target_root"; \
		for skill in $(SKILL_DIRS); do \
			skill_name=$$(basename $$skill); \
			copy_path="$$target_root/$$skill_name"; \
			source_path="$$repo_dir/$$skill"; \
			rm -rf "$$copy_path"; \
			cp -R "$$source_path" "$$copy_path"; \
			printf 'copy %s -> %s\n' "$$source_path" "$$copy_path"; \
		done; \
	done

fmt:
	dprint fmt
	@if [ -n "$(PYTHON_FILES)" ]; then \
		ruff format $(PYTHON_FILES); \
	fi

lint: fmt
	gitleaks detect --no-banner --redact --source .
