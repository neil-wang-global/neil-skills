# pr-merge baseline

Fresh agents received no `pr-merge` guidance. Simulations made no writes.

## Scenario results

| Scenario | Result | Observed gap |
|---|---|---|
| A | FAIL | Asked for target identity but supplied no required one-preview/one-confirmation merge contract. |
| B | FAIL | Did not define the matching target-repository boolean `self-reviewed:true` predicate that authorizes a direct or orchestrated post-preview merge. |
| C | FAIL | Said the draft MR should be marked ready, but did not require every Task 4 gate before the ready write. |
| D | PASS | Re-read state before merge and waited for a confirmed merged state. |
| E | PASS | Distinguished auto-merge registration from completed merge. |
| F | PASS | Stopped for stale heads, approvals, protection, or conflicts. |
| G | FAIL | Allowed a deferred finding when "formally accepted"; Task 4 requires zero deferred findings, without exception. |
| H | PASS | Kept a direct `self-reviewed:false` call confirmation-gated despite a request to skip it. |
| I | FAIL | Provider commands made self-hosted routing and current syntax optional or wrong. |

## Exact baseline assumptions

The public-flow agent stopped for missing identity, but omitted the required preview: "I would ask for the PR URL/number". Its green path said only: "after one final state check tied to reviewed SHA, I would invoke the chosen merge command".

The trust-gate agent said: "Deferred finding: confirm it is formally accepted, non-blocking, tracked". That contradicts the required zero-deferred gate.

The provider agent assumed: "authenticated `gh` targets the intended GitHub Enterprise host" and emitted `gh pr ready "$PR" --repo "$OWNER/$REPO"`, without the parsed host. For GitLab readiness it incorrectly proposed changing a title: "GitLab uses a title prefix, so remove Draft:/WIP: from title", instead of installed `glab mr update <iid> --ready`. For pending GitLab it used deprecated `merge_when_pipeline_succeeds=true`, while current GitLab REST documents `auto_merge=true` and `glab mr merge --auto-merge`. A pressure agent also invented `glab mr merge <MR> --when-pipeline-succeeds --yes`; installed `glab mr merge --help` exposes no such flag.

## REFACTOR regression: review provenance

A fresh guided reviewer found that a standalone caller could present the current head as an alleged `snapshotSha`: "someone can present the current HEAD SHA as an alleged final-review snapshot". The first skill/contract required a snapshot but did not require a validated final `/pr-review` result bound to the normalized target. This failed the new review-provenance scenario.

## RED regression: GitLab authoritative merge gate

The prior guidance said to require "every required pipeline status" and permitted immediate merge for generic "green required CI" or auto-merge for generic "pending required CI". The only listed GitLab read capable of producing those labels was the pipeline list. This fails the regression: a pipeline list neither exposes GitLab's required merge gate nor authorizes merging. It did not distinguish `detailed_merge_status: mergeable` from `ci_still_running`, and would allow a list-derived decision despite `ci_must_pass`, `checking`, an approval/protection block, a conflict, or an unknown status.

## RED conclusion

The skill must make the merge contract structural: fixed revalidation order, complete preview, one confirmation when config is false/absent, config-authorized continuation when it is true, zero deferred/new/unresolved review state, host-routed provider operations, SHA-guarded writes, and final merged-state confirmation. No registration response is merge success.
