---
name: implementation-acceptance-contract
description: >-
  Internal component for implementation-orchestrator: turn a material
  software change into testable acceptance criteria, risks, and a validation
  matrix before implementation. Use for external behavior, destructive work,
  high-risk changes, or multiple implementation candidates.
---

# Implementation Acceptance Contract

Define what must be true before choosing how to implement. Keep criteria
observable and independent of the implementation design.

## Produce

1. Goal and non-goals.
2. Acceptance criteria with stable IDs, expected results, and affected scope.
3. Prioritized risks and explicit rejection/no-side-effect criteria for
   destructive behavior.
4. Validation matrix mapping each criterion to a command, fixture, or manual
   check and its observable oracle.
5. Assumptions and open questions.

Create `.implementation-orchestrator/evidence.json` using
[`evidence-schema.md`](../../references/evidence-schema.md), then run:

```bash
python3 "<orchestrator-dir>/scripts/validate_evidence.py" \
  --stage plan .implementation-orchestrator/evidence.json
```

The plan must name every required acceptance criterion, material risk, and
selected check. Do not add final results during contract creation.

For a public CLI, library, plugin, service, or installable artifact, include
consumer-entry, module/package identity when applicable, and build/install
criteria. If candidates will be compared, freeze the contract and prevent
candidate changes to the harness before implementation.

Do not create a heavyweight acceptance harness for a tiny internal change with
no changed observable behavior.
