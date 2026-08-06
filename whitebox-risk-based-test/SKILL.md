---
name: whitebox-risk-based-test
description: Design risk-based tests from source code, control flow, data flow, architecture, dependencies, concurrency, configuration, and runtime behavior. Use when prioritizing implementation-focused tests, code review validation, unit/integration coverage, mutation resistance, technical regression analysis, or high-risk changes such as authentication, migrations, infrastructure, and performance work.
---

# Whitebox Risk-Based Test

## Purpose

Design tests using knowledge of how the system is implemented. Prioritize code
and architecture areas where a defect is both plausible and costly. Use this
skill to complement externally observable tests; do not treat line or branch
coverage alone as evidence of adequate risk coverage.

## Workflow

1. Establish the technical test basis: diff, call graph, architecture,
   interfaces, data model, configuration, dependency behavior, tests, logs,
   metrics, and deployment constraints. Capture the base revision and changed
   components when reviewing a change.
2. Trace affected entry points, branches, error paths, state changes, data
   ownership, retries, transactions, caching, resource lifetimes, and external
   calls. Identify direct and indirect callers.
3. Enumerate implementation risk items. Consider security boundaries,
   authorization decisions, parsing and validation, data corruption,
   migration compatibility, concurrency, cancellation, failure recovery,
   resource leaks, performance bottlenecks, configuration drift, dependency
   failures, observability, and portability.
4. Estimate impact, likelihood, and uncertainty using `High`, `Medium`, or
   `Low`. Keep uncertainty separate from likelihood. Consider
   blast radius, recoverability, exposure, affected data, operational cost,
   change complexity, coupling, code churn, novelty, and historical defects.
5. Calculate `Base Risk = Impact score × Likelihood score`, where Low=1,
   Medium=2, and High=3. Assign priority deterministically: P0 for score 9
   or a critical/irreversible failure; P1 for score 6-8 or High impact with
   High uncertainty; P2 for score 3-5; and P3 for score 1-2. Raise the
   priority by one level when uncertainty is High and the result is difficult
   to observe, reproduce, or recover, up to P0. Explain any other override and
   do not substitute coverage percentages for risk analysis.
6. Select tests and analyses that expose each risk: unit tests, branch and
   condition tests, MC/DC where safety-critical, data-flow tests, property or
   mutation tests, integration/contract tests, fault injection, race/stress
   tests, resource-leak checks, performance tests, static analysis, and
   migration/recovery rehearsals.
7. Check testability: controllability, observability, isolation,
   determinism, cleanup, test data, mocks/fakes, and failure injection. Report
   design changes needed when a critical risk cannot be tested reliably.
8. Record unexecuted checks, coverage limitations, and residual technical
   risk. Never infer a successful validation from an unrun command.

## Required Output

Produce a Markdown report with these sections:

```markdown
## Scope, Baseline, and Technical Test Basis

## Risk Summary

### RISK-001: <implementation risk>

- Components and paths:
- Impact: High|Medium|Low
- Likelihood: High|Medium|Low
- Uncertainty: High|Medium|Low
- Base risk score: <1-9>
- Priority: P0|P1|P2|P3
- Evidence:
- Failure mode and blast radius:
- Existing controls:

## Prioritized Test and Analysis Conditions

### TC-001: <condition>

- Covers: RISK-001
- Level: unit|component|integration|system|operational|static
- Technique:
- Setup and fault injection:
- Oracle or observable evidence:
- Required validation command:
- Automation: required|recommended|optional

## Coverage and Testability Assessment

## Not Run / Deferred Checks

## Residual Technical Risks

## Recommended Implementation or Observability Changes
```

Use `NOT RUN` with a reason for unavailable execution. Separate confirmed
defects from risks, assumptions, and questions. Point to concrete files,
symbols, branches, data paths, or runtime boundaries when evidence exists.

## Combination Guidance

Use after `multi-agent-tounament-development` candidates are available to
compare technical risk coverage, or before implementation to define focused
validation conditions. Pair with `security-review`, `data-integrity-review`,
`migration-review`, `concurrency-review`, or `performance-review` when those
risks are material. Pair with `blackbox-risk-based-test` to ensure technical
coverage still protects user-visible behavior.
