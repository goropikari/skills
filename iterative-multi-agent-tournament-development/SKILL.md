---
name: iterative-multi-agent-tournament-development
description: "Run an initial multi-agent implementation tournament, choose and repair the strongest candidate when all are rejected, then improve the result through repeated evidence-driven three-candidate rounds. Use for medium- or high-risk changes where independent implementations, recovery, and per-round comparison reports improve confidence."
---

# Iterative Multi-Agent Tournament Development

Run an initial tournament, recover from bounded failures when possible, and then improve the result through successive rounds. Each executable round produces three isolated alternatives, selects and integrates one winner, then makes that integrated result the only base for the next round. If every candidate is rejected, select the strongest repairable candidate, fix its known issues, and rerun the round from the repaired integrated commit. A fallback candidate is provisional until it passes independent verification; never report it as verified merely because it was the least bad option.

## Establish the initial contract

Capture the caller's current directory, Git root, branch, HEAD commit, and working-tree status. Define the task's goal and non-goals, functional and non-functional requirements, constraints, observable acceptance criteria, risks, and a validation matrix before creating candidates. Preserve unrelated user changes.

Use the captured HEAD as the initial base. If the caller is detached, obtain an explicit base branch before creating candidates. Start an improvement round from a verified integrated winner when available; when the all-rejected protocol has produced an eligible but still unverified repaired base, start the next candidate round from that base with the failed criteria and repair evidence carried into its contract. Preserve failed-round evidence when retrying.

## Preserve tournament discipline

For every candidate, use the independent-candidate, judge, and final-verifier rules in the sibling `multi-agent-tounament-development` skill. This skill controls the initial-round and iteration-specific naming and report rules below when they differ.

- Do not let candidates inspect another candidate's worktree, branch, commit, diff, output, or design.
- Give every candidate the exact absolute `ASSIGNED_WORKTREE` and `ASSIGNED_BRANCH`, launch it with the assigned worktree as cwd, and require the sibling skill's path/root/branch preflight before any file access.
- Snapshot the caller's tracked and untracked status before each candidate and verify it is unchanged afterward except for explicitly authorized integration or repair changes. Classify unauthorized changes as `WORKTREE_BOUNDARY_VIOLATION`, exclude that candidate, and preserve the evidence.
- Start all candidates in a round from one identical base commit.
- Judge from requirement compliance and executed evidence before design preference or prose.
- Integrate only one winner per round into the caller's original branch. Do not splice candidate implementations.
- Preserve worktrees unless the user requests removal. Never report an unexecuted check as successful.
- Only the orchestrator may edit the caller's worktree, and only for recorded winner integration, review-driven repair, or all-rejected repair. Judges, verifiers, reviewers, and candidates are read-only with respect to the caller unless their role explicitly says otherwise.

## Execute the initial tournament (round 0)

Create these branches and worktrees from the captured initial base commit, creating `<caller-current-directory>/.worktrees/` as needed:

| Candidate | Branch                | Worktree       | Perspective                 |
| --------- | --------------------- | -------------- | --------------------------- |
| A         | `<original-branch>-a` | `.worktrees/a` | Conservative implementation |
| B         | `<original-branch>-b` | `.worktrees/b` | Defensive implementation    |
| C         | `<original-branch>-c` | `.worktrees/c` | Structural implementation   |

If any required branch or worktree already exists, stop and ask for direction; do not reuse or overwrite it. Give each candidate the initial acceptance contract, its perspective, and validation commands. Judge the completed candidates read-only, integrate one winner into the caller's original branch, and run independent final verification.

Write `multi-agent-tournament-comparison.md` in the caller's current directory after verification and all intended integration commits. If it already exists, use the first non-existing numbered variant. This is a local, untracked artifact: never stage, commit, amend, or include it in the winner's branch.

If the initial tournament has no integrated winner or has a `FAIL` verdict, first run the bounded recovery procedure below. If all candidates were rejected for repairable issues, use the all-rejected protocol below before declaring the tournament blocked.

## Select and repair when all candidates are rejected

The judge must distinguish a candidate that is unsafe, destructive, unrelated to the task, or impossible to validate from a candidate that is close but has concrete, repairable defects. The former is ineligible for fallback. For the latter, return a fallback ranking even when no candidate satisfies the full contract:

1. strongest executed evidence and greatest number of satisfied acceptance criteria;
2. fewest and smallest blocking defects;
3. lowest security, data-integrity, compatibility, and operational risk;
4. clearest repair and validation plan.

Select the highest-ranked eligible candidate as a `PROVISIONAL WINNER`, record why every other candidate ranked lower, and integrate that candidate alone. Apply the documented repair plan as a deliberate, minimal change on the caller's branch, then run the complete validation matrix and independent verifier. Do not merge snippets from the losing candidates. If the repair makes the result pass, it becomes the verified winner; if it does not, preserve the evidence and run the next candidate round from the repaired result, carrying the remaining defects into that round's contract. Do not silently skip a repair, mark a failed check as passed, or select an ineligible candidate.

For the repair retry, use fresh non-overwriting branches and worktrees derived from the round name (for example, `<original-branch>-improve-1-repair-1-a` with `.worktrees/improve-1-repair-1-a`, and corresponding `-b` and `-c` pairs). Start all three from the repaired integrated commit, give them the exact known defects and repair evidence, and apply the same judge and verifier rules. Preserve the original rejected candidates and reports.

This protocol applies to the initial tournament, bounded recovery, and improvement rounds. It replaces “stop because there is no winner” for repairable failures. Stop only for an ineligible fallback, a missing user decision, a destructive-state conflict, an unavailable base repository, or exhaustion of the explicitly configured round/recovery budget. If no budget was supplied by the caller, use the normal two improvement rounds plus one all-rejected repair retry per round, and report the remaining blocker if that still fails.

## Recover a failed initial tournament (at most once)

Classify the failure using executed evidence:

- `SETUP`: a branch, worktree, or agent orchestration failure prevented candidates from completing;
- `EVIDENCE`: candidates may contain useful work, but required validation or verifier evidence is missing or irreproducible;
- `IMPLEMENTATION`: candidates completed, but the required behavior genuinely failed; or
- `ENVIRONMENT`: a declared check was blocked by an external limitation.

Write the initial comparison report before retrying. Then run exactly one recovery tournament unless the failure is a missing user decision, a destructive-state conflict, or an unavailable base repository. Use the same captured base for `SETUP`, `EVIDENCE`, and `IMPLEMENTATION` failures. For `ENVIRONMENT`, retry only with an explicit, safe workaround in the recovery contract; never silently treat the check as passed.

Use fresh recovery branches and worktrees:

| Candidate | Branch                        | Worktree               | Perspective                            |
| --------- | ----------------------------- | ---------------------- | -------------------------------------- |
| A         | `<original-branch>-retry-1-a` | `.worktrees/retry-1-a` | repair the smallest blocker            |
| B         | `<original-branch>-retry-1-b` | `.worktrees/retry-1-b` | harden failure and evidence paths      |
| C         | `<original-branch>-retry-1-c` | `.worktrees/retry-1-c` | simplify the design around the blocker |

Give every recovery candidate the original contract, failure classification, exact failed evidence, and recovery acceptance criteria. Require the complete validation matrix. Candidates must not relax criteria, hide failures, or inspect one another. Judge and verify recovery using the sibling tournament rules, then integrate at most one recovery winner into the original branch.

Write `multi-agent-tournament-recovery.md` after recovery (using the first non-existing numbered variant). If recovery has no eligible provisional winner or still verifies as `FAIL` after its permitted repair retry, continue with the all-rejected protocol when the failure is repairable; otherwise stop. Still write blocked reports with A, B, and C as `NOT RUN` only for a genuine blocker. Never manufacture a selected winner: label an unverified fallback `PROVISIONAL WINNER` and include its exact defects.

## Execute round 1

Use only the verified initial-tournament integrated commit, or the repaired integrated commit produced by the all-rejected protocol, as the base. Read its comparison report and verifier output, then carry forward only unresolved risks, failed criteria, or concrete improvement opportunities. Do not reopen settled requirements without a user request. Define round-specific acceptance criteria and use the same validation matrix for all three candidates in that round.

Create these worktrees under the caller's current directory, creating `.worktrees/` as needed:

| Candidate | Branch                          | Worktree                 | Perspective              |
| --------- | ------------------------------- | ------------------------ | ------------------------ |
| A         | `<original-branch>-improve-1-a` | `.worktrees/improve-1-a` | Conservative improvement |
| B         | `<original-branch>-improve-1-b` | `.worktrees/improve-1-b` | Defensive improvement    |
| C         | `<original-branch>-improve-1-c` | `.worktrees/improve-1-c` | Structural improvement   |

`<original-branch>` is the branch captured from the caller. If any required branch or worktree already exists, stop and ask for direction; do not reuse or overwrite it.

Give each candidate the round contract, its perspective, and validation commands. After all finish, use a read-only judge to compare their commits, diffs, validation output, and limitations. Integrate the winner, run an independent final verification, and record the verdict.

## Orchestrate targeted reviews in every round

After the judge selects a contract winner or `PROVISIONAL WINNER`, invoke `$review-orchestrator` to decide whether targeted review is warranted for that round's integrated candidate. Do this for the initial tournament, bounded recovery, and both improvement rounds; do not assume that a previous round's review decision applies to the next round.

Provide the review orchestrator with the round contract, candidate comparison, integrated diff, validation evidence, carried-forward risks, and the exact repair changes. Ask it to select the smallest effective review set using its routing matrix. In particular, consider review when the round changes an API, configuration, persistence, authentication, personal data, concurrency, tests, observability, deployment behavior, or a high-risk responsibility boundary; also consider it when the verifier reports a residual risk or when all candidates were rejected. A local, low-risk change with no such signals may be explicitly recorded as skipped.

Run the selected reviews before the round's final verifier. If a review finds a concrete defect or missing evidence, turn it into a repair item, fix it through a deliberate tested change on the integrated candidate, rerun affected validation, and run the final verifier again. Do not let a review agent edit the candidate or caller worktree directly. Findings that remain unresolved must be carried into the next round's contract; a high-severity security, data-integrity, compatibility, or release blocker prevents a `PASS`. If multiple reviewers run, calibrate their results as required by `$review-orchestrator`; validate existing findings before relying on them.

Record in every round report the selected reviews, skipped reviews and reasons, findings with severity/location/evidence, repairs made, recalculated validation outcomes, and remaining uncertainty. Review output informs the repair and next-round contract; it does not replace candidate isolation, the judge, or independent verification.

Write `multi-agent-tournament-improvement-round-1.md` in the caller's current directory after the final verification and all intended integration commits. If it already exists, use the first non-existing numbered variant. This is a local, untracked artifact: never stage, commit, amend, or include it in the winner's branch.

## Execute round 2

Use only the verified round-1 integrated commit as the base; do not return to losing candidates, the initial-tournament baseline, or recovery losers. Reassess the round-1 report and verifier output, then define a round-2 contract that targets remaining risks or measurable improvements.

Create these branches and worktrees from that base:

| Candidate | Branch                          | Worktree                 | Perspective              |
| --------- | ------------------------------- | ------------------------ | ------------------------ |
| A         | `<original-branch>-improve-2-a` | `.worktrees/improve-2-a` | Conservative improvement |
| B         | `<original-branch>-improve-2-b` | `.worktrees/improve-2-b` | Defensive improvement    |
| C         | `<original-branch>-improve-2-c` | `.worktrees/improve-2-c` | Structural improvement   |

Repeat the round-1 candidate, judging, integration, and independent verification process. If round 1 has no contract winner or has a `FAIL` verdict, use the all-rejected protocol once within its configured budget and then use that repaired commit as round-2's base. Still write the round-2 report marked `BLOCKED` only when the fallback is ineligible or the retry budget is exhausted, with A, B, and C as `NOT RUN` and the precise blocker. If round 2 fails, report the failure and residual risk; do not perform an unbounded third tournament.

Write `multi-agent-tournament-improvement-round-2.md` with the same untracked-artifact rules as round 1, and use a numbered non-overwriting variant when needed.

## Required contents of each comparison report

Write every comparison report in Japanese, regardless of the language used by the candidates or reviewers. Use headings and short bullet lists; do not use Markdown tables for candidate comparisons or validation results.

Write a Markdown report for every completed or blocked round. Include:

1. caller context, base commit, carried-forward findings, failure classification/recovery input when applicable, and round acceptance contract;
2. separate `候補 A`, `候補 B`, and `候補 C` sections. In each section, record the branch, worktree, commit, changed files/diff summary, criterion result, exact validation outcomes, and limitations or risks;
3. the judge's winner or `PROVISIONAL WINNER` decision and rationale, including rejection reasons and the repair plan when applicable;
4. integration commit or diff, final-verifier evidence and verdict; and
5. review-orchestrator selection, findings, repair/reverification evidence, skipped-review reasons, and next-round input or a clear blocker, including whether bounded recovery was attempted and why it stopped.

Use `NOT RUN` with a reason for unavailable candidates or checks. Return every applicable report path (initial, recovery, round 1, and round 2), selected winners, integration details, validation outcomes, residual risks, and the final round-2 verdict or terminal recovery blocker.
