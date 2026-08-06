---
name: dw-phase-tournament-flow
description: Orchestrate a repeatable software delivery flow from reviewed dw-phase design through blackbox and whitebox risk-based test design, dependency-aware parallel implementation, multi-agent tournament selection for high-risk phases, review, integration, and final verification. Use when a repository uses dw-phase together with dw-phase-parallel-light and multi-agent-tounament-development, or when the user asks for an end-to-end phase implementation workflow.
---

# DW Phase Tournament Flow

Run the delivery flow as a sequence of explicit gates. Preserve the existing
skills' state, worktree, branch, review, and `NOT RUN` rules. Do not bypass a
gate merely because an implementation appears small or obvious.

## Flow

```text
Requirements and context
  -> dw-phase design + acceptance contract
  -> review and approve
  -> acceptance-criteria traceability + blackbox risk/test design
  -> dependency and phase risk classification
  -> dw-phase-parallel-light implementation waves
       -> direct implementation for routine phases
       -> tournament inside the assigned phase worktree for high-risk phases
  -> phase-level whitebox review and test-quality review
  -> integration and verification
  -> dw-phase review/approve/next
```

## Gate 0: Capture Context

Before changing code, record the repository root, current directory, branch,
HEAD, working-tree status, active `.dev-workflow-phase/` state, and the user's
scope. Identify existing uncommitted changes and do not overwrite them.

Confirm that the requested work is represented by the current requirements and
phase design. If the design is missing, stale, not reviewed, or not approved,
run `dw-phase` and stop at its review gate. Do not start implementation before
`Global Step: 1` has `Status: REVIEWED` and the phase design has been approved.

## Gate 1: Establish the Acceptance Contract

Treat `.dev-workflow-phase/acceptance-contract.md` as the primary delivery
contract. `dw-phase` requires it before Global Step 1 can advance. It must
contain at least:

- `## Goal`
- `## Non-goals`
- `## Phase Scope`
- `## Acceptance Criteria`
- `## Constraints and Compatibility`
- `## Prioritized Risks`
- `## Validation Matrix`
- `## Assumptions and Open Questions`

The contract is derived from the project requirements and phase design; it is
not a copy of the PRD. Every acceptance criterion must be observable,
testable, and attributable to one or more phases. Give each criterion a stable
identifier such as `AC-001`, assign it to a phase, and state its expected
result and evidence. Give each validation condition a stable identifier such as
`VM-001`, assign it to a phase, and state the exact command or manual procedure.
If a criterion is ambiguous or unverifiable, stop at the review gate and record
it as an open question rather than allowing agents to infer behavior.

For each ready phase, build a traceability slice containing only the relevant
acceptance criteria, constraints, risks, and validation commands. Mark entries
with `- **Phase**: phaseN` (or a comma-separated list). This slice is what
implementation agents receive. Keep the full requirements document and
unrelated phase criteria in orchestrator context.

## Gate 2: Build the Test and Risk Basis

For the approved acceptance contract and phase slices, use
`blackbox-risk-based-test` to derive:

- observable business and user risks linked to `AC-*` criteria;
- user-visible test conditions and expected evidence for each criterion;
- regression scope, test data, oracles, and manual checks;
- a shared validation command set for comparable implementations.

Use `whitebox-risk-based-test` when the design exposes technical concerns such
as persistence, concurrency, security boundaries, migrations, external calls,
performance, or failure recovery. It may be run before implementation to shape
the plan and again after implementation to inspect the actual diff.

Do not replace acceptance criteria with a coverage percentage. Record risk, impact,
likelihood, priority, test condition, evidence, and residual risk. Carry the
highest-priority conditions into each phase's traceability slice and
`03_test_design.md` where applicable. Every `AC-*` criterion must have a
validation condition or an explicit `NOT RUN` reason.

## Gate 3: Classify Phases

For every ready phase, record the following assessment before choosing an
implementation mode:

```markdown
- Impact: High|Medium|Low
- Likelihood: High|Medium|Low
- Uncertainty: High|Medium|Low
- Base Risk Score: Impact score × Likelihood score (1-9)
- Blast Radius: local|component|system|external
- Reversibility: easy|moderate|hard
- Validation Confidence: high|medium|low
- Implementation Mode: direct|tournament|serial
- Rationale:
```

Score Low=1, Medium=2, and High=3. Use `Base Risk Score` as the starting
point, not as the only decision. Classify implementation mode using these
rules, in order:

- **Serial**: a required dependency is unfinished or the phase cannot be
  tested meaningfully until another phase is integrated.
- **Tournament**: a critical domain is involved; or Impact is High and either
  Likelihood or Uncertainty is Medium/High; or Uncertainty is High together
  with component-or-larger blast radius, hard reversibility, or low validation
  confidence; or two or more materially different designs are plausible.
- **Direct light implementation**: Impact and Likelihood are Low/Medium,
  Uncertainty is Low, blast radius is local/component, reversibility is easy or
  moderate, validation confidence is high, and no tournament trigger applies.

When multiple rules apply, choose the more conservative mode. Record the
triggering rule in `Rationale`; do not silently override it.

Keep the dependency graph from `dw-phase` authoritative. Start only ready
phases and use `dw-phase-parallel-light next` to launch at most its supported
parallel batch. Do not create a second ad-hoc dependency graph.

## Gate 4: Implement in Isolated Worktrees

Use `dw-phase-parallel-light` for the ready implementation wave. Each agent
must work only in its assigned phase worktree and must return the required
completion marker/status. It must not push, open a PR, or modify the caller's
root unless the underlying skill explicitly requires it.

For a phase classified as tournament:

1. Launch the tournament from that phase's assigned worktree, not the caller's
   repository root.
2. Give all candidates the phase-specific acceptance-criteria slice,
   blackbox test conditions, validation commands, and exact assigned
   worktree/branch. Do not give the full PRD by default.
3. Select by executed evidence and requirement compliance. Use Level 1 for a
   small isolated change, Level 2 by default, and Level 3 for critical or
   high-impact changes.
4. Let the tournament integrate one winner and run its independent verifier in
   that phase worktree.
5. Preserve candidate worktrees and produce the required Japanese comparison
   report. Never indiscriminately splice candidate code.

For routine phases, the light agent may implement directly, but it must still
execute the shared validation commands, record unavailable checks as `NOT RUN`,
and perform a self-review before returning `READY_TO_COMMIT`.

## Gate 5: Review the Result

After each implementation wave, run the smallest effective reviews based on
the changed behavior:

- `whitebox-risk-based-test` for implementation risk coverage and testability;
- `test-quality-review` for assertion strength, determinism, and false
  positives;
- `security-review`, `migration-review`, `data-integrity-review`,
  `concurrency-review`, or `performance-review` when the risk basis calls for
  them;
- `blackbox-risk-based-test` to confirm every applicable `AC-*` criterion and
  user-visible condition remains covered.

Use `review-finding-validator` when findings come from multiple agents or an AI
review and need evidence-based validation. Do not repair code inside an
independent verifier/reviewer role; apply fixes in the implementation role and
rerun affected checks.

## Gate 6: Integrate and Advance State

Before integration, verify branch, canonical worktree path, commit, diff,
tracked/untracked status, validation results, and boundary compliance. Reject
any candidate or agent with an unauthorized caller-root modification.

Integrate only completed, reviewed phase work. Resolve conflicts deliberately,
rerun impacted tests, and keep phase artifacts and implementation commits
traceable. Before advancing state, perform an acceptance-criteria gate:

- every applicable `AC-*` criterion is `PASS`, or has an explicit
  `NOT RUN`/residual-risk record;
- the phase's highest-priority risks have executed evidence;
- failed criteria block completion unless the user explicitly accepts the
  residual risk;
- implementation, tests, and validation evidence are traceable to the
  criterion IDs.

After this gate and the phase's required artifacts are complete, run `dw-phase
review`, obtain the user's approval where required, and then run `dw-phase
next` to advance the state. Do not mark a phase complete based only on a
passing unit-test command if an acceptance criterion or highest-risk observable
behavior was not checked.

## Completion Report

At the end of the overall flow, summarize in Japanese:

- requirements, approved phase design, acceptance contract, and implementation waves;
- acceptance-criteria traceability, including every `AC-*` result and evidence;
- each phase's mode: direct or tournament, with rationale;
- each phase's Impact, Likelihood, Uncertainty, Base Risk Score, blast radius,
  reversibility, and validation confidence;
- blackbox risks and acceptance coverage;
- whitebox risks and technical coverage;
- branches, worktrees, commits, changed files, and integration details;
- validation commands and outcomes, including every `NOT RUN` reason;
- review findings and resolutions;
- residual risks and recommended follow-up;
- final verdict: `PASS`, `PASS WITH RISKS`, or `FAIL`.

Do not claim success for an unexecuted command, an unverified property, or an
unapproved phase. Keep generated comparison reports untracked as required by
the tournament skill.

## Decision Summary

Use this skill as the entry point when the user describes the whole workflow.
Delegate the actual state transitions to `dw-phase`, parallel scheduling to
`dw-phase-parallel-light`, candidate comparison to
`multi-agent-tounament-development`, and risk analysis to the blackbox and
whitebox skills. This skill coordinates them; it does not replace their
individual invariants.
