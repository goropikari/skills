---
name: coderabbit-review
description: Runs CodeRabbit CLI review 3 times with API limit handling and evaluates the consistency of the findings, outputting a markdown report. Use this to assess the stability and variety of CodeRabbit's AI-driven code reviews.
---

# CodeRabbit Review

## Overview

This skill evaluates the consistency and quality of CodeRabbit findings by running
the CodeRabbit CLI three times and comparing the results. The CLI is invoked
directly; do not call a Python wrapper or other helper script.

## Workflow

1. **Trigger**: Invoke the skill when you want to evaluate CodeRabbit's performance.
2. **Execution**: Run `coderabbit review --agent` directly once per evaluation
   run, for a total of three runs. If the repository contains
   `.coderabbit.yaml`, pass it with `-c .coderabbit.yaml`.
3. **Collection**: Capture each CLI result separately so findings from one run
   cannot be confused with another. Preserve the CLI's JSONL output, including
   status messages, while collecting it.
4. **API safety**: Wait 5 seconds between successful runs. If a run fails or
   reports a limit, quota, or rate error without findings, retry it up to two
   times with waits of 10 and 20 seconds. If it still fails, stop and report
   how many runs completed.
5. **Analysis**: Compare findings by their `fileName` and
   `codegenInstructions` fields. List findings present in every completed run
   as consistent, and findings present in only some runs as variable, including
   the run numbers.
6. **Output**: Write `coderabbit_evaluation.md` in the current directory with
   the date, completed-run count, per-run finding counts, and the comparison
   analysis.

## Usage

Ask Gemini CLI to "Run coderabbit evaluation" or "Evaluate coderabbit findings".

### Example

"Evaluate coderabbit findings on the current branch."

## Resources

### Outputs

- `coderabbit_evaluation.md`: The generated evaluation report.
