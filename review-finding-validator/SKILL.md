---
name: review-finding-validator
description: Validate code review findings against the actual source, tests, specifications, and observable behavior. Use when reviewing AI or human findings for false positives, duplicate findings, incorrect locations, unsupported severity, weak evidence, or unsafe remediation suggestions.
---

# Review Finding Validator

Validate review findings; do not perform a new broad review and do not modify source code.

## Inputs

Accept any combination of:

- A review report pasted by the user or stored in a file.
- The relevant diff, commit range, pull request, or changed files.
- Tests, requirements, API contracts, issue descriptions, logs, or reproduction steps.

If the findings or the code under review are missing, state exactly what is unavailable. Do not invent evidence.

## Validation workflow

For every finding, follow this order:

1. Parse the finding into its claim, location, expected behavior, observed behavior, severity, and suggested fix. Preserve the original wording for traceability.
2. Confirm that the referenced file, line, symbol, and code path exist in the supplied revision. Correct line drift only when the matching code is unambiguous; otherwise mark the location uncertain.
3. Trace the relevant execution path, including callers, error handling, state transitions, configuration, persistence, and external boundaries as applicable.
4. Compare the claim with tests, requirements, types, comments, API schemas, and runtime evidence. Treat explicit repository evidence as stronger than conventions or speculation.
5. Decide whether the finding is substantiated. A plausible concern without a demonstrated failure mode is not confirmed.
6. Check whether another finding describes the same root cause. Keep the more specific finding and identify the duplicates.
7. Evaluate severity independently from validity. Base it on realistic impact, likelihood, affected scope, exploitability or data criticality, and whether a workaround exists.
8. Evaluate the suggested fix for completeness, scope, regression risk, and compatibility. Do not endorse a fix merely because the finding is valid.

When a behavior cannot be established statically, propose the smallest safe verification: a focused test, reproduction, type check, race detector, query, or inspection. Label it as unverified until it is run or supplied as evidence.

## Decision rules

Use exactly one status per finding:

- **Confirmed**: The claim is supported by concrete evidence in the reviewed material.
- **Partially confirmed**: The underlying risk is real, but the location, scope, mechanism, or severity is overstated.
- **Unverified**: The concern is plausible, but the available evidence cannot establish it.
- **Rejected**: The claim is contradicted by code, tests, specification, or runtime evidence.
- **Duplicate**: The claim is substantively covered by another finding; name the retained finding.

Do not use `Confirmed` for style preferences, hypothetical future requirements, or issues detectable only by a tool that has not been run. If a compiler, linter, test, or security scanner can settle the claim, report whether it was run and its result.

## Evidence standards

Good evidence includes:

- An executable path from input or caller to the alleged failure.
- A failing or insufficient test, a minimal reproduction, or a concrete counterexample.
- A contradiction between implementation and an explicit requirement or public contract.
- A data-flow, state, concurrency, or compatibility consequence that follows from the code.

Weak evidence includes “might”, “could”, or “seems” without conditions, impact, and a way to observe the failure. Keep weak evidence as `Unverified`, not as a lower-severity confirmed issue.

## Output

Default to Japanese unless the user requests another language. Report findings first and preserve the input finding identifier when one exists.

```markdown
# Review Finding Validation

## Summary

- Findings reviewed:
- Confirmed:
- Partially confirmed:
- Unverified:
- Rejected:
- Duplicate:
- Validation limitations:

## Validated Findings

### [F-1] [Status: Confirmed] Title

- Original finding:
- Location:
- Verdict:
- Evidence:
- Validation:
- Severity assessment:
- Remediation assessment:
- Recommended next action:

## Duplicates

## Missing Evidence / Suggested Checks
```

For `Rejected`, explain the contradiction. For `Unverified`, state the exact missing evidence and the smallest check that would resolve it. For `Duplicate`, identify the retained finding. If no findings are supplied, say that validation could not start and list the required inputs.

Do not rewrite the source, silently alter the original findings, or report unrelated new defects. A newly noticed issue may be listed only under “Out-of-scope observations”, clearly marked as a new finding rather than validation.
