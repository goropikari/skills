# Gate evaluation guidance

## Finding severity

- `critical`: blocks delivery immediately; examples include security compromise, data loss, broken required behavior, or a regression in a protected path.
- `major`: blocks delivery when it violates a Must Quality rule or leaves a high-confidence defect in the requested scope.
- `minor`: non-blocking improvement or Performance Quality issue.

Every finding needs a file or behavior location, observed evidence, impact, and a remediation or explicit disposition. Avoid vague findings such as “could be cleaner.”

## Check status

- `PASS`: command ran and passed.
- `FAIL`: command ran and failed.
- `SKIPPED`: not applicable, with a reason.
- `BLOCKED`: could not obtain evidence because of environment or external state.

Pre-existing failures may be marked `FAIL` with `blocking: false` only when the changed scope does not affect them and the evidence is recorded. Never convert a changed-path failure to non-blocking merely because it existed before.
