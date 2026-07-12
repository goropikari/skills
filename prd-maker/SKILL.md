---
name: prd-maker
description: Interview the user one question at a time to turn rough ideas, feature requests, or ambiguous requirements into a Japanese PRD. Use when the user asks to create, draft, refine, or pressure-test a PRD, product requirements, or feature spec.
---

# Grill Prd

## Overview

Use this skill to interview the user until the product intent is clear enough to write a concise Japanese PRD in Markdown.

## Workflow

1. Build context first.
   - Inspect linked files, product docs, tickets, existing specs, or nearby code before asking questions.
   - If the user is only starting from an idea, skip investigation and start the interview.
2. Ask one question at a time.
   - Present 2-4 numbered answer options when possible.
   - Mark the recommended option clearly.
   - Do not bundle unrelated decisions into one question.
3. Resolve dependencies in order.
   - Start with the problem, target user, and desired outcome.
   - Then cover scope, non-goals, key flows, requirements, constraints, metrics, risks, rollout, and open questions.
4. Keep the interview tight.
   - Skip questions that can be inferred from context.
   - Stop asking once the remaining gaps are minor assumptions that can be stated explicitly.
5. Draft the PRD when ready.
   - Use `references/prd-template.md` as the default outline.
   - Write a complete Markdown PRD with assumptions, scope, and open questions called out clearly.
   - If the user wants a revision, update the PRD instead of restarting the interview.

## Output Rules

- Default to writing the PRD to `docs/prd.md` unless the user specifies another path.
- Write the PRD body in Japanese.
- Keep the document concrete and implementation-agnostic.
- Prefer short sections over long prose.
- Include non-goals and open questions explicitly so the PRD is reviewable.

## Question Sequence

Use this order unless the user already answered a later question:

1. What problem are you solving, and for whom?
2. What does success look like?
3. What is in scope for the first version, and what is out of scope?
4. What are the main user flows or scenarios?
5. What constraints, dependencies, or known risks matter?
6. How will the feature be measured, launched, or validated?

## Guidance

- Treat the conversation as a decision tree, not a free-form brainstorm.
- If the user asks for a PRD from an existing product or codebase, anchor the PRD to the current behavior before proposing new behavior.
- When the request is ambiguous, state the assumption you are making and continue.
