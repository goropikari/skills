---
name: ai-auto-dev
description: >-
  Monitor the current GitHub repository for open issues labeled `auto-implement`,
  delegate each issue to a subagent that drives `dw-phase` in an issue-specific
  git worktree, run required reviews at the end of every phase, commit after each
  phase, and open a PR that closes the issue on merge.
---

# AI Auto Dev

This skill orchestrates issue-driven implementation in the current repository.
The main agent is a scheduler and reviewer of reviewer output. Subagents do the
actual development work.

## Scope

- Target only the current repository.
- Process only open GitHub issues with the `auto-implement` label.
- Handle one issue at a time.
- Use `gh` for discovery, issue inspection, commenting, and PR management.

## Startup Parameters

- Accept a `poll_interval` at startup.
- Default `poll_interval` to 5 minutes if the caller does not specify one.
- Use `scripts/poll.py` to handle polling and issue selection.
- Keep polling forever until the operator stops the skill.

## Issue Selection

1. Use `scripts/poll.py` to poll open issues with `gh issue list`.
2. Select the next issue labeled `auto-implement`.
3. Skip issues that already have a `processing` marker comment.
4. Skip issues that already have a terminal `failed` marker comment.
5. If an issue has an existing open PR or branch for the same issue number, reuse it.

## Worktree and Branch Naming

- Create one fixed worktree per issue.
- Reuse an existing worktree if it already exists.
- Name the worktree and branch with the pattern:
  - `issue-<number>-<short-english>`
- Derive `<short-english>` from the issue title or body.
- Keep `<short-english>` short and human-readable, about 3 to 5 words.
- Avoid changing the slug once the worktree or branch exists.
- Let `scripts/poll.py` derive the branch slug so the main agent does not have
  to reimplement that logic.

## Processing Flow

For each selected issue:

1. Add a `processing` comment before any development work starts.
2. Gather the issue body and the `gh issue view` / `gh issue list` output.
3. Hand the issue to a subagent with only that issue context emitted by
   `scripts/poll.py`.
4. Instruct the subagent to work in the issue-specific worktree.
5. Instruct the subagent to use `dw-phase` for the entire implementation.
6. Instruct the subagent to commit after every completed phase.
7. Instruct the subagent to keep the issue comment trail updated at phase boundaries.

## Required Review Suite

At the end of every completed phase, run review skills before allowing the next
phase to proceed.

Required reviews:

- `ta-review`
- `tta-review`
- `jr`
- `comment-review-orchestrator`

Additional reviews:

- If another review skill is clearly relevant, select it automatically.
- Prefer review coverage over minimalism.

Review handling rules:

1. The main agent decides whether each review finding is valid.
2. Only accepted findings block progress.
3. Rejected findings must be recorded in the issue or PR comments with a reason.
4. If any accepted finding remains, the subagent must fix it before the phase can continue.

## `dw-phase` Usage

- Use the standard `dw-phase` workflow for the issue worktree.
- Follow the phase progression enforced by `dw-phase`.
- Do not skip required phase steps.
- Do not let the main agent implement directly unless a subagent cannot be started.

## Phase Boundaries

At the end of each phase:

1. Run the required review suite.
2. Triage review findings.
3. Apply accepted fixes.
4. Commit the phase result.
5. Leave a phase-complete comment on the issue.

## Failure Handling

- If the subagent cannot complete the issue, mark the issue as failed.
- Leave a `failed` comment that explains the reason.
- Remove the `processing` state from consideration.
- Do not keep retrying the same failed issue automatically.

## Marker Comments

- `processing` marker: `[ai-auto-dev] processing`
- `failed` marker: `[ai-auto-dev] failed`
- Phase-complete comments should include the completed phase name and commit
  hash when available.

## Pull Request Rules

- Open or update one PR per issue.
- Include `Closes #<issue-number>` in the PR body so merge closes the issue.
- Reuse the existing PR if one already exists for the issue.
- Do not create duplicate PRs for the same issue.

## Completion

- When the PR is merged, clean up the issue worktree.
- Keep polling for the next labeled issue.
- Continue until the operator stops the skill.

## Resources

- `scripts/poll.py`: polls GitHub, filters eligible issues, derives the branch
  slug, and emits the next issue candidate as JSON.
