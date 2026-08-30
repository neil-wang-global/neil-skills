# pr-merge verification

Fresh agents used the current `pr-merge` skill, shared contract, provider reference, and scenarios. All operations were simulated.

## Scenario sweep

| Scenario | Result | Evidence |
|---|---|---|
| A: standalone preview | PASS | One complete preview and one explicit confirmation occur before any write. |
| B: direct `true` exact head | PASS | Matching boolean config authorizes the post-preview path for a direct or orchestrated call only when `snapshotSha == reviewedHeadSha` and every gate passes. |
| C: ready gate | PASS | Every review and provider gate passes before ready; all re-fetch after it. |
| D: immediate merge | PASS | Green GitHub path uses `--match-head-commit`; success waits for `state: MERGED`, `mergedAt`, and merge SHA. |
| E: pending auto-merge | PASS | GitLab uses `--sha` with `--auto-merge` only when the current-head MR reports `detailed_merge_status: ci_still_running`; registration remains pending until final `state: merged`. |
| F: stop gates | PASS | Failed/cancelled CI, missing approvals, protection, conflicts, non-mergeability, inaccessible state, and stale heads stop before writes. |
| G: review completion | PASS | Any deferred/new finding or unresolved thread/discussion stops without resolving, fixing, or merging. |
| H: direct `false` confirmation | PASS | False or absent config remains confirmation-gated; request text and envelope metadata do not change the result. |
| I: executable providers | PASS | GitHub Enterprise uses host-qualified `--repo`/`--hostname`; self-hosted GitLab uses full `--repo`/`--hostname`, current CLI flags, and SHA guards. |
| review provenance | PASS | A bare current-head SHA or user prose stops before preview; a validated final `/pr-review` result must match the normalized target. |
| GitLab authoritative merge gate | PASS | Current-head `detailed_merge_status: mergeable` is the sole immediate-merge state; `ci_still_running` is the sole auto-merge state; `ci_must_pass`, `checking`, all failures/unknowns, and independent approval/protection/conflict blocks stop. Pipeline-list state never supplies or overrides this gate. |
| stale after preview | PASS | Changed head invalidates authorization and requires fresh review/gates plus a new preview. |
| fresh merge language | PASS | Fresh non-empty target-base language governs every GitHub `--subject`/`--body` and GitLab `--message`/applicable `--squash-message` field without changing guards, gates, auto-merge, or attestation behavior. |

## Provider regressions

Installed help validated `gh` 2.98.0 and `glab` 1.115.0. GitHub uses `gh pr ready`, `gh pr checks --required`, `gh pr merge --match-head-commit`, `--auto`, `--subject`, and `--body`; final reads require `state: MERGED`. GitLab uses `glab mr update --ready`, `glab mr merge --sha --auto-merge=false` or `--auto-merge`, `--message`, and applicable `--squash-message`; final reads require `state: merged`, `merge_commit_sha`, and `merged_at`. Non-empty freshly resolved target-base language governs all generated merge commit content, not generic provider comments/notes. GitLab REST `GET /projects/:id/merge_requests/:merge_request_iid` documents `detailed_merge_status` as the authoritative merge-status field: only `mergeable` permits immediate merge and only `ci_still_running` permits auto-merge at the current SHA; `ci_must_pass`, `checking`, all other/unknown statuses, and independent blocks stop. The pipeline list does not establish requirements. `--when-pipeline-succeeds` is not an installed `glab` flag, and REST `merge_when_pipeline_succeeds` is deprecated in favor of `auto_merge`.

## Refactor

A guided audit found that a bare current-head `snapshotSha` could substitute for final-review evidence. The contract now requires a validated final `/pr-review` result bound to the normalized target; a fresh provenance regression confirms user prose or a bare SHA stops before preview. Both readiness APIs lack a SHA precondition, so the final contract preserves immediate full re-fetch before and after readiness, while every merge-capable write is SHA-guarded. A focused GitLab regression replaced pipeline-list inference with the current-head `detailed_merge_status` gate: `mergeable` merges immediately, `ci_still_running` alone registers auto-merge, and every other status stops.

## Result

All A-I scenarios plus review-provenance, GitLab-authoritative-gate, and stale-head regressions pass in fresh, read-only simulations. The skill contains no review, fix, or issue-close behavior; it owns only configured post-merge remote head cleanup.

## Task 7 Cross-Skill Pressure Evidence

Fresh end-to-end simulations confirm that a trusted simple-finding path reaches this skill only after a changed-head clean re-review, then reaches `issue-close` only after provider evidence of actual merge (`state`, SHA, timestamp). A merge blocked by missing approval or failed required check terminates `merge-blocked`; it neither merges nor dispatches `issue-close`. Auto-merge registration or queueing remains owned by this skill as pending work and is never reported as the parent terminal result.

## Remote Attestation Revision

Fresh read-only simulations J-N passed after the reviewer-driven refactor. A remote-base true direct merge with no exact provider record stops `missing-attestation` before preview confirmation, readiness, or merge write. The automatic path accepts only a two-line `neil-self-reviewed/v1` body with exactly the seven required JSON keys, exact target/head/base-config tuple, and provider metadata author matching the authenticated merge actor. Head, provider/host/repository, base ref, or config blob mismatch reports its field and requires a fresh converged review to write replacement evidence. GitHub uses host-routed Contents/reviews APIs and `event:"COMMENT"`; GitLab uses host-routed file/MR-notes APIs and a general non-diff note. No High/Medium security gap was found in the final read-only contract simulation; it does not substitute for a live provider integration run.
