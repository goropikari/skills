---
name: goreadable
description: Use the github.com/goropikari/goreadable Go CLI to find and prioritize code that needs a human or AI readability review. Trigger for Go code, diffs, pull requests, or refactors where function length, nesting, cyclomatic complexity, argument count, struct size, or type method count should guide review scope; do not treat its candidates as automatic failures.
---

# Goreadable

Use goreadable as a quantitative triage step before reviewing Go readability. It
reports measurements, the threshold that was exceeded, the reason, source
location, and (in JSON mode) a source excerpt. It does not call an AI service
and a detected candidate is not a correctness or quality verdict.

## Workflow

1. Determine the analysis root and requested scope. For a pull request or
   focused change, prefer `--diff <base>`; otherwise analyze the relevant
   package or `./...`.
2. Assume the `goreadable` binary is the normal interface. Check it with
   `command -v goreadable`. If it is missing, install it before continuing:

   ```sh
   go install github.com/goropikari/goreadable/cmd/goreadable@latest
   ```

   Ensure Go's install directory is on `PATH`, then verify with
   `goreadable --help` or `command -v goreadable`. If installation fails,
   report the error and stop the goreadable-based analysis; do not silently
   substitute another analyzer or change project files.
3. Run JSON output when the results will drive an AI review, and text output
   when a short human-readable triage list is enough:

   ```sh
   goreadable --format json ./...
   goreadable --diff HEAD --format json ./...
   goreadable --format text ./...
   ```

   Use the repository's actual invocation if goreadable is installed
   elsewhere. Save a report only in a clearly scoped temporary or user-named
   location when the output must be passed to another step.
4. Rank candidates by review risk: changed production code first, then
   production code with multiple exceeded metrics, then test code. Within a
   group, inspect the largest threshold margin and the most difficult control
   flow first.
5. Open the reported source locations and nearby callers/tests before judging
   readability. Use the `source` field as a starting point, not as a substitute
   for repository context.
6. Report the measured value, applied threshold, source location, and the
   concrete reader burden. Separate a metric signal from a finding: a long
   function can be cohesive, and a short function can still be cryptic.
7. Keep intentional exceptions visible. `goreadable:ignore` may be placed
   immediately before a function or type when the repository intentionally
   accepts the complexity; verify or request the rationale rather than adding
   the comment merely to silence a report.

## Metrics and defaults

The CLI checks functions for function lines (80), nesting depth (4),
cyclomatic complexity (10), and arguments (5). It checks types for struct
fields (8) and related methods (10). `*_test.go` is labeled as `test`; other
code is labeled `production`. Generated code and `vendor/` are excluded by
default.

Treat these defaults as triage heuristics. If the project has a
`goreadable.json`, record that configuration because CLI flags override the
configuration file, which overrides defaults. A typical configuration is:

```json
{
  "thresholds": {
    "function_lines": 60,
    "nesting_depth": 3,
    "cyclomatic_complexity": 8,
    "function_arguments": 4,
    "struct_fields": 6,
    "type_methods": 8
  }
}
```

Use lower thresholds only when the review needs a wider candidate set, and
state that choice in the report. Do not convert candidate presence into a
non-zero CI gate: candidates exit successfully; invalid options, invalid
configuration, and analysis errors do not.

## JSON review handoff

For each candidate, preserve at least `kind`, `name`, `path`, `start_line`,
`end_line`, `code_kind`, `metrics`, `thresholds`, `reasons`, and `source`.
Use these fields to construct a focused readability review, then inspect the
actual files for naming, responsibility boundaries, local understanding,
consistency, comments, and ease of change. Avoid reporting security,
correctness, performance, or formatting issues unless they directly create a
readability burden.

When no candidates are found, say so and state the analyzed scope and
thresholds. This means goreadable found no threshold breaches; it does not
prove that the code is readable.

## Useful commands

```sh
# Review only changed Go code, using a stricter temporary threshold.
goreadable --diff HEAD --max-function-lines 40 ./...

# Produce a machine-readable handoff for a later review step.
goreadable --format json --max-function-lines 60 ./... > /tmp/goreadable-report.json
```

Do not edit source code or add ignore comments as part of triage unless the
user separately asks for implementation or suppression changes.
