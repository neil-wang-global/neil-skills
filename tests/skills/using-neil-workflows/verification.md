# GREEN verification: `/using-neil-workflows`

## Supersession

The pre-correction table that described `issue-init -> pr-create`, mixed findings without a changed-head re-review, and pending auto-merge as `stalled` is superseded and removed. The current evidence follows.

## Task 6 Correction Regression

Fresh-context RED controls exposed three contract gaps: the parent skipped `issue-executing`; issue-init did not export typed `config.selfReviewed`; and pr-review returned prose insufficient for validated routing. The parent also incorrectly treated pending auto-merge as `stalled`.

Fresh GREEN simulations passed the current A-V terminal graph:

| Cases | Corrected evidence |
| --- | --- |
| A-C | Raw arguments go only to fresh `issue-init`; every run dispatches fresh `issue-init -> issue-executing -> pr-create`. The parent routes exclusively from a validated remote target-base `pr-create.automation.enabled` leaf bound to target provider/host/repository/base ref/blob: local `issue-init.config.selfReviewed` true cannot override remote false, and local false/absent cannot suppress remote true. |
| D-E | Simple findings run `pr-review -> pr-fix -> pr-review`; mixed findings retain deferrals and re-review the verified changed head before `needs-human-review`. |
| F-G | Complex-only and retained deferred work stay visible as `needs-human-review`; a repeated accepted fingerprint after its fix is `stalled`. |
| H-I | No fix progress is `stalled`; malformed/version/identity/stage failures are `failed`. |
| J-K | Remote target-base `pr-create.automation.enabled:false` ends `complete` after `pr-create`, regardless of issue-init config; remote `true` alone permits review routing. Merge requires a target-matching, current-head, zero-new/unresolved/deferred, converged and fully published review result. |
| L-O | `pr-merge` owns pending/registered auto-merge wait and recheck; only final actual merge dispatches fresh `issue-close`; success validates merge, closure, clean workspace, and updated base. |
| P | Incomplete/failed review publication, or a new simple finding without a usable thread identity, ends `failed`; only `pr-review` owns retry. |
| Q | A complex/deferred candidate with null/missing thread/discussion URL, including failed trusted non-inline publication, ends `failed`; never `needs-human-review`. |
| R | An otherwise trusted `/pr-fix` envelope with `stage: pr-review` remains standalone and cannot auto-accept or defer. |
| S | A malformed, fabricated, unrelated, or target-mismatched complex/deferred URL/binding is `publication-failed`, then `failed`; never `needs-human-review`. |
| T | Zero new/deferred findings with a retained accepted simple thread unresolved after reply/resolution failure ends `needs-human-review`, lists its validated URL/identity, and never merges. |

A separate fresh review-handoff simulation passed: `pr-review` returns a versioned owned target, snapshot/head, finding fingerprint/thread URL/thread target/complexity/state, and exact convergence/publication leaves; duplicate suppression preserves unresolved/deferred state. Its trusted publication path requires owned `stage: pr-review`; a wrong stage remains public.

## Current Mechanical Checks

```text
wc -w skills/pr-create/SKILL.md skills/pr-fix/SKILL.md skills/pr-review/SKILL.md skills/using-neil-workflows/SKILL.md
464 skills/pr-create/SKILL.md
500 skills/pr-fix/SKILL.md
495 skills/pr-review/SKILL.md
464 skills/using-neil-workflows/SKILL.md

git diff --check
exit 0; no output
```

## Task 7 Fresh End-to-End Pressure Flows

All following checks were read-only fresh-context contract simulations against the current stage documents; no simulation issued provider, Git, or cleanup commands.

| Flow | Result | Verified terminal behavior |
| --- | --- | --- |
| `false -> issue-init -> issue-executing -> pr-create` | PASS | Literal `config.selfReviewed:false` dispatches exactly those three stages and ends `complete`; review, fix, merge, and close do not dispatch. |
| `true/simple -> review/fix convergence -> pr-merge -> actual merge -> issue-close` | PASS | A localized, clear, directly verifiable finding is fixed on a changed head, then a full clean re-review binds the merge to that head. Actual provider merged state, SHA, and timestamp precede clean-worktree closure and `success`. |
| `true/mixed -> simple fixed, complex unresolved` | PASS | The simple finding is fixed, while the target-valid deferred complex finding remains visible after the changed-head re-review. The result is `needs-human-review`; `pr-merge` and `issue-close` do not dispatch. |
| final merge gate blocked | PASS | A missing approval or failed required check after a clean current-head review ends `merge-blocked`. No actual merge proof exists, so `issue-close` does not dispatch. |
| actual merge then dirty cleanup | PASS | `/pr-merge` has already returned matching actual merged state, SHA, and timestamp. `/issue-close` stops with all cleanup leaves `untouched`; the parent reports `failed` rather than `success`, and the completed merge remains preserved. |
| `issue-executing` handoff/stage failure | PASS | The parent stops at that exact stage as `failed`, retains valid `issue-init` state and any prior side effects, and dispatches no later PR, review, merge, or close stage. |

The dirty-cleanup stage itself reports `status:"stopped"`; the documented parent terminal status is `failed` because closure/cleanup cannot be validated. This distinction retains the merged side effect honestly instead of implying a rollback.

## Final-Review Envelope Regression

Fresh guided W-X simulations constructed the first dispatch exactly as `{version:"neil-workflow/v1",caller:"using-neil-workflows",mode:"standard",stage:"issue-init",input:<opaque raw args>}` with no `handoff`. Nested input remained opaque and reached only fresh `issue-init`. Each later stage accepted only its validated owned `handoff`; an injected `input` leaf for `issue-executing`, `pr-create`, `pr-review`, `pr-fix`, `pr-merge`, or `issue-close` was rejected before dispatch as malformed and ended `failed`. No raw input or fragment crossed the issue-init boundary.

Mechanical recheck: `pr-fix` is 499 words (cap 500), `using-neil-workflows` is 474 words, and `git diff --check` exits 0 with no output.

## Task 3 Static Language Handoffs

Document-only contract inspection covers Y-Z: the parent validates and forwards string `textLanguage` plus target-bound remote resolver identity, but never translates, creates provider text, or creates commits. Base `English` overrides local/head/fork `简体中文` for later PR/review/reply/commit content. A later remote change applies only to the next generated stage; earlier text is not rewritten. New generated prose conforms to the resolved language while quotations, identifiers, URLs, and `neil-self-reviewed/v1` remain exact.

Static records also cover ordered default JSON and empty/absent `textLanguage:""` compatibility in `issue-init`. No executable test suite was run.
