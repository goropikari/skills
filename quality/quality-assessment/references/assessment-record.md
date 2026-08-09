# Assessment record

Keep the assessment compact, reproducible, and traceable to the baseline
version.

```json
{
  "schema_version": 1,
  "baseline_version": "1.2.0",
  "result": "PASS_WITH_NOTES",
  "changed_scope": ["src/orders"],
  "factors": [
    {
      "id": "maintainability.responsibility_separation",
      "status": "PASS",
      "confidence": "high",
      "metrics": [
        {
          "id": "cyclomatic_complexity",
          "entity": "src/orders/Checkout.java:submit",
          "raw_value": 8,
          "rating": 3.2,
          "threshold_source": "baseline:benchmark-2026-01"
        }
      ],
      "aggregate": {
        "method": "logarithmic_risk_emphasis",
        "value": 3.7,
        "worst_entities": ["src/orders/Checkout.java:submit"]
      },
      "evidence": ["architecture-review: finding-001", "test: unit-42"],
      "unknowns": []
    }
  ],
  "findings": [],
  "notes": ["Performance measure not applicable to this change"]
}
```

Every finding should include severity, location or behavior, observed
evidence, impact, and remediation or disposition. The state record is an audit
trail, not a replacement for the baseline contract.
