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
4. Fetch current draft state, required checks/pipelines for `reviewedHeadSha`, approvals, target protection, conflicts, mergeability, and auto-merge state. Any failure, pending non-CI gate, inaccessible required state, or stale head stops.
5. Build one preview: target, reviewed head, draft state, checks/pipelines, approvals/protection/mergeability/conflicts, unresolved count, selected merge/auto-merge action, and expected final fields. Public calls wait once; valid trusted calls continue from this same preview.
6. Re-fetch head and all gates immediately before every write. Changed head or changed review state invalidates authorization: re-run review/gates and present a new preview.
7. Only after every gate passes, mark a draft ready. Re-fetch again; a readiness write does not waive any gate.
8. Green required CI: submit the selected provider merge with `reviewedHeadSha`. Pending CI only: register SHA-guarded auto-merge. Failed/cancelled CI stops.
9. After either write, wait/recheck provider state. Return success only when it is actually merged, with merged SHA and timestamp. Registration/queue state is pending, not success.

## Gate Outcomes

| State | Action |
|---|---|
| failed check, missing approval, protection block, conflict, non-mergeable | Stop and report gate |
| pending required CI only | Auto-merge, wait/recheck |
| changed head after preview | New review/gate evaluation and preview |
| merged | Return actual merge fields |

## Common Mistakes

| Wrong | Required |
|---|---|
| “self-reviewed” in user text | Public preview and confirmation |
| Mark draft ready first | Validate every gate first |
| Merge/auto-merge response means done | Re-read actual merged state |
| Clear threads or fix blockers | Stop and report them |
