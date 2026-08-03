# Placement rubric

Use this when the destination is ambiguous.

| Question | Best destination |
| --- | --- |
| Does it govern every task in a repository or directory? | `AGENTS.md` |
| Does it govern a repeatable task class independent of one repository? | A skill's `SKILL.md` |
| Is it detailed, conditional, or too large for the skill body? | A skill `references/` file |
| Can a machine check it reliably? | Test, linter, script, or configuration |
| Is it unresolved, temporary, or specific to one incident? | Issue, PR, or session notes |

## Promotion test

Promote a lesson into durable guidance only when all of these are true:

- The behavior is likely to recur.
- The desired behavior can be stated clearly.
- The guidance has a clear owner and scope.
- The rule does not expose sensitive information.
- A future task can validate compliance or usefulness.

If any condition is false, keep it as a deferred candidate and say what evidence is missing.
