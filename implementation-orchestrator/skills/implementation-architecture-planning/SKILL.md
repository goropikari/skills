---
name: implementation-architecture-planning
description: >-
  Internal component for implementation-orchestrator: select the smallest
  architecture and repository pattern that satisfies the change contract,
  preserving responsibility boundaries, dependency direction, compatibility,
  and testability. Do not invoke as the primary workflow.
---

# Implementation Architecture Planning

Inspect the closest existing implementation before inventing an abstraction.
Produce only the design needed to make the next implementation steps safe.

## Check

- ownership of changed behavior and data;
- callers, public boundaries, and dependency direction;
- error, transaction, configuration, concurrency, and lifecycle boundaries;
- compatibility and migration strategy;
- test seams and observable verification points;
- whether the design can be implemented as a smallest-change patch.

State decisions, alternatives rejected, assumptions, and human gates. Escalate
only decisions with material product, data, security, compatibility, or
operational consequences. Do not turn a local change into a new foundation.
