---
name: new-app-engineering-workflow
description: >-
  Guide greenfield apps, services, MVPs, and PRD-driven feature development
  through a minimal Product Contract, human-gated architecture decisions,
  Golden Path, pattern reuse, smallest-change implementation, and explicit
  verification. Use when an AI will build a new application or continue a
  newly established codebase; do not impose greenfield ceremony on mature
  repositories.
---

# New App Engineering Workflow

Use this skill when a PRD or broad product request could otherwise lead to a
large speculative implementation. The governing rule is: **never implement a
whole app directly from a PRD**. Convert intent into a contract, settle only
architecture decisions that need a human, establish a Golden Path, then build
features in small verified loops.

## Start by choosing the route

Inspect the repository before asking questions: worktree changes, framework,
runtime, conventions, existing tests, commands, and the closest implementations.
Preserve unrelated changes.

- **Small route:** for a small, local change with no product, data, security,
  or architecture decision. State the acceptance criteria, reuse the nearest
  pattern, implement the smallest change, verify, and self-review.
- **Established route:** for a mature repository. Treat its existing patterns
  as the Golden Path; do not create a new foundation. Produce the feature plan,
  implement, verify, and review.
- **New-app route:** for a greenfield app/service, an MVP, or a PRD that spans
  multiple features. Use the phases below.

When the route is unclear, choose the smallest route that still protects a
decision with product, data, security, or architectural consequences.

## Document output

Write generated workflow documents under the repository-root
`.new-app-engineering-workflow/` directory dedicated to this skill. Create the
directory when it does not exist; do not place generated contracts, specs,
plans, or verification reports in the repository root, the repository's
general `docs/` directory, or the skill's `references/` directory. Use clear
filenames, such as `.new-app-engineering-workflow/product-contract.md`,
`.new-app-engineering-workflow/architecture-contract.md`, and
`.new-app-engineering-workflow/implementation-plan.md`; use a suitable
subdirectory for multiple feature documents. If the user explicitly provides
another output path, use that path instead.

## New-app phases

```text
PRD → Product Contract → Architecture/Foundation Contract → Human Approval
  → Golden Path → Human Review → Feature Spec → Implementation Plan
  → Implement → Verify → Over-engineering Review → Self Review
```

Do not silently cross a Human Approval/Review gate. Present a concise decision
record and wait for approval unless the user explicitly authorizes an
autonomous workflow. An explicit authorization permits routine progression,
but does not make an unresolved product or safety decision valid.

### 1. Product Contract

Create a concise Product Contract before implementation. Capture goal, target
user, core flows, functional requirements, observable acceptance criteria,
important edge cases, non-goals, product decisions, and constraints. Classify
unknowns as:

- **Must clarify:** changing product meaning, user promise, legal/safety
  posture, irreversible data behavior, or acceptance criteria.
- **Reasonable default:** a reversible choice supported by repository/framework
  convention; record the assumption.
- **Implementation detail:** delegate to the agent using the simplest existing
  pattern.

Ask only Must-clarify questions. Use the template in
`references/product-contract.md`.

### 2. Architecture/Foundation Contract

For a new app with no established pattern, document runtime/framework,
language, UI/design system, application structure, storage, data access,
API/server communication, validation, authentication/authorization, state,
errors, observability, testing, dependency policy, and deployment assumptions.
Choose the simplest architecture satisfying current requirements. Prefer
framework-native and boring conventions. Do not add layers for hypothetical
scale or future flexibility.

The following are Architecture Decisions and require Human Approval:
new framework or major dependency; storage technology or major schema policy;
global state; repository/service-wide layering; event bus/queue/messaging;
microservices; internal generic/shared framework; authentication or
authorization architecture; caching; background workers; or major deployment
architecture changes. Show only a few viable options using:

```text
Decision
Why this is needed
Simplest option
Alternatives
Trade-offs
Recommendation
```

Do not request approval for naming, ordinary decomposition, framework-standard
details, obvious test placement, or small styling choices.

### 3. Golden Path

Implement one representative vertical slice only after architecture approval.
Prefer a slice that exercises UI, validation, business logic, data access,
persistence, response/UI update, loading, errors, authorization if applicable,
and tests. Record the resulting directory, naming, component, API,
validation, error, state, logging, and test conventions. Obtain Human Review
of this reference implementation before multiplying its pattern.

For an established repository, identify the existing Golden Path by finding
2–3 closest implementations; record what is reusable, what is not applicable,
and every deviation.

Increase autonomy gradually: architecture has low AI autonomy/high human
involvement; the Golden Path has medium autonomy/very high involvement; the
next 2–3 features have medium autonomy/high involvement; once patterns are
stable, routine features have high autonomy/low-to-medium involvement. Any new
Architecture Decision resets the process to the Human Gate.

### 4. Feature loop

Before each feature, write the fixed Implementation Plan from
`references/implementation-plan.md`. Always make `New Dependencies`, `New
Abstractions`, and `Architecture Decisions` explicit; write `None` when empty.

When requirements name an explicit external contract (a standard, public
interface, format, or compatibility target), record boundary and invalid-input
examples in the Feature Spec. For destructive behavior, the expected result
includes absence of side effects after rejection. Do not substitute a merely
plausible implementation for the stated contract because ordinary examples
pass.

Apply these constraints:

1. Implement the smallest change that satisfies the acceptance criteria.
2. Reuse 2–3 closest implementations before inventing a pattern.
3. Do not add future-proofing, unrelated refactors, migrations, or libraries.
4. Prefer duplication over premature abstraction. Consider shared code around
   the third real use, except for duplicated security, correctness, or critical
   business rules.
5. For every new abstraction, record the concrete problem, why the existing
   pattern fails, current/immediate usages, and the alternative without it.
6. For every new dependency, record the problem, why built-in/existing code is
   insufficient, maintenance and runtime/bundle impact, and the alternative.
7. Keep routine implementation choices autonomous; return to a Human Gate if
   a listed Architecture Decision, product decision, irreversible data choice,
   security-sensitive choice, costly dependency, or major scope expansion arises.

Before handoff, apply a complexity budget: an interface should not outnumber
its implementations, a factory/adapter/repository/service should have a
concrete current need, a generic type should have more than one real use, and
local/server state should be preferred to global state. Treat premature
caching, concurrency, plugin/config systems, and one-line wrappers as review
findings unless current acceptance criteria justify them.

### 5. Verify and review

Return to the Product Contract and run applicable tests, typecheck, lint,
build, and manual acceptance checks. Never claim a check ran when it did not.
For an unavailable check, record `Not verified`, the reason, impact, alternate
evidence, and residual risk. Use `references/verification-checklist.md`.

For anything consumed outside its process (CLI, library, plugin, executable,
or service), add a critical-flow test through the built or installed consumer
entry point. Verify public module/package identity and build/install target as
part of this check. Unit tests, direct internal calls, and help/version tests
are necessary evidence but are not a substitute. Exercise relevant exceptional
states and partial failures, and state their intended behavior when they
cannot be tested.

Perform a separate Over-engineering Review after correctness verification:
remove unjustified layers, interfaces, factories, adapters, wrappers,
repositories, services, generics, global state, caching, concurrency,
configuration, dependencies, and framework-duplicate code. Also check scope
creep and unrelated refactoring. Simplify when requirements remain satisfied.

Finish with a reviewer-style Self Review in this order: product correctness,
missing requirements, edge cases, security/authorization, data correctness,
pattern consistency, over-engineering, test quality, maintainability, and
scope control. Report remaining risks and unverified checks plainly.

## Compact user-facing output

Do not print the entire checklist on every turn. For ordinary feature work use:

```text
Plan
Existing patterns: ...
Files: ...
New abstractions: None | ...
New dependencies: None | ...
Architecture decisions: None | Human Approval required: ...
Implementation: ...
Verification: ...
```

Show the detailed Decision Gate only when a Human Gate is actually triggered.
Load the references only for the corresponding phase; they are templates, not
mandatory artifacts for the small route.

## Usage example

For a request such as “Build a small task-tracking web app from this PRD,”
invoke `$new-app-engineering-workflow`. Inspect the repository, produce the
Product Contract, ask only product-meaning questions, present an Architecture
Contract if no foundation exists, wait for approval, build one task CRUD
Golden Path, and then handle each remaining feature with the compact plan and
verification loop. For “add a label filter to the existing task list,” use the
small or established route unless the change introduces a listed gate.
