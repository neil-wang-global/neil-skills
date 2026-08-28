# PR Workflow Contract

Shared contract for `pr-create`, `pr-review`, and `pr-fix`. Public skills own decisions; provider references own command and API syntax.

## Optional Configuration

The PR skills may read `.workflow-config.json` only when it belongs to the target repository. They never create or modify it.

| Field | Missing default |
|---|---|
| `base-branch` | `main` |
| `branch-template` | `feature/{issue-no}-{issue-subject}` |
| `need-worktree` | `true` |
| `pr-draft` | `false` |
| `pr-auto-close-issue` | `false` |

A malformed present config is an error for the fields the current skill needs. Do not silently rewrite it.

## Normalized Target

Use these field names across provider branches:

```text
provider, host, repository, number, url, baseBranch,
headRepository, headBranch, headSha
```

For `pr-create`, resolve provider and repository from the current Git remote, `headBranch` from the current branch, and `baseBranch` from config/defaults. Populate number, URL, and head SHA from an existing or newly created PR/MR response.

## Issue Resolution

Apply `branch-template` to the complete current branch and extract `{issue-no}`. If extraction fails, use an issue number explicitly supplied by the user. Otherwise ask; never guess from unrelated digits or branch text.

Verify the issue exists before creating a PR/MR.

## Identity and Configuration

An explicit future PR/MR URL is authoritative for provider, host, repository, and number. Ignore configuration from an unrelated local repository. Local configuration applies only when its Git remote matches the target repository.

## Error Semantics

Distinguish:

- Authentication failure: missing, invalid, or expired credentials.
- Authorization failure: authenticated identity lacks the required permission.
- Not found: resource is absent, or a private resource is hidden; report both possibilities.
- Invalid state: wrong branch, closed target, dirty state, or missing issue relationship.
- Stale state: remote head/diff changed; re-fetch before a write.

Never expose tokens or credential contents.

## Idempotency

Read remote state before every create. If the current head branch already has an open PR/MR, return it unchanged. Do not duplicate it, edit it merely to match generated text, or invoke the next workflow stage.

## Review Selectors

Resolve review targets in this order: explicit PR/MR URL, explicit number in the current repository, then target associated with the current branch. A full URL supplies provider, host, repository, and number and requires neither a clone nor local config.

## Review Snapshot

A review snapshot owns `headSha`, changed-file metadata, complete available diff, and existing review threads. Review the full diff every run.

Before any remote write, fetch the current head again. If it changed, withhold publication, re-fetch the diff, remap/revalidate findings, and re-preview changed or new findings.

## Finding Identity

Each finding has severity, concise title, validity reason, consequence, correction direction, path, side, line/range, and a versioned hidden fingerprint. Build the fingerprint from normalized category, path, relevant code context, and remediation identity; do not rely on line number alone.

Compare fingerprints and semantics with existing threads. Suppress previously reported unchanged findings. Preview only new actionable findings while noting suppressed prior items locally.

## Review Publication

Always show one complete preview and wait for one explicit confirmation before a remote write, even when the request says publish. User edits to the preview become the authoritative set.

No findings produces a local report only: no approval and no no-op comment. A finding without a reliable diff location is marked non-inline; convert it to PR-level feedback only after explicit user choice.

GitHub may submit one atomic review. GitLab discussions are individual writes: record each success and retry only failed items. Include target, snapshot SHA, successes, failures, and skipped items in the report.

## Fix Selectors and Clone

A review-comment/discussion URL selects exactly that thread. A PR/MR URL or number selects its unresolved threads. With no argument, use the target for the current branch.

Code changes require a matching writable local clone; never clone automatically. Explicit URL identity remains authoritative. If local remote, provider, host, or repository does not match, stop. Use an isolated worktree by default (`need-worktree` defaults true), checked out at the PR/MR head branch. Never change the caller's base checkout.

## Classification and Confirmation

Verify each thread against current code and classify `accept`, `reject`, or `clarify` with a concise reason and intended reply. Show one complete confirmation table. After confirmation, accepted items proceed; rejected and clarification items receive replies but remain unresolved.

## Delegation and Git State

Before delegation, capture head, clean/dirty state, local-only commits, and upstream relation. Send accepted feedback to `/issue-executing` as an implementation-neutral brief containing context, locations, and observable outcomes only. It must not prescribe code methods, architecture, techniques, or test commands.

After delegation, inspect actual Git state. Preserve every commit or push already produced by the configured execution strategy: never squash, amend, recommit, force-push, or push redundantly. If accepted changes remain uncommitted, create one completion commit containing only those changes. Push only commits not already present upstream.

## Thread Completion

For each accepted thread, verify the observable outcome, then reply with the result and relevant commit. Resolve only after the reply succeeds. A reply failure leaves the thread unresolved and is reported for retry.

For each rejected or clarification thread, post the confirmed rationale/question and leave it unresolved. No accepted changes means no completion commit. Record per-thread reply and resolution outcomes; retry only incomplete remote operations.
