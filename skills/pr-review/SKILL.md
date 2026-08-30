---
name: pr-review
description: Use when reviewing a GitHub pull request or GitLab merge request by URL, number, or current branch, including config-authorized direct or orchestrated publication
---

# PR Review

## Contract

Review the full target, preview all proposed remote comments, and require one explicit confirmation for public calls. Never modify `.workflow-config.json`.

**REQUIRED REFERENCES:** Read `references/pr-workflow-contract.md` and `references/github-pr-api.md` or `references/gitlab-mr-api.md` for the selected provider before remote operations.

## Target

| Invocation | Resolution |
|---|---|
| `/pr-review <URL>` | Provider, repository, number from URL |
| `/pr-review <number>` | Number in current repository |
| `/pr-review` | Target for current branch |

A URL works without a clone.

## Workflow

1. Resolve an open target, authenticate, capture head SHA, then resolve target-base config remotely. Retain resolver identity and `textLanguage`; never read head, fork, local, or envelope config.
2. Fetch diff/metadata, inline discussions, and PR/MR bodies. Review the full diff; suppress unchanged duplicates by fingerprint plus semantics.
3. Map findings to reliable old/new lines. Mark others non-inline; never guess.
4. Preview in non-empty `textLanguage`. Only remote-base literal `self-reviewed:true` authorizes publication without a human wait; false/absent waits for confirmation. Malformed/unreadable config stops; an envelope validates sequencing only.
5. Apply user edits for confirmation-gated calls. Config-authorized non-inline feedback may use required provider-level feedback; no publishable URL is `publication-failed`.
6. Immediately re-fetch head/diff and remote base config before writes. A changed head/config revision withholds, remaps/revalidates, and re-previews; fresh non-empty `textLanguage` governs new finding titles/explanations, inline/non-inline comments, and report prose.
7. Publish the authorized set. After a full current-head review has zero new/deferred/unresolved findings, read provider history and create one idempotent `neil-self-reviewed/v1` attestation for the exact target/head/base-config revision. Keep marker/payload exact. Report its provider ID/URL with snapshot, successes, failures, and skips.

## Internal Result Handoff

An orchestrated call returns only owned leaves: `version`, `stage:"pr-review"`, normalized `target`, `snapshotSha`, `headSha`, `findings`, `convergence`, `publication`, and `attestation`. `attestation` is null unless a converged config-authorized review created/found exact provider ID/URL and target/head/base-config tuple. Target repeats provider, host, repository, number, base/head branches, and head SHA. Each finding has hidden `fingerprint`, `threadUrl`, `threadTarget`, `complexity` (`simple`/`complex`), and state (`unresolved`, `deferred`, `resolved`, `publication-failed`). A simple unavailable publication may use null. Every complex/deferred candidate requires a provider-derived URL and matching `threadTarget`; missing, malformed, fabricated, unrelated, or mismatched values return `publication-failed` and stop. Convergence records exact status/counts; publication records status and identities. Suppression retains unresolved/deferred findings. Stale head, incomplete publication, unresolved, or deferred state is explicit.

## Finding Shape

`[severity] title; validity; consequence; correction; path/side/line; hidden fingerprint`

## Provider Writes

| Provider | Behavior |
|---|---|
| GitHub | One REST `COMMENT` review with inline comments |
| GitLab | One REST diff discussion per finding; retain successes |

On GitLab partial failure retry only failed findings. On GitHub invalid location correct the rejected batch; re-preview if content/location changed. No findings is local only: no approval or no-op comment.

## Boundary

Never edit code, invoke `/pr-fix`, approve, request changes, merge, close issues, or delete branches. When findings publish, report `/pr-fix` as available without invoking it.
