---
name: multi-agent-tournament-development
description: "Run a multi-agent implementation tournament for a software change: turn requirements into an acceptance contract, create isolated Git worktree candidates, independently judge them using execution evidence, integrate one winner, and verify the final result. Use for medium- or high-risk implementation tasks where comparing independent approaches improves confidence, especially authentication, payments, personal data, migrations, infrastructure, or changes with unclear implementation choices."
---

# Multi-Agent Tournament Development

Produce the most verifiable, maintainable implementation—not merely the first implementation. Keep candidate implementations isolated and select using reproducible evidence.

## Select a level

| Level | Use for                                                                           | Roles                                    |
| ----- | --------------------------------------------------------------------------------- | ---------------------------------------- |
| 1     | Small, low-risk change                                                            | Candidate ×1, Judge, Verifier            |
| 2     | Default                                                                           | Candidate ×3, Judge, Verifier            |
| 3     | Auth, payments, personal data, migration, infrastructure, or a high-impact change | Candidate ×3 or more, Judge(s), Verifier |

## Read role prompts

Read [ORCHESTRATOR.md](ORCHESTRATOR.md) before starting and use it as the controlling prompt.

- Give every implementation agent [CANDIDATE.md](CANDIDATE.md), together with its assigned perspective and the acceptance contract.
- Give the selection agent [JUDGE.md](JUDGE.md), the contract, and only candidate artifacts after all candidates finish.
- Give the final independent checker [VERIFIER.md](VERIFIER.md), the contract, and the integrated working tree.

Do not let candidates inspect another candidate's worktree, branch, commits, diff, output, or design. Do not let the judge alter candidate code. Do not let the verifier repair the final implementation.

## Required invariants

1. Define acceptance criteria before candidate implementation.
2. Capture caller context: current directory, Git root, branch, HEAD, and working-tree status.
3. Start every candidate from the same base commit in its own worktree and branch.
4. Run the same declared validation commands for every candidate whenever feasible; record unavailable checks as `NOT RUN` with a reason.
5. Base selection first on requirement compliance and executed evidence, not prose or code volume.
6. Integrate one winner into the caller's original branch. Bring over another candidate's insight only through a deliberate, tested change—never by indiscriminate code splicing.
7. Preserve candidate worktrees unless the user explicitly requests their removal.
8. Never describe an unexecuted command or unverified property as successful.

## Candidate perspectives for Level 2+

- **A — conservative:** existing design, smallest compatible change, maintainability.
- **B — defensive:** boundaries, failures, security, recovery and edge cases.
- **C — structural:** simple responsibilities, alternative design, long-term evolution.

Use actual parallel execution when available. If execution must be sequential, retain worktree isolation and state that it was sequential.

## Completion report

Report the selected candidate, selection rationale, integration commit or diff, validation commands and outcomes, any `NOT RUN` checks, residual risks, and the final `PASS`, `PASS WITH RISKS`, or `FAIL` verdict.
