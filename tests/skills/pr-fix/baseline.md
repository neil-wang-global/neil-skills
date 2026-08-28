# pr-fix baseline

Fresh agents received no `pr-fix` guidance. Simulations performed no writes.

## Core scenarios

| Scenario | Result | Observed behavior |
|---|---|---|
| A: one comment URL | PASS | Only linked thread selected |
| B: classification | FAIL | Missed valid items or blocked all accepted work on clarify |
| C: default worktree | PASS | Isolated worktree; no config/main change |
| D: delegated git states | FAIL | Squashed and force-pushed already-pushed commits |
| E: partial git completion | PASS | Preserved commit, added completion commit, pushed |
| F: reject/clarify | FAIL | Resolved rejected thread |
| G: reply failure | FAIL | Treated work as complete without explicit no-resolve gate |
| H: implementation boundary | FAIL | Added detailed architecture, methods, tests, and commands |

## Classification controls

Five repeated samples correctly named accept/reject/clarify, but commonly refused to implement accepted items until clarification completed. The required contract is one confirmation table, then accepted items proceed while reject/clarify receive replies and remain unresolved.

## Delegated git-state controls

Of five repeated samples, four squashed the two existing pushed commits and recommended `--force-with-lease`; one preserved them. This makes an explicit no-rewrite/no-redundant-push rule necessary.

## Implementation-brief controls

All five repeated samples failed neutrality. They prescribed cache architecture, cache keys, TTL/LRU, concurrency methods, tests, and concrete test commands. The brief must carry only accepted feedback, context, locations, and observable outcomes.

## RED conclusion

Minimal guidance must enforce:

1. Comment URL selects exactly one thread.
2. One accept/reject/clarify table and confirmation; accepted work may proceed independently.
3. Default isolated worktree without config creation.
4. Delegate only an implementation-neutral brief to `/issue-executing`.
5. Snapshot before/after git state; preserve existing commits and pushes.
6. Add one completion commit only for remaining accepted uncommitted changes; push only missing commits.
7. Reject and clarify replies remain unresolved.
8. Reply failure prevents thread resolution.
