---
name: coding-quality-gate
description: Orchestrate quality assessment and stabilize coding-agent changes against a repository quality model instance. Use after implementing or modifying code, before delivery or review, when tests/builds need a consistent gate, or when a change must be repaired until it meets repository quality requirements.
---

# Coding Quality Gate

Prevent below-baseline code from reaching the user. Treat `baseline.json` as
the calibrated quality-model instance and `state.json` as the assessment audit
trail. This Skill owns orchestration, deterministic execution, assessment,
repair, and delivery readiness. Its `quality-assessment` procedure is an
internal component, not a directly invoked skill.

Use the bundled deterministic tools before asking an AI to reason about quality:

```bash
python3 <skill-dir>/scripts/run_quality_gate.py --repo-root .
python3 <skill-dir>/scripts/build_quality_context.py --repo-root . > /tmp/quality-context.md
```

The runner executes the exact commands declared by `mechanical_checks`, including repository-specific inspection tools, applies required/optional semantics, redacts likely secrets, bounds captured output, and writes the result to `.quality/state.json`. The context builder gives the semantic reviewer only the baseline, failures, changed scope, and a bounded diff. Do not paste full logs or the entire repository into the model when this packet is sufficient.

## Automatic execution

Run the bundled Python tools yourself as part of the normal Agent workflow. Do not stop after printing commands or ask the user to run tests, build, or inspection scripts. After implementation, automatically run the mechanical gate, inspect its result, repair failures when the cause is in scope, rebuild the compact context packet, and complete semantic review.

Ask the user before continuing only when the action requires a policy decision, changes the quality baseline, accesses an external authenticated service, performs a destructive operation, or remains blocked by an environment issue after safe local alternatives are exhausted. A routine read-only Python quality tool is not a reason to pause for confirmation.

Read [tool-vs-ai.md](references/tool-vs-ai.md) before evaluating Must Quality. Classify each rule as `TOOL`, `AI`, or `BOTH`, and report tool evidence separately from semantic judgment.

## Preconditions

1. Find `.quality/baseline.json` at the repository root.
2. If it does not exist, invoke `$repository-quality-baseline` first. Do not invent a repository-specific baseline silently. Run its initializer and inspection tools automatically.
3. Read the current task requirements, changed files, repository guidance, and the baseline. Determine the smallest relevant check set, but never skip a required check without recording why.
4. Use the internal `quality-assessment` component with the baseline path and
   changed scope. Do not create new factors, thresholds, or weights during the
   gate run.

This Skill is the post-implementation gate. Let the task-specific implementation Skill own planning and code changes; let this Skill own evidence collection, quality classification, repair, and delivery readiness.

## Gate workflow

1. Inspect the diff and map each requirement to implementation and tests. Identify public API, persistence, security, concurrency, migration, and compatibility risks.
2. Automatically run `run_quality_gate.py` first. Run every applicable `mechanical_checks` entry through the script so exit codes, timeouts, redaction, and state recording are consistent. Prefer the repository's documented commands and deterministic tools: build, typecheck, lint, unit/integration tests, generated-file checks, and security/static analysis.
3. Classify failures as implementation failure, environment/tooling failure, flaky test, or unrelated pre-existing failure. Preserve raw command, exit code, and concise evidence in the result.
4. Automatically generate `build_quality_context.py` output and use it as
   bounded evidence for the internal `quality-assessment` component. Perform
   semantic review against the selected quality factors, `must_quality`, and
   the task. Check behavior, edge cases, error handling, scope, architecture
   fit, maintainability, and meaningful tests. Use Performance Quality only
   after all Must Quality rules pass.
5. Apply a Quality Gate:

   - `FAIL` for any critical defect or unmet Must Quality rule;
   - `BLOCKED` when required evidence cannot be obtained because of an external/environment issue;
   - `PASS` only when all applicable required checks and Must Quality rules pass;
   - `PASS_WITH_NOTES` only for non-blocking Performance Quality observations.

6. If the result is not passable, repair the implementation or tests, rerun affected checks, then rerun the complete required set. Do not relax the baseline to accommodate the change.
7. Update `.quality/state.json` with the baseline version, changed scope, check evidence, findings, gate result, and timestamp. Keep the record concise and factual.
8. Deliver only when the gate is `PASS` or the user explicitly accepts a documented exception. Report exceptions and unverified checks prominently.

For every Must Quality rule, state what a tool established, what AI established, and what remains unknown. When a stable repeated semantic judgment can be converted into a deterministic oracle, propose or create a repository-specific inspection tool through `$repository-quality-baseline`.

## Non-negotiable rules

- Mechanical evidence cannot prove semantic correctness; semantic review cannot replace a failing build or test.
- A high average score never compensates for a critical defect.
- Do not report success from a command that was not actually run.
- Do not modify unrelated pre-existing failures unless the task requires it.
- Do not expose secrets or sensitive command output in `state.json`.

Read [evaluation.md](references/evaluation.md) for the finding and state-recording format.
