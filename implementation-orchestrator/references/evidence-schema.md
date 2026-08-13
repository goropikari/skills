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
    {
      "id": "AC-001",
      "status": "PASS",
      "evidence": [
        "Command: go test ./cmd/goreadable -run TestExecute",
        "Outcome: exit 0; selected CLI scenarios passed"
      ]
    }
  ],
  "residual_risks": []
}
```

Run `validate_evidence.py --stage plan` before implementation and `--stage
final` before delivery. Plan-stage `results` must be empty. A non-passing
required result needs an explicit entry in `residual_risks` with `subject_id`,
`reason`, and a user-provided
`accepted_by` value.

For final results, record the exact command or review invocation and its
observable outcome in `evidence`. A superset command is valid only when the
entry identifies the focused behavior it exercised.
