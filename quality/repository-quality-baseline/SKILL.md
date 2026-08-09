---
name: repository-quality-baseline
description: Instantiate and version a repository-specific quality model and quality state by selecting factors, measures, instruments, thresholds, and required checks. Use when starting work in an unfamiliar repository, when a repository has no quality contract, when quality expectations change, or when repeated assessment evidence requires a baseline revision.
---

# Repository Quality Baseline

Instantiate `quality-modeling` for one repository. Create a small, explicit
quality contract so agents can evaluate work against local expectations instead
of generic coding advice. The baseline is the model instance and policy; it is
not the generic quality taxonomy and it is not the current assessment result.

## Three-layer quality system

Use the following ownership boundaries:

```text
quality-modeling
  generic characteristics → factors → measures → instruments → evidence
        ↓ select and calibrate
  repository-quality-baseline
  GQM selection, benchmark calibration, thresholds, rating, aggregation,
  severity, weights, exceptions
        ↓ execute
quality-assessment
  current evidence → factor statuses → gate decision → state history
```

Invoke `$quality-modeling` when a factor or measure needs to be designed or
revised. During baseline initialization, use its vocabulary and record the
selected model instance under `quality_model` in `baseline.json`. Do not make
the baseline depend on a universal score or copy every available factor.

## Analysis skill set

Treat the following named skills as available in the shared `~/.agents/skills` directory. Invoke them by name or read their `SKILL.md` directly; do not reference or clone a remote repository during normal analysis.

Always apply:

- `$requirements-review`: clarify expected behavior and unverifiable requirements;
- `$architecture-review`: identify responsibility, dependency, and extension boundaries;
- `$change-impact-review`: trace callers, data, APIs, configuration, and operations;
- `$security-review`: identify authentication, authorization, input, secret, privacy, and abuse risks;
- `$whitebox-risk-based-test`: identify implementation-driven regression and test gaps.

Apply conditionally when the repository or change calls for them:

- `$api-compatibility-review` for public APIs, events, CLIs, schemas, or configuration;
- `$data-integrity-review` or `$migration-review` for persistence, schema, or data-format changes;
- `$concurrency-review` for parallelism, cancellation, shared state, or shutdown;
- `$privacy-review` for personal data;
- `$performance-review` for latency, throughput, memory, I/O, or scale-sensitive code;
- `$observability-review` and `$release-readiness-review` for production behavior and rollout;
- `$test-quality-review` for existing or newly added tests;
- `$readability-review` or `$code-smell-review` for maintainability expectations.

Use these skills as analysis procedures, not unquestionable policy. Translate only repository-supported findings into `must_quality`, `mechanical_checks`, `critical_defects`, or `performance_quality`. Record the names of applied skills and their evidence in `baseline.json`. Do not apply every conditional skill by default; unrelated reviews dilute the baseline and create false requirements.

## Optional analysis tools

Use `ask devin` and `graphify` when they are already exposed as callable skills or tools in the current environment and their output materially improves repository understanding:

- Use `ask devin` for an independent repository survey, likely conventions, dependency boundaries, and candidate verification commands.
- Use `graphify` for a dependency, call, module, or ownership graph when structural relationships affect the baseline.

Treat both as advisory evidence. Confirm important claims against repository files, manifests, CI, tests, and command output. If either tool is unavailable, do not install, configure, or wait for it; continue with local analysis using file search, repository metadata, manifests, CI configuration, and existing scripts. Record unavailable optional tools in `assumptions` only when their absence materially limits the analysis.

## Files to manage

Keep these files under `.quality/` at the repository root:

- `baseline.json`: versioned expectations and deterministic checks. Review and commit this file with intentional policy changes.
- `state.json`: latest gate result, check history, defects, and baseline version used. Update it after a gate run; do not use it as the quality contract.
- `README.md`: short human orientation generated only when the directory is initialized.

Read [schema.md](references/schema.md) before changing the file shape. Keep
generic factor definitions in the model Skill or its references; keep
repository-specific applicability and policy in `baseline.json`.

Before adding a rule, classify whether it is mechanically observable, semantically interpretable, or both. Use a tool for stable pass/fail oracles; use the named review Skills for intent, architecture, risk, and trade-offs. See [tool-vs-ai.md](../coding-quality-gate/references/tool-vs-ai.md) for the shared boundary and output contract.

## Repository-specific inspection tools

Create a repository-owned inspection tool when a quality rule cannot be checked reliably by the existing build, test, lint, static-analysis, or review skills. Prefer the repository's established tooling location; otherwise use `.quality/tools/` and register the tool in `baseline.json` and `mechanical_checks`.

Good candidates include API/schema compatibility checks, forbidden dependency or import checks, migration safety checks, generated-file freshness, permission matrices, domain invariants, and repository-specific configuration validation.

Every generated inspection tool must be:

- deterministic and read-only by default;
- bounded in runtime and output size;
- runnable from the repository root without network access or undeclared services;
- explicit about exit codes (`0` pass, `1` quality failure, `2` unable to evaluate);
- covered by focused fixtures or tests, including at least one failing case;
- registered with its purpose, command, applicability, and owner/evidence in `baseline.json`.

Do not create a custom tool merely to encode a subjective style preference. If the rule needs semantic judgment, keep it in the appropriate review Skill and use a custom tool only to narrow the evidence supplied to the reviewer.

## Initialize

1. Identify the repository root and inspect its manifests, CI configuration, contribution guide, scripts, and existing tests. Apply the named skills from **Analysis skill set**, then check whether `ask devin` or `graphify` is callable and use them only under **Optional analysis tools**.
2. Run the bundled initializer from the repository root:

   ```bash
   python3 <skill-dir>/scripts/init_quality_state.py --repo-root .
   ```

   Use `--force` only when the user explicitly asks to replace an existing baseline. The default is non-destructive and refuses to overwrite `baseline.json` or `state.json`.
   Execute this command automatically as the Agent; do not ask the user to copy or run it.
3. Review every discovered command. Remove commands that are not valid and add repository-specific build, typecheck, lint, unit, integration, security, or packaging checks. If an important rule still lacks a reliable check, create a repository-specific inspection tool under **Repository-specific inspection tools**, test it, and register it before declaring the baseline complete.
4. For each selected measurement family, record its GQM goal/question/metric
   relationship. Derive thresholds from documented expert sources and, where
   useful, a comparable benchmark population. Record distribution, quantile,
   rationale, date, and confidence; never present an uncalibrated threshold as
   an objective fact.
5. Select rating functions and aggregation rules. Preserve leaf-level values
   and define the drill-down path before allowing system-level aggregation.
6. Define Must Quality as pass/fail rules. At minimum cover requested behavior, build/type validity where applicable, regression protection, tests appropriate to the change, repository conventions, and critical security defects.
7. Separate Performance Quality from Must Quality. Do not make style preferences a blocking gate unless the repository already treats them as required.
8. Record assumptions in `baseline.json`, commit the baseline when the repository workflow permits it, and never claim that an unverified command is passing.

Routine baseline inspection and read-only Python helpers are Agent-owned actions. Ask the user only for policy decisions, external authenticated access, destructive changes, or an unresolved environment blocker.

## Update

Update the baseline only when evidence shows that the repository's expected normal has changed:

- add or remove a check when CI or project tooling changes;
- promote a recurring escaped defect into a Must Quality rule;
- adjust a threshold with its rationale and baseline version increment;
- preserve prior state history rather than rewriting a failed result as passed.

Do not weaken a Must Quality rule merely to make a current change pass. Repair the change or obtain an explicit policy decision from the user.

## Handoff to assessment and gate

After initialization or update, invoke `$quality-assessment` for assessment
work. `$coding-quality-gate` may orchestrate that assessment and its bundled
mechanical runner, but neither the gate nor an implementation Skill may
redefine the model or baseline during a task.

## Compose with implementation skills

Use this Skill as the quality-contract phase around an implementation Skill from the shared `~/.agents/skills` directory:

```text
$repository-quality-baseline  (once per repository or when the baseline changes)
        ↓
$<goropikari implementation skill>  (plan and implement the task)
        ↓
$quality-assessment / $coding-quality-gate  (evidence, evaluation, repair loop)
        ↓
Deliver only after PASS or an explicitly accepted exception
```

Pass the implementation Skill the repository root, task acceptance criteria, and the path to `.quality/baseline.json`. Do not ask the implementation Skill to redefine Must Quality during the task. If implementation work reveals a missing stable rule, finish the task using the current baseline, then propose a repository-specific tool or baseline update as a separate evidence-backed change.

Do not rerun baseline initialization for every task when `.quality/baseline.json` is current. Reanalyze only when the stack, CI, architecture, public contract, recurring defects, or team expectations have materially changed.
