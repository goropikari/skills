---
name: coderabbit-review
description: Runs CodeRabbit CLI review 3 times with API limit handling and evaluates the consistency of the findings, outputting a markdown report. Use this to assess the stability and variety of CodeRabbit's AI-driven code reviews.
---

# CodeRabbit Review

## Overview

This skill automates the process of running CodeRabbit code reviews multiple times to evaluate the consistency and quality of the AI findings. It executes `coderabbit review --agent` three times, handles API limits and retries, compares the results, and generates a markdown report (`coderabbit_evaluation.md`).

## Workflow

1. **Trigger**: Invoke the skill when you want to evaluate CodeRabbit's performance.
2. **Execution**: The skill runs `scripts/evaluate.py`.
3. **API Safety**: The script includes a 10s delay between runs and retry logic (up to 2 times) to handle rate limits or temporary failures. It also monitors CodeRabbit status messages for quota warnings.
4. **Analysis**: The script parses JSON output, identifies common findings, and highlights unique ones.
5. **Output**: `coderabbit_evaluation.md` is created in the current directory.

## Usage

Ask Gemini CLI to "Run coderabbit evaluation" or "Evaluate coderabbit findings".

### Example

"Evaluate coderabbit findings on the current branch."

## Resources

### scripts/

- `evaluate.py`: Python script that executes the 3 runs and generates the report.

### Outputs

- `coderabbit_evaluation.md`: The generated evaluation report.
