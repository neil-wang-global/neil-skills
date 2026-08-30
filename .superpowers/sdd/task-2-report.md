# Task 2 Report: Target-Stage Text Generation

## Scope

Implemented only Task 2 in `/Users/neil/Workspace/mine_craft/neil-skills`, preserving the shared remote target-base resolver contract from commit `bae4ebe` and leaving the pre-existing Task 1 reference-path edits uncommitted.

## Changes

- `skills/pr-create/SKILL.md`
  - Resolves target-base configuration before creating a new target.
  - Uses non-empty remote `textLanguage` for a new PR/MR title and generated `Summary`, `Testing`, and `Issue` prose.
  - Leaves an existing target unchanged and returns `textLanguage` in the automation routing leaf.

- `skills/pr-review/SKILL.md`
  - Resolves `textLanguage` before preview and re-resolves it with the existing stale head/config check before provider writes.
  - Applies the fresh language to newly generated finding titles/explanations, inline and non-inline comments, and report prose.
  - Explicitly retains the exact `neil-self-reviewed/v1` marker and payload.

- `skills/pr-fix/SKILL.md`
  - Applies remote language to classification reasons, all generated replies, and completion commit subject/body.
  - Keeps the existing delegation, completion, and per-provider-write gates; fresh language affects only content created after each gate.

- `skills/pr-merge/SKILL.md` and `skills/issue-close/SKILL.md`
  - Require target-base language for any existing generated provider body.
  - Document that current ready/merge and issue-close operations have no generated body and must not receive invented messages.
  - Preserve existing merge proof, attestation, stale-state, and cleanup safeguards.

- `references/github-pr-api.md` and `references/gitlab-mr-api.md`
  - Document `language` parsing to `textLanguage` and distinguish generated prose from fixed API/protocol values.
  - Preserve endpoint values, API field names, enums, URL/ID/SHA bindings, fingerprints, fixed issue relationship syntax, and the exact attestation marker/payload.

## Static Verification

Executed only the user-requested static checks; no executable test suite was run.

```text
git diff --check
# exit 0, no whitespace errors

wc -w skills/pr-create/SKILL.md skills/pr-review/SKILL.md skills/pr-fix/SKILL.md skills/pr-merge/SKILL.md skills/issue-close/SKILL.md
476 skills/pr-create/SKILL.md
500 skills/pr-review/SKILL.md
415 skills/pr-fix/SKILL.md
493 skills/pr-merge/SKILL.md
412 skills/issue-close/SKILL.md
```

## Concern

`pr-create`, `pr-review`, and `pr-merge` contained a pre-existing uncommitted Task 1 reference-path change. The Task 2 commit stages only Task 2 hunks and intentionally excludes those pre-existing edits.
