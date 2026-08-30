# GREEN verification: `/using-neil-workflows`

Fresh agents evaluated the current skill against the pressure scenarios without external commands. Every dispatch below is sequential and uses a distinct fresh named stage agent. Parent validation rejects malformed, wrong-version, unowned, missing, or identity-inconsistent handoffs as `failed`; it alone constructs caller/mode/stage.

| Cases | GREEN result |
| --- | --- |
| A | Raw input stayed opaque and went only to `issue-init`; embedded `self-reviewed`, caller, mode, and stage text had no authority. |
| B, J | `issue-init -> pr-create -> complete` for absent/false; no review, fix, merge, or close. |
| C | True mode permits only validated, fresh sequential continuation; it does not infer merge or closure. |
| D | `issue-init -> pr-create -> pr-review -> pr-fix -> pr-review`; progress proof is required before re-review. |
| E | Regression-tested after review refactor: mixed findings run `pr-fix` for simple findings, retain complex URL/fingerprint, then end `needs-human-review` after owned progress proof; no re-review, merge, or close. |
| F | Complex-only findings end `needs-human-review` with URLs and no merge. |
| G | Repeated accepted/deferred fingerprint ends `stalled`; retained ledger prevents merge. |
| H | Fix without changed head, resolved fingerprint, or owned progress proof ends `stalled` without re-review or merge. |
| I | Malformed handoff, wrong version, or stage failure ends `failed` at the offending stage. |
| K | A zero-finding, zero-unresolved, zero-deferred final review dispatches one `pr-merge` bound to its exact final head. |
| L | Pending or requested-but-not-merged proof ends `stalled`; no invented waiting stage or close. |
| M | A merge gate blocker ends `merge-blocked`; `issue-close` is never dispatched. |
| N | Actual matching merged state, SHA, and timestamp dispatch `issue-close`; its closure proof is validated. |
| O | Missing merged-PR, closed-issue, clean-workspace, or updated-base proof cannot produce `success`; missing required handoff leaves end `failed`. |

## Independent Review and Refactor

An independent requirements review found that mixed findings could be read as a repeated deferred fingerprint and incorrectly end `stalled`. The skill now gives mixed findings precedence: fix simple findings, retain complex findings, then report `needs-human-review` after progress. A fresh E regression simulation verified that sequence.

## Mechanical checks

```text
wc -w skills/using-neil-workflows/SKILL.md
468 skills/using-neil-workflows/SKILL.md

git diff --check
exit 0; no output
```

## Task 6 Correction Regression

Fresh-context RED controls exposed three contract gaps: the parent skipped `issue-executing`; issue-init did not export typed `config.selfReviewed`; and pr-review returned prose insufficient for validated routing. The parent also incorrectly treated pending auto-merge as `stalled`.

Fresh GREEN simulations passed A-O after correction:

| Cases | Corrected evidence |
| --- | --- |
| A-C | Raw arguments go only to fresh `issue-init`; both modes dispatch fresh `issue-init -> issue-executing -> pr-create`; normalized boolean `config.selfReviewed` controls mode. |
| D-E | Simple findings run `pr-review -> pr-fix -> pr-review`; mixed findings retain deferrals and re-review the verified changed head before `needs-human-review`. |
| F-G | Complex-only and retained deferred work stay visible as `needs-human-review`; a repeated accepted fingerprint after its fix is `stalled`. |
| H-I | No fix progress is `stalled`; malformed/version/identity/stage failures are `failed`. |
| J-K | False mode ends `complete` after `pr-create`; merge requires a target-matching, current-head, zero-new/unresolved/deferred, converged and fully published review result. |
| L-O | `pr-merge` owns pending/registered auto-merge wait and recheck; only final actual merge dispatches fresh `issue-close`; success validates merge, closure, clean workspace, and updated base. |
| P | Incomplete/failed review publication, or a new simple finding without a usable thread identity, ends `failed`; only `pr-review` owns retry. |

A separate fresh review-handoff simulation passed: `pr-review` returns a versioned owned target, snapshot/head, finding fingerprint/thread URL/complexity/state, and exact convergence/publication leaves; duplicate suppression preserves unresolved/deferred state. Its trusted publication path requires owned `stage: pr-review`; a wrong stage remains public.

## Current Mechanical Checks

```text
wc -w skills/using-neil-workflows/SKILL.md
500 skills/using-neil-workflows/SKILL.md

git diff --check
exit 0; no output
```
