# Quality model record

Use this shape when documenting a factor in a model or baseline. Adapt field
names to the repository's JSON schema, but preserve the distinction between
meaning, measurement, evidence, and policy.

```json
{
  "id": "maintainability.responsibility_separation",
  "characteristic": "maintainability",
  "factor": "responsibility_separation",
  "intent": "Each component has a small, understandable reason to change.",
  "measures": [
    {
      "id": "single_responsibility_review",
      "question": "Are unrelated reasons to change coupled in one component?",
      "instrument": {
        "kind": "review_skill",
        "name": "architecture-review"
      },
      "evidence": "Finding with file, symbol, behavior, and impact",
      "limitations": "Requires semantic judgment; does not prove runtime behavior."
    }
  ],
  "applicability": "Production application code",
  "default_confidence": "medium"
}
```

Use `kind: tool` for deterministic commands, `kind: test` for executable
behavioral evidence, `kind: observation` for runtime or operational evidence,
and `kind: review_skill` for semantic assessment. Keep threshold, severity,
required status, and exceptions in the repository baseline rather than here.
