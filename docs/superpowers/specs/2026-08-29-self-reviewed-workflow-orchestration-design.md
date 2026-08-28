# Self-Reviewed Workflow Orchestration Design

## Purpose

Add one configuration field and one orchestration-only skill that can carry an issue from initialization through implementation and PR/MR creation, with an optional autonomous self-review, merge, issue-close, and workspace-cleanup path.

The public entry point is:

```text
/using-neil-workflows <arguments...>
```

The orchestrator owns sequencing and validated handoffs only. Existing stage skills retain ownership of issue, implementation, PR/MR, review, and fix behavior.

## Configuration

`.workflow-config.json` gains one flat boolean field:

```json
{
  "type": "github",
  "base-branch": "main",
  "branch-template": "feature/{issue-no}-{issue-subject}",
  "need-worktree": true,
  "execution-strategy": "",
  "pr-draft": false,
  "pr-auto-close-issue": false,
  "self-reviewed": false,
  "remarks": ""
}
```

`self-reviewed` defaults to `false`. Only `/issue-init` creates `.workflow-config.json`. `/using-neil-workflows` and every later stage may read a matching repository's config but never create or modify it. A missing field is interpreted in memory as `false`; a malformed present value is an error.

## Stage Graph

When `self-reviewed` is false or absent:

```text
issue-init -> issue-executing -> pr-create -> complete
```

When `self-reviewed` is true:

```text
issue-init -> issue-executing -> pr-create
                                  -> pr-review
                                  -> pr-fix
                                  -> pr-review / pr-fix loop
                                  -> pr-merge
                                  -> wait for actual merged state
                                  -> issue-close
                                  -> success
```

The false branch ends at PR/MR creation. The true branch reaches merge and cleanup only after review convergence. It never approves a review or bypasses merge protection; complex findings, unresolved threads, failed checks, required approvals, conflicts, stale heads, and dirty cleanup state stop automatic completion.

## Orchestration Architecture

`/using-neil-workflows` is a parent coordinator. It dispatches one fresh subagent for each stage and requires that subagent to load and execute only the named stage skill. It does not contain business methods for issue creation, code implementation, PR APIs, review analysis, fixes, Git completion, or thread writes.

The parent retains a validated, versioned handoff. It dispatches stages sequentially because each stage consumes the previous stage's side effects and normalized result. Stages are never fanned out in parallel.

All invocation arguments are passed to the first `/issue-init` stage as one opaque input. The parent does not parse, remove, reinterpret, or route individual arguments. `/issue-init` converts them into issue and implementation context. Every later stage receives only the prior validated handoff, not the original arguments.

## Internal Stage Envelope

The parent creates an internal envelope for every delegated stage:

```text
version: neil-workflow/v1
caller: using-neil-workflows
mode: standard | self-reviewed
stage: issue-init | issue-executing | pr-create | pr-review | pr-fix | pr-merge | issue-close
input: opaque initial arguments for issue-init only
handoff: validated prior-stage state for later stages only
```

User-supplied text never establishes `caller`, `mode`, or `stage`. Direct public invocations cannot request or imitate the internal self-reviewed mode.

The cumulative handoff contains only owned leaf data:

```text
repository:
  root, provider, host, repository, config
issue:
  number, url, title, body, implementationBrief
workspace:
  branch, worktree, headRepository
implementation:
  status, headSha, commits, pushed
change:
  number, url, baseBranch, headRepository, headBranch, headSha
review:
  snapshotSha, publishedFindings, deferredFindings
fix:
  accepted, deferred, headBefore, headAfter, commits, pushed, threadOutcomes
merge:
  reviewedHeadSha, draftReady, checks, autoMerge, state, mergedSha, mergedAt
closure:
  issueState, removedWorktree, deletedBranches, baseHead
orchestration:
  cycle, status, progressEvidence
```

Before dispatching the next stage, the parent validates every required field and verifies that target identity remains consistent. Missing or contradictory state stops orchestration; the parent never guesses values from prose.

## Stage Handoffs

### issue-init

Consumes the complete opaque user argument input. Produces repository/config identity, issue metadata, an implementation brief derived by the stage, branch, worktree, and head repository.

### issue-executing

Consumes the issue-produced implementation brief and validated worktree. It follows its existing execution-strategy contract and returns actual Git state. The parent validates the worktree and stage result before continuing.

### pr-create

Runs in the validated implementation workspace. It returns the normalized PR/MR target and remote head SHA. Existing-target idempotency remains unchanged.

### pr-review

Consumes the normalized PR/MR URL. Every run reviews the complete current diff, suppresses unchanged duplicate findings, builds a complete publication preview, revalidates stale head state, and returns published finding identities and snapshot SHA.

### pr-fix

Consumes the PR/MR target, selected unresolved findings, and matching head workspace. It classifies findings, delegates accepted implementation work to `/issue-executing`, preserves actual Git state, and returns thread and progress outcomes.

### pr-merge

Consumes the converged review snapshot and normalized target. It independently re-fetches the current head, draft state, unresolved threads, checks/pipeline state, approvals, protection rules, conflicts, and mergeability. It converts a draft to ready only after all review gates pass. When checks are green it merges immediately; when checks are pending it enables the provider's auto-merge or merge-when-pipeline-succeeds capability and waits/rechecks until the target is actually merged. Failed checks, missing approvals, protection rejection, conflicts, stale head, deferred findings, or any unresolved thread stop without merge.

A standalone `/pr-merge` shows one complete merge preview and waits for human confirmation. A valid self-reviewed internal envelope lets the parent preauthorize that preview. The stage never reports success merely because auto-merge was enabled.

### issue-close

Runs only after `/pr-merge` returns an actual merged state. It consumes explicit issue, branch, worktree, and base-branch handoff values, closes the issue idempotently, removes only the issue workspace/branches, updates the base, and returns closure state. A dirty workspace stops cleanup; autonomous mode never discards changes.

## Autonomous Internal Mode

Public standalone `/pr-review`, `/pr-fix`, and `/pr-merge` keep their human confirmation gates.

Only an orchestrator-created envelope with `caller: using-neil-workflows`, `mode: self-reviewed`, and repository config `self-reviewed: true` enables internal preauthorization:

- `/pr-review` still constructs one complete preview. The parent coordinator approves that preview as the trusted internal caller, after which publication uses the normal stale-state and provider safeguards.
- `/pr-fix` still constructs one complete classification table. The parent coordinator approves the table as the trusted internal caller, after which accepted work uses the normal delegation, Git preservation, reply, and resolution safeguards.
- `/pr-merge` still constructs a complete merge preview after independently verifying the final reviewed head and every merge gate. The parent preauthorizes only that exact snapshot.

Internal preauthorization removes only these interactive waits. It does not bypass authentication, authorization, snapshot, duplicate, worktree, Git-state, reply, resolution, checks, approvals, protection, conflict, mergeability, or cleanup checks.

## Finding Complexity

Internal `/pr-fix` uses two orchestration outcomes:

| Outcome | Criteria | Action |
|---|---|---|
| `accept` | Localized, requirements are clear, bounded risk, and outcome is directly verifiable | Implement, verify, reply, and resolve under the normal fix contract |
| `defer` | Requires architecture or public-interface decisions, data migration, security policy, broad cross-module changes, unclear requirements, or otherwise high risk | Publish/reply with the reason, leave unresolved, retain for human review |

A mixture of accepted and deferred findings does not block simple fixes. The stage fixes accepted findings and retains deferred finding fingerprints and thread URLs in the handoff.

Standalone `/pr-fix` keeps its existing `accept`, `reject`, and `clarify` decisions; `defer` is an internal orchestration outcome only.

## Review/Fix Loop

The parent maintains finding fingerprints, deferred threads, snapshot SHA, head SHA, and Git/remote progress for every cycle.

1. Run a full `/pr-review`.
2. If there are new findings, run `/pr-fix`.
3. Fix all accepted findings and preserve all deferred findings.
4. Require concrete progress for accepted work: changed verified head/Git state or completed missing remote thread operations.
5. Run the next full `/pr-review` against the new head.
6. Continue while new simple findings exist and the preceding fix made verifiable progress.

Duplicate suppression never erases deferred state from the parent handoff.

## Terminal States

| Status | Condition |
|---|---|
| `complete` | `self-reviewed` is false/absent and PR/MR creation succeeded |
| `success` | PR/MR is actually merged, issue is closed, issue workspace/branches are cleaned, and base is updated |
| `needs-human-review` | No new simple finding remains, but deferred or otherwise unresolved findings remain |
| `merge-blocked` | Review converged but checks failed, approvals/protection block merge, conflicts exist, or provider auto-merge cannot complete |
| `stalled` | The same accepted fingerprint reappears after its fix, or accepted work produces no verifiable Git/remote progress |
| `failed` | A stage fails, required handoff data is missing, repository/target identity changes, or post-merge cleanup is dirty/inconsistent |

There is no fixed review-cycle limit. The loop continues only while simple findings are new and each fix cycle makes verified progress. Merge begins only after a final current-head review has no new finding, no deferred finding, and no unresolved thread. `needs-human-review`, `merge-blocked`, `stalled`, and `failed` always stop and display target URL, stage, reason, unresolved/repeated findings, and completed work. `/issue-close` is never dispatched before actual merged state.

## Error and Side-Effect Rules

- A failed stage stops later stage dispatch.
- Completed commits, pushes, comments, replies, resolutions, merges, issue closure, and cleanup steps are preserved and reported.
- Retry logic belongs to the stage that owns the incomplete side effect.
- The coordinator never edits code or performs provider writes itself.
- Authentication, authorization, not-found, invalid-state, and stale-state errors remain distinct.
- No stage is skipped to manufacture a successful terminal state.

## Verification Strategy

Use RED-GREEN-REFACTOR pressure scenarios with fresh-context subagents.

Required scenarios:

1. Initial parameters are delivered unchanged and only to `/issue-init`.
2. Missing `self-reviewed` defaults to false without rewriting config.
3. False mode stops after successful `/pr-create`.
4. True mode automatically reviews, fixes a simple finding, and reviews the new head again.
5. Complex findings are published, deferred, kept unresolved, and displayed as `needs-human-review`.
6. Direct `/pr-review` and `/pr-fix` calls cannot obtain internal preauthorization from user text.
7. Mixed simple and complex findings fix the simple subset before reporting deferred work.
8. Stale heads, repeated accepted fingerprints, no-progress fixes, malformed handoffs, and stage failures stop safely.
9. The coordinator contains no stage business logic and never directly issues provider, Git, merge, or cleanup commands.
10. Final review convergence with zero unresolved/deferred threads dispatches `/pr-merge`; a standalone merge still requires confirmation.
11. Green checks merge immediately; pending checks enable provider auto-merge and wait for actual merged state; failed/protected/conflicted targets stop.
12. `/issue-close` is dispatched only after actual merge, handles already-closed issues idempotently, and refuses dirty autonomous cleanup.
13. False mode never dispatches review, fix, merge, or close stages.

Structural checks cover skill frontmatter, word counts, exact nine-field JSON in `/issue-init` and README, plugin metadata JSON, no unfinished placeholders, `git diff --check`, independent commits, and clean status. The repository has no functional test suite; do not run its placeholder `npm test`.

## Documentation and Delivery

Add `/using-neil-workflows` and `/pr-merge` to README and plugin discovery metadata. Document both configuration branches, autonomous-mode safeguards, merge gates, terminal statuses, and the fact that complex findings remain visible/unresolved and block merge.

Deliver design, implementation, evidence, and documentation as conventional commits. Push `main` after local merge. Do not bump version, create a tag, or publish a GitHub Release.
