# Self-Reviewed Workflow Orchestration Design

## Purpose

Add one configuration field and one orchestration-only skill that can carry an issue from initialization through implementation and PR/MR creation, with an optional autonomous self-review loop.

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
                                  -> success | needs-human-review | stalled | failed
```

The graph ends at PR/MR creation or review convergence. It never approves, merges, closes the issue, deletes branches, or cleans worktrees.

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
stage: issue-init | issue-executing | pr-create | pr-review | pr-fix
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

## Autonomous Internal Mode

Public standalone `/pr-review` and `/pr-fix` keep their existing human confirmation gates.

Only an orchestrator-created envelope with `caller: using-neil-workflows`, `mode: self-reviewed`, and repository config `self-reviewed: true` enables internal preauthorization:

- `/pr-review` still constructs one complete preview. The parent coordinator approves that preview as the trusted internal caller, after which publication uses the normal stale-state and provider safeguards.
- `/pr-fix` still constructs one complete classification table. The parent coordinator approves the table as the trusted internal caller, after which accepted work uses the normal delegation, Git preservation, reply, and resolution safeguards.

Internal preauthorization removes only the two interactive waits. It does not bypass authentication, authorization, snapshot, duplicate, worktree, Git-state, reply, or resolution checks.

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
| `success` | Self-review finds no new actionable finding and no deferred unresolved finding remains |
| `needs-human-review` | No new simple finding remains, but deferred unresolved findings remain |
| `stalled` | The same accepted fingerprint reappears after its fix, or accepted work produces no verifiable Git/remote progress |
| `failed` | A stage fails, required handoff data is missing, or repository/target identity becomes inconsistent |

There is no fixed cycle limit. The loop continues only while simple findings are new and each fix cycle makes verified progress. `needs-human-review`, `stalled`, and `failed` always stop and display target URL, stage, reason, deferred/repeated findings, and completed work.

## Error and Side-Effect Rules

- A failed stage stops later stage dispatch.
- Completed commits, pushes, comments, replies, and resolutions are preserved.
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
9. The coordinator never merges, approves, closes issues, cleans branches/worktrees, or implements stage business logic.

Structural checks cover skill frontmatter, word counts, exact nine-field JSON in `/issue-init` and README, plugin metadata JSON, no unfinished placeholders, `git diff --check`, independent commits, and clean status. The repository has no functional test suite; do not run its placeholder `npm test`.

## Documentation and Delivery

Add `/using-neil-workflows` to README and plugin discovery metadata. Document both configuration branches, autonomous-mode safeguards, terminal statuses, and the fact that complex findings remain visible and unresolved.

Deliver design, implementation, evidence, and documentation as conventional commits. Push `main` after local merge. Do not bump version, create a tag, or publish a GitHub Release.
