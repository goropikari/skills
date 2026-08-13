# Repository Guidelines

## Project Structure & Module Organization

This repository contains reusable Agent Skills. Each active skill normally has
a `SKILL.md`; the implementation route selector lives under
`implementation-orchestrator/`, which owns the active implementation workflow
and its internal components. The review entry point is root-level
`review-orchestrator/`, with its individual reviewer components owned beneath
that orchestrator. Some
also contain `agents/openai.yaml`, `scripts/`, or skill-specific reference
files.
Python validators and focused tests live with their owning active skill or
under the repository-level `tests/`.
The `deprecated/` tree is historical and is excluded from the Makefile’s
active skill set. Keep new shared documentation and tooling at the repository
root only when it applies across skills.

When creating a new skill or updating an existing skill, update that skill’s
`VERSION` file as part of the same change.

## Build, Test, and Development Commands

- `python3 -m pytest` — run the Python test suite.
- `make fmt` — format Markdown/configuration files with `dprint` and Python
  files with Ruff.
- `make lint` — run formatting, then scan the repository for secrets with
  `gitleaks`.
- `make install` — copy active skills into `~/.claude/skills` and
  `~/.agents/skills`.
- `make link` — create non-overwriting symlinks to the active skills.
- `make install-hooks` — enable the repository pre-commit hook.

Run commands from the repository root. Formatting tools used by CI/hooks must
be installed locally before running the corresponding checks.

## Coding Style & Naming Conventions

Use clear Markdown headings, short paragraphs, and fenced examples in
`SKILL.md` files. Match existing Japanese or English terminology within the
file being edited. Use four-space indentation for Python, descriptive
`snake_case` names for Python functions/variables, and lowercase hyphenated
directory names for skills. Keep `agents/openai.yaml` metadata aligned with
the skill’s documented purpose. Run `make fmt` before committing.

## Testing Guidelines

Tests use `pytest` and follow `test_*.py` naming. Add or update focused tests
for changes to scripts, especially workflow state transitions and subprocess
behavior; run the full suite with `python3 -m pytest` before submitting.

## Commit & Pull Request Guidelines

Recent commits use concise imperative summaries (for example, “Add …”, “Fix
…”). Keep commits focused and explain behavior changes in the body when the
summary is not enough. Pull requests should describe the affected skills,
include tests and lint/format results, link the relevant issue when one
exists, and call out any installation or workflow-state impact.
