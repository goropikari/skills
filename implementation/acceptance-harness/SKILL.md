---
name: acceptance-harness
description: Create and freeze an executable black-box acceptance harness from a PRD or acceptance contract before implementation. Use for externally consumed CLIs, libraries, plugins, services, destructive workflows, implementation tournaments, or whenever multiple agents must be judged against the same observable contract.
---

# Acceptance Harness

Create an implementation-independent acceptance harness before product code is
written. The harness is the shared oracle for implementation agents, tournaments,
and final verification; it is not a post-hoc test summary.

Do not use this skill for a tiny internal refactor with no changed observable
behavior unless the user requests a harness.

## Workflow

1. Inspect the PRD, repository conventions, test commands, consumer entry point,
   existing tests, and current worktree state.
2. Convert every required behavior and important exceptional state into an
   `AC-*` criterion. Do not leave a supported edge case only as free text.
3. Create a black-box test for each required criterion. Test the built or
   installed artifact through its consumer-facing entry point; do not call
   internal APIs as the acceptance oracle.
4. Add `.acceptance-harness/manifest.json`, resolve this installed skill's
   directory, and run
   `python3 "<skill-directory>/scripts/validate_manifest.py" --stage plan .acceptance-harness/manifest.json`.
5. Add the manifest and harness test files to `immutable_paths`, then run the
   validator with `--stage frozen`. Record the harness base commit after the
   user or orchestrator freezes it.
6. Before selecting or accepting an implementation, run every criterion command
   against the candidate artifact. Run
   `python3 "<skill-directory>/scripts/validate_manifest.py" --stage frozen --base <harness-base>`
   to prove the candidate did not alter the harness.
7. Report each criterion as `PASS`, `FAIL`, or `NOT RUN` with its command and
   observable oracle. Required `NOT RUN` entries block completion unless the
   user explicitly accepts the residual risk.

## Required coverage

For every external artifact, include criteria tagged `consumer-entry` and
`module-identity` when a public module/package identity exists. Verify the
build/install target and invoke the artifact as a consumer would.

For destructive behavior, set the top-level `risks` value to include
`destructive` and include a `rejection-no-side-effect` criterion. For relevant
exceptional states, add explicit criteria rather than relying on a generic
error-path test.

Use a temporary fixture and isolated test data. Do not contact production
systems, require credentials, or use uncontrolled network access.

## Manifest

Use this minimal shape. Keep the manifest and the listed test files immutable
after the harness is frozen.

```json
{
  "version": 1,
  "artifact": {
    "kind": "cli",
    "build_command": "go build -o /tmp/git-br ./cmd/git-br",
    "consumer_command": "git br -D '^feature/'"
  },
  "risks": ["external-artifact", "destructive", "module-identity"],
  "immutable_paths": [
    ".acceptance-harness/manifest.json",
    "tests/acceptance/git_br_test.go"
  ],
  "criteria": [
    {
      "id": "AC-001",
      "required": true,
      "scenario": "A built helper is invoked through git br.",
      "test_path": "tests/acceptance/git_br_test.go",
      "command": "go test ./tests/acceptance -run TestConsumerEntry",
      "oracle": "The selected local branch is deleted and exit status is zero.",
      "tags": ["consumer-entry"]
    }
  ]
}
```

Use `module-identity` and `rejection-no-side-effect` tags when their
corresponding risk is declared. Add tags for domain-specific risks as useful.

## Tournament and verifier rules

- Create and freeze the harness before candidate worktrees are created.
- Give every candidate the same harness base commit and prohibit edits to its
  immutable paths.
- Have the orchestrator or verifier, not the candidate, run the common harness
  and supply its results to the judge.
- Disqualify candidates that change immutable paths or fail a required
  criterion. Candidate-written tests are supplemental evidence only.
- If all candidates fail, identify the strongest repairable candidate and rerun
  the unchanged harness after repair.

## Output

Return the manifest path, immutable paths, harness base commit, criterion
matrix, commands, results, and residual risks. State clearly whether the
harness is `PLANNED`, `FROZEN`, or `VERIFIED`.
