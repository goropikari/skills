# Verification Checklist

Record the command or manual procedure and the actual result for each item.

- [ ] All acceptance criteria satisfied
- [ ] Required edge cases handled
- [ ] Explicit external contracts are verified at relevant boundaries and invalid inputs
- [ ] Rejected destructive operations leave no side effect
- [ ] Relevant tests added or an explicit reason recorded
- [ ] Existing tests pass
- [ ] Typecheck passes
- [ ] Lint passes
- [ ] No unnecessary files created
- [ ] No unnecessary abstraction introduced
- [ ] No unnecessary dependency introduced
- [ ] No unrelated refactor performed
- [ ] Existing project patterns followed
- [ ] Public module/package identity matches the requested distribution identity
- [ ] Build/install target produces the requested artifact
- [ ] A built/installed artifact passes its critical consumer-facing flow
- [ ] Relevant exceptional states and partial failures are verified or explicitly documented
- [ ] Security-sensitive behavior reviewed
- [ ] Out-of-scope behavior not implemented

For every unchecked item:

```text
Not verified:
Reason:
Impact:
Alternative evidence:
Residual risk:
```
