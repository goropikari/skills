# Implementation evidence schema

Store the task record in `.implementation-orchestrator/evidence.json`. The
acceptance-contract component owns the plan-stage fields. The verification gate
owns `results` and the final decision evidence.

```json
{
  "version": 1,
  "acceptance_criteria": [
    { "id": "AC-001", "required": true, "expected": "..." }
  ],
  "risks": [
    { "id": "RISK-API-001", "type": "compatibility" }
  ],
  "selected_checks": [
    {
      "id": "CHECK-001",
      "risk_ids": ["RISK-API-001"],
      "required": true,
      "instrument": "api-compatibility-review"
    }
  ],
  "results": [
    { "id": "AC-001", "status": "PASS", "evidence": ["go test ./..."] }
  ],
  "residual_risks": []
}
```

Run `validate_evidence.py --stage plan` before implementation and `--stage
final` before delivery. Plan-stage `results` must be empty. A non-passing
required result needs an explicit entry in `residual_risks` with `subject_id`,
`reason`, and a user-provided
`accepted_by` value.
