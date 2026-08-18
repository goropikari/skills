---
name: quality-modeling
description: Define explainable software-quality models by connecting quality characteristics to product factors, measures, instruments, evidence, and evaluation rules. Use when designing or revising a repository quality baseline, translating quality goals into observable checks, or extending a Quamoco-inspired quality model.
---

# Quality Modeling

Define the model that makes software quality assessable. Keep this Skill
generic: it describes what a quality concern means and how it can be observed;
it does not decide which concerns a particular repository must enforce.

## Model vocabulary

Represent each quality concern as a chain:

```text
quality characteristic → product factor → measure → instrument → evidence
```

- **Quality characteristic**: an abstract outcome such as maintainability,
  reliability, security, or performance.
- **Product factor**: an actionable property of the product, such as clear
  responsibility boundaries, controlled input handling, or recoverable errors.
- **Measure**: an observable question or value, such as a forbidden dependency,
  a test result, or a complexity distribution.
- **Instrument**: the source of evidence: a deterministic tool, test, runtime
  observation, or named review Skill.
- **Evidence**: the bounded output used to support a finding. Record what was
  observed, not what the instrument was expected to prove.

Read [model-schema.md](references/model-schema.md) for the recommended record
shape and examples. Read [gqm-and-calibration.md](references/gqm-and-calibration.md)
when turning stakeholder goals into metrics or deriving thresholds.

## QE artefact quality extension

When a repository creates requirements, acceptance criteria, test cases, or BDD
scenarios with an LLM, model their quality as a conditional extension rather
than a universal software-quality score:

```text
QE artefact quality
  → clarity, completeness, consistency, testability
  → rubric score, coverage/traces, contradiction and duplication findings
  → qe-artifact-baseline, embedding/lexical comparison, human review
  → versioned report with source IDs, raw scores, decisions, and open gaps
```

Treat semantic alignment (for example, cosine similarity) as corroborating
evidence for traceability, not as a proxy for correctness or safety. Record the
embedding model, preprocessing, threshold source, calibration sample, and
unmeasured blind spots. Keep the quality model generic; let
`repository-quality-baseline` decide whether these factors are applicable or
blocking for a particular repository.

## GQM design

Use Goal–Question–Metric before choosing a metric:

1. State the stakeholder, object, purpose, quality viewpoint, and context in a
   single goal.
2. Derive questions whose answers distinguish acceptable from risky quality.
3. Select the smallest set of metrics that answers the questions. Prefer
   metrics with evidence of validity for the target risk; do not select a
   metric merely because a tool can calculate it.
4. Record each metric's relationship back to its question and goal.

If the goal is early source-code risk estimation, say so explicitly. Do not
silently generalize source metrics to runtime reliability, user experience, or
business outcomes.

## Modeling workflow

1. State the quality outcome and the product boundary being assessed.
2. Decompose the outcome into factors that an implementer can change.
3. Define one or more measures for each factor. Prefer measures that can be
   repeated and compared over time.
4. Assign the smallest sufficient instrument. Use tools for stable pass/fail
   facts and review Skills for intent, trade-offs, and architecture.
5. Describe evidence, limitations, applicability, and confidence.
6. Define rating, aggregation, and evaluation rules separately from the model.
   A factor may be
   informative, required, or critical depending on the repository baseline.
7. Check for blind spots, double-counting, proxy measures, and incentives that
   could make the metric look good while the product gets worse.

## Design rules

- Keep the model explanatory rather than prescriptive.
- Do not equate a high weighted average with acceptable quality.
- Never let a proxy measure silently replace the quality outcome it represents.
- Keep subjective judgments explicit and attach their evidence and reviewer.
- Make unavailable evidence visible; do not turn “not measured” into “pass.”
- Prefer a small, high-signal factor set over an exhaustive catalogue.
- Distinguish product quality from process quality and from delivery readiness.
- Define factors so that an assessment can produce a concrete improvement
  action or a justified decision not to act.

## Handoff to a repository baseline

When a repository needs an enforceable policy, pass the model to
`repository-quality-baseline`. That Skill selects applicable factors, sets
thresholds and severity, registers instruments, and stores the resulting model
instance in `.quality/baseline.json`. Do not add repository-specific thresholds
to this Skill.

## Handoff to assessment

`coding-quality-gate` consumes the baseline and produces current evidence and
a decision through its internal assessment component. It must not invent a new
factor, threshold, or weighting scheme during a gate run. If the model is
inadequate, record the gap and propose a separate baseline/model revision.
