---
name: pr-review
description: Use when reviewing a GitHub pull request or GitLab merge request by URL, number, or current branch, including standalone web-based review without a local clone
---

# PR Review

## Contract

Review the full PR/MR, preview every proposed remote comment, and require one explicit confirmation for public calls. Never create or modify `.workflow-config.json`.

**REQUIRED REFERENCES:** Read `../../references/pr-workflow-contract.md` and the selected provider reference before remote operations.

## Target

| Invocation | Resolution |
|---|---|
| `/pr-review <URL>` | Provider, repository, and number from URL |
| `/pr-review <number>` | Number in current repository |
| `/pr-review` | Target for current branch |

A full URL works from any directory without a clone. Ignore unrelated local config.

## Workflow

1. Resolve target, authenticate, require an open PR/MR, and capture head SHA.
2. Fetch complete available changed-file metadata/diff, inline threads/discussions, and PR/MR-level review/comment bodies.
3. Review the full diff every run, not only commits since a prior review.
4. Keep actionable defects. Suppress previously reported unchanged findings by fingerprint plus semantic comparison.
5. Map each finding to a reliable old/new diff line. Mark unlocatable findings non-inline; never guess.
6. Show one complete preview. Public calls wait for explicit confirmation; internal preauthorization is allowed only under the Contract's valid envelope, trusted `caller: using-neil-workflows`, `mode: self-reviewed`, `stage: pr-review`, and matching `self-reviewed: true` predicates.
7. Apply authoritative user edits. Convert non-inline findings to PR-level feedback only when explicitly selected.
8. Immediately before publication, re-fetch head and diff. If changed, withhold writes, remap/revalidate, and re-preview affected or new findings.
9. Publish the authorized set and report snapshot SHA, successes, failures, and skipped items.

## Internal Result Handoff

For a trusted internal call, return a versioned owned leaf-only result for the parent, bound to the reviewed target and current snapshot: `version`, `stage:"pr-review"`, normalized `target`, `snapshotSha`, `headSha`, `findings`, `convergence`, and `publication`. The target repeats provider, host, repository, number, base/head branches, and head SHA from the authoritative review target so the parent can validate it against `pr-create`. Each newly actionable finding records its hidden `fingerprint`, `threadUrl` when published or an explicit null when unavailable, `complexity` (`simple` or `complex`), and state (`unresolved`, `deferred`, `resolved`, or `publication-failed`). `convergence` records exact `status` plus `newCount`, `unresolvedCount`, and `deferredCount`; `publication` records exact status plus successes, failures, and skipped identities. Duplicate suppression cannot omit unresolved/deferred prior findings from this result. A stale head, incomplete publication, or unresolved/deferred state is explicit, never inferred from prose.

## Finding Shape

```text
[critical|high|medium|low] concise title
Why the issue is valid
Observable consequence or risk
Suggested correction direction
Path, old/new side, and line/range
Hidden versioned fingerprint
```

Do not publish speculative style preferences as defects.

## Provider Writes

| Provider | Behavior |
|---|---|
| GitHub | One REST review containing inline comments; event `COMMENT` |
| GitLab | One REST diff discussion per finding; retain each success |

On GitLab partial failure, retry only failed findings. On GitHub invalid location, correct the rejected batch; re-preview when content or location meaning changed.

## Empty or Unlocatable Results

No findings produces a local report only: no approval, request changes, or no-op comment.

For binary, truncated, outdated, or unanchorable content, preview why inline publication is unavailable. PR-level feedback requires explicit user choice.

## Boundary

Never edit code, invoke `/pr-fix`, approve, request changes, merge, close issues, or delete branches. When published findings exist, report `/pr-fix` as an available command without invoking it.

## Common Mistakes

| Wrong | Required |
|---|---|
| Clone for URL review | Remote provider APIs |
| Publish immediately | Public calls preview and wait; internal uses Contract predicates |
| Incremental-only review | Full diff every run |
| Repeat old finding | Fingerprint and semantic suppression |
| Auto-approve empty result | Local report only |
| Guess/promote a line | Mark non-inline and ask |
