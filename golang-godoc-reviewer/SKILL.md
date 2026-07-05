---
name: golang-godoc-reviewer
description: Reviews Go documentation comments for GoDoc and Effective Go conventions only.
---

# GoDoc Reviewer

## Purpose

Review Go documentation comments for compliance with Go documentation conventions.

This skill reviews **GoDoc conventions only**.

It does **not** review comment content or API contract quality.

Those concerns belong to the Comment Contract Reviewer.

Do not rewrite comments.

---

# Scope

Review only:

- GoDoc conventions
- Effective Go documentation conventions
- Documentation discoverability
- Exported symbol documentation
- Package documentation

Do not review:

- implementation leaks
- caller behavior
- API contract quality
- architecture
- history
- wording quality

---

# Review Rules

Report only the following issues.

## Exported Identifiers

- Exported functions without documentation
- Exported methods without documentation
- Exported types without documentation
- Exported constants without documentation
- Exported variables without documentation

---

## Comment Form

For exported identifiers:

The first sentence should begin with the identifier name.

Example:

```go
// Parse parses...
func Parse(...)
```

Report violations.

---

## Package Documentation

Report missing package documentation for public packages.

---

## GoDoc Formatting

Report:

- malformed documentation comments
- invalid formatting that reduces GoDoc readability

Ignore stylistic preferences beyond documented Go conventions.

---

# Reporting

Report only Go documentation convention violations.

Do not suggest rewrites.

Do not report contract issues.

---

# Output

For every issue:

```text
Location
Category
Reason
```

If there are no issues, report nothing.
