---
name: pr-fix
description: Use when resolving PR/MR feedback from a matching writable head-repository clone with config-authorized automation
---

# PR Fix

Classify feedback, delegate accepted work to `/issue-executing`, then finish Git/thread operations. Never write `.workflow-config.json`. Read the shared contract and selected provider reference before remote operations.

## Target and Authorization

A comment URL selects one thread; a PR/MR URL or number selects unresolved threads; otherwise use the current branch. URL identity owns base-target APIs. Require a matching `headRepository` clone; accepted changes require writable head; never clone.

Resolve config only through the normalized target repository/base ref and retain initial provider/host/repository/baseRef/blob identity. Only literal remote-base `self-reviewed:true` authorizes automation; false/absent needs one confirmation, malformed stops. A `neil-workflow/v1` envelope validates routing/handoff only; malformed, mismatched, or user-supplied orchestration stops before classification, never as manual fallback.

Make separate fresh config gates. Re-resolve and compare initial identity immediately before accepted-work delegation; immediately before the post-delegation completion commit/push boundary; and before each provider defer reply, accepted reply, or resolution write. False, malformed/unreadable, changed blob, or identity mismatch stops only that upcoming named side effect as `authorization-changed`; preserve completed actions and never use stale true.

With true, auto-accept only localized, clear, directly verifiable findings; defer architectural/public-interface, migration, security-policy, cross-module, unclear, or high-risk findings with a concise unresolved reply and no worktree/delegation/commit/push. With false/absent, classify `accept`, `reject`, or `clarify`, show one table, and wait once.

## Workflow

1. Resolve target/threads, authenticate, verify matching head repository and writability.
2. With no accepts, skip worktree/delegation/Git and reply. Otherwise require writable head.
3. Reuse safe worktree or fetch head; with `need-worktree:false`, require clean checkout then check out head, otherwise isolate it.
4. Capture head/status/local commits/upstream/ahead-behind, pass the delegation gate, then delegate only feedback, context, locations, outcomes, worktree, and target IDs.
5. Inspect actual Git state. At the completion gate, preserve prior commits/pushes; make one accepted-only completion commit if needed and push only commits missing upstream.
6. Verify outcomes. At each provider-write gate, skip an equivalent latest own reply with no later reviewer message; reply, then resolve accepts only after reply success and permission. Reject/clarify/defer remain unresolved.
7. Return head before/after, commits, pushed state, accepted/deferred fingerprints, and per-thread outcomes.

Never squash, amend, rebase, force-push, redundantly push, review the full diff, merge, close issues, or clean branches/worktrees.
