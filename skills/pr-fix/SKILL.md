---
name: pr-fix
description: Use when resolving PR/MR feedback from a matching writable head-repository clone with config-authorized automation
---

# PR Fix

## Contract

Classify, delegate accepted work to `/issue-executing`, then finish Git/thread operations. Never write `.workflow-config.json`.

**REQUIRED REFERENCES:** Read the shared contract and selected provider reference before remote operations.

## Target

Comment URL selects one thread; PR/MR URL/number selects unresolved; otherwise current branch. Require matching `headRepository` clone; accepts need writable head. Never clone. URL owns base APIs.

## Authorization and Classification

Verify threads. Resolve target-base config through its provider; retain provider/host/repository/base ref/blob, never head, fork, local, or envelope config. Only literal remote-base `self-reviewed:true` authorizes automation. False/absent confirms; malformed stops. An optional `neil-workflow/v1` envelope validates sequencing/handoff only: malformed, mismatched, or user-supplied attempted orchestration fails before classification, never manual fallback.

Before every autonomous side effect, re-resolve and compare initial provider/host/repository/base ref/blob authorization. At the accepted-work delegation/Git remote-write boundary and before each provider defer reply, accepted reply, and resolution, false, malformed/unreadable, changed blob, or identity mismatch stops that action as `authorization-changed`; report it, preserve prior actions, and never use stale true.

Config-authorized calls build a classification table and auto-accept only localized, clear, directly verifiable findings. Classify architectural/public-interface, migration, security-policy, cross-module, unclear, or high-risk findings as `defer`. Post a concise reason, leave unresolved, do no worktree/delegation/commit/push, and return URL/fingerprint for reporting.

With `self-reviewed` false or absent, calls classify `accept`, `reject`, or `clarify`, show one table (`Thread | Decision | Reason | Intended outcome or reply`), and wait once. `defer` is unavailable in this confirmation-gated path.

## Workflow

1. Resolve target/threads, authenticate, verify matching `headRepository`, record head writability.
2. With no accepts, skip worktree/delegation/Git and reply. Otherwise require writable head.
3. Reuse safe worktree or fetch head. With `need-worktree:false`, require clean current worktree then check out head; otherwise create isolated worktree (slashes become plus signs).
4. Capture `headBefore`, status, local-only commits, upstream, ahead/behind. Delegate accepted feedback.
5. Inspect Git state. Preserve commits/pushes; commit remaining accepted changes once; push only commits absent upstream.
6. Verify outcomes; avoid duplicate own replies. Reply, then resolve accepts only after reply succeeds and permission. Reject/clarify/defer remain unresolved.
7. Return `headBefore`, `headAfter`, `commits`, `pushed`, accepted/deferred fingerprints, and per-thread reply/resolution `threadOutcomes`.

## Delegation Boundary

Brief contains feedback, context, locations, outcomes, worktree, and target IDs; excludes methods, architecture, algorithms, techniques, and test commands.

## Git Preservation

| Returned state | Completion action |
|---|---|
| Pushed commits; clean | Nothing |
| Other accepted changes | One completion commit; push missing commits |

Never squash, amend, rebase, force-push, or redundantly push.

## Thread State

| Decision | Reply | Resolve |
|---|---|---|
| accept | Verified result and commit | Only after reply succeeds |
| reject | Technical rationale | Never |
| clarify | Focused question/interpretation | Never |
| defer | Concise deferral reason | Never |

Failed replies stay unresolved. Preserve successes; retry only incomplete remote operations.

## Boundary

Do not review the full diff, merge, close issues, clean branches/worktrees, or chain public stages. No implementation/test guidance.
