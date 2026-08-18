# Implementation Route Selection

Use repository evidence, not keywords alone. Select one execution mode and the
smallest set of allowed skills that improves safety or evidence.

| Signal                                                                   | Execution mode                 | Supporting skills                                                             |
| ------------------------------------------------------------------------ | ------------------------------ | ----------------------------------------------------------------------------- |
| Small local change, clear design, low risk                               | Direct                         | focused criteria, targeted tests, self-review                                 |
| Mature app, ordinary feature or bug fix                                  | Direct or staged               | `review-orchestrator` (impact review), relevant test-design skill             |
| Greenfield app, MVP, or broad product request                            | Staged                         | `prd-maker`, `review-orchestrator` (architecture / requirements review)       |
| Requirements, tests, acceptance criteria, or BDD need semantic alignment | Direct or staged               | `qe-artifact-baseline`, then matching acceptance/test-design skill            |
| Multiple dependent work units                                            | Staged                         | `review-orchestrator` (architecture / impact review), test-design skill       |
| Independent work units with clear boundaries                             | Parallel                       | `review-orchestrator` (architecture / test review)                            |
| Competing viable designs with material risk                              | Comparative                    | `review-orchestrator`, `blackbox-risk-based-test`, `whitebox-risk-based-test` |
| External artifact needs a stable black-box oracle                        | Direct, staged, or comparative | internal `implementation-acceptance-harness` plus matching test-design skill  |
| Security, privacy, migration, or compatibility risk                      | Direct, staged, or comparative | `review-orchestrator` (matching risk review) plus test-design skill           |

## Precedence rules

1. Resume an active workflow state rather than creating another one.
2. Protect destructive, security, privacy, financial, migration, and
   compatibility risks before optimizing delivery speed.
3. Use the least complex mode that covers those risks.
4. Use review findings as plan inputs, not as proof that implementation is
   complete.
5. Do not parallelize dependent work or use comparison to compensate for an
   unclear requirement.
6. Freeze a black-box oracle before implementation when the consumer-facing
   contract, destructive behavior, or candidate comparison makes it valuable.
7. Run `qe-artifact-baseline` before freezing acceptance criteria when the
   source and generated QE artefacts may not preserve the same intent. Its
   similarity bands are triage signals; human decisions and unresolved gaps
   must remain visible in the plan.

## Route decision questions

- What user-visible or consumer-visible behavior changes?
- Is the repository greenfield, newly established, or mature?
- Are there independent work units, or only sequential dependencies?
- Is there more than one implementation design worth comparing?
- What must be frozen before implementation?
- Which checks prove completion, and which failure would be unacceptable?

## Installation boundary

Select only skills available in the current installation. Resolve this
orchestrator's internal components relative to its own directory, and request
reviews through the public `review-orchestrator` entry point. The orchestrator
owns the implementation plan and performs the implementation itself.
