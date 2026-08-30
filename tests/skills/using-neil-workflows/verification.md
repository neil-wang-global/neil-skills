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
