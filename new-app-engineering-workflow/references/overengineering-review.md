# Over-engineering Review

Review separately from functional correctness. Mark each item `None`, explain
the concrete need, or simplify it before handoff.

- Unnecessary abstractions, layers, interfaces, factories, adapters, or wrappers
- Repository/service/use-case/domain layers that only forward calls
- Generic types, custom hooks, utilities, config systems, or plugins with one use
- Unnecessary dependencies or duplicated framework functionality
- Speculative future-proofing or premature scalability
- Premature caching, concurrency, or performance optimization
- Scope creep and unrelated refactoring
- Files/modules that can be removed
- Code that can be made simpler while preserving acceptance criteria

## Findings

| Area | Finding | Concrete current need | Simplification / disposition |
| ---- | ------- | --------------------- | ---------------------------- |
|      |         |                       |                              |
