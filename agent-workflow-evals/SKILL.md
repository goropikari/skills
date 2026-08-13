---
name: agent-workflow-evals
description: Evaluate implementation workflows by running representative coding tasks against frozen black-box acceptance harnesses and recording correctness, verification completeness, stability, cost, and residual risk. Use when comparing or improving agent skills, implementation-orchestrator routes, or coding-agent reliability over time.
---

# Agent Workflow Evals

Evaluate generated implementation outcomes, not the prose quality of skills.
Use this skill only with tasks that have an implementation-independent,
black-box acceptance harness.

## Workflow

1. Define representative tasks across the risks that matter: local behavior,
   public contracts, destructive actions, persistence, authorization,
   concurrency, and performance where applicable.
2. Freeze each task's acceptance harness before running a workflow. Keep the
   harness, manifest, and fixtures immutable to evaluated agents.
3. Create `.agent-workflow-evals/manifest.json` and validate it with the
   bundled script before evaluation.
4. Run the named workflow against each task in a clean worktree. Record the
   resulting commit, commands, elapsed time, tool failures, and task-local
   implementation evidence.
5. Run every frozen harness independently after implementation. Do not accept
   a workflow's self-report as evidence.
6. Record task outcomes as `PASS`, `FAIL`, or `BLOCKED`. Separate harness
   failures, missing verification, environment failures, and accepted residual
   risks.
7. Compare results by task risk and workflow version. Treat a drop in required
   harness pass rate or verification completeness as a regression.
8. Send recurring failures to `session-learning`; update the narrowest owning
   component, route rule, test design rule, or validator. Do not change a
   frozen harness to make an evaluated workflow pass.

## Evaluation manifest

```json
{
  "version": 1,
  "workflows": [
    { "id": "WF-ORCHESTRATOR", "skill": "implementation-orchestrator" }
  ],
  "tasks": [
    {
      "id": "TASK-API-001",
      "harness": "tasks/api/.implementation-orchestrator/acceptance-harness/manifest.json",
      "risks": ["compatibility", "external-artifact"]
    }
  ]
}
```

Run:

```bash
python3 "<skill-dir>/scripts/validate_eval_manifest.py" \
  .agent-workflow-evals/manifest.json
```

## Reporting

For each workflow/task pair, record the harness result, acceptance-evidence
result, elapsed time, retries, changed scope, and residual risk. Summarize
results by risk class before drawing conclusions from a small sample.
