SKILL_DIRS := $(sort $(patsubst %/SKILL.md,%,$(wildcard */SKILL.md)))
TARGET_SKILL_ROOTS := $(HOME)/.claude/skills $(HOME)/.agents/skills

.PHONY: default install link

default: link

install: link

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
