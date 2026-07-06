---
name: code-smell-review
description: Review code, PRs, diffs, and implementation plans for AI-detectable code smells focused on design, maintainability, responsibilities, abstractions, coupling, changeability, readability, and testability. Use when asked for a code smell review, maintainability smell review, design smell review, PR or diff smell inspection, or a review for issues that "AIだからこそ検知できる" / only AI can notice from context.
---

# Code Smell Review

Review code for design and maintainability smells that require contextual judgment. Exclude issues that compilers, linters, formatters, type checkers, or basic static analyzers can reliably detect.

## Review Method

1. Inspect the requested diff, files, snippets, or implementation plan.
2. Identify only smells with concrete evidence in the reviewed material. Include file paths, line numbers, symbols, or quoted snippets when available.
3. Default to Japanese output unless the user explicitly asks for another language.
4. Report findings first, ordered by severity. Do not include positive commentary unless it is needed to explain context.
5. If evidence is weak or the concern is only a personal preference, do not report it.
6. If no findings exist, state that no AI-detectable code smells were found and briefly mention review limitations.

## Review Criteria

Look for these smell categories when supported by evidence:

- Responsibility smells: god objects, hidden multiple responsibilities, feature envy, inappropriate ownership, or behavior living in a layer that should not own it.
- Abstraction smells: wrong abstraction, speculative generality, leaky abstraction, misleading domain model, or an abstraction that hides important policy instead of clarifying it.
- Coupling smells: temporal coupling, shotgun surgery risk, implicit dependencies, over-shared mutable state, or call sequences that must be remembered by callers.
- Changeability smells: code that makes likely future changes expensive, brittle branching, policy scattered across layers, or local changes that require coordinated edits elsewhere.
- Readability smells: intent that cannot be inferred from structure, surprising behavior hidden behind ordinary names, or code whose public shape misleads future readers.
- Testability smells caused by design: uncontrollable dependencies, hard-to-isolate behavior, hidden global state, or tests that would need excessive setup because responsibilities are tangled.

## Exclusions

Avoid these unless they are direct evidence of one of the design smells above:

- Formatting, import order, unused variables, simple duplication, naming-only preferences, or style-guide preferences.
- Issues detectable by a compiler, linter, formatter, type checker, dead-code detector, or basic complexity tool.
- Cyclomatic-complexity-only findings where the deeper design risk is not explained.
- Findings based only on personal taste, preferred architecture, or speculative future requirements.
- General PR review topics such as correctness bugs, security bugs, performance bugs, or missing tests unless the root problem is a design smell.
- Positive commentary, broad summaries, or "looks good" sections.

## Severity Guidance

- Critical: The smell plausibly causes data loss, security failure, severe production impact, or blocks safe change.
- High: The smell is likely to cause repeated defects, unsafe coupling, or expensive change in important code.
- Medium: The smell creates meaningful maintainability or testability risk with plausible future cost.
- Low: The smell is localized and worth fixing opportunistically.

## Output Format

Use this structure unless the user asks for a different format:

```markdown
## Findings

### [Severity: Critical/High/Medium/Low] Title

- Evidence:
- Smell:
- Why it matters:
- Suggested improvement:

## Additional Checks
```

Keep each finding concrete and actionable. The suggested improvement may be a refactoring direction rather than a full implementation, but it must address the identified smell rather than only changing names or formatting.
