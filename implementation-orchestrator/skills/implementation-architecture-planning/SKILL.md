---
name: implementation-architecture-planning
description: >-
  Internal component for implementation-orchestrator: select the smallest
  architecture and repository pattern that satisfies the change contract,
  preserving responsibility boundaries, dependency direction, compatibility,
  and testability. Do not invoke as the primary workflow.
---

# Implementation Architecture Planning

Inspect the closest relevant implementations before inventing an abstraction.
Treat them as evidence of conventions and constraints, not as automatically
correct designs. Produce only the design needed to make the next
implementation steps safe.

## Check

- ownership of changed behavior and data;
- callers, public boundaries, and dependency direction;
- error, transaction, configuration, concurrency, and lifecycle boundaries;
- compatibility and migration strategy;
- test seams and observable verification points;
- whether the design can be implemented as a smallest-change patch.

## Existing-pattern decision

For each material boundary or abstraction, inspect the closest relevant
precedent and choose one relationship:

- **Reuse** when the precedent has an appropriate responsibility boundary,
  dependency direction, test seam, and complexity for this change.
- **Adapt** when its local convention is useful but its boundary, API, or
  behavior needs a contained adjustment.
- **Intentionally do not follow** when it mixes responsibilities, has harmful
  dependency direction, uncontrolled conditional growth, weak test seams, or
  known operational or compatibility risk.

State the selected relationship and a short rationale in the implementation
plan. A named design or architecture pattern is justified only when it solves
a concrete change pressure: a variation point, responsibility or integration
boundary, state/lifecycle concern, or compatibility constraint. Do not add
one merely to match nearby code, create symmetry, or use pattern terminology.

If a precedent is unsuitable, do not expand the requested work into a broad
cleanup. Isolate the new design behind the smallest viable boundary; propose a
separate refactor only when it is required to make the requested change safe.

State decisions, alternatives rejected, assumptions, and human gates. Escalate
only decisions with material product, data, security, compatibility, or
operational consequences. Do not turn a local change into a new foundation.
