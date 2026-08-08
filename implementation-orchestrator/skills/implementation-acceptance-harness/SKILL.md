---
name: implementation-acceptance-harness
description: >-
  Internal component for implementation-orchestrator: create and freeze an
  implementation-independent black-box acceptance harness for externally
  observable, destructive, high-risk, or candidate-compared changes. Do not
  invoke as a standalone workflow or read the repository's implementation/
  skills.
---

# Implementation Acceptance Harness

Create a shared observable oracle before product implementation. Use this
component only when a stable consumer-facing contract materially reduces risk:
public APIs, CLIs, libraries, plugins, services, destructive behavior, or
multiple implementation candidates. Do not add a harness for a tiny internal
refactor with no changed observable behavior.

## Workflow

1. Inspect the consumer entry point, build/install command, repository test
   conventions, current worktree, and requested behavior.
2. Convert required behavior and important exceptional states into stable
   criteria such as `AC-001`. Include expected results and rejection criteria.
3. For each criterion, define a command that exercises the built or installed
   artifact through its consumer-facing entry point. Do not use internal APIs
   as the acceptance oracle.
4. Create `.implementation-orchestrator/acceptance-harness/manifest.json` and,
   when needed, black-box test files beside it. The manifest must contain:

   ```json
   {
     "version": 1,
     "goal": "...",
     "consumer_entry": "...",
     "criteria": [
       {
         "id": "AC-001",
         "tags": ["consumer-entry"],
         "command": "...",
         "expected": "..."
       }
     ],
     "immutable_paths": [],
     "base_revision": "..."
   }
   ```

5. Add `module-identity`, `build-install`, and `consumer-entry` criteria when
   they apply. For destructive behavior, add a rejection/no-side-effect
   criterion.
6. Freeze the harness before implementation. Record the current base revision
   or an explicit dirty-worktree baseline, add manifest and test paths to
   `immutable_paths`, and do not edit them while implementing candidates.
7. Run every criterion against each candidate or the direct implementation.
   Report `PASS`, `FAIL`, or `NOT RUN` with the exact command and observable
   result. A required `NOT RUN` blocks completion unless the user accepts the
   residual risk.

## Boundaries

- Keep the harness implementation-independent and consumer-facing.
- Do not copy or invoke any skill from the repository's `implementation/`
  directory.
- Do not treat a passing unit test that bypasses the consumer entry point as
  acceptance evidence.
- Do not silently modify frozen criteria to make an implementation pass.
