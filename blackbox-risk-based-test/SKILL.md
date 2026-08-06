---
name: blackbox-risk-based-test
description: Design risk-based tests from externally observable behavior, user workflows, business rules, requirements, acceptance criteria, APIs, and UI behavior. Use when prioritizing functional tests without relying on implementation details, especially for feature changes, regression analysis, acceptance testing, exploratory testing, and multi-agent implementation contracts.
---

# Blackbox Risk-Based Test

## Purpose

Design tests from the perspective of a user, client, business stakeholder, or
external system. Do not infer coverage from source-code structure. Use the
observable contract and the consequences of failure to decide what to test
first.

## Workflow

1. Identify the test basis: requirements, user stories, acceptance criteria,
   API contracts, UI flows, business rules, domain examples, incident history,
   and changed behavior.
2. Enumerate observable risk items. Include core workflows, invalid input,
   authorization-visible behavior, state transitions, data boundaries,
   interoperability, usability, accessibility, and regression surfaces.
3. Estimate each item's impact, likelihood, and uncertainty using `High`,
   `Medium`, or `Low`. Keep uncertainty separate from likelihood.
   Consider business loss, user harm, compliance, data integrity, reputation,
   and recovery difficulty for impact. Consider complexity, change size,
   novelty, usage frequency, defect history, and requirement uncertainty for
   likelihood.
4. Calculate `Base Risk = Impact score × Likelihood score`, where Low=1,
   Medium=2, and High=3. Assign priority deterministically: P0 for score 9
   or a critical/irreversible failure; P1 for score 6-8 or High impact with
   High uncertainty; P2 for score 3-5; and P3 for score 1-2. Raise the
   priority by one level when uncertainty is High and the result is difficult
   to observe, reproduce, or recover, up to P0. Explain any other override.
5. Map each priority risk to concrete test conditions and suitable techniques:
   equivalence partitions, boundary values, decision tables, state
   transitions, scenario tests, error guessing, exploratory sessions, or
   contract/interoperability tests.
6. Define test data, preconditions, actions, observable oracle, environment,
   and regression scope. Mark an oracle as unclear when expected behavior is
   not testable.
7. Record what is not tested, why it was deferred, and the resulting residual
   risk.

## Required Output

Produce a Markdown report with these sections:

```markdown
## Scope and Test Basis

## Risk Summary

### RISK-001: <observable risk>

- Impact: High|Medium|Low
- Likelihood: High|Medium|Low
- Uncertainty: High|Medium|Low
- Base risk score: <1-9>
- Priority: P0|P1|P2|P3
- Evidence:
- Failure consequence:
- Mitigations or existing controls:

## Prioritized Test Conditions

### TC-001: <condition>

- Covers: RISK-001
- Technique:
- Preconditions and data:
- Steps or scenario:
- Expected observable result:
- Automation: recommended|optional|not worthwhile

## Regression and Exploratory Coverage

## Not Run / Deferred Checks

## Residual Risks and Assumptions

## Acceptance Criteria Improvements
```

Use `NOT RUN` with a reason for unavailable execution. Distinguish confirmed
behavior from assumptions and open questions. Do not claim code-path coverage;
this skill is strictly behavior- and contract-oriented.

## Combination Guidance

Use before `multi-agent-tounament-development` to create the acceptance
contract and shared validation plan. Use `ta-review` when requirements or
business value need a broader review. Pair with `whitebox-risk-based-test`
when implementation details are available and technical risk matters.
