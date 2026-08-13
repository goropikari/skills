---
name: implementation-change-analysis
description: >-
  Internal component for implementation-orchestrator: classify a requested
  software change by repository maturity, scope, observable behavior, risk,
  uncertainty, and delivery constraints before selecting an implementation
  workflow. Do not invoke as the primary workflow.
---

# Implementation Change Analysis

Produce evidence for route selection. Inspect before asking questions.

## Analyze

Record:

- repository maturity: greenfield, newly established, or mature;
- change shape: feature, bug fix, refactor, migration, infrastructure, or
  documentation-only;
- scope: local, cross-cutting, multi-phase, or product-wide;
- observable contract: none, internal, API/CLI/UI, data format, or destructive;
- risk: security, privacy, financial, data integrity, compatibility,
  concurrency, performance, or operational risk;
- uncertainty: settled design, one plausible design, or materially competing
  designs;
- execution constraints: human gates, parallel work, worktree isolation,
  existing workflow state, and available validation commands.

## Decide

Recommend the smallest route that protects the highest risks. A broad PRD is
not by itself evidence for a staged or comparative route; distinguish a new
app, acceptance-harness need, and ordinary Web/API work.

Return the route decision in the orchestrator's required format and include the
repository evidence supporting it. If evidence is missing, name the smallest
fact needed to proceed and use a conservative route meanwhile.
