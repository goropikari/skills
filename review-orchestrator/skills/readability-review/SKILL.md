---
name: readability-review
description: Review source code, diffs, pull requests, and implementation plans for readability using a fixed, evidence-based 1–5 scoring rubric. Use when asked to assess code readability, clarity, cognitive load, understandability for a first-time developer, naming, responsibility separation, control-flow complexity, local reasoning, consistency, comments, or ease of change.
---

# Readability Review

Assess how easily an unfamiliar developer can understand and safely change the reviewed material. Use the fixed axes and scoring anchors below to make results comparable. Review only the supplied scope; do not infer missing code or requirements.

## Review Workflow

1. Inspect the requested files, diff, snippets, and nearby definitions needed to understand them. Record paths and line numbers where available.
2. Identify cognitive-load points: a reader must mentally translate a name, hold multiple states or conditions, jump to distant code, or guess intent or a change's impact.
3. Score every axis from 1 to 5 using the anchors. Cite at least one concrete code location for every score, including 4 or 5. Do not use an aggregate score: it conceals different improvement priorities.
4. Distinguish general readability issues from preferences. Report a general issue only when the evidence demonstrates avoidable cognitive load, ambiguity, inconsistency, or change risk.
5. Propose at most five improvements, ordered by expected readability benefit. Preserve observable behavior and the existing design intent unless the evidence establishes that a design change is needed.

Use quantitative measures, such as function length, parameter count, maximum nesting depth, cyclomatic complexity, or duplicated branches, when available. State the measured value and scope. Treat metrics as evidence, not pass/fail thresholds: explain the concrete reading burden they create. Do not fabricate measurements or run tools that are unavailable.

## Fixed Evaluation Axes

Score each axis against the full reviewed scope. A localized exception may lower a score, but explain its scope rather than generalizing it.

| Axis                    | 1                                                                               | 3                                                                      | 5                                                                                               |
| ----------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Naming                  | Names obscure role, unit, state, or side effect.                                | Most names are understandable; some require context or are misleading. | Names consistently reveal intent, domain meaning, and side effects at the needed level.         |
| Single responsibility   | Units combine unrelated decisions, I/O, state changes, or policies.             | Main purpose is recognizable, with some mixed concerns.                | Each unit has one coherent reason to change and its structure reflects that purpose.            |
| Control-flow complexity | Nested branches, long conditions, or state transitions are hard to trace.       | Branching is understandable but requires notable mental simulation.    | Flow is linear or clearly structured; conditions and exceptional paths are easy to follow.      |
| Local understanding     | A reader must repeatedly jump across distant code or retain hidden context.     | Some nonlocal references are needed but relationships are traceable.   | Most behavior can be understood locally; dependencies and data flow are explicit.               |
| Consistency             | Similar concepts use conflicting names, styles, error handling, or conventions. | Established patterns are mostly followed with limited exceptions.      | Equivalent cases use consistent vocabulary, structure, and error-handling conventions.          |
| Comments                | Comments are misleading, redundant noise, or essential intent is unexplained.   | Comments usually help, but some intent or rationale remains unclear.   | Comments are sparse and accurate, explaining non-obvious rationale, constraints, or trade-offs. |
| Ease of change          | A small plausible change requires coordinated, scattered, or fragile edits.     | Typical changes are localized, with a few coupled areas.               | Likely changes have clear ownership and localized impact.                                       |

Use 2 or 4 only for evidence that falls between the adjacent anchors, and state why. Do not penalize code merely for being concise, long, comment-free, functional, object-oriented, or stylistically different. In particular, do not demand comments for self-explanatory code; assess whether existing comments and omitted rationale are appropriate.

## Evidence and Scope Rules

- Cite `path:line`, symbol names, or short snippets for every score and finding. Never state a score without evidence.
- Explain the reader task made difficult, not only the code shape. For example, say which state a reader must track or which condition is ambiguous.
- Mark conclusions as `Insufficient evidence` when the supplied material cannot establish an axis. Still give a provisional 1–5 score only if the user explicitly requires every axis to be scored; otherwise omit that axis and explain why.
- Classify a concern as `General readability issue` or `Preference`. Include preferences only when the user asks for them; do not let them change the score.
- Do not report correctness, security, performance, formatting, or test-coverage issues unless they directly create a documented readability burden.

## Output Format

Write the review in Japanese by default, unless the user requests another language.

```markdown
## レビュー範囲

- `<files, diff, or snippets reviewed>`
- 制約: `<unavailable context or measurements, if any>`

## 可読性スコア

| 観点               | 点数 (1–5) | 根拠                                       |
| ------------------ | ---------: | ------------------------------------------ |
| 命名               |            | `<path:line> — evidence and reader impact` |
| 関数の責務         |            |                                            |
| 制御フローの複雑さ |            |                                            |
| 局所理解性         |            |                                            |
| 一貫性             |            |                                            |
| コメント           |            |                                            |
| 変更容易性         |            |                                            |

## 定量的な補助指標

- `<measurement, value, scope, and interpretation>`

## 改善提案（効果順）

1. **<General readability issue>** — `<path:line>`: `<reader burden>`。`<behavior-preserving improvement>`

## 好みとして扱った点

- `<Preference and why it does not affect the score>`
```

Omit empty sections. When no material readability issue is supported, state that explicitly and retain the evidence-backed score table. Do not edit code unless the user separately asks for an implementation.
