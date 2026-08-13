---
name: implementation-orchestrator
description: >-
  Analyze a software implementation request and choose the safest plan before
  changing code. Use for feature work, bug fixes, refactors, new applications,
  migrations, infrastructure, and other changes where requirements, tests,
  design, risk, and verification must be composed. Do not use for review-only,
  explanation-only, or documentation-only requests.
---

# Implementation Orchestrator

Analyze the requested change, compose an implementation plan from allowed
repository skills, and carry the work through implementation and verification.

## Operating contract

1. Inspect the repository, current worktree, project conventions, existing
   tests, build/lint commands, and active workflow state. Treat repository
   instructions such as `AGENTS.md`, contribution guides, and package-local
   rules as higher priority than this skill; find and read the applicable
   instructions before planning or editing.
2. Resolve the directory containing this `SKILL.md` as `<orchestrator_dir>`.
   Read `<orchestrator_dir>/skills/implementation-change-analysis/SKILL.md`
   and produce a route decision covering request type, repository maturity,
   scope, observable behavior, risk, dependencies, and validation needs.
3. Read [route-selection.md](references/route-selection.md) and choose the
   smallest safe plan. Select only skills available in the current installation.
   Request reviews through the public `review-orchestrator` entry point rather
   than invoking its bundled reviewer components directly.
4. Write `.implementation-orchestrator/implementation-plan.md` before
   changing product code. Use [implementation-plan-template.md](references/implementation-plan-template.md)
   and include the required route-decision block, selected skills, their order,
   expected outputs, decision gates, implementation steps, and validation
   commands.
5. Read only the internal component skills needed for planning, resolving each
   path from `<orchestrator_dir>`, for example
   `<orchestrator_dir>/skills/implementation-acceptance-contract/SKILL.md`.
   Read `implementation-architecture-planning` when a non-mechanical change
   creates or changes a responsibility boundary, extension point, state or
   lifecycle boundary, external integration, or has material design
   uncertainty. They are under this skill's own `skills/` directory and are
   not repository implementation workflows.
6. Establish acceptance criteria and a validation matrix before implementation
   when the change affects externally observable behavior, has material risk,
   or involves multiple contributors. Use the internal acceptance-contract
   component. For public artifacts, destructive behavior, or candidate
   comparison, also use the internal acceptance-harness component to freeze a
   black-box oracle before implementation. An existing harness is sufficient
   only when its immutable criteria directly cover the new behavior; a
   regression-only harness does not independently prove a new public contract.
7. Use the internal execution-strategy component to choose direct, staged,
   parallel, or comparative execution. Prefer the smallest reversible change.
8. Implement in the caller's worktree according to the plan. Preserve
   unrelated changes and do not commit, push, or create a pull request unless
   requested.
9. Before implementation and again after meaningful edits, inspect the actual
   diff and affected call sites. Unless the change is mechanical, keep the
   total changed lines under 800. For complex logic changes, keep it under 500
   lines. Count additions and deletions in the relevant diff, not just the
   number of files.
10. If the change exceeds the applicable limit, do not force it into one
    branch or PR. Identify the smallest coherent stage that can land first,
    base the split on actual diff boundaries, dependencies, and affected call
    sites, and record the branch/PR sequence in
    `.implementation-orchestrator/implementation-plan.md`. Continue only with
    the first reviewable stage unless the user explicitly requests a combined
    change.
11. Use the internal verification-gate component before declaring completion.
    Every required check must be `PASS`, or an explicitly reported accepted
    residual risk.

## Allowed supporting skills

Use the smallest set that covers the change; do not invoke every reviewer by
default.

- Requirements: `prd-maker`, `grill-me`, and `review-orchestrator` when a
  requirements review is needed.
- External behavior and test design: `blackbox-risk-based-test` and
  `whitebox-risk-based-test`; request mutation or property-based test review
  through `review-orchestrator` when appropriate.
- Frozen black-box oracle: use the internal
  `implementation-acceptance-harness` component when the consumer-facing
  contract must be protected before implementation.
- Review selection and coordination: `review-orchestrator`. It owns the
  internal reviewers for design and impact, risk-specific, behavioral,
  operational, and finding-calibration reviews.

Use `engineering-compass` as a design principle when the user or repository
calls for readability, testability, or loose coupling.

## Planning rules

- For a small local change or a conventional mature-repository change, define
  focused criteria; inspect the nearest relevant implementation as evidence,
  then explicitly choose to reuse it, adapt it, or not follow it; implement,
  run targeted checks, and self-review. Existing code is not automatically a
  design authority.
- For every non-mechanical change, consider the relevant existing pattern
  before introducing an abstraction or named design pattern. Prefer a pattern
  only when it addresses a concrete change pressure, such as a responsibility
  boundary, variation point, integration boundary, or state/lifecycle
  concern. Do not introduce a pattern merely for symmetry or terminology.
- Do not follow an existing pattern when it has mixed responsibilities,
  harmful dependency direction, uncontrolled conditional growth, poor test
  seams, or known operational or compatibility risk. Record the chosen
  relationship to the closest precedent (reuse, adapt, or intentionally do
  not follow) and a short rationale in the implementation plan. Keep any
  corrective design local to the requested change unless a separate refactor
  is necessary and explicitly scoped.
- For high-risk or uncertain work, compose a plan with the relevant allowed
  reviewers before implementation.
- When implementing or changing complex logic, check whether distinct
  responsibilities or reasons to change are mixed together. Extract a
  clearly named helper only when it hides detail and makes the caller's
  control flow easier to follow; do not split code by line count alone.
- Treat repository-specific conventions as authoritative when they differ from
  the default workflow or size guidance here.
- When splitting work, make each stage independently reviewable and testable;
  document the dependency from each later branch/PR to its predecessor.
- When adding or changing documentation that contains a user-runnable command,
  API request, or configuration example, include a validation that exercises a
  representative example exactly as documented. Use an isolated fixture when
  the repository itself would make the example ambiguous or unsafe.
- Do not treat review skills as implementation owners; use their findings as
  plan inputs and verify the resulting changes yourself.
- If an active workflow state exists, resume or report it instead of creating a
  second state directory.

## Required route decision

```text
Primary execution: <direct|staged|parallel|comparative>
Supporting skills: <list or none>
Why: <evidence-based reason>
Rejected options: <option -> reason>
Required gates: <list>
```
