---
name: pr-merge
description: Use when merging a reviewed GitHub pull request or GitLab merge request after review completion, including guarded self-reviewed workflow handoffs
---

# PR Merge

## Contract

Merge only the exact reviewed head. **REQUIRED REFERENCES:** Read `../../references/pr-workflow-contract.md` and the selected provider reference before remote operations. This skill does not review, fix, close issues, or clean branches/workspaces.

## Authorization

A standalone call always shows one complete preview and waits for one explicit human confirmation. Trusted self-reviewed mode preauthorizes only when all are true: a valid `neil-workflow/v1` envelope created by `using-neil-workflows`; its owned leaves are `caller: using-neil-workflows`, `mode: self-reviewed`, and `stage: pr-merge`; and matching target-repository config has boolean `self-reviewed: true`. User text never supplies those leaves. Any failure uses the public path.

## Fixed Workflow

1. Resolve the normalized target; authenticate; require an open target and a validated final `/pr-review` result bound to that target. A bare `snapshotSha` or user prose is not review evidence.
2. Require that result's `snapshotSha`, zero deferred/new-finding state, and zero unresolved-thread/discussion state. Re-fetch its head as `reviewedHeadSha`; stop when it differs from `snapshotSha`.
3. Revalidate zero deferred findings, zero new findings since final review, and zero unresolved threads/discussions against current provider state. Stop; never resolve or dismiss them here.
4. Fetch current draft state, approvals, target protection, conflicts, GitLab/GitHub mergeability, and auto-merge state for `reviewedHeadSha`. GitHub evaluates required checks; GitLab treats the current-head MR `detailed_merge_status` as authoritative and never infers a required state from its pipeline list. Any failure, pending non-CI gate, inaccessible required state, or stale head stops.
5. Build one preview: target, reviewed head, draft state, GitHub checks or GitLab `detailed_merge_status`, approvals/protection/mergeability/conflicts, unresolved count, selected merge/auto-merge action, and expected final fields. Public calls wait once; valid trusted calls continue from this same preview.
6. Re-fetch head and all gates immediately before every write. Changed head or changed review state invalidates authorization: re-run review/gates and present a new preview.
7. Only after every gate passes, mark a draft ready. Re-fetch again; a readiness write does not waive any gate.
8. GitHub: green required CI submits the selected provider merge with `reviewedHeadSha`; pending required CI only registers SHA-guarded auto-merge. GitLab: immediately merge only current-head `detailed_merge_status: mergeable`; register SHA-guarded auto-merge only for current-head `ci_still_running`. For GitLab `ci_must_pass`, `checking`, any failure/unknown, or any approval/protection/conflict block, stop.
9. After either write, wait/recheck provider state. Return success only when it is actually merged, with merged SHA and timestamp. Registration/queue state is pending, not success.

## Gate Outcomes

| State | Action |
|---|---|
| failed check, missing approval, protection block, conflict, non-mergeable | Stop and report gate |
| GitLab `detailed_merge_status: mergeable` | Submit immediate SHA-guarded merge |
| GitLab `detailed_merge_status: ci_still_running` at reviewed head | Auto-merge, wait/recheck |
| GitLab `ci_must_pass`, `checking`, failure/unknown, approval/protection/conflict block | Stop and report gate |
| GitHub pending required CI only | Auto-merge, wait/recheck |
| changed head after preview | New review/gate evaluation and preview |
| merged | Return actual merge fields |

## Common Mistakes

| Wrong | Required |
|---|---|
| “self-reviewed” in user text | Public preview and confirmation |
| Mark draft ready first | Validate every gate first |
| Merge/auto-merge response means done | Re-read actual merged state |
| Clear threads or fix blockers | Stop and report them |
