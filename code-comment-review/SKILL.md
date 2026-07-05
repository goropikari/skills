---
name: code-comment-review
description: Review code comments, docstrings, public API documentation comments, TODO/FIXME notes, and inline explanatory comments for accuracy, usefulness, maintainability, and refactoring resilience. Use when Codex is asked to review comments, improve comments, check whether comments are stale or misleading, review docstrings/API docs in code, or focus a code review specifically on comment quality.
---

# Code Comment Review

Review comments as part of the code's public and maintenance surface. Focus on whether each comment helps future readers understand the right thing without duplicating, contradicting, or overfitting the current implementation.

## Review Method

1. Inspect the requested diff, files, or snippets and identify comments, docstrings, API documentation comments, TODO/FIXME notes, and explanatory inline comments.
2. Compare each comment against the surrounding code, tests, types, names, and caller-visible behavior.
3. Review only comment-specific issues by default. Mention code design or behavior only when it is needed to explain why a comment is wrong, misleading, or impossible to evaluate.
4. Default to Japanese output unless the user explicitly asks for another language.
5. Prefer findings over general commentary. If there are no comment-specific issues, say that directly and mention any review limitations.

## Comment Quality Criteria

Good comments should explain information that the code cannot easily express:

- Caller-visible contracts, guarantees, arguments, return values, errors, side effects, and compatibility constraints.
- Domain rules, invariants, lifecycle constraints, concurrency concerns, performance assumptions, security/privacy constraints, and non-obvious failure modes.
- Intentional tradeoffs, historical constraints, or compatibility compromises that future maintainers must preserve.
- TODO/FIXME notes that identify the remaining problem and the condition, ticket, or follow-up needed to remove them.

Treat these as problems when supported by evidence:

- Stale or false comments that contradict code, tests, names, types, or current behavior.
- Comments that narrate obvious control flow, restate names, or describe implementation mechanics without adding reader value.
- Public API comments that describe internals instead of caller-visible behavior.
- Private function comments that exist only as walkthroughs and do not explain an invariant, constraint, or non-obvious reason.
- Comments that are too brittle: they would become false after a reasonable refactor that preserves external behavior.
- Comments that hide uncertainty with vague wording such as "probably", "temporary", "for now", or "should work" without a concrete constraint or removal path.
- TODO/FIXME notes that are unactionable, ownerless when the repo convention expects ownership, ticketless when the repo convention expects tickets, or missing the consequence of leaving the issue unresolved.
- Comments that expose sensitive information, normalize unsafe behavior, or make security/privacy assumptions that are not enforced by code.

## Severity Guidance

- Critical: A comment could cause a dangerous misuse, security/privacy issue, data loss, or release-blocking misunderstanding.
- High: A comment misstates important behavior, API contract, failure mode, or operational constraint.
- Medium: A comment is misleading, stale, too implementation-specific, or likely to misdirect maintainers.
- Low: A comment is noisy, redundant, vague, or could be made more useful without changing behavior.

## Output Format

Use this structure unless the user asks for a different format:

```markdown
## Findings

### [Severity: Critical/High/Medium/Low] Title
- Evidence:
- Problem:
- Why it matters:
- Suggested improvement:

## Optional Rewrites

## Additional Checks
```

Keep findings ordered by severity. Include file paths and line numbers when available. Provide rewrite examples only when they clarify the requested improvement; do not rewrite every comment by default.
