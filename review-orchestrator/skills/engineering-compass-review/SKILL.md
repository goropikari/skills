---
name: engineering-compass-review
description: "Review code, PRs, diffs, or implementation plans against the user's Engineering Compass principles: readability, understandability, testability, loose coupling, and refactoring-resilient comments. Use when the user asks for an Engineering Compass review or review from the user's personal standards."
---

# Engineering Compass Review

Apply the `engineering-compass` principles to the supplied code, PR, diff, or implementation plan.

## Review Process

- Focus on clear negative factors; do not generally mention positive points.
- Raise a finding only when it is supported by a concrete problem rather than a preference.
- Explain why each finding matters and suggest a proportionate improvement.
- Assess comments using the Engineering Compass comment policy, including whether they remain accurate after a behavior-preserving refactor.

## File Output

Write the review result to a Markdown file under `docs/reviews/`. Create the directory if needed. If the user specifies an output path, use it. Otherwise, create or update `docs/reviews/engineering-compass-review.md`.

## Output Format

```markdown
## Overall Assessment

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Problem:
- Why it matters:
- Suggested improvement:

## Optional Improvements

## Additional Points to Check
```

## Memory Use

After a review, add a newly revealed review criterion to memory only when the user's actual review comments or accepted/rejected outcomes establish it as durable. Do not turn temporary, context-dependent judgments into permanent rules.
