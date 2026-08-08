---
name: implementation-verification-gate
description: >-
  Internal component for implementation-orchestrator: verify an implementation
  against acceptance criteria, regression checks, formatting, lint, build,
  security, compatibility, and operational evidence appropriate to the change.
  Do not invoke as the primary workflow.
---

# Implementation Verification Gate

Run the validation matrix from the selected route. Add focused checks for
changed branches and preserve the project's normal test, format, lint, build,
and security commands.

## Report

For every required check, report `PASS`, `FAIL`, or `NOT RUN` with the exact
command and observable result. Do not call an unavailable or unexecuted check
successful. Trace each acceptance criterion to evidence and list residual
risk, changed files, and any follow-up required before commit or PR.

For parallel or tournament routes, verify worktree/branch boundaries, common
base, candidate selection evidence, integration behavior, and the final
working tree. The verifier must not silently repair the implementation while
claiming to have independently verified it.
