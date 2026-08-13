---
name: implementation-acceptance-harness
description: >-
  Internal component for implementation-orchestrator: create and freeze an
  implementation-independent black-box acceptance harness for externally
  observable, destructive, high-risk, or candidate-compared changes. Invoke
  only through implementation-orchestrator, not as a standalone workflow.
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
   Determine whether an existing frozen harness directly covers every new
   observable behavior. If it covers only unchanged behavior, add independent
   consumer-facing criteria and fixtures before freezing it; do not treat its
   regression pass as proof of the new contract.
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
         "required": true,
         "tags": ["consumer-entry"],
         "command": "...",
         "expected": "...",
         "test_path": "tests/acceptance/consumer_test.py"
       }
     ],
     "immutable_paths": [
       ".implementation-orchestrator/acceptance-harness/manifest.json",
       "tests/acceptance/consumer_test.py"
     ],
     "base_revision": "..."
   }
   ```

5. Add `module-identity`, `build-install`, and `consumer-entry` criteria when
   they apply. For destructive behavior, add a rejection/no-side-effect
   criterion.
6. Validate the planned harness:

   ```bash
   python3 "<orchestrator-dir>/scripts/validate_harness.py" \
     --stage plan .implementation-orchestrator/acceptance-harness/manifest.json
   ```

7. Freeze the harness before implementation. Record the current base revision
   or an explicit dirty-worktree baseline, add manifest and test paths to
   `immutable_paths`, and do not edit them while implementing candidates. Run
   the validator again with `--stage frozen --base <base-revision>` before
   accepting an implementation.
8. Run every criterion against each candidate or the direct implementation.
   Report `PASS`, `FAIL`, or `NOT RUN` with the exact command and observable
   result. A required `NOT RUN` blocks completion unless the user accepts the
   residual risk.

## Boundaries

- Keep the harness implementation-independent and consumer-facing.
- Do not treat a passing unit test that bypasses the consumer entry point as
  acceptance evidence.
- Do not silently modify frozen criteria to make an implementation pass.
