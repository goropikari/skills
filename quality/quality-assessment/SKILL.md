---
name: quality-assessment
description: Assess software or a change against a repository quality baseline using deterministic checks, tests, observations, and semantic review. Use after implementation, during quality-gate work, for regression assessment, or when reporting evidence-backed quality findings and improvement actions.
---

# Quality Assessment

Execute the quality model instance in `.quality/baseline.json`. Produce an
auditable decision from evidence; do not redesign the model while assessing a
change. Use [assessment-record.md](references/assessment-record.md) for the
output structure. Use the baseline's GQM links, rating functions, threshold
sources, and aggregation rules as the assessment contract.

## Assessment workflow

1. Read the task requirements, changed scope, baseline version, applicability,
   GQM goal/question/metric links, and prior state. Identify factors affected
   by the change.
2. Run the baseline's applicable deterministic instruments first. Preserve
   command, exit status, bounded output, timestamp, and scope.
3. Normalize raw metric values without discarding entity identity, distribution,
   outliers, or missing values. A skipped or
   unavailable instrument needs a reason and must not be reported as passing.
4. Convert raw values to ratings using the recorded threshold-, utility-, or
   probabilistic function. Preserve the raw value, rating, threshold source,
   and confidence.
5. Aggregate from leaf entities upward through the recorded product hierarchy.
   Retain worst entities and a drill-down path; do not let aggregation hide a
   critical local defect.
6. Perform semantic review for measures assigned to review Skills. Separate
   observed evidence from interpretation and make every finding location- or
   behavior-specific.
7. Map every applicable factor to `PASS`, `FAIL`, `BLOCKED`, or `NOT_APPLICABLE`.
   Include confidence, raw metrics, ratings, aggregate values, and evidence
   references.
8. Apply the baseline policy: critical defects and unmet required factors block
   delivery; optional weaknesses become notes; unknown required evidence is
   `BLOCKED`.
9. Record the assessment in `.quality/state.json` without exposing secrets or
   unbounded logs.
10. If the result is not passable, repair the implementation or tests and rerun
    the affected instruments, followed by the complete required set.
11. If the model, threshold, rating, or aggregation rule is wrong, stop changing
    the current result. Propose a versioned model/baseline revision separately.

## Evidence discipline

- Tools establish deterministic facts, not semantic correctness.
- Tests establish observed behavior for their covered cases, not all behavior.
- Review establishes a reasoned judgment, not a measured universal truth.
- A weighted score is useful for trends and prioritization only; it never
  overrides a critical failure or missing required evidence.
- A high-level score must remain traceable to the leaf entities and raw values
  that produced it.
- Use distribution-aware ratings for skewed metrics and document every
  benchmark transfer.
- Keep pre-existing failures separate from findings introduced by the change.
- State the smallest unknown that prevents a stronger conclusion.

## Decision rules

- `FAIL`: any critical defect or unmet required factor.
- `BLOCKED`: required evidence cannot be obtained because of environment,
  unavailable instrumentation, or an unresolved external dependency.
- `PASS_WITH_NOTES`: all required factors pass; only optional findings remain.
- `PASS`: all applicable required instruments and semantic checks pass with no
  blocking finding.

Use the baseline's exact policy and statuses. Do not relax a threshold because
the current change fails it, and do not promote an advisory observation to a
required rule during an assessment.

## Handoff boundaries

- `quality-modeling` defines the generic factors, measures, instruments,
  limitations, and GQM relationships.
- `repository-quality-baseline` selects and calibrates them for one repository.
- This Skill measures, rates, aggregates, and evaluates the calibrated instance.

When repeated assessment findings show that the expected normal has changed,
send the evidence to `repository-quality-baseline` for a separate baseline
update.
