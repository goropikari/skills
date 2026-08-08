---
name: implementation-execution-strategy
description: >-
  Internal component for implementation-orchestrator: choose direct,
  staged, parallel, or tournament execution for a software change from its
  scope, risk, uncertainty, dependencies, and repository state. Do not invoke
  as the primary workflow.
---

# Implementation Execution Strategy

Choose one execution mode:

- **Direct**: small, local, low-risk, or conventional change with one clear
  design.
- **Staged**: cross-cutting work with dependency order or human design gates;
  use `dw-phase` when phase state is valuable.
- **Parallel**: independent reviewed phases with separable worktree scope;
  use `dw-phase-parallel-light` only after phase design is reviewed.
- **Tournament**: high-impact or materially uncertain change where independent
  implementations can be compared using the same frozen contract.
- **End-to-end tournament flow**: requirements, acceptance, phase design,
  parallel execution, tournament, and integration are all in scope; use
  `dw-phase-tournament-flow`.

Do not parallelize dependent work, and do not use a tournament to compensate for
an unclear requirement. Preserve the caller worktree and existing workflow
state. State the mode, prerequisites, worktree policy, and fallback if a gate
cannot be satisfied.
