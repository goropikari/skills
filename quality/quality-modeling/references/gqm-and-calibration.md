# GQM, rating, and calibration

## Goal–Question–Metric

Use this compact record for each measurement family:

```json
{
  "goal": {
    "object": "source_code",
    "purpose": "estimate_quality_risk",
    "viewpoint": "developers",
    "quality": "maintainability",
    "context": "large_backend_service"
  },
  "question": "Where is maintainability risk concentrated?",
  "metric": {
    "id": "cyclomatic_complexity",
    "unit": "complexity_points_per_method",
    "entity": "method",
    "validity_basis": "predicts_post_release_defects in the benchmark"
  }
}
```

Every metric needs an interpretation, entity level, direction of goodness,
distribution notes, validity basis, and known limitations. A metric without a
question is an orphan measurement and should not affect a quality decision.

## Threshold derivation

Derive thresholds in this order:

1. Collect expert or domain thresholds and record their source.
2. Build a relevant benchmark population. Record language, architecture,
   system size, domain, inclusion rules, and sample count.
3. Inspect the distribution. Treat skewed or power-law metrics as such; do not
   use an arithmetic mean as a normality boundary.
4. Compare expert thresholds with benchmark quantiles and explain the choice.
5. Transfer quantiles only when the benchmark is sufficiently comparable.
6. Store the threshold, rationale, source, population, date, and confidence in
   the baseline.

Thresholds are policy parameters, not natural laws. Recalibrate them when the
population, architecture, language, or risk profile changes.

## Rating and aggregation

Choose a rating function that matches the metric:

- Use threshold levels for unbounded or heavy-tailed metrics.
- Use a utility function for bounded ratio metrics with defensible best and
  worst cases.
- Use probabilistic output when uncertainty matters more than a single score.

Aggregate in the product hierarchy so that a system score can be drilled down
to the entity that produced the risk. Use logarithmic or risk-emphasizing
aggregation when a small number of bad entities must remain visible. Use
simple averages when weights cannot be justified. Use weighted averages only
when stakeholder weights and their evidence are recorded.

Always retain leaf-level values and worst entities. An aggregate without a
drill-down path is unsuitable for remediation.
