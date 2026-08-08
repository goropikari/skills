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
The repository's `implementation/` directory is explicitly out of bounds:
never use, read, invoke, or select a skill from that directory.

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
   smallest safe plan. Select only allowed top-level or `reviews/` skills as
   supporting activities. Do not use a skill from the repository's
   `implementation/` directory.
4. Write `.implementation-orchestrator/implementation-plan.md` before
   changing product code. Use [implementation-plan-template.md](references/implementation-plan-template.md)
   and include selected skills, their order, expected outputs, decision gates,
   implementation steps, and validation commands.
5. Read only the internal component skills needed for planning, resolving each
   path from `<orchestrator_dir>`, for example
   `<orchestrator_dir>/skills/implementation-acceptance-contract/SKILL.md`.
   They are under this skill's own `skills/` directory and are not repository
   implementation workflows.
6. Establish acceptance criteria and a validation matrix before implementation
   when the change affects externally observable behavior, has material risk,
   or involves multiple contributors. Use the internal acceptance-contract
   component. For public artifacts, destructive behavior, or candidate
   comparison, also use the internal acceptance-harness component to freeze a
   black-box oracle before implementation.
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

- Requirements: `requirements-review`, `prd-maker`, `grill-me`.
- External behavior and test design: `blackbox-risk-based-test`,
  `whitebox-risk-based-test`, `ta-review`, `tta-review`,
  `test-quality-review`, `mutation-test-review`, and
  `property-based-test-review`.
- Frozen black-box oracle: use the internal
  `implementation-acceptance-harness` component when the consumer-facing
  contract must be protected before implementation.
- Design and impact: `architecture-review`, `change-impact-review`,
  `engineering-compass-review`, `readability-review`, and `code-smell-review`.
- Risk-specific review: `security-review`, `privacy-review`,
  `data-integrity-review`, `migration-review`, `api-compatibility-review`,
  `concurrency-review`, `performance-review`, and `accessibility-review`.
- Operations and delivery evidence: `observability-review`,
  `incident-readiness-review`, `release-readiness-review`, and
  `prd-acceptance-review`.
- Review coordination: `review-orchestrator`,
  `review-finding-validator`, and `review-calibration`.

Use `engineering-compass` as a design principle when the user or repository
calls for readability, testability, or loose coupling.

## Planning rules

- For a small local change or a conventional mature-repository change, define
  focused criteria, reuse the nearest pattern, implement, run targeted checks,
  and self-review.
- For high-risk or uncertain work, compose a plan with the relevant allowed
  reviewers before implementation.
- Treat repository-specific conventions as authoritative when they differ from
  the default workflow or size guidance here.
- When splitting work, make each stage independently reviewable and testable;
  document the dependency from each later branch/PR to its predecessor.
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
