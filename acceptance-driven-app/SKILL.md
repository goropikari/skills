---
name: acceptance-driven-app
description: >-
  Drive Web/API application development from acceptance criteria through
  implementation, verification, and PR-ready evidence. Use for new apps and
  changes to existing apps when work should be acceptance-test-driven,
  risk-aware, gated by review, and traceable to a commit and pull request.
---

# Acceptance-Driven App Workflow

Use the bundled `scripts/workflow.py` to manage state in the target project's
`.acceptance-driven-app/` directory. Do not reuse `.dev-workflow-phase/`; this workflow
has its own state and artifact format.

## Commands

Resolve the installed skill directory and run:

```text
$acceptance-driven-app
$acceptance-driven-app next
$acceptance-driven-app review
$acceptance-driven-app approve
$acceptance-driven-app status
$acceptance-driven-app auto
```

`auto` advances through the current phase, stopping at the next phase gate.
Never use it to ignore a blocker. A user instruction to auto-advance is an
explicit approval for the encountered gates in that phase; record the mode in
the state and artifacts.

## Operating rules

1. Inspect the repository before asking for information: branch, worktree,
   existing changes, app type, framework, CI, test/lint/build commands, API
   contracts, and project conventions.
2. Preserve unrelated uncommitted changes. Continue only when the requested
   scope can be isolated; stop if files or dependencies overlap materially.
3. Work through these phases:

   ```text
   bootstrap → acceptance-contract → design → implement-loop → verification → pr-ready
   ```

4. Stop at each phase gate for `review` and `approve`, unless the user
   explicitly requests `auto`. `approve` is not permission to skip failed
   acceptance criteria.
5. In `acceptance-contract`, create `acceptance-contract.md` with `AC-*`
   criteria, Gherkin scenarios, constraints, risks, and a validation matrix.
   Every criterion must have an observable expected result and validation
   command or manual procedure.
6. In `implement-loop`, select one unmet `AC-*` at a time. Establish a failing
   test or explicit failing observable (`red`), design and implement the
   smallest change, then rerun the condition (`green`). Record evidence before
   selecting the next criterion.
7. Apply mandatory gates to every change: applicable acceptance tests,
   regression checks, basic security checks, and evidence completeness. Add
   performance, compatibility, data-integrity, observability, accessibility,
   or other gates according to risk.
8. If a check cannot run, record `NOT RUN`, the exact reason, impact,
   alternative evidence, and residual risk. Important unverified criteria
   block PR readiness unless the user explicitly accepts the residual risk.
9. Before `pr-ready`, inspect the final diff and create a work branch and
   commit. Do not push or create the remote PR unless explicitly instructed.
10. Generate PR-ready evidence containing summary, changed files, AC matrix,
    executed commands and outcomes, review results, assumptions, and residual
    risks. Do not claim a check passed unless it actually ran.

## Artifacts

Keep artifacts under `.acceptance-driven-app/`:

```text
state.json
CURRENT_STEP.md
00_bootstrap.md
acceptance-contract.md
design.md
iterations/AC-001.md
verification.md
pr.md
```

The script owns `state.json` and `CURRENT_STEP.md`. The agent owns the other
artifacts and must update them at the relevant phase. Keep stable IDs (`AC-*`,
`VM-*`, `RISK-*`) so implementation and PR evidence remain traceable.

## Phase gates

- `bootstrap`: repository context and scope are recorded.
- `acceptance-contract`: requirements become executable behavioral contracts.
- `design`: architecture, interfaces, data changes, risks, and test strategy
  are recorded.
- `implement-loop`: each acceptance criterion is red, implemented, and green.
- `verification`: mandatory and risk-selected checks run; failures and `NOT
  RUN` items are explicit.
- `pr-ready`: diff, branch, commit, and PR evidence are complete.

Do not deploy or define post-release monitoring; those are outside this
skill's responsibility.
