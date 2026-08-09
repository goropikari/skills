# Composition example

Use the shared implementation Skill for the domain task and keep quality enforcement as an explicit surrounding phase.

## First use in a repository

```text
User: Initialize the repository quality baseline.
Agent: $repository-quality-baseline
```

Use `$quality-modeling` to define or select the generic quality factors first.
Then initialize the repository baseline and review `.quality/baseline.json`,
especially `quality_model`, discovered commands, `must_quality`, and
`analysis_skills`. Correct assumptions before implementation begins.

## Feature or bug-fix task

```text
User: Implement <task>.
Agent: $<implementation-skill>
      Use the repository's acceptance criteria and `.quality/baseline.json`.
      After implementation, invoke $quality-assessment or $coding-quality-gate.
```

The implementation Skill should not spend tokens rereading the whole repository quality policy. Give it the baseline path and the task-specific requirements. The assessment/gate handles build, typecheck, lint, tests, repository-specific tools, and semantic review; the semantic reviewer receives the bounded context packet.

## Repair loop

```text
mechanical tool fails → fix code/tests → rerun tool
mechanical pass        → semantic review → fix findings → rerun gate
gate pass              → deliver
```

Do not update the baseline just because an implementation failed it. Update the baseline only when evidence shows that the repository's expected normal has changed.
