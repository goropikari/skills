---
name: gocomment-contract-review
description: Extract Go comments from git diffs with gocomment, batch them into 10-record chunks, delegate each chunk to comment-contract-reviewer, and write a markdown report.
---

# gocomment Contract Review

Review Go comments found in a git diff by using `gocomment diff` as the extractor and `comment-contract-reviewer` as the reviewer.

Do not review comments yourself.

## Workflow

1. Run `gocomment diff` against the target git diff and capture its JSONL output.
   - If the user did not specify a diff scope, use the current repository diff against `HEAD`.
2. Drop records that are clearly not review targets:
   - comment text that is only `arrange`, `act`, `assert`, `TODO`, `FIXME`, or `HACK`
   - the same labels followed only by punctuation or whitespace
   - keep the record if the label is followed by substantive text
3. Split the remaining JSONL records into chunks of 10 records.
4. For each chunk, create a temporary file that preserves the original file path, line number, nearest enclosing Go symbol signature, and comment text for every record in that chunk.
5. Spawn one subagent per chunk and invoke `comment-contract-reviewer` on the chunk file.
6. Collect the subagent findings, remove duplicate underlying issues, and map temporary locations back to the original source locations.
   - Treat findings as duplicates when they refer to the same original source path, line number, and category after normalizing the reason text.
   - Prefer the finding with the narrower scope or the more specific reason text.
7. Write the merged result to `gocomment_comment_contract_review.md` in the current directory.

## Reporting Rules

- Preserve each reviewer finding's category and reason.
- Prefer the most specific finding when two subagents report the same underlying issue.
- If there are no findings, state that clearly in the markdown report.
- Include a short summary of skipped records and the reason they were skipped.
- Use this markdown structure:
  - `# gocomment Contract Review`
  - `## Summary`
  - `## Skipped Records`
  - `## Findings`
  - `## Per-Chunk Results`
- If there are no findings, the `## Findings` section should say `No comment contract issues found.`

## Chunk File Contract

Each temporary chunk file should contain only the extracted record data needed for review:

- original source path
- original line number
- nearest enclosing Go symbol signature
- comment text

Keep the file compact and one record per block so the reviewer can focus on the comment contract.
