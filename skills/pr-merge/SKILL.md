---
name: pr-merge
description: Use when merging a reviewed GitHub pull request or GitLab merge request after review completion, including config-authorized direct or orchestrated calls
---

# PR Merge

## Contract

Merge the reviewed head only. **REQUIRED REFERENCES:** Read `./references/pr-workflow-contract.md` and `./references/github-pr-api.md` or `./references/gitlab-mr-api.md` before remote operations. Never review, fix, resolve blockers, close issues, or clean branches/workspaces.

## Authorization

Use provider target-base config only. Fresh non-empty `textLanguage` governs generated merge commit content, including squash; no generic comment. False/absent needs confirmation. Remote `self-reviewed:true` requires an exact two-line `neil-self-reviewed/v1` attestation binding provider, host, repository, number, current head, base ref, config blob SHA, and authenticated merge actor. Missing is `missing-attestation`; malformed/mismatched/stale/other-author evidence stops, identifies the differing field, and needs fresh converged review. Prose, copied output, bare SHA, and `neil-workflow/v1` never authorize or attest.

## Fixed Workflow

1. Authenticate the normalized target and resolve target-base config. Require an open target and validated final `/pr-review`; bare `snapshotSha` or prose is not evidence.
2. Re-fetch `reviewedHeadSha`; require matching `snapshotSha`, zero deferred/new findings, and zero unresolved threads/discussions.
3. For remote-base true, query provider history for the exact attestation before automated merge; missing/mismatched evidence stops `missing-attestation`. False/absent retains confirmation.
4. Revalidate zero deferred/new findings and unresolved threads/discussions. Never resolve or dismiss them.
5. Fetch draft, approvals, protection, conflicts, mergeability, and auto-merge for `reviewedHeadSha`. GitHub evaluates required checks; GitLab uses current-head `detailed_merge_status`, never a pipeline list. Failed/pending non-CI gates, inaccessible state, or stale head stop.
6. Preview target, reviewed head, config/attestation revision, gates, unresolved count, selected action, and expected final fields. Config-authorized calls continue; false/absent waits once.
7. Immediately before every write, re-fetch head, base config, attestation, and gates. Bind fresh `textLanguage` to generated merge content. Changed head/config/review state requires new review, gates, and preview.
8. Mark a draft ready only after gates pass; re-fetch. Readiness waives no gate.
9. GitHub: green required CI uses SHA-guarded `--subject`/`--body` merge; pending required CI registers the same auto-merge. GitLab: immediately merge only `mergeable`; auto-merge only `ci_still_running`, with `--message` and applicable `--squash-message`. Fresh non-empty `textLanguage` governs those fields. `ci_must_pass`, `checking`, other/failure/unknown statuses, or approval/protection/conflict blocks stop.
10. After either write, wait/recheck. Return success only when merged, with SHA and timestamp; registration/queue is pending.
11. After confirmed merge, resolve current target-base `pr-auto-delete-branch`: default true; false preserves remote head. When enabled, revalidate merged target and delete only normalized `headRepository`/`headBranch`. Missing is `already-deleted`; permission/provider failure reports branch-cleanup failure without changing merge success.

## Stop Conditions

| State | Action |
|---|---|
| Failed check, missing approval, protection block, conflict, non-mergeable, stale/inaccessible state | Stop and report gate |
| GitLab `mergeable` | Submit immediate SHA-guarded merge |
| GitLab `ci_still_running` | Register auto-merge, wait/recheck |
| GitHub pending required CI only | Register auto-merge, wait/recheck |
| Changed head after preview | Re-run review/gates and preview |
| Merged | Return actual merge fields |
