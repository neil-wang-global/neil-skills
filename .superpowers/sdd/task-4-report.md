# Task 4 Report: Guarded `/pr-merge`

## Scope

Implemented only Task 4 in the assigned worktree:

- Created `skills/pr-merge/SKILL.md`.
- Created RED/GREEN/REFACTOR evidence in `tests/skills/pr-merge/`.
- Added merge-stage contract rules and GitHub/GitLab provider guidance.
- Did not modify Task 5+ files and did not run `npm test`.

## Provider Research

Validated installed CLI surfaces before provider guidance:

- `gh 2.98.0`: `gh pr ready`, `gh pr checks --required`, `gh pr merge --match-head-commit`, `--auto`, host-qualified `--repo`, and `gh api --hostname`.
- `glab 1.115.0`: `glab mr update --ready`, `glab mr merge --sha`, `--auto-merge`, `--auto-merge=false`, full-URL `--repo`, and `glab api --hostname`.
- GitHub OpenAPI confirmed merge request fields including `sha` and merge method.
- GitLab current REST documentation confirmed `PUT /projects/:id/merge_requests/:merge_request_iid/merge`, `sha`, and `auto_merge`; `merge_when_pipeline_succeeds` is deprecated.

All provider reads route self-hosted calls explicitly. Both merge-capable paths bind the reviewed head SHA. Final success requires provider `MERGED`/`merged` state plus merged SHA and timestamp; queue or auto-merge registration is pending only.

## RED-GREEN-REFACTOR Evidence

Fresh no-skill agents exposed absent one-preview confirmation, an insufficient trusted-envelope contract, an impermissive deferred-finding assumption, missing host routing, and invented/obsolete GitLab syntax. These are recorded in `tests/skills/pr-merge/baseline.md`.

Fresh guided simulations passed scenarios A-I: public confirmation, strict trusted self-reviewed predicates, draft readiness gates, immediate merge, pending auto-merge wait/recheck, all stop conditions, review-completion blocks, spoof resistance, and provider execution. The stale-preview regression passed.

A guided refactor audit found that a bare current-head `snapshotSha` could masquerade as final-review evidence. The final guidance now requires a validated final `/pr-review` result bound to the normalized target; a fresh provenance regression passed and stops before preview/confirmation/writes for bare SHA or user prose.

## Verification

- `wc -w skills/pr-merge/SKILL.md`: 464 words.
- `git diff --check`: exit 0.
- Fresh-agent simulation evidence: all A-I plus provenance and stale-head regressions pass.

## Concern

Neither provider ready operation offers a SHA precondition. The skill/contract therefore require a complete immediate re-fetch before and after readiness; every operation that can merge remains SHA-guarded.

## Follow-up: GitLab Authoritative Merge Gate

A review found that the GitLab pipeline list was being used to infer a required status. GitLab REST identifies the current MR `detailed_merge_status` as the authoritative merge-status field, so this focused correction removes the pipeline-list gate.

- Immediate GitLab merge is permitted only for current-head `detailed_merge_status: mergeable`.
- GitLab auto-merge is permitted only for current-head `detailed_merge_status: ci_still_running`.
- `ci_must_pass`, `checking`, failures, unknown statuses, conflicts, protection blocks, approval blocks, and inaccessible data stop before a write.
- Pipeline-list state neither establishes nor overrides a required status.

Validated with GitLab REST merge-status documentation and installed `glab 1.115.0` help. A fresh read-only regression passed the complete status matrix, SHA binding, preview/confirmation, review-completion gates, and actual-merged-state confirmation. `git diff --check` also passed; the focused skill is 544 words.

## Follow-up: Word-Cap Correction

Compressed only `skills/pr-merge/SKILL.md` from 548 to 430 words, below the 500-word cap, without changing the shared or provider references or Task 5+ files. Fresh read-only simulated regression passed: public preview/confirmation; strict owned trusted-envelope/config authorization; reviewed-head and zero deferred/new/unresolved gates; GitLab `mergeable` immediate merge, `ci_still_running` auto-merge, and every other status block; stale-preview re-evaluation; GitHub/GitLab actual-merged-state wait/recheck; and no review/fix/close/cleanup actions. `git diff --check` exited 0.

## Configuration-Authorization Revision

**RED:** the old provenance branch failed to permit a direct `self-reviewed:true` merge and did not state the false/absent contrast.

**GREEN:** a matching target-repository boolean `self-reviewed:true` authorizes the post-preview merge path for direct and orchestrated calls; false/absent calls wait once for confirmation. The reviewed-head, final-review, protection, approval, CI, conflict, stale-state, SHA-guard, and actual-merged-state gates remain unchanged. Envelope data is handoff metadata only.
