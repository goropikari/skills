---
name: explain-code-flow
description: "Use when someone asks how code works, how a request or event moves through a codebase, or what a function, feature, or data flow does. Trace the observable execution path from the entry point through calls, branches, transformations, persistence, and external side effects, then explain it with precise file and line references."
---

# Explain Code Flow

Explain code by reconstructing an evidence-based execution path. Start from the
user's entry point or the most concrete symbol available; do not summarize files
in isolation or infer behavior from names alone.

## Workflow

### 1. Define the scope and entry point

- Restate what is being explained: a request, CLI command, event, function,
  background job, startup path, or end-to-end feature.
- Identify the entry point from routes, commands, event registrations, tests,
  exported functions, or the caller named by the user.
- If the entry point is ambiguous, choose the most likely one and state the
  assumption. Search for all plausible callers before declaring it unique.
- Read repository guidance and the smallest relevant set of files first. Expand
  outward only when a call, configuration value, type, or side effect requires it.

### 2. Trace the execution path

Follow the path in runtime order and record each meaningful transition:

1. Entry point and input construction.
2. Validation, normalization, and default values.
3. Calls into application or domain logic.
4. Important conditionals, loops, retries, and early returns.
5. Data transformations and ownership changes.
6. Persistence, messaging, network, filesystem, cache, or other boundaries.
7. Response construction, emitted events, returned errors, and cleanup.

For every transition, verify the caller and callee in source. Follow dependency
injection, callbacks, middleware, decorators, hooks, and configuration when they
change the actual route. Distinguish code that always runs from code that runs
only for a branch, failure, retry, or environment setting.

### 3. Build a compact flow model

Before writing the explanation, organize the evidence into a small model:

- **Nodes:** functions, modules, handlers, jobs, stores, services, or external
  systems that materially affect behavior.
- **Edges:** calls, data handoffs, events, returned values, or failure paths.
- **State:** values that are created, mutated, persisted, cached, or discarded.
- **Boundaries:** process, thread, transaction, network, permission, or async
  boundaries.

Use a sequence diagram or flow diagram only when it makes branching,
asynchrony, or multiple boundaries easier to understand. Otherwise use a short
numbered sequence.

### 4. Explain behavior and uncertainty

- Explain why each important step exists, not merely what its syntax does.
- Name the condition that selects each important branch and describe the visible
  consequence of taking it.
- Call out hidden behavior such as middleware, implicit transactions, lazy
  evaluation, background work, error translation, or cleanup.
- Separate confirmed behavior from an inference. If a runtime value or dynamic
  dispatch cannot be resolved statically, say what evidence is missing and give
  the possible paths.
- Do not claim that a function is reached, a side effect occurs, or an error is
  handled unless the source, tests, configuration, or runtime evidence supports
  it.

## Investigation Techniques

- Search definitions and references before reading large files. Prefer precise
  symbol and route searches, then inspect surrounding context.
- Read configuration, dependency wiring, schemas, and tests when they determine
  the path or meaning of a value.
- Compare success and failure paths when the request involves errors, retries,
  authorization, or fallbacks.
- Treat comments and names as clues, not proof; prefer executable code and tests.
- Track async boundaries explicitly: identify who schedules work, when it runs,
  what is awaited or detached, and where errors are observed.
- Track data at boundaries using field names and types rather than repeating
  entire objects or implementation details that do not affect the flow.

## Response Format

Tailor the depth to the question, but normally report:

1. **Summary:** one or two sentences describing the overall behavior.
2. **Entry point:** the starting file, symbol, and how it is invoked.
3. **Execution flow:** an ordered sequence with precise file and line links.
4. **Branch and failure paths:** conditions, early exits, retries, and error
   translation that materially change the result.
5. **Data and side effects:** important transformations and external state
   changes, including async work.
6. **Uncertainty:** unresolved dynamic behavior or assumptions.

Use repository-relative paths when that is the established convention, and cite
line numbers for claims that depend on a specific implementation. Keep code
quotes short; prefer paraphrase and small focused snippets.

For a quick explanation, compress the same model into three to seven steps. For
an end-to-end request, include the layers and boundaries but omit unrelated
helpers. If the user asks for a diagram, provide Mermaid only when the symbols
and direction are supported by the inspected code.

## Guardrails

- This Skill explains behavior; do not modify code unless the user separately
  asks for a fix or change.
- Do not confuse a static call graph with the actual runtime flow when dispatch,
  configuration, feature flags, or dependency injection can alter it.
- Do not bury the main path under every helper. Include a helper only if it
  changes control flow, data, security, state, performance, or an observable
  side effect.
- If the requested path cannot be established from the available repository,
  state exactly what was inspected and what additional entry point, input, or
  runtime information is needed.
