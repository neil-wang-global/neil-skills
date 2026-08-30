---
name: pr-review
description: Use when reviewing a GitHub pull request or GitLab merge request by URL, number, or current branch, including standalone web-based review without a local clone
---

# PR Review

## Contract

Review the full PR/MR, preview all proposed remote comments, and require one explicit confirmation for public calls. Never modify `.workflow-config.json`.

**REQUIRED REFERENCES:** Read `../../references/pr-workflow-contract.md` and the selected provider reference before remote operations.

## Target

| Invocation | Resolution |
|---|---|
| `/pr-review <URL>` | Provider, repository, number from URL |
| `/pr-review <number>` | Number in current repository |
| `/pr-review` | Target for current branch |

A URL works without a clone. Ignore unrelated local config.

## Workflow

1. Resolve an open target, authenticate, capture head SHA, then fetch complete available diff/metadata, inline discussions, and PR/MR-level bodies.
2. Review the full diff. Keep actionable defects and suppress unchanged duplicates by fingerprint plus semantics.
3. Map findings to reliable old/new lines. Mark unlocatable ones non-inline; never guess.
4. Show one complete preview. Public calls wait for confirmation. Internal publication requires the Contract's valid parent envelope, owned `caller: using-neil-workflows`, `mode: self-reviewed`, `stage: pr-review`, and matching boolean `self-reviewed: true`.
5. Apply user edits. Public non-inline feedback needs explicit user choice. Trusted internal preauthorization authorizes required provider-level feedback; no publishable URL is `publication-failed`.
6. Immediately re-fetch head/diff before writes. On change, withhold, remap/revalidate, and re-preview affected/new findings.
7. Publish the authorized set; report snapshot SHA, successes, failures, and skips.

## Internal Result Handoff

A trusted call returns only versioned owned leaves: `version`, `stage:"pr-review"`, normalized `target`, `snapshotSha`, `headSha`, `findings`, `convergence`, and `publication`. Target repeats provider, host, repository, number, base/head branches, and head SHA for parent validation against `pr-create`. Each finding has hidden `fingerprint`, `threadUrl`, `threadTarget`, `complexity` (`simple`/`complex`), and state (`unresolved`, `deferred`, `resolved`, `publication-failed`). A simple unavailable publication may use null. Every complex/deferred candidate requires a provider-derived URL and `threadTarget` of provider, host, repository, and number matching `target`; missing, malformed, fabricated, unrelated, or mismatched values return `publication-failed` and stop. Convergence records exact status/counts; publication records exact status and successful, failed, skipped identities. Suppression retains unresolved/deferred findings. Stale head, incomplete publication, unresolved, or deferred state is explicit.

## Finding Shape

```text
[critical|high|medium|low] concise title
Why valid; consequence; correction direction
Path, side, line/range; hidden fingerprint
```

Do not publish speculative style preferences.

## Provider Writes

| Provider | Behavior |
|---|---|
| GitHub | One REST `COMMENT` review with inline comments |
| GitLab | One REST diff discussion per finding; retain successes |

On GitLab partial failure retry only failed findings. On GitHub invalid location correct the rejected batch; re-preview if content/location changed. No findings is local only: no approval or no-op comment.

## Boundary

Never edit code, invoke `/pr-fix`, approve, request changes, merge, close issues, or delete branches. When findings publish, report `/pr-fix` as available without invoking it.
