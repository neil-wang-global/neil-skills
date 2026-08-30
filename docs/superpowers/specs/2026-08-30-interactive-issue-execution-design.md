# Interactive Issue Execution Design

## Purpose

Change Neil workflow execution from a one-turn implementation stage into an explicitly completed, continuable development subagent. The user performs normal multi-turn development work with that `issue-executing` child, including Superpowers, SDD, and any other framework. The parent coordinator advances to the next Neil stage only after the child receives the explicit command:

```text
/issue-executing-complete
```

The command means "the development stage may now be handed back to Neil". It does not mean the entire issue-to-PR workflow has completed.

## Scope

This change applies to `/using-neil-workflows`, `/issue-executing`, and a new `/issue-executing-complete` skill. It preserves the existing issue, PR/MR, review, fix, merge, and close ownership boundaries.

The protocol must not depend on an embedded browser UI. A client with a continuable-subagent conversation surface opens the child directly. A client without that surface can present a parent-mediated relay of the same child conversation. Both paths use the same child identity, completion command, and handoff contract.

## Architecture

```text
main coordinator
  -> fresh issue-init
  -> continuable issue-executing child
       <-> user and development frameworks
       -> /issue-executing-complete
  -> validated completion handoff
  -> fresh pr-create
  -> existing Neil routing
```

The coordinator owns sequencing and handoff validation only. The development child owns code changes, tests, commits, and its interactive conversation. `pr-create` and later public stages remain fresh agents with their existing business ownership.

The coordinator records a durable workflow run containing the validated `issue-init` handoff, the direct child session identity, and state. That record is orchestration metadata, never authorization. Every target-consuming stage still resolves its own provider authorization and revalidates actual Git state.

## States

| State | Meaning | Valid transition |
|---|---|---|
| `initializing` | `issue-init` is running | `developing`, `failed` |
| `developing` | One `issue-executing` child is active or resumable | `completion-requested`, `failed`, `cancelled` |
| `completion-requested` | The child received the exact completion command | `validated`, `developing`, `failed` |
| `validated` | Parent accepted a matching actual-Git handoff | `pr-creating`, `failed` |
| `pr-creating` | Existing fresh `pr-create` stage is running | existing Neil terminal/routing states |

A child becoming idle, settling, reporting progress, making a commit, pushing, or saying that work is done leaves the run in `developing`. Child settlement is resumable state, not completion. A cancellation or unrecoverable child failure ends `failed` and does not dispatch `pr-create`.

At most one active development child may exist for a workflow run. The parent rejects a second child, a completion report from another child, or a completion command outside the owned child session.

## Completion Command

`/issue-executing-complete` is available only in an `issue-executing` child with a valid Neil workflow context. It accepts no user-supplied handoff, target, repository, branch, or authorization fields.

On invocation the child:

1. Reads the sealed incoming `issue-init` handoff and its assigned worktree.
2. Verifies that the worktree is accessible, belongs to the expected repository, and is on the expected branch.
3. Reads actual Git state without normalizing it: `status`, `headSha`, reachable/new commits, dirty state, and push state.
4. Returns exactly one completion request to its parent with `version`, `stage`, `status`, and `handoff` at the top level. The handoff re-emits every validated `issue-init` leaf unchanged and appends only actual `git` data.

The result has this shape:

```json
{
  "version": "neil-workflow/v1",
  "stage": "issue-executing",
  "status": "completed",
  "handoff": {
    "version": "neil-workflow/v1",
    "repository": { "provider": "github", "host": "github.com", "name": "acme/widgets" },
    "configIdentity": { "repository": "acme/widgets", "path": ".workflow-config.json" },
    "textLanguage": "",
    "issue": { "number": 42, "url": "...", "title": "...", "body": "..." },
    "implementationBrief": { "summary": "Cache invalidation", "outcomes": ["Invalidate stale cache entries"] },
    "branch": "feature/42-cache",
    "worktree": "/repo/.worktrees/feature+42-cache",
    "headRepository": "acme/widgets",
    "git": {
      "status": "clean",
      "headSha": "abc123",
      "commits": ["abc123"],
      "dirty": false,
      "pushState": "pushed"
    }
  }
}
```

The command may reject completion for an inaccessible or mismatched worktree, missing Git state, malformed inherited handoff, or a child that is not the run's active child. The user then remains in the child conversation and can repair the condition before invoking the command again.

## Parent Validation and Resumption

The parent accepts a completion request only when all of the following hold:

1. Its workflow run is in `developing` or `completion-requested`.
2. The report source is the recorded direct child identity.
3. The top-level result contains only `version`, `stage`, `status`, and `handoff`.
4. The handoff re-emits each issue-init leaf byte-for-value and has a matching repository, provider, host, issue, branch, worktree, and head repository.
5. The parent independently re-reads the supplied worktree's current branch and head and finds them equal to the reported actual Git fields.

After successful validation the parent moves to `validated` and dispatches fresh `pr-create` using an envelope containing only the validated completion handoff. It never accepts prose, a copied JSON fragment, a child final message, a user message in the parent thread, or a generic `report` as a completion request.

## Client and Framework Compatibility

The protocol names no framework. Superpowers, SDD, and any other framework run inside the child as normal development guidance. They may create their own internal agents and user checkpoints, but must not invoke later Neil stages or synthesize the completion handoff.

A high-fidelity client exposes the continuable child transcript and routes user input directly to it. A client that has no nested-session surface keeps the parent selected and relays messages to and from the same child. The completion command remains explicit and is routed only to the child. A client that cannot retain or resume a child session must stop with a clear unsupported-capability result rather than silently treating its last response as completion.

## Error and Recovery Rules

- A child may be resumed after idle settlement, client reconnect, or process restart when its session is available; this does not create another workflow run.
- The parent must retain the run as `developing` until a valid completion request arrives or an explicit cancellation/failure is recorded.
- A failed `pr-create` preserves the validated development handoff and leaves no automatic retry. The coordinator reports the exact failed stage.
- New target-stage authorization remains governed by existing remote-base checks; neither child identity nor workflow records authorize provider writes.
- No completion path cleans, amends, commits, pushes, squashes, or otherwise changes Git state solely to satisfy the handoff.

## Verification Strategy

Use fresh-context RED-GREEN-REFACTOR scenarios for the skill contracts and an integration simulation for routing.

1. `/using-neil-workflows` starts a continuable `issue-executing` child after a valid `issue-init` handoff and does not dispatch `pr-create` yet.
2. The user can hold multiple ordinary development conversations with the child; its commits, reports, idle settlement, and "done" prose do not advance Neil.
3. `/issue-executing-complete` outside the active child is rejected.
4. The command in the active child returns only the owned four-top-level-field result with actual Git fields.
5. A malformed, stale, foreign-child, wrong-worktree, wrong-branch, or head-mismatched completion request stops before `pr-create`.
6. A valid command causes exactly one fresh `pr-create` dispatch with the validated completion handoff.
7. A client with direct child access and a parent-relay client produce the same completion payload and parent transition.
8. Child restart/resume retains `developing`; a child failure or explicit cancellation never opens a PR/MR.
9. Existing false/true self-review routing begins only after successful `pr-create` and remains unchanged.

## Non-Goals

- Do not infer completion from conversational language, tool output, Git status, tests, commits, or child settlement.
- Do not require a particular framework, agent model, browser, or IDE.
- Do not alter remote authorization, review/fix logic, merge criteria, or issue-close behavior.
- Do not add provider or Git business operations to the parent coordinator.
