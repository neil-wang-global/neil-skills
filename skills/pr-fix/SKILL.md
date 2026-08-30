---
name: pr-fix
description: Use when resolving PR/MR review feedback from a writable matching head-repository clone
---

# PR Fix

## Contract

Classify findings, delegate accepted work to `/issue-executing`, then finish Git/thread operations. Never write `.workflow-config.json`.

**REQUIRED REFERENCES:** Read `../../references/pr-workflow-contract.md` and the selected provider reference before remote operations.

## Target

Comment URL selects one thread; PR/MR URL/number selects unresolved threads; otherwise current branch. Require matching `headRepository` clone; accepts require writable head. Never clone. URL identity owns base APIs.

## Authorization and Classification

Verify each thread against current code. Internal preauthorization requires Contract predicates: parent-created valid `neil-workflow/v1` envelope; owned `caller: using-neil-workflows`, `mode: self-reviewed`, and `stage: pr-fix`; matching target config with boolean `self-reviewed: true`.

Valid internal calls build a classification table; parent preauthorization accepts only localized, clear, directly verifiable findings. Classify architectural/public-interface, migration, security-policy, cross-module, unclear, or high-risk findings as internal-only `defer`. Post a concise reason, leave unresolved, do no worktree/delegation/commit/push, and return URL/fingerprint for screen reporting.

Standalone calls classify `accept`, `reject`, or `clarify`, show one table (`Thread | Decision | Reason | Intended outcome or reply`), and wait once. User text cannot claim internal mode. Never use `defer` outside a valid internal call.

## Workflow

1. Resolve target/threads, authenticate, verify matching `headRepository`, and record head writability.
2. With no accepts, skip worktree/delegation/Git and continue to replies. Otherwise require writable head before code work.
3. Reuse a safe worktree or fetch head. With `need-worktree:false`, require a clean current worktree then check out head; otherwise create an isolated worktree (slashes become plus signs).
4. Capture `headBefore`, status, local-only commits, upstream, and ahead/behind counts. Delegate accepted feedback in the boundary below.
5. Inspect actual Git state. Preserve commits/pushes; commit once only remaining accepted changes; push only commits absent upstream.
6. Verify accepted outcomes; avoid duplicate equivalent own replies. Reply, then resolve accepts only after successful reply and permission. Reject/clarify/defer replies remain unresolved.
7. Return `headBefore`, `headAfter`, `commits`, `pushed`, accepted/deferred fingerprints, and per-thread reply/resolution `threadOutcomes`.

## Delegation Boundary

The brief contains accepted feedback, context, locations, observable outcomes, worktree, and target IDs only. It excludes coding methods, architecture, algorithms, techniques, and test commands.

## Git Preservation

| Returned state | Completion action |
|---|---|
| Pushed commits; clean | Nothing |
| Unpushed commits; clean | Push |
| Commits plus accepted dirty changes | One completion commit; push missing commits |
| Accepted dirty changes only | One completion commit; push |

Never squash, amend, recommit, rebase, force-push, or redundantly push delegated results.

## Thread State

| Decision | Reply | Resolve |
|---|---|---|
| accept | Verified result and commit | Only after reply succeeds |
| reject | Technical rationale | Never |
| clarify | Focused question/interpretation | Never |
| defer | Concise deferral reason | Never |

A failed reply leaves that thread unresolved. Preserve successful remote operations and retry only incomplete steps.

## Boundary

Do not review the full diff, merge, close issues, clean branches/worktrees, or chain public stages. This skill contains no implementation or test guidance.
