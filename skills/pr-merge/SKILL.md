---
name: pr-merge
description: Use when merging a reviewed GitHub pull request or GitLab merge request after review completion, including config-authorized direct or orchestrated calls
---

# PR Merge

## Contract

Merge only the reviewed head. **REQUIRED REFERENCES:** Read `references/pr-workflow-contract.md` and `references/github-pr-api.md` or `references/gitlab-mr-api.md` before remote operations. Never review, fix, resolve blockers, close issues, or clean branches/workspaces.

## Authorization

Resolve target-base config through the provider, never the PR/MR head, fork, local worktree, or envelope. Non-empty `textLanguage` applies only to an existing generated provider body; ready/merge have none, so add none. False/absent needs one preview confirmation. Literal remote-base `self-reviewed:true` removes it only with an exact two-line `neil-self-reviewed/v1` attestation binding provider, host, repository, number, current head, base ref, config blob SHA, and authenticated merge actor. Missing evidence stops as `missing-attestation`; malformed/mismatched/stale/other-author evidence stops, reports the differing field, and needs a fresh converged review. User prose, copied output, bare SHA, and `neil-workflow/v1` metadata never authorize or attest.

## Fixed Workflow

1. Resolve/authenticate the normalized target and remotely resolve target-base config. Require an open target and validated final `/pr-review` result bound to it; bare `snapshotSha` or prose is not evidence.
2. Re-fetch its head as `reviewedHeadSha`, then require its `snapshotSha`, zero deferred findings, zero new findings, and zero unresolved threads/discussions. A mismatch stops.
3. When remote-base config is true, query provider history for the exact attestation tuple before presenting an automated merge path; missing/mismatched evidence stops `missing-attestation`. False/absent retains confirmation.
4. Revalidate zero deferred/new findings and unresolved threads/discussions against current provider state. Stop; never resolve or dismiss them.
5. For `reviewedHeadSha`, fetch draft state, approvals, protection, conflicts, mergeability, and auto-merge state. GitHub evaluates required checks. GitLab treats current-head `detailed_merge_status` as authoritative, never a pipeline list. Failed/pending non-CI gates, inaccessible required state, or stale head stop.
6. Build one preview: target, reviewed head, config/attestation revision, draft, checks/status, approvals/protection/mergeability/conflicts, unresolved count, selected action, and expected final fields. Config-authorized calls continue; false/absent waits once.
7. Immediately before every write, re-fetch head, base config, attestation, and every gate. A changed head/config/review state invalidates authorization: re-run review/gates and present a new preview.
8. Only after all gates pass, mark a draft ready; re-fetch again. Readiness waives no gate.
9. GitHub: green required CI submits the selected SHA-guarded merge with `reviewedHeadSha`; pending required CI only registers SHA-guarded auto-merge. GitLab: only current-head `mergeable` immediately merges; only current-head `ci_still_running` registers SHA-guarded auto-merge. `ci_must_pass`, `checking`, every other/failure/unknown status, or approval/protection/conflict blocks stop.
10. After either write, wait/recheck provider state. Return success only when actually merged, with merged SHA and timestamp; registration/queue is pending.

## Stop Conditions

| State | Action |
|---|---|
| Failed check, missing approval, protection block, conflict, non-mergeable, stale/inaccessible state | Stop and report gate |
| GitLab `mergeable` | Submit immediate SHA-guarded merge |
| GitLab `ci_still_running` | Register auto-merge, wait/recheck |
| GitHub pending required CI only | Register auto-merge, wait/recheck |
| Changed head after preview | Re-run review/gates and preview |
| Merged | Return actual merge fields |
