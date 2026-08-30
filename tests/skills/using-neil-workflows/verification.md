# GREEN verification: `/using-neil-workflows`

## Supersession

The pre-correction table that described `issue-init -> pr-create`, mixed findings without a changed-head re-review, and pending auto-merge as `stalled` is superseded and removed. The current evidence follows.

## Task 6 Correction Regression

Fresh-context RED controls exposed three contract gaps: the parent skipped `issue-executing`; issue-init did not export typed `config.selfReviewed`; and pr-review returned prose insufficient for validated routing. The parent also incorrectly treated pending auto-merge as `stalled`.

Fresh GREEN simulations passed the current A-P terminal graph:

| Cases | Corrected evidence |
| --- | --- |
| A-C | Raw arguments go only to fresh `issue-init`; both modes dispatch fresh `issue-init -> issue-executing -> pr-create`; normalized boolean `config.selfReviewed` controls mode. |
| D-E | Simple findings run `pr-review -> pr-fix -> pr-review`; mixed findings retain deferrals and re-review the verified changed head before `needs-human-review`. |
| F-G | Complex-only and retained deferred work stay visible as `needs-human-review`; a repeated accepted fingerprint after its fix is `stalled`. |
| H-I | No fix progress is `stalled`; malformed/version/identity/stage failures are `failed`. |
| J-K | False mode ends `complete` after `pr-create`; merge requires a target-matching, current-head, zero-new/unresolved/deferred, converged and fully published review result. |
| L-O | `pr-merge` owns pending/registered auto-merge wait and recheck; only final actual merge dispatches fresh `issue-close`; success validates merge, closure, clean workspace, and updated base. |
| P | Incomplete/failed review publication, or a new simple finding without a usable thread identity, ends `failed`; only `pr-review` owns retry. |
| Q | A complex/deferred candidate with null/missing thread/discussion URL, including failed trusted non-inline publication, ends `failed`; never `needs-human-review`. |
| R | An otherwise trusted `/pr-fix` envelope with `stage: pr-review` remains standalone and cannot auto-accept or defer. |

A separate fresh review-handoff simulation passed: `pr-review` returns a versioned owned target, snapshot/head, finding fingerprint/thread URL/complexity/state, and exact convergence/publication leaves; duplicate suppression preserves unresolved/deferred state. Its trusted publication path requires owned `stage: pr-review`; a wrong stage remains public.

## Current Mechanical Checks

```text
wc -w skills/pr-fix/SKILL.md skills/pr-review/SKILL.md skills/using-neil-workflows/SKILL.md
498 skills/pr-fix/SKILL.md
453 skills/pr-review/SKILL.md
484 skills/using-neil-workflows/SKILL.md

git diff --check
exit 0; no output
```
