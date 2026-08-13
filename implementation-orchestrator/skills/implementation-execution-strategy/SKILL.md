---
name: implementation-execution-strategy
description: >-
  Internal component for implementation-orchestrator: choose direct,
  staged, parallel, or comparative execution for a software change from its
  scope, risk, uncertainty, dependencies, and repository state. Do not invoke
  as the primary workflow.
---

# Implementation Execution Strategy

Choose one execution mode:

- **Direct**: small, local, low-risk, or conventional change with one clear
  design.
- **Staged**: cross-cutting work with dependency order or human design gates.
- **Parallel**: independent, reviewed work units with separable worktree
  scope.
- **Comparative**: high-impact or materially uncertain change where independent
  implementations can be compared using the same frozen contract.

Do not parallelize dependent work, and do not use comparison to compensate for
an unclear requirement. Preserve the caller worktree and existing workflow
state. State the mode, prerequisites, worktree policy, and fallback if a gate
cannot be satisfied.
