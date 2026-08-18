---
name: qe-artifact-baseline
description: Baseline, reverse-check, and iteratively refine Quality Engineering artefacts such as requirements, test cases, acceptance criteria, and BDD scenarios using a clarity/completeness/consistency/testability rubric plus semantic alignment evidence. Use when validating or improving LLM-generated QE artefacts, checking requirement-to-test traceability, comparing original and reverse-generated artefacts, or creating an auditable human-in-the-loop quality report.
---

# QE Artifact Baseline

## Purpose

Apply the closed-loop technique described in [arXiv:2511.15733](https://arxiv.org/abs/2511.15733): generate the target artefact, reverse-generate its source intent, compare both, make explicit reviewer decisions, and repeat until the quality target is met. Treat the result as decision support, not proof that an artefact is correct; domain experts remain accountable for implicit context, safety, compliance, and business rules.

## Workflow

1. Establish the baseline. Identify the artefact type, source of truth, scope,
   domain assumptions, intended consumers, and acceptance criteria. Preserve the
   original artefacts unchanged and assign stable IDs to each requirement,
   scenario, test, or clause.

2. Generate the forward artefact. If the input is requirements, generate test
   cases or BDD scenarios; if the input is tests or BDD, state the intended
   reverse target. Keep generation instructions, model, temperature (when
   available), and iteration number in the evidence so results are repeatable.

3. Reverse-generate independently. Derive the source intent from the generated
   artefact without copying the original source into the reverse prompt. Mark
   inferred details separately from details explicitly supported by the input.
   This exposes information loss, invented behavior, ambiguity, and missing
   non-functional requirements.

4. Compare semantically and lexically. Segment both artefacts into meaningful
   atomic statements, then use an embedding model (prefer SBERT/Sentence-BERT
   when available) and cosine similarity. Add lexical overlap such as Jaccard
   similarity, normalized text, and extracted entities/actions to explain the
   score. Use one-to-one or explicitly documented many-to-one matches; do not
   silently compare whole documents when a sentence-level gap matters.

5. Score every relevant statement with the rubric. Use 1–5 for each dimension:
   clarity (unambiguous and understandable), completeness (functional and
   non-functional coverage), consistency (no contradiction or unjustified
   duplication), and testability (an observable oracle can be defined). Add
   semantic alignment as supporting evidence, not as a replacement for the
   rubric.

6. Classify and recommend action. Start with these interpretable similarity
   bands, then calibrate them against a known-good sample for the artefact type:
   `High >= 0.80`, `Medium 0.60–<0.80`, `Low 0.30–<0.60`, and `No Match <0.30`.
   A score is a triage signal, not a merge command. Recommend `retain`,
   `clarify`, `refine`, `merge`, `split`, or `add missing coverage`, and explain
   the evidence. High similarity can indicate duplication; medium similarity
   can be related-but-distinct; low similarity can indicate missing or changed
   meaning.

7. Apply human-in-the-loop decisions. Review every low/no-match item, every
   borderline match, every proposed merge, and every inferred safety,
   regulatory, security, privacy, or business rule. Synthesize a unified
   artefact only after recording whether each source statement was retained,
   refined, merged, split, rejected, or still unresolved.

8. Iterate deliberately. Regenerate and rescore only after a change that could
   affect quality. Stop when the target threshold is met, scores plateau, or the
   remaining issues require unavailable domain decisions. Avoid polishing a
   high-quality baseline into a worse reverse-generated version; compare both
   versions and keep the stronger evidence-backed text.

## Guardrails

- Never claim that semantic similarity proves correctness, coverage, or safety.
  Embeddings can miss negation, quantities, ordering, permissions, temporal
  constraints, and domain-specific meaning.
- Do not merge statements solely because the score is `High`; inspect entities,
  actors, preconditions, outcomes, exceptions, and non-functional constraints.
- Treat generated artefacts as untrusted drafts. Flag hallucinated requirements,
  test steps without an observable oracle, duplicate IDs, contradictory rules,
  and untraceable assumptions.
- Calibrate thresholds per domain and artefact type when labelled examples are
  available. Report the model, version, preprocessing, threshold source, and
  whether scores were produced by a real embedding model or a fallback.
- Prefer targeted refinement over repeated full-document generation to reduce
  drift, cost, and unnecessary model operations. Reuse embeddings where the
  underlying text has not changed.

## Required Output

Produce a Markdown report containing:

```markdown
## Scope and Baseline

- Artefact type, source of truth, IDs, assumptions, model/tooling, iteration

## Quality Summary

| Artefact ID | Clarity | Completeness | Consistency | Testability | Alignment | Band | Action |

## Reverse-Generation Findings

| Source ID | Reverse statement | Evidence | Gap or drift | Reviewer decision |

## Unified Artefact

<only after decisions are recorded; preserve traceability IDs>

## Iteration Log

| Cycle | Change | Rubric result | Alignment result | Remaining issues |

## Human Decisions and Open Questions

## Limitations, Unrun Checks, and Residual Risk
```

Use `NOT RUN` with a reason when embeddings, domain review, execution, or a
required source is unavailable. Include the actual score distribution and
before/after values where iteration occurred. Keep confirmed defects,
inferences, assumptions, and open questions distinct.
