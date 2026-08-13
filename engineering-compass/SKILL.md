---
name: engineering-compass
description: Apply the user's personal engineering principles to code, designs, implementation plans, and refactorings. Use when the user asks for design or implementation guidance grounded in readability, understandability, testability, loose coupling, or the user's own standards.
---

# Engineering Compass

Apply the following principles when evaluating or proposing code, designs, implementation plans, and refactorings.

## Core Priorities

- Prioritize readability and understandability.
- Treat code whose intent is not clear on first read as a maintenance risk.
- Judge design quality by testability.
- Value loose coupling.

## Design Criteria

- If test preconditions become complex, suspect excessive responsibility.
- If mocks or dependencies grow too much, suspect excessive responsibility.
- Treat code that is difficult to test in isolation as a design problem.
- Prefer responsibilities and behavior that can be inferred from names and types.
- Treat a structure whose responsibility cannot be understood without reading its implementation as a problem.
- When code uses the name of a common tool or concept, make its behavior match the reader's intuition for that name.

## Responsibility Boundaries

- When a function mixes distinct reasons to change, abstraction levels, or
  independently explainable operations, consider a named helper function or a
  dedicated type or module.
- Make a helper hide implementation detail from its caller. Its name must
  explain the operation without merely restating a nearby comment.
- Keep a short, linear operation together when extracting it would only force
  readers to jump between functions.
- Do not extract a helper when doing so increases the state or arguments that
  readers must trace, or when the resulting name cannot express a clear
  responsibility.
- Do not use line count alone as a reason to split code.

## Comment Policy

- Write comments for future callers, not as a walkthrough of the current implementation.
- Describe specifications, behavior, design intent, and tradeoffs.
- Document caller-visible contracts, guarantees, invariants, failure modes, non-obvious constraints, concurrency concerns, and performance characteristics when relevant.
- Keep private functions uncommented unless an invariant, concurrency concern, non-obvious algorithmic reason, or important design tradeoff needs recording.
- Make compromises and constraints explicit.
- Avoid comments that describe control flow, algorithms, internal state, current dependencies, obvious code, or temporary implementation choices.
- Check whether a comment would remain true after a reasonable refactor that preserves external behavior.

## Applying the Principles

- Explain the concrete tradeoff when the principles support a recommendation.
- Do not present personal preference alone as a requirement.
- When the task is a code review, use `engineering-compass-review` for the review procedure and report format.
