SKILL_DIRS := $(sort $(patsubst %/SKILL.md,%,$(wildcard */SKILL.md)))
TARGET_SKILL_ROOTS := $(HOME)/.claude/skills $(HOME)/.agents/skills
PYTHON_FILES := $(shell git ls-files '*.py')

.PHONY: default install link copy fmt

default: copy

install: copy

link:
	@set -eu; \
	repo_dir=$$(pwd); \
	for target_root in $(TARGET_SKILL_ROOTS); do \
		mkdir -p "$$target_root"; \
		for skill in $(SKILL_DIRS); do \
			link_path="$$target_root/$$skill"; \
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
			copy_path="$$target_root/$$skill"; \
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
