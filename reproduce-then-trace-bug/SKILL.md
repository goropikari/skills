---
name: reproduce-then-trace-bug
description: "Use when investigating a bug, regression, failing test, incident, or unexpected behavior. Enforce the order of operations: first reproduce the behavior, then inspect relevant logs and runtime evidence, and only then trace the code to identify the cause. Do not jump straight to speculative code changes."
---

# Reproduce Then Trace a Bug

Investigate bugs from observable evidence toward an explainable root cause. Keep reproduction steps, log evidence, hypotheses, and source locations separate so that a plausible-looking guess is not presented as a diagnosis.

## Investigation Workflow

Follow these phases in order. Do not edit production code while still in the reproduction or log-inspection phases unless a temporary, explicitly documented diagnostic change is necessary and reversible.

### 1. Establish the reproduction

- Read the issue, failing test, request, or incident description and turn it into a concrete expected-versus-actual statement.
- Inspect the repository's documented setup, test, run, and fixture commands before inventing commands. Check `AGENTS.md`, README files, Makefiles, and package scripts when relevant.
- Reproduce with the smallest safe command or test. Capture the exact command, inputs, environment assumptions, timestamp, and complete failure output.
- Prefer a deterministic automated reproduction. If it is intermittent, run a bounded number of repetitions and record the observed rate and conditions.
- If reproduction fails, do not claim the bug is fixed or disproven. Record what was tried, check for setup/version/data differences, and ask for the missing information or continue only with clearly labeled evidence.

### 2. Inspect logs and runtime evidence

- After obtaining a reproduction, locate the logs produced by that run: test output, application logs, structured events, traces, metrics, browser/server console output, or captured request/response data.
- Use timestamps, request/job/correlation IDs, stack traces, error codes, and before/after state to connect log entries to the reproduced failure.
- Separate direct evidence from interpretation. Quote or summarize the key log lines with their source and explain why they belong to the failing run.
- Check for masking: swallowed exceptions, retries, stale logs, clock skew, sampling, redaction, and concurrent requests. Never treat a generic error message as the root cause without tracing its context.
- If logs are insufficient, add the narrowest safe diagnostic observation or identify exactly which instrumentation/data is missing before proceeding.

### 3. Trace the code cause

- Start from the strongest runtime evidence: exception type/message, stack frame, event name, request path, or incorrect state transition. Trace callers, inputs, transformations, persistence, and downstream effects until the first incorrect assumption or state is found.
- Compare the failing path with a successful path, boundary case, recent change, and relevant tests. Search for callers and configuration rather than inspecting only the named function.
- Form a falsifiable root-cause statement that links: trigger/input -> faulty condition or state -> observed log/error -> user-visible behavior.
- Cite precise file paths and line numbers, and distinguish confirmed cause, contributing factor, and unresolved hypothesis.
- Only after the cause is evidenced should you propose or implement a fix. Add or update a regression test that fails before the fix and passes after it when implementation work is requested.

## Handoff Format

Report the investigation in this order:

1. Reproduction: command, inputs, expected result, actual result, and whether it is deterministic.
2. Log evidence: relevant source, timestamp/identifier, and the key entries.
3. Root cause: exact code location and the evidence chain from trigger to failure.
4. Scope and confidence: confirmed facts, hypotheses, affected paths, and remaining uncertainty.
5. Next action: regression test, fix proposal, or the precise information needed to continue.

Never present a code location as the cause merely because it looks suspicious; it must explain the reproduced behavior and agree with the runtime evidence.
