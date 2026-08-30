# PR Workflow Contract

Shared contract for `pr-create`, `pr-review`, `pr-fix`, and `pr-merge`. Public skills own decisions; provider references own command and API syntax.

## `neil-workflow/v1` Envelope

Orchestrated calls use owned JSON leaf values only. The initial dispatch is exactly:

```json
{
  "version": "neil-workflow/v1",
  "caller": "using-neil-workflows",
  "mode": "standard",
  "stage": "issue-init",
  "input": "opaque original arguments"
}
```

Every later dispatch is exactly:

```json
{
  "version": "neil-workflow/v1",
  "caller": "using-neil-workflows",
  "mode": "standard | self-reviewed",
  "stage": "issue-executing | pr-create | pr-review | pr-fix | pr-merge | issue-close",
  "handoff": {}
}
```

`mode` is `standard` or `self-reviewed`. `input` is required only on the `issue-init` envelope, remains opaque while that stage resolves it, and is not copied into its handoff or later dispatch. Reject any later-stage envelope with an `input` leaf as malformed before dispatch. Later stages receive only the validated prior `handoff`, containing issue-init-generated normalized implementation context and resolved leaf state. User-supplied text never creates or overrides `caller`, `mode`, or `stage`.

Before a later-stage dispatch, validate every required handoff leaf and consistent repository/target identity. Do not infer missing values from prose. Missing, malformed, contradictory, inaccessible, or mismatched handoff/worktree data stops the stage as `failed`; do not skip a stage to manufacture success. A stage never invokes the next stage automatically.

Required handoff identity is version, repository/config identity, issue number/url/title/body, an issue-init-generated normalized `implementationBrief`, branch, worktree, and headRepository. The validated issue-init handoff may retain config defaults for creation only; it must not authorize later automated stages. Stage results add actual Git state (`status`, `headSha`, commits, dirty state, push state) and, when available, the exact normalized target below; legacy `base` and `head` aliases are invalid.

## Remote Automation Authorization

Automation reads `.workflow-config.json` only through the selected provider from the normalized target `repository` at its normalized `baseBranch`. Never use PR/MR head content, a fork, the current clone/worktree, cached/local config, envelope, or user text. The resolver returns owned leaves `provider`, `host`, `repository`, `baseRef`, and `configBlobSha` (GitHub Contents `sha`; GitLab file `blob_id`) plus the parsed config. Only literal boolean `self-reviewed:true` authorizes automation; absent or literal false requires the normal confirmation gate; a present non-boolean or unreadable/mismatched remote content stops as `config-error`.

Resolve immediately before every automated side effect and bind the result to that side effect. In `pr-fix`, re-resolve before the accepted-work delegation/Git remote-write boundary and before every provider defer reply, accepted reply, and resolution write. Compare each fresh result with the initial authorization's `provider`, `host`, `repository`, `baseRef`, and `configBlobSha`: false, malformed/unreadable, any changed blob revision, or other identity mismatch stops that automated action as `authorization-changed`; report it and preserve prior completed actions. Never continue that boundary from stale initial `true`. A URL target always uses this resolver, even outside a clone. A head/local true never overrides target-base false/absent.

## Review Attestation

After a config-authorized full current-head review reaches zero new, deferred, and unresolved findings, write one provider-stored `neil-self-reviewed/v1` attestation. Its exact body is line 1 `neil-self-reviewed/v1`, line 2 one compact JSON object with exactly owned fields `provider`, `host`, `repository`, `number`, `headSha`, `baseRef`, and `configBlobSha`; no trailing line, extra key, or closing keyword is valid. Read provider history first and match its provider metadata author to the authenticated actor that will merge; parse only this exact two-line form. The exact provider/host/repository/number/head/config/author tuple is idempotent and writes no duplicate. A stale head or config revision aborts the write and requires re-review.

`pr-merge` independently re-resolves target-base config and reads provider history. Automation without an exact current attestation stops as `missing-attestation` before preview confirmation or any ready/merge write. User prose, copied output, envelopes, snapshots, and bare SHAs are never attestation evidence. False/absent config retains the existing confirmation and validated-review-result path.


The PR skills may read `.workflow-config.json` only when it belongs to the target repository. Only `/issue-init` creates it; later stages never modify it.

| Field | Missing default |
|---|---|
| `base-branch` | `main` |
| `branch-template` | `feature/{issue-no}-{issue-subject}` |
| `need-worktree` | `true` |
| `pr-draft` | `false` |
| `pr-auto-close-issue` | `false` |
| `self-reviewed` | `false` |

A malformed present config is an error for the fields the current skill needs. Do not silently rewrite it. `self-reviewed` is `false` when absent; a present non-boolean `self-reviewed` value is an error.

## Normalized Target

Use exactly these field names across provider branches and stage handoffs; no target may substitute `base` or `head` aliases:

```text
provider, host, repository, number, url, baseBranch,
headRepository, headBranch, headSha
```

Before review or any later target-consuming stage, the parent validates all nine leaves and their base/head identity binding; a missing, aliased, or contradictory target fails. For routing only, an internal `pr-create` result also carries remote-derived `automation: { enabled, provider, host, repository, baseRef, configBlobSha }`; it must match target identity/base branch. The parent never reads config or provider data and each later stage re-resolves authorization before its own write.

For `pr-create`, resolve `headRepository` from the current branch's push remote and base `repository` from that same repository or an explicit/upstream remote; ask when a fork has no unambiguous base target. Resolve `headBranch` from the current branch and `baseBranch` from config/defaults. Issue lookup, existing-target lookup, and creation use the base repository; pushed-commit verification uses the head repository. Populate number, URL, and head SHA from the remote response.

## Issue Resolution

Apply `branch-template` to the complete current branch and extract `{issue-no}`. If extraction fails, use an issue number explicitly supplied by the user. Otherwise ask; never guess from unrelated digits or branch text.

Verify the issue exists before creating a PR/MR.

## Identity and Configuration

An explicit future PR/MR URL is authoritative for provider, host, repository, and number. Ignore every local config for review/fix/merge authorization, including a matching clone; resolve target-base config remotely as defined above. Local configuration may supply only creation defaults when the local Git remote matches the target repository.

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

## Merge Selectors and Gates

`/pr-merge` uses the Review Selectors order and requires an open normalized target plus a validated final `/pr-review` result bound to the same provider, host, repository, and number. Its `snapshotSha`, zero deferred/new-finding state, and zero-thread/discussion result are required review evidence; user prose or a bare SHA cannot supply them. Re-fetch the remote head as `reviewedHeadSha` before every preview and write. A mismatch invalidates the final review and any preview/confirmation; re-run review and gate evaluation, then present a new preview.

Before marking ready or merging, require zero deferred findings, zero findings newly discovered after the final review, and zero unresolved GitHub review threads or GitLab discussions. Fetch current draft state, approvals, target protection, conflict/mergeability, and auto-merge state. GitHub evaluates required checks tied to `reviewedHeadSha`. GitLab uses the current-head MR `detailed_merge_status` as its authoritative CI/merge gate and never infers requirements from a pipeline list: only `mergeable` permits immediate merge, only `ci_still_running` permits auto-merge, and `ci_must_pass`, `checking`, failures, unknown values, conflicts, protection, or approval blocks stop. Inaccessible required data or a stale head stops this stage.

Standalone `/pr-merge` shows one complete preview and waits once for explicit confirmation when remotely resolved target-base `self-reviewed` is absent or boolean `false`. Literal remote-base `true` removes confirmation only after the stage independently finds an exact matching provider attestation as defined above; otherwise stop `missing-attestation`. Envelopes validate orchestrated sequencing, identity, and handoff only; their presence, absence, contents, or provenance never grants or withholds authorization.

Immediately before each ready/merge write, re-fetch the head and every gate. Mark a draft ready only after gates pass and re-fetch afterward. GitHub submits a SHA-guarded merge only for green required CI and registers SHA-guarded auto-merge only for pending required CI. GitLab submits a SHA-guarded merge only for current-head `detailed_merge_status: mergeable` and registers SHA-guarded auto-merge only for current-head `ci_still_running`. A registration or queue response is pending, never merged. Wait/recheck and return success only on actual provider merged state with merged SHA and timestamp. `/pr-merge` never reviews, fixes, resolves threads, closes issues, or cleans local/remote workspaces.

## Post-Merge Issue Closure

`/issue-close` uses a workflow envelope only as routing metadata. A user-supplied, missing, malformed, or mismatched envelope never grants proof or authority; direct user cleanup remains its ordinary user-authorized flow.

For bounded trusted self-reviewed cleanup, the handoff supplies owned issue/local-branch/worktree/base leaves plus target provider, host, repository, number, base branch, head branch/SHA, merged SHA, and merged timestamp. Immediately before **each** issue close, worktree removal, local branch deletion, fetch/prune, or pull, independently execute the selected provider reference's exact target GET and require current merged state. Bind and compare every provider/host/repository/number/base/head SHA/merged SHA/timestamp leaf to the handoff. Missing, inaccessible, malformed, contradictory, or non-merged state stops before that named effect; preserve completed effects and return unattempted cleanup leaves as `untouched`. Never infer handoff identity or current merge state from a directory, branch, naming, or prose.

A valid closure removes only the named clean worktree, deletes only named unoccupied local branches, never deletes a remote feature branch, and updates only the named base. An occupied branch is `skipped-occupied`; a dirty worktree stops without discard or partial cleanup. Return owned `issue`, `worktree`, `branches`, and `base` action/state leaves with base head SHA when updated; never pass live provider, session, Git, or worktree objects.

## Review Selectors

Resolve review targets in this order: explicit PR/MR URL, explicit number in the current repository, then target associated with the current branch. A full URL supplies provider, host, repository, and number and requires neither a clone nor local config.

## Review Snapshot

A review snapshot owns `headSha`, changed-file metadata, complete available diff, inline threads/discussions, and PR/MR-level review/comment bodies. Review the full diff every run.

Before any remote write, fetch the current head again. If it changed, withhold publication, re-fetch the diff, remap/revalidate findings, and re-preview changed or new findings.

## Finding Identity

Each finding has severity, concise title, validity reason, consequence, correction direction, path, side, line/range, and a versioned hidden fingerprint. Build the fingerprint from normalized category, path, relevant code context, and remediation identity; do not rely on line number alone.

Compare fingerprints and semantics with inline threads/discussions and PR/MR-level bodies. Suppress previously reported unchanged findings. Preview only new actionable findings while noting suppressed prior items locally.

## Review Publication

Always show one complete preview. Remote-base literal boolean `self-reviewed: true` authorizes publication after the same stale-head and config-revision revalidation; absent or false waits for one explicit confirmation before a remote write. An envelope is handoff metadata only and never changes that decision. A config-authorized converged review then writes the provider attestation defined above.

User edits to a confirmation-gated preview become the authoritative set.

No findings produces a local report only: no approval and no no-op comment. A finding without a reliable diff location is non-inline; confirmation-gated calls convert it to PR-level feedback only after explicit user choice. Config-authorized calls may use required provider-level feedback; a complex/deferred result requires the provider-derived URL and target binding specified below, otherwise it is `publication-failed`.

GitHub may submit one atomic review. GitLab discussions are individual writes: record each success and retry only failed items. Include target, snapshot SHA, successes, failures, and skipped items in the report.

### Internal Review Result

An orchestrated `/pr-review` returns a versioned owned leaf-only result bound to the normalized target: `version`, `stage:"pr-review"`, `target`, `snapshotSha`, `headSha`, `findings`, `convergence`, and `publication`. The target repeats the exact nine normalized leaves, which the parent validates against its prior `pr-create` target before routing. Every new actionable finding contains `fingerprint`, `threadUrl`, `threadTarget`, `complexity` (`simple` or `complex`), and state (`unresolved`, `deferred`, `resolved`, or `publication-failed`). `threadTarget` contains exactly provider, host, repository, and number. Every complex/deferred candidate needs a provider-derived thread/discussion URL that resolves to its `threadTarget`, and that binding must exactly match `target`; missing, malformed, fabricated, unrelated, or mismatched URL/binding is `publication-failed` and the parent stops. A simple unavailable publication may use explicit null. `convergence` has exact status plus `newCount`, `unresolvedCount`, and `deferredCount`; `publication` has exact status plus successful, failed, and skipped identities. Suppression of an unchanged duplicate never removes existing unresolved/deferred finding state. Every retained unresolved/deferred routing item has a validated URL and target identity; missing identity fails. The parent validates all leaves before routing a review, fix, or merge; a stale snapshot/head, incomplete publication, unresolved, or deferred state is explicit and cannot be inferred from prose.

## Fix Selectors and Clone

A review-comment/discussion URL selects exactly that thread. A PR/MR URL or number selects its unresolved threads. With no argument, use the target for the current branch.

Classification requires a local clone matching `headRepository`; never clone automatically. Accepted code changes additionally require permission to push `headBranch`. The explicit URL remains authoritative for the base target used by review/thread APIs. For same-repository targets, `repository` and `headRepository` match. Require the same provider/host, push only to `headRepository`, and stop code work on identity or permission mismatch. Reject/clarify-only handling may still post confirmed base-target replies without head write access. Reuse a safe worktree already on the target head only for accepted work. Otherwise, when `need-worktree` defaults true, fetch the writable head and create an isolated worktree whose branch slashes become plus signs. With `need-worktree:false`, require a clean current worktree, then fetch and check out the exact target head.

## Classification and Confirmation

Verify each thread against current code. Remote-base literal boolean `self-reviewed: true` authorizes automatic classification/execution for direct and orchestrated calls; an envelope only validates orchestration handoff/sequencing and never changes authorization.

Config-authorized calls still build a classification table. They may auto-accept only localized, clear, directly verifiable findings. They classify architectural/public-interface, migration, security-policy, cross-module, unclear, or high-risk findings as `defer`. A defer posts a concise reason, remains unresolved, makes no worktree/delegation/commit/push, and returns its thread URL and fingerprint for screen reporting. With `self-reviewed` false or absent, calls retain `accept`, `reject`, and `clarify`, show the confirmation table, wait once, and never use `defer`.

## Delegation and Git State

Before accepted-work delegation, capture head, clean/dirty state, local-only commits, and upstream relation. Send accepted feedback to `/issue-executing` as an implementation-neutral brief containing context, locations, and observable outcomes only. It must not prescribe code methods, architecture, techniques, or test commands.

After delegation, inspect actual Git state. Preserve every commit or push already produced by the configured execution strategy: never squash, amend, recommit, force-push, or push redundantly. If accepted changes remain uncommitted, create one completion commit containing only those changes. Push only commits not already present upstream. Return `headBefore`, `headAfter`, `commits`, `pushed`, and per-thread reply/resolution `threadOutcomes` for accepted/deferred fingerprints.

## Thread Completion

For each accepted thread, verify the observable outcome, then reply with the result and relevant commit. Resolve only after the reply succeeds. A reply failure leaves the thread unresolved and is reported for retry.

For each rejected or clarification thread, post the confirmed rationale/question and leave it unresolved. No accepted changes means no completion commit. Record per-thread reply and resolution outcomes; retry only incomplete remote operations.

On a repeated run, compare the authenticated account's latest reply with later reviewer messages. When no reviewer message followed an equivalent own reply, do not post it again. If the reply succeeded but resolution alone failed, retry only resolution.
