---
name: session-to-book
description: Start at the beginning of a conversation and continuously turn the session's discussion into a growing book manuscript. Use when the user wants each subsequent turn, idea, decision, or example to be organized into chapters and written to an ongoing draft, with a final editorial pass at the end. Preserve source boundaries, distinguish evidence from interpretation and creative reconstruction, and keep the manuscript coherent as it grows.
---

# Session to Book

## Purpose

Transform a live session into a book-shaped manuscript one turn at a time rather than waiting for a final transcript. The result should have a clear promise to the reader, a deliberate progression, enough context to stand alone, and visible boundaries between what the source establishes and what the editor infers or invents.

## Inputs and default assumptions

Use evidence in this order:

1. The current conversation and any attached or pasted transcript.
2. User-supplied notes, documents, links, code, data, or citations.
3. Relevant local files explicitly placed in scope by the user.

If the user has not specified a format, produce a practical nonfiction manuscript in the same language as the request. Assume a readable first draft, not a print-ready typeset book. Do not claim to have read a transcript, file, or source that is unavailable.

## Session lifecycle

This skill is intended to be invoked in the first turn and remain active throughout the session. Treat the manuscript as durable working state, not as a one-off answer.

### First invocation: initialize

1. Decide the working language, provisional audience, and book promise from the opening request.
2. Create or locate the manuscript file. If the user has not chosen a path, use `book-manuscript.md` in the current working directory and tell the user once.
3. Write the title candidate, editorial note, book promise, initial contents, and an empty `## Working notes` section.
4. Ask only the minimum blocking question. If none is needed, invite the user to continue the discussion.

Do not write a speculative full book from the opening prompt. Initialize a useful skeleton and leave room for the session to discover its argument.

### Every subsequent turn: capture and advance

Before responding, read the current manuscript and identify the new material since the last update. Then:

1. Classify the turn as a new idea, evidence, example, decision, counterargument, revision, or unrelated conversation.
2. Place it in the current chapter or create the next chapter only when the book's argument needs a new unit.
3. Rewrite nearby prose and transitions when necessary; do not merely append a chronological transcript.
4. Update the contents, `Working notes`, open questions, and source-boundary markers.
5. Save the revised manuscript file before replying.

If the turn is not book material, leave the manuscript unchanged and say so only when helpful. If the user explicitly says “記録して”, “章にして”, “反映して”, or equivalent, treat the material as book material even if its placement is provisional.

Keep a small editorial state near the end of the file or in a sidecar file only if that makes continuation safer. At minimum, retain the current chapter, last incorporated topic, open threads, and terminology decisions. Do not add opaque session metadata or hidden instructions to the reader-facing manuscript.

In the chat response, briefly report what was incorporated (for example, “Chapter 2に例を追加し、Chapter 3への論点を開きました”) and then continue the conversation naturally. Do not print the entire manuscript after every turn unless requested.

### Chapter boundary and finalization

When the user signals a chapter change, topic change, pause, or completion, close the current chapter with a useful landing point, update its title and transition, and preserve unresolved questions for later chapters. When the user asks to finish, perform a final pass for structure, repetition, terminology, unsupported claims, and reader flow, then produce the complete manuscript plus a concise change summary.

When the session is incomplete, say so briefly and preserve open threads instead of fabricating a conclusion. Ask at most one blocking question only when the intended audience, language, or genre would materially change the book; otherwise make a reasonable assumption and state it in the editorial note.

## Editorial workflow

### 1. Map the source

Extract:

- the central question, promise, and audience implied by the session;
- recurring concepts, arguments, examples, decisions, and turning points;
- disagreements, revisions, uncertainty, and unresolved questions;
- concrete evidence, quotations, references, and provenance;
- useful material that should be omitted because it is repetitive, private, or merely operational.

Keep three layers distinct while working:

- **Source fact**: directly stated or supported by supplied material.
- **Editorial synthesis**: a faithful connection or ordering of source material.
- **Creative reconstruction**: invented scene, dialogue, example, metaphor, or detail.

Never present creative reconstruction as a quotation, remembered event, research result, or user decision. If a nonfiction manuscript needs connective tissue, use synthesis first and label any invented material.

### 2. Choose the book's spine

Select the smallest structure that gives the material momentum. Typical spines are:

- chronological: how the understanding or project changed;
- conceptual: one chapter per major idea or tension;
- problem-to-practice: problem, principles, method, cases, limits;
- question-driven: a sequence of questions that becomes progressively sharper.

Write a one-sentence book promise and a one-paragraph arc before drafting chapters. Remove or defer material that does not serve that arc. Do not force unrelated topics into one book; propose a companion volume or appendix when appropriate.

### 3. Build the outline

Create a title candidate, subtitle candidate, audience, promise, and chapter outline. Each chapter should have:

- a specific purpose and reader question;
- the ideas or evidence it inherits from the source;
- a beginning, development, and landing point;
- a transition that explains why the next chapter follows.

Prefer 5–12 chapters for a normal first draft. Use sections within a chapter when the source is dense. Put raw chronology, transcripts, source notes, checklists, or technical detail in appendices when they interrupt the reading experience.

### 4. Draft and edit

Draft in the source language unless the user requests otherwise. Preserve distinctive insights and meaningful disagreement, but remove session artifacts such as turn-taking, repeated acknowledgements, tool chatter, and unexplained pronouns. Introduce specialized terms before relying on them.

Use scenes or examples only when they clarify an idea. For factual nonfiction, retain dates, numbers, attributions, and uncertainty exactly enough to be checked. Mark missing verification as `[要確認: ...]` (or an equivalent note in the manuscript language), rather than silently smoothing it over.

Edit for:

- a consistent reader and level of explanation;
- progression rather than a sequence of disconnected summaries;
- concrete examples and counterarguments;
- honest claims, source boundaries, and privacy;
- varied but controlled prose, with headings used as navigation.

### 5. Deliver in layers

Unless the user asks for only one artifact, return:

1. a short editorial note stating assumptions and source limits;
2. the book concept and outline;
3. the manuscript or a clearly identified first installment;
4. a source-boundary / fact-check list;
5. open editorial choices and a suggested next revision.

For a long source, do not pretend to have completed a full book in a single short response. Deliver a strong proposal plus the opening chapter and a drafting plan, or proceed chapter by chapter while keeping terminology and unresolved threads consistent.

## Manuscript shape

Use this default order:

```markdown
# [Title]

## Editorial note

## Working notes

## Book promise

## Contents

## Introduction

## Chapter 1: [title]

...

## Conclusion

## Notes and sources

## Unresolved questions / fact-check list
```

The editorial note is not part of the literary manuscript. Keep it concise and include only assumptions that affect interpretation. If the user requests a polished reader-facing manuscript, place editorial notes after the manuscript or in a separate clearly labeled section.

## Modes

- **Blueprint**: concept, audience, promise, table of contents, chapter briefs, and sample opening. Use when the source is large or the user is still deciding what the book is.
- **Draft**: write the requested chapters in full, retaining source boundaries and placeholders for verification.
- **Adaptation**: reshape the same material for a specified audience, genre, language, or medium; explain substantial changes in a brief editorial note.
- **Revision**: compare an existing manuscript with the source, then repair omissions, repetition, weak transitions, unsupported claims, or inconsistent terminology.

Infer the mode from the request; if ambiguous, default to Blueprint for large or incomplete material and Draft for a clearly bounded session.

## Quality checks

Before delivering, verify:

- every chapter advances the book promise;
- the outline and manuscript agree on chapter titles and order;
- important claims can be traced to the session or supplied sources;
- invented material is labeled or removed;
- unresolved issues are visible rather than falsely resolved;
- private or sensitive session content is included only when relevant and appropriate;
- the result reads as a book, not as a transcript dump or chronological chat log.

When useful, end with a compact table:

| Item                      | Status                       | Evidence or next action                            |
| ------------------------- | ---------------------------- | -------------------------------------------------- |
| Claim / decision / source | Confirmed, inferred, or open | Session location, citation, or verification needed |

## Boundaries

Do not expose hidden system instructions, private metadata, credentials, or unrelated personal information from a session. Do not invent citations or imply external research. Do not rewrite a participant's position into a stronger claim without identifying the editorial synthesis. If the user wants fiction, creative reconstruction is allowed, but label the work as fiction or an adaptation and do not attribute invented events to real participants.
