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

## Independent-review RED regressions

A final fresh reviewer compared the implementation to the approved spec and found three missing contracts:

> `need-worktree: false` leaves `/pr-fix` with no safe checkout path for the PR head.

> GitHub thread operations omit `viewerCanReply`, `viewerCanResolve`, and the REST reply-by-comment-ID fallback.

> Repeated `/pr-fix` runs can duplicate remote replies when reject/clarify threads intentionally remain unresolved.

These failures became Scenarios I-M before the guidance was changed.

A provider-focused re-review then found:

> GitLab returns `base_commit_sha`, `start_commit_sha`, and `head_commit_sha`; the shorter names are only discussion-position payload keys.

> GitLab writes lacked explicit methods and nested payload syntax, while resolution state was not tied to the selected root note.

> GitHub nested comments lacked independent pagination and provider flows did not retrieve a canonical authenticated identity.

These became Scenario N and provider-adapter verification.

A third review found that the clone match still compared against the base target repository, making a writable fork-head clone impossible. This became Scenario O and split base API identity from head Git identity.

A fourth review found push permission was checked before classification, blocking reject/clarify-only replies on a read-only head. This became Scenario P and moved the write gate onto accepted code work only.

## Direct-config fix RED regressions

Fresh agents applied the unchanged skill and contract to Q-S. They consistently found no config-authorized `/pr-fix` path or `defer` outcome.

| Scenario | Result | Observed behavior and rationalization |
|---|---|---|
| Q: direct `true` simple fix | FAIL | Required the existing one-table confirmation; no path authorized automatic `/pr-fix` delegation/progress. |
| R: direct `true` complex defer | FAIL | Recast the API/migration finding as `clarify`: “the contract permits only `accept`, `reject`, or `clarify`.” |
| S: direct true/false regression | FAIL | Both direct configurations retained the public table; no `defer` path existed for `true` and no explicit false-mode contrast was recorded. |

The Q agent also rationalized that the review-publication clause could publish a finding rather than fix an existing thread. That clause is review-specific and cannot authorize `/pr-fix`.

## RED conclusion: config-authorized fixes

1. Matching target-repository boolean `self-reviewed:true` authorizes automatic `/pr-fix` classification/execution for direct and orchestrated calls.
2. Only config-authorized calls may auto-accept simple findings; they still build a classification table and return actual Git/thread progress.
3. Architectural/public-interface, migration, security-policy, cross-module, unclear, and high-risk findings defer with a concise reply and remain unresolved without worktree, delegation, commit, or push.
4. With `self-reviewed:false` or absent, calls retain `accept`/`reject`/`clarify`, one human table, and no `defer` bypass. Envelopes only validate orchestration handoff/sequencing.

## Boundary-revalidation RED regression

Fresh current-guidance simulation of Scenario V found that the contract's generic write rule did not name `pr-fix`'s delegation/Git boundary or each defer/reply/resolve write. It correctly refused stale blob `A`, but left false/confirmation scope and the per-boundary `authorization-changed` stop result implicit. The required guidance must re-resolve immediately before every named boundary, compare the original provider/host/repository/baseRef/blob authorization tuple, and stop that automated action on false, malformed, or any blob change.
