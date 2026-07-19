---
name: concurrency-review
description: Review concurrent code for data races, deadlocks, leaks, unsafe ownership, cancellation, and shutdown defects.
---

# Concurrency Review

並行・非同期コードの lifecycle と共有状態をレビューする。具体的な実行順序で問題を説明する。

## Workflow

1. goroutine/thread/task、channel/queue、lock、atomic、future の所有者と終了条件を表にする。
2. 共有可変状態と read/write の同期方法を追跡する。
3. lock ordering、channel close、buffer、wait/join、callback 再入を確認する。
4. timeout、cancellation、context、error、retry、shutdown の各経路を追跡する。
5. race、deadlock、leak、use-after-close、double completion、重複実行の interleaving を構成する。
6. race detector、stress test、timeout test など最小の検証を提案する。

## Focus

- ownership と close responsibility
- cancellation の伝播と無視される error
- blocking operation と bounded resource
- shared state の visibility
- graceful shutdown と drain
- idempotency、重複 callback、再入

## Output

```markdown
## Concurrency Summary

## Findings

### [Severity: Critical/High/Medium/Low] Title

- Evidence:
- Triggering interleaving:
- Failure:
- Scope:
- Suggested fix:
- Suggested verification:

## Lifecycle / Ownership Map

## Unverified Schedules
```

実行順序を示せない推測は Unverified として扱う。
