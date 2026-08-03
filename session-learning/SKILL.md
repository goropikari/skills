---
name: session-learning
description: Analyze a Codex session, transcript, task result, or debugging trail and extract durable, reusable lessons. Use when the user asks to review what was learned from a session, improve skills or AGENTS.md from past work, capture recurring workflow mistakes, or turn a retrospective into concrete instruction changes. Produce a concise evidence-backed report and proposed patches; edit repository guidance only when the user explicitly asks to apply the changes.
---

# Session Learning

## Purpose

Turn a completed Codex session into maintainable guidance. Separate durable rules from one-off details, identify where each lesson belongs, and give the user small, reviewable changes to `SKILL.md`, `AGENTS.md`, tests, scripts, or other project documentation.

## Inputs

Use the evidence available in this order:

1. The current conversation and any transcript or session log supplied by the user.
2. User-provided summaries, tool output, review findings, and stated corrections.
3. Relevant repository files, especially `AGENTS.md`, skill files, changed files, tests, and git history/diff.

Do not claim to have inspected a session log that is not present or accessible. If evidence is thin, label conclusions as hypotheses and state what would validate them.

## Workflow

### 1. Reconstruct the important events

Extract only events that teach something reusable:

- the user's intent and constraints;
- assumptions that proved wrong or required correction;
- repeated failures, confusing instructions, missed checks, or wasted actions;
- decisions that worked well and why;
- the final observable outcome and verification evidence.

Keep facts, interpretations, and recommendations distinct. Do not treat a model's mistake alone as a process problem unless a better instruction, check, tool, or test could prevent recurrence.

### 2. Find patterns worth preserving

For each candidate lesson, ask:

- Is it likely to recur in this repository, skill, task family, or agent workflow?
- Is it specific enough to act on and verify?
- Does it prevent a meaningful failure, ambiguity, security issue, or wasted effort?
- Is the evidence stronger than a single arbitrary preference?
- Would adding it reduce future errors more than it increases context and maintenance cost?

Reject or mark as low confidence lessons that are merely stylistic, tied to a single file, based on an unverified assumption, or already covered by clear existing guidance. Prefer a short rule plus a concrete trigger/check over a broad narrative.

### 3. Choose the right destination

Use the narrowest scope that owns the behavior:

- `AGENTS.md`: repository or directory-wide operating rules, validation commands, boundaries, conventions, and stable local facts.
- `SKILL.md`: reusable agent procedure for a task type, including decision criteria, tool usage, and output expectations.
- `references/`: detailed domain rules or examples needed only by a skill in selected cases.
- code, tests, scripts, or configuration: behavior that must be enforced mechanically rather than remembered.
- issue/PR/session notes: unresolved hypotheses, one-off context, or rationale that should not influence every future task.

If a lesson could fit multiple places, recommend one canonical home and explain why. Avoid duplicating the same rule across `AGENTS.md` and skills.

### 4. Check for conflicts and scope problems

Before proposing an update, inspect nearby guidance and check:

- duplicate or contradictory rules;
- instructions that would apply outside their intended directory or task;
- obsolete commands, paths, versions, or assumptions;
- secrets, personal data, customer data, or sensitive transcript content;
- advice that would bypass tests, approvals, safety boundaries, or user intent.

Generalize examples and redact sensitive values. Never promote credentials, tokens, private URLs, raw user data, or transcript text into durable guidance.

### 5. Produce the report

Use this compact structure:

````markdown
# Session learning

## Summary

One paragraph describing the durable outcome.

## Findings

| Priority | Evidence | Reusable lesson | Destination | Confidence |
| -------- | -------- | --------------- | ----------- | ---------- |

## Proposed changes

### path/to/file

```diff
...minimal patch...
```

Reason: ...

## Rejected or deferred

- Candidate and why it is one-off, weakly evidenced, already covered, or better enforced elsewhere.

## Follow-up validation

- A test, prompt, or future task that would confirm the change works.
````

Prioritize findings as `high`, `medium`, or `low` based on recurrence and impact, not how surprising the incident was. Include source locations or quoted evidence when available, but keep quotations short.

## Applying changes

Default to analysis and proposed diffs only. Apply edits only when the user explicitly requests implementation (for example, “反映して”, “適用して”, or “更新して”). After editing, run the narrowest relevant validation, inspect the diff, and report exactly which files changed. Preserve unrelated worktree changes.

## Quality bar

A good result is actionable, scoped, minimal, and testable. It should answer:

1. What happened?
2. What general rule or missing guardrail does it reveal?
3. Where should that rule live?
4. How will we know the update prevents recurrence?

Do not manufacture lessons just to fill the report. It is valid to conclude that no durable update is warranted.
