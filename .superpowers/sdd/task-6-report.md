# Task 6 Report: `/using-neil-workflows`

## Scope

Completed only Task 6 artifacts in the assigned worktree:

- `skills/using-neil-workflows/SKILL.md`
- `tests/skills/using-neil-workflows/verification.md`

Existing RED artifacts `scenarios.md` and `baseline.md` were retained without rewrite. No Task 7 files, specs, plans, or npm tests were touched.

## GREEN and Refactor Evidence

Fresh simulations covered A-O. They confirmed opaque raw forwarding only to fresh `issue-init`, sequential fresh-stage dispatch, parent-owned envelope leaves, false/absent stop after `pr-create`, review/fix progress controls, deferred-finding retention, exact-head merge dispatch, actual-merge gate before close, and four-proof success validation. Details are in `tests/skills/using-neil-workflows/verification.md`.

An independent requirements review identified one Task 6 design gap: a mixed simple/complex review could be interpreted as a repeated deferred fingerprint and terminate `stalled`. The skill was refactored to give mixed findings precedence: dispatch `pr-fix` for simple findings, retain complex finding URLs/fingerprints, require owned progress, then stop `needs-human-review`. A fresh Case E regression simulation confirmed that sequence.

## Verification

- `wc -w skills/using-neil-workflows/SKILL.md`: 468 words, below 500.
- `git diff --check`: exit 0 with no output.
- No npm test was run, per instruction.

## Remaining Integration Concerns

The surrounding stage skills do not yet expose every handoff leaf this parent contract expects: `issue-init`'s documented internal return does not include a normalized `self-reviewed` boolean, and `pr-review` does not document a structured internal snapshot/findings result. Also, a broader plan reportedly includes `issue-executing` between init and PR creation, while Task 6 explicitly requires `issue-init -> pr-create`. These are outside the permitted Task 6 files and were not changed. The Task 6 skill fails closed when such required owned handoffs are unavailable.

## Correction Evidence: Integration Findings Closed

This appendix supersedes the concerns above where they described missing handoff contracts. The correction changed only Task 6 artifacts and required shared/earlier-skill contracts; no specs, plans, Task 7 files, metadata, or `.build/` output were changed.

### RED Findings

Fresh no-skill controls failed because the standard path skipped `issue-executing`, issue-init had no typed `config.selfReviewed` handoff leaf, and pr-review exposed only snapshot/publication prose. The old parent also classified a pending/requested auto-merge response as `stalled` and omitted an explicit post-merge `issue-close` dispatch.

### Corrected Contracts

- Both modes now dispatch fresh sequential `issue-init -> issue-executing -> pr-create`; execution consumes normalized brief/worktree and `pr-create` consumes actual Git state.
- `issue-init` and the shared contract define `config.selfReviewed`: literal boolean true only; missing false; present non-boolean error.
- `pr-review` and the shared contract define a versioned owned result with normalized target identity, snapshot/head, finding fingerprint/thread URL/complexity/state, unresolved/deferred counts, and exact convergence/publication status. The parent validates these leaves before fix or merge routing.
- Mixed review results fix simple findings, then fully re-review the verified changed head before reporting retained deferred work as `needs-human-review`.
- Review publication preauthorization requires the parent-created owned `stage: pr-review` leaf; a wrong stage remains public.
- Review publication must be complete and successful before `pr-fix`; a failed publication or missing simple-finding thread identity is `failed`, and only `pr-review` may retry it.
- `pr-merge` owns auto-merge waiting/recheck. The parent accepts only final actual-merged, `merge-blocked`, or `failed`; actual merged state/SHA/timestamp dispatches fresh `issue-close`, whose closure/cleanup proof gates `success`.

### Fresh GREEN Simulations

A final fresh-context paper simulation passed all Task 6 A-O cases plus the publication-failure P regression, and pr-review H-K. It confirmed opaque initial arguments, fresh sequential dispatch, type normalization, review target/snapshot/finding validation, complete-publication gating, progress and repeated-fingerprint stops, mixed changed-head re-review, pending merge ownership, actual-merge-only closure, and all four success proofs. A separate fresh cross-skill simulation found no High/Medium contradiction. An independent review found and the correction closed four Medium issues: target identity in review results, mixed-head re-review, exact review-stage authorization, and incomplete publication routing.

### Mechanical Verification

- `wc -w skills/using-neil-workflows/SKILL.md`: `500` (limit `500`).
- `git diff --check`: exit `0`, no output.
- No `npm test` was run, as directed by the approved design.
