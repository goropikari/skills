---
name: prd-to-issue
description: Convert a completed PRD Markdown file into a GitHub issue in the current repository and always attach the auto-implement label. Use when the user asks to publish a PRD as an issue, queue it for implementation, or turn a PRD draft into a tracked issue.
---

# PRD to Issue

## Overview

Use this skill after a PRD is ready to hand off to implementation and should become a GitHub issue in the current repository.

## Workflow

1. Build context first.
   - Inspect the current repository and the PRD file before creating anything.
   - Default input is `docs/prd.md` unless the user specifies another path.
   - If the PRD file is missing, ask the user where the PRD lives.
2. Derive the issue fields from the PRD.
   - Use the PRD's first top-level heading as the issue title when available.
   - If no clear title exists, ask one concise clarification question before creating the issue.
   - Use the PRD body as the issue body, preserving the structure and wording as much as practical.
3. Ensure the implementation label is present.
   - Always attach the `auto-implement` label to the issue.
   - If the repository does not already have that label, create it before issue creation.
4. Create the GitHub issue.
   - Use `gh issue create` against the current repository.
   - Include the PRD-derived title and body.
   - Include `--label auto-implement` in the create command.
   - Do not add unrelated labels unless the user explicitly asks.
5. Report the result.
   - Return the issue URL and number.
   - Mention the title used and whether the label was created or reused.

## Output Rules

- Default to publishing from `docs/prd.md`.
- Keep the issue title concise and aligned with the PRD title.
- Keep the issue body faithful to the PRD and avoid inventing new requirements.
- If the PRD is clearly incomplete, stop and ask for the missing decision rather than publishing a misleading issue.

## Suggested Issue Shape

Use this structure for the issue body when the PRD does not already provide a better one:

1. Summary
2. Problem
3. Goal
4. Scope
5. Non-goals
6. Requirements
7. Risks and open questions
8. Links to the source PRD and related notes

## Guidance

- Treat the PRD as the source of truth for implementation intent.
- Do not rewrite the PRD into a different spec unless the user asks for a summary-only issue.
- If the repository already uses a custom issue template, adapt the PRD content to that template while preserving the `auto-implement` label.
