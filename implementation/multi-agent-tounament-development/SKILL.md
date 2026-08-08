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

- Give every implementation agent [CANDIDATE.md](CANDIDATE.md), together with its assigned perspective, exact `ASSIGNED_WORKTREE`, exact `ASSIGNED_BRANCH`, and the acceptance contract.
- Give the selection agent [JUDGE.md](JUDGE.md), the contract, and only candidate artifacts after all candidates finish.
- Give the final independent checker [VERIFIER.md](VERIFIER.md), the contract, and the integrated working tree.

Do not let candidates inspect another candidate's worktree, branch, commits, diff, output, or design. Do not let candidates edit the caller's worktree or repository root. Do not let the judge alter candidate code. Do not let the verifier repair the final implementation.

## Required invariants

1. Define acceptance criteria before candidate implementation.
2. Capture caller context: current directory, Git root, branch, HEAD, and working-tree status.
3. Start every candidate from the same base commit in its own worktree and branch. Create the worktrees under `<caller-current-directory>/.worktrees/`; do not place them in Git's default worktree location.
4. For the three Level 2+ candidates, name branches from the original branch: `<original-branch>-a`, `<original-branch>-b`, and `<original-branch>-c`. Assign A, B, and C to those branches respectively. If the caller is detached, stop and obtain an explicit base branch name before creating candidates.
5. Run the same declared validation commands for every candidate whenever feasible; record unavailable checks as `NOT RUN` with a reason.
6. Base selection first on requirement compliance and executed evidence, not prose or code volume.
7. Integrate one winner into the caller's original branch. Bring over another candidate's insight only through a deliberate, tested change—never by indiscriminate code splicing.
8. Preserve candidate worktrees unless the user explicitly requests their removal.
9. Never describe an unexecuted command or unverified property as successful.
10. Before candidate execution, verify the assigned worktree's canonical path and current branch; launch the candidate with that worktree as cwd.
11. After candidate execution, verify the candidate stayed on the assigned branch and compare the caller's tracked and untracked status with its pre-candidate snapshot.
12. Treat any unauthorized caller/repository-root modification as `WORKTREE_BOUNDARY_VIOLATION` and do not integrate that candidate.

## Candidate perspectives for Level 2+

- **A — conservative:** existing design, smallest compatible change, maintainability.
- **B — defensive:** boundaries, failures, security, recovery and edge cases.
- **C — structural:** simple responsibilities, alternative design, long-term evolution.

Use actual parallel execution when available. If execution must be sequential, retain worktree isolation and state that it was sequential.

## Completion report

After all three candidates have completed and the final integration has been verified, write a Japanese Markdown comparison report in the caller's current directory. Use `multi-agent-tournament-comparison.md`; if that path already exists, choose a non-overwriting numbered variant and report the exact path. Generate it only after every intended integration commit is complete. It is a local, untracked artifact: never stage, commit, amend, or otherwise include it in the winner's branch. Do not use Markdown tables; use candidate headings and short bullet lists instead.

The report must compare A, B, and C in separate sections and include each branch, worktree path, commit, changed files/diff summary, acceptance-criteria result, validation outcomes, limitations or risks, the selected winner and rationale, integration details, and the final verifier verdict. Write the report even if no candidate wins or the tournament fails; mark missing work and unavailable checks as `NOT RUN` with reasons. Keep the report entirely in Japanese except for literal branch names, paths, commands, verdict labels, and other required identifiers.

Also return the selected candidate, selection rationale, report path, integration commit or diff, validation commands and outcomes, any `NOT RUN` checks, residual risks, and the final `PASS`, `PASS WITH RISKS`, or `FAIL` verdict.
