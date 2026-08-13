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

Read `.implementation-orchestrator/evidence.json` and use
[`evidence-schema.md`](../../references/evidence-schema.md) as the completion
contract. Record one result with bounded evidence for every required acceptance
criterion and selected check. A finding from a selected review must be repaired,
rejected with evidence, or retained as an explicitly accepted residual risk.

## Report

For every required check, report `PASS`, `FAIL`, or `NOT RUN` with the exact
command, exit status, and observable result. Put the command and result in the
evidence entry itself; do not rely on a broader command to imply that a more
focused check ran. Do not call an unavailable or unexecuted check successful.
Trace each acceptance criterion to evidence and list residual risk, changed
files, and any follow-up required before commit or PR.

For parallel or comparative routes, verify worktree/branch boundaries, common
base, candidate selection evidence, integration behavior, and the final
working tree. The verifier must not silently repair the implementation while
claiming to have independently verified it.

Before delivery, run:

```bash
python3 "<orchestrator-dir>/scripts/validate_evidence.py" \
  --stage final .implementation-orchestrator/evidence.json
```

Do not report `PASS` when this validation fails. An accepted residual risk must
identify the affected criterion or check, reason, and the user who accepted it.
