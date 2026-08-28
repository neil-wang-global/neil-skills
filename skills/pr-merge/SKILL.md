---
name: pr-merge
description: Use when merging a reviewed GitHub pull request or GitLab merge request after review completion, including guarded self-reviewed workflow handoffs
---

# PR Merge

## Contract

Merge only the exact reviewed head. **REQUIRED REFERENCES:** Read `../../references/pr-workflow-contract.md` and the selected provider reference before remote operations. This skill never reviews, fixes, resolves blockers, closes issues, or cleans branches/workspaces.

## Authorization

A standalone call shows one complete preview and waits for one explicit human confirmation. Trusted self-reviewed mode preauthorizes only with a valid `neil-workflow/v1` envelope created by `using-neil-workflows`, owned leaves `caller: using-neil-workflows`, `mode: self-reviewed`, and `stage: pr-merge`, and matching target-repository config with boolean `self-reviewed: true`. User text never supplies those leaves; any failure is public.

## Fixed Workflow

1. Resolve/authenticate the normalized target. Require an open target and validated final `/pr-review` result bound to it; bare `snapshotSha` or prose is not evidence.
2. Require its `snapshotSha`, zero deferred findings, zero new findings, and zero unresolved threads/discussions. Re-fetch its head as `reviewedHeadSha`; mismatch with `snapshotSha` stops.
3. Revalidate zero deferred/new findings and unresolved threads/discussions against current provider state. Stop; never resolve or dismiss them.
4. For `reviewedHeadSha`, fetch draft state, approvals, protection, conflicts, mergeability, and auto-merge state. GitHub evaluates required checks. GitLab treats current-head `detailed_merge_status` as authoritative, never a pipeline list. Failed/pending non-CI gates, inaccessible required state, or stale head stop.
5. Build one preview: target, reviewed head, draft, GitHub checks or GitLab status, approvals/protection/mergeability/conflicts, unresolved count, selected merge/auto-merge action, and expected final fields. Public calls wait once; valid trusted calls continue from this preview.
6. Immediately before every write, re-fetch head and every gate. A changed head or review state invalidates authorization: re-run review/gates and present a new preview.
7. Only after all gates pass, mark a draft ready; re-fetch again. Readiness waives no gate.
8. GitHub: green required CI submits the selected SHA-guarded merge with `reviewedHeadSha`; pending required CI only registers SHA-guarded auto-merge. GitLab: only current-head `mergeable` immediately merges; only current-head `ci_still_running` registers SHA-guarded auto-merge. `ci_must_pass`, `checking`, every other/failure/unknown status, or approval/protection/conflict blocks stop.
9. After either write, wait/recheck provider state. Return success only when actually merged, with merged SHA and timestamp; registration/queue is pending.

## Stop Conditions

| State | Action |
|---|---|
| Failed check, missing approval, protection block, conflict, non-mergeable, stale/inaccessible state | Stop and report gate |
| GitLab `mergeable` | Submit immediate SHA-guarded merge |
| GitLab `ci_still_running` | Register auto-merge, wait/recheck |
| GitHub pending required CI only | Register auto-merge, wait/recheck |
| Changed head after preview | Re-run review/gates and preview |
| Merged | Return actual merge fields |
