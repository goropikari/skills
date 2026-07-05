---
name: comment-contract-reviewer
description: Reviews code comments to ensure they describe only the public contract of the documented symbol. Reports contract violations only.
context: fork
arguments:
  - name: filepath
    description: The path to the file to review
    required: true
---

# Comment Contract Reviewer

## Purpose

Review comments from the perspective of a consumer of the documented API.

Comments should document only the public contract of the documented symbol.

This skill performs **contract review only**.

Do not review language-specific documentation conventions.

Do not review formatting or style guide issues.

Do not rewrite comments.

Do not modify source code.

Only report violations.

---

# Execution Protocol (Anti-Attention-Drift)

When this skill is invoked for a `<filepath>`, you MUST execute the following exact pipeline to prevent full-file implementation details from distracting your evaluation:

1. **Pre-processing (Strip Implementation)**: Scan the entire file, but **completely strip away all inner implementation logic** (e.g., function bodies, loops, internal variable assignments). Retain ONLY:
   - Line numbers.
   - Comments / Docstrings.
   - The symbol signatures (e.g., function/method definitions, class declarations) immediately following the comments.
2. **Isolate Context**: Discard the raw, full source code from your immediate working memory. Perform the contract review **ONLY on the stripped text** generated in Step 1.
3. **Sentence-by-Sentence Evaluation**: For every sentence within the remaining comments, strictly apply the "Review Tests" below.

---

# Scope

This skill is responsible only for:

- Public contract
- Responsibility
- Preconditions
- Postconditions
- Observable side effects
- Error conditions
- Public guarantees

This skill intentionally does **not** review:

- GoDoc conventions
- JavaDoc conventions
- Rustdoc conventions
- XML documentation conventions
- Markdown formatting
- Language-specific documentation style

Those concerns belong to language-specific review skills.

---

# Allowed Content

Comments may describe only:

- Responsibility
- Purpose
- Public behavior
- Parameters
- Return values
- Preconditions
- Postconditions
- Observable side effects
- Error conditions
- Public invariants

---

# Forbidden Content

Report comments that describe:

- implementation details
- caller behavior
- internal state
- architecture
- usage patterns
- historical decisions
- future intentions
- speculation

---

# Review Tests

For every sentence in the extracted comments:

## Public Contract Test

Does this sentence describe the public contract?

If not:

Report a violation.

---

## Stability Test

Would this sentence remain true after a complete reimplementation preserving the same externally observable behavior?

If not:

Report a violation.

---

## Hidden Knowledge Test

Does understanding this sentence require implementation knowledge?

If yes:

Report a violation.

---

## Caller Test

Does this describe behavior outside the documented symbol?

If yes:

Report a violation.

---

# Reporting

Report only objective violations.

Do not rewrite comments.

Do not suggest alternative wording.

Do not report style preferences.

---

# Output

For every issue found, output EXACTLY in the following format. Do not include any introductory text, concluding text, or markdown code blocks around the entire output.

```text
Location: <filepath>:<line_number>
Category: [Forbidden Content type or Test Name that failed]
Reason: [Clear explanation of why it is a violation based on the tests]
