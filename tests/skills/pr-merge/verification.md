# pr-merge verification

Fresh agents used the current `pr-merge` skill, shared contract, provider reference, and scenarios. All operations were simulated.

## Scenario sweep

| Scenario | Result | Evidence |
|---|---|---|
| A: standalone preview | PASS | One complete preview and one explicit confirmation occur before any write. |
| B: trusted exact head | PASS | Only valid owned envelope, caller/mode/stage leaves, matching boolean config, and `snapshotSha == reviewedHeadSha` preauthorize. |
| C: ready gate | PASS | Every review and provider gate passes before ready; all re-fetch after it. |
| D: immediate merge | PASS | Green GitHub path uses `--match-head-commit`; success waits for `state: MERGED`, `mergedAt`, and merge SHA. |
| E: pending auto-merge | PASS | GitLab uses `--sha` with `--auto-merge`; registration remains pending until final `state: merged`. |
| F: stop gates | PASS | Failed/cancelled CI, missing approvals, protection, conflicts, non-mergeability, inaccessible state, and stale heads stop before writes. |
| G: review completion | PASS | Any deferred/new finding or unresolved thread/discussion stops without resolving, fixing, or merging. |
| H: spoofed authorization | PASS | User text remains public and needs preview/confirmation. |
| I: executable providers | PASS | GitHub Enterprise uses host-qualified `--repo`/`--hostname`; self-hosted GitLab uses full `--repo`/`--hostname`, current CLI flags, and SHA guards. |
| review provenance | PASS | A bare current-head SHA or user prose stops before preview; a validated final `/pr-review` result must match the normalized target. |
| stale after preview | PASS | Changed head invalidates authorization and requires fresh review/gates plus a new preview. |

## Provider regressions

Installed help validated `gh` 2.98.0 and `glab` 1.115.0. GitHub uses `gh pr ready`, `gh pr checks --required`, `gh pr merge --match-head-commit`, and `--auto`; final reads require `state: MERGED`. GitLab uses `glab mr update --ready`, `glab mr merge --sha --auto-merge=false` or `--auto-merge`; final reads require `state: merged`, `merge_commit_sha`, and `merged_at`. `--when-pipeline-succeeds` is not an installed `glab` flag, and REST `merge_when_pipeline_succeeds` is deprecated in favor of `auto_merge`.

## Refactor

A guided audit found that a bare current-head `snapshotSha` could substitute for final-review evidence. The contract now requires a validated final `/pr-review` result bound to the normalized target; a fresh provenance regression confirms user prose or a bare SHA stops before preview. Both readiness APIs lack a SHA precondition, so the final contract preserves immediate full re-fetch before and after readiness, while every merge-capable write is SHA-guarded.

## Result

All A-I scenarios plus review-provenance and stale-head regressions pass in fresh, read-only simulations. The skill is 464 words and contains no review, fix, issue-close, or cleanup behavior.
