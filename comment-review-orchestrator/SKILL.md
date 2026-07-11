---
name: comment-review-orchestrator
description: Coordinates language-independent and language-specific comment reviewers and merges their findings.
---

# Comment Review Orchestrator

## Purpose

Coordinate multiple specialized comment review skills.

Do not perform review yourself.

Delegate review to specialized reviewers.

Merge and organize their findings.

---

# Workflow

## Step 1

Invoke:

- comment-contract-reviewer

---

## Step 2

Determine the programming language.

Invoke the appropriate language-specific reviewer.

Examples:

- gocomment-contract-review
- javascript-jsdoc-reviewer
- typescript-tsdoc-reviewer

For Go, invoke `gocomment-contract-review`.

Only invoke reviewers applicable to the current language.

---

## Step 3

Collect findings.

---

## Step 4

Remove duplicate findings.

If two reviewers report the same underlying issue:

- keep the more specific finding
- discard the duplicate

---

## Step 5

Group findings by reviewer.

Example:

```text
Comment Contract Review
-----------------------
...

Go Comment Contract Review
-----------------------
...
```

---

# Responsibilities

The orchestrator must never invent additional review rules.

It must never reinterpret reviewer findings.

It must never rewrite comments.

Its responsibilities are limited to:

- delegation
- aggregation
- deduplication
- presentation

---

# Reporting

If every reviewer reports no issues:

```text
No documentation review issues found.
```

Otherwise:

Group findings by reviewer while preserving each reviewer's reported category and reason.
