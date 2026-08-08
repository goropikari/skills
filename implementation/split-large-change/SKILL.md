---
name: split-large-change
description: Decompose an oversized AI-generated code change into reviewable, responsibility-based branches and pull requests. Use when a diff spans multiple responsibilities, layers, features, migrations, refactors, or operational changes; when one PR is too large to review safely; or when the user asks to split a branch/PR. Preserve behavior and dependency order, and produce an executable branch/PR plan before making changes.
---

# Split Large Changes

Turn a large change into a small sequence of coherent PRs. Split by responsibility and dependency, not by an arbitrary number of files or lines. The result must let each PR be understood, tested, reviewed, and reverted independently as far as the architecture allows.

## Workflow

### 1. Establish the change boundary

Inspect the repository guidance, worktree status, current branch, base branch, commits, diff statistics, changed files, tests, build commands, and any stated acceptance criteria. Preserve unrelated user changes. Do not rewrite history or create branches until the plan is accepted when the user requested planning only.

Identify whether the large change is:

- an uncommitted working-tree change;
- one or more commits on the current branch; or
- a proposed change described only in a request or PR.

Use the actual merge base for comparisons. Record assumptions, especially when the intended base branch is unknown.

### 2. Map responsibilities and coupling

Group changed behavior into responsibilities such as domain rules, persistence/schema, API or UI contract, adapters/integrations, migration, tests, documentation, and operational configuration. For every group, record:

- the responsibility and user-visible outcome;
- owning modules/files and their current state;
- inputs, outputs, public contracts, and data ownership;
- dependencies on other groups;
- required tests and rollback concerns.

Trace callers and consumers before deciding that a file belongs in a slice. A shared file may need a preparatory extraction or a narrowly scoped compatibility change. Flag generated files, lockfiles, formatting churn, and unrelated cleanup as noise or separate work.

### 3. Choose slice boundaries

Prefer the smallest vertical slices that deliver a coherent responsibility. A slice should have one review question, one clear reason to exist, and a testable outcome. Keep implementation and its contract tests together unless a pre-existing harness or migration policy requires otherwise.

Use these rules:

- Put prerequisites before consumers; make dependency edges explicit.
- Keep schema/data migrations separate from feature behavior when they can be deployed safely, but include compatibility code in the migration or preparation PR.
- Keep pure mechanical moves separate from semantic changes only when that materially improves reviewability and does not create a misleading standalone PR.
- Do not split a transaction, invariant, authorization rule, or atomic public behavior across PRs merely to reduce diff size.
- Avoid PRs that only move half of a responsibility and leave the branch broken, unbuildable, or untestable, unless the repository explicitly supports that intermediate state.
- Keep refactors separate from behavior changes when the refactor can be proven behavior-preserving; otherwise combine the minimum refactor needed for the behavior.
- Place docs, dashboards, and rollout controls with the behavior they describe unless they have an independent lifecycle.

If two responsibilities are inseparable, state why and keep them in one PR. If a split would require risky history surgery, propose a fresh branch/cherry-pick or stacked branch plan instead of destructive commands.

### 4. Select branch and PR topology

Choose one explicitly:

- **Independent branches:** each PR targets the same base and can merge in any order. Use only when the slices are genuinely independent.
- **Stacked branches:** `base -> prerequisite -> consumer -> follow-up`, with each PR targeting its immediate parent. Use when dependencies are real and the intermediate commits are valid.
- **Single PR:** use when the change has an inseparable invariant, atomic deployment requirement, or no safe reviewable seam. Recommend follow-up refactors if useful.

For every branch/PR, define its parent/base, title, scope, excluded work, dependency links, migration/rollout order, test commands, acceptance criteria, rollback plan, and expected review question. Keep each branch free of unrelated formatting or cleanup.

### 5. Validate the decomposition

Check that:

1. Every changed file and behavior is assigned exactly once, or explicitly marked shared/generated/noise.
2. The dependency graph is acyclic and merge order is clear.
3. Each PR has a meaningful diff and a passing build/test state appropriate to its intermediate contract.
4. Public behavior, data compatibility, permissions, observability, and rollback remain covered.
5. The final union of slices equals the original intended change, with no silent omissions.

When implementation is requested, execute the plan in order, creating branches and commits only within the user's repository scope. After each slice, inspect the diff against its parent and run focused tests; run the full relevant verification after integration. Never use `reset --hard`, force-push, or destructive cleanup to manufacture a split without explicit authorization.

## Required output

Return a compact responsibility matrix and an ordered PR table. Include:

- detected base, current branch, and change boundary;
- responsibility groups and dependency edges;
- branch name, parent branch, PR title, and exact scope for each slice;
- files/behaviors deliberately excluded or deferred;
- acceptance tests, verification commands, rollout and rollback notes;
- unresolved risks and whether the split is `READY`, `NEEDS DECISION`, or `NOT SAFELY SPLIT`.

For an implementation task, also report created branch/commit identifiers, verification results, and any remaining integration work. Do not claim a split is complete if any slice is untested, unbuildable, or missing from the final coverage map.

## Common failure modes

- **Layer-only splitting:** separate model/controller/test PRs that cannot be understood or run independently. Recombine into vertical responsibility slices.
- **File-count splitting:** divide files at an arbitrary threshold while splitting one invariant. Restore atomicity.
- **Hidden dependency:** a later PR relies on an unmerged commit or migration. Make the edge and target explicit.
- **Refactor camouflage:** bury a behavior change in a broad rename or cleanup. isolate mechanical work or reduce it to the required seam.
- **Test-afterthought:** postpone tests until the final PR. Move the relevant contract and regression checks into each slice.
