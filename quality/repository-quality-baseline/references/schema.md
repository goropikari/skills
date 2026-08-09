# Quality state schema

The schema is intentionally small and JSON-based so it can be inspected without extra tooling.

## `.quality/baseline.json`

Required top-level fields:

```json
{
  "schema_version": 1,
  "baseline_version": "1.0.0",
  "repository": { "root": "." },
  "quality_model": {
    "source": "quality-modeling",
    "version": "1.0.0",
    "characteristics": ["maintainability", "reliability"],
    "factors": [
      {
        "id": "maintainability.responsibility_separation",
        "applicable": true,
        "required": true,
        "severity": "major",
        "gqm": {
          "goal": "Estimate maintainability risk in source code from the developer viewpoint.",
          "questions": ["Where is maintainability risk concentrated?"],
          "metrics": ["cyclomatic_complexity"]
        },
        "measures": ["single_responsibility_review", "cyclomatic_complexity"],
        "rating": {
          "method": "threshold",
          "levels": ["very_low", "low", "medium", "high", "very_high"]
        },
        "thresholds": {
          "source": "benchmark-2026-01",
          "population": "comparable production Java services",
          "quantiles": [0.95, 0.99, 0.995, 0.999],
          "confidence": "medium"
        },
        "aggregation": {
          "entity_hierarchy": ["method", "class", "file", "module", "system"],
          "method": "logarithmic_risk_emphasis",
          "retain_worst_entities": 10
        }
      }
    ]
  },
  "repository_tools": [
    {
      "id": "api-contract",
      "path": ".quality/tools/check_api_contract.py",
      "purpose": "Detect incompatible API changes",
      "command": "python3 .quality/tools/check_api_contract.py",
      "required": true
    }
  ],
  "analysis_skills": [
    { "name": "requirements-review", "applied": true, "evidence": "..." }
  ],
  "mechanical_checks": [
    {
      "id": "test",
      "command": "npm test",
      "required": true,
      "when": "if applicable"
    }
  ],
  "must_quality": [
    {
      "id": "requirements",
      "rule": "Task requirements are demonstrably satisfied",
      "severity": "critical"
    }
  ],
  "performance_quality": [
    {
      "id": "readability",
      "rule": "Keep the change easy to understand",
      "severity": "non_blocking"
    }
  ],
  "critical_defects": [
    "Known security vulnerability introduced by the change",
    "Data loss, corruption, or unrecoverable migration behavior",
    "Breaking public API without an approved compatibility decision"
  ],
  "assumptions": []
}
```

Commands are documentation for the agent and should be executable from the repository root. Keep shell-specific syntax out of `command` unless the repository explicitly requires it.

## `.quality/state.json`

Record the latest run with `schema_version`, `baseline_version`, `run_id`, `started_at`, `finished_at`, `result`, `checks`, `findings`, `changed_scope`, and `notes`. Each check should include `id`, `status`, `command`, `exit_code`, and `evidence`. Allowed results are `PASS`, `PASS_WITH_NOTES`, `FAIL`, and `BLOCKED`.
