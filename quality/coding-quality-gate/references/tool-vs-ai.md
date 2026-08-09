# Tool-versus-AI evaluation boundary

Classify every quality question before evaluating it. Use a deterministic tool when the question has an observable, reproducible oracle. Use AI semantic review when the answer requires interpreting intent, context, trade-offs, or unstated behavior. Use both when a tool can narrow the evidence but cannot establish the full claim.

## Prefer deterministic tools

| Question                                                              | Typical tool                             | AI responsibility                                      |
| --------------------------------------------------------------------- | ---------------------------------------- | ------------------------------------------------------ |
| Does it compile, build, or typecheck?                                 | compiler, build, typechecker             | Explain relevance of failures                          |
| Do known tests pass?                                                  | unit/integration/e2e test runner         | Assess whether tests cover the requirement             |
| Does formatting or linting pass?                                      | formatter, linter                        | Decide whether a reported issue is in scope            |
| Is a file/schema/API generated and up to date?                        | generation check, diff checker           | Judge compatibility and intended change                |
| Is a dependency/import/configuration forbidden?                       | repository-specific scanner              | Confirm whether the rule applies                       |
| Does a data invariant hold over fixtures or migrations?               | validator, migration checker             | Identify missing scenarios and production risk         |
| Are secrets or unsafe patterns present?                               | secret scanner, SAST, dependency scanner | Investigate findings and residual risk                 |
| Are required files, routes, permissions, or manifest entries present? | structural checker                       | Confirm behavior behind the structure                  |
| Did a performance threshold pass?                                     | benchmark, load test, profiler           | Judge whether the threshold represents the requirement |

## Require semantic AI review

- Whether the implementation actually fulfills the user's intent, not merely the test cases;
- whether an edge case matters and what the correct behavior should be;
- whether the chosen architecture fits existing responsibility and dependency boundaries;
- whether the change is unnecessarily complex, broad, or difficult to maintain;
- whether tests are meaningful, representative, and resistant to false positives;
- whether an API or migration is conceptually backward-compatible for real consumers;
- whether a security, privacy, reliability, or operational trade-off is acceptable;
- whether an absence of evidence is meaningful or simply an untested path.

## Boundary rules

1. Never infer “passed” from a command that was not run.
2. Never infer semantic correctness from build, typecheck, lint, or coverage alone.
3. Treat tool output as evidence, not as the requirement itself.
4. If a semantic claim recurs and has a stable oracle, propose a repository-specific inspection tool and add a failing fixture before promoting it to Must Quality.
5. If a tool reports a failure but the rule is not applicable, record the applicability decision and preserve the raw evidence; do not silently discard it.
6. State what was checked by tools, what was judged by AI, and what remains unknown.

## Output contract for the AI reviewer

For each Must Quality rule, record:

```text
Rule: ...
Evaluation mode: TOOL | AI | BOTH
Evidence: command/output, file/line, or reasoning context
Result: PASS | FAIL | UNKNOWN | NOT_APPLICABLE
Reason: one concise explanation
Follow-up: repair, add a tool, add a test, or ask the user
```
