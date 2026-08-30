# Interactive Issue Execution Design

## Purpose

Turn Neil implementation from a one-turn stage into an explicitly completed development subagent. The user performs normal multi-turn work with that `issue-executing` child, including Superpowers, SDD, and any other framework. The coordinator advances only after the child receives:

```text
/issue-executing-complete
```

The command means "the development stage may be handed back to Neil". It does not mean the entire issue-to-PR workflow has completed.

## Scope

This change defines a client-neutral Neil protocol and updates `/using-neil-workflows`, `/issue-executing`, and a new `/issue-executing-complete` skill. It preserves existing issue, PR/MR, review, fix, merge, and close ownership boundaries.

The protocol names no AI client, UI, agent provider, message transport, session implementation, or framework. A client integration is only responsible for mapping the protocol to its own child-agent and message facilities. Neil owns workflow state, validation, and next-stage dispatch.

## Architecture

```text
Neil coordinator
  -> issue-init agent
  -> issue-executing development child
       <-> user and development frameworks
       -> /issue-executing-complete
  -> validated completion envelope
  -> pr-create agent
  -> existing Neil routing
```

The coordinator owns sequencing, durable state, and handoff validation. The development child owns code changes, tests, commits, and its interactive conversation. `pr-create` and later public stages retain their existing business ownership.

A coordinator persists one workflow run containing the validated `issue-init` handoff, an opaque child reference, and a state. The record is orchestration metadata, never authorization. Every target-consuming stage still resolves its own provider authorization and revalidates actual Git state.

## Portable Adapter Contract

An AI client integration implements these capability-neutral operations. Names are protocol descriptions, not required API names.

| Operation | Input | Required outcome |
|---|---|---|
| start development child | workflow run and sealed issue-init handoff | returns one opaque `childRef` |
| deliver user message | `childRef` and user content | appends content to that child only |
| deliver child event | `childRef` and protocol event | sends the event to the owning coordinator |
| resume coordinator | workflow run and validated event | starts the coordinator's next decision turn |
| start named stage | named skill and validated handoff | starts the specified next agent only |

A capable client can surface the child as a nested chat, separate tab, terminal session, or any equivalent interaction. The protocol does not prescribe the UI. A client without native child UI may proxy messages through its main conversation while preserving the same `childRef` and event payload. A client that cannot create a child or return a child event reports `unsupported-capability`; it must not treat a closing reply, Git activity, or user prose as completion.

The coordinator guarantees automatic continuation only after its adapter receives a valid completion event. This is the required truth boundary: a client that cannot return events cannot provide automatic continuation, but remains interoperable through an explicit transfer of the same completion envelope to the coordinator.

## States

| State | Meaning | Valid transition |
|---|---|---|
| `initializing` | `issue-init` is running | `developing`, `failed` |
| `developing` | One owned `issue-executing` child exists | `completion-requested`, `failed`, `cancelled` |
| `completion-requested` | The child received the exact completion command | `validated`, `developing`, `failed` |
| `validated` | Coordinator accepted actual Git handoff | `pr-creating`, `failed` |
| `pr-creating` | Existing `pr-create` stage is running | existing Neil terminal/routing states |

A child becoming idle, ending one response, reporting progress, making a commit, pushing, or saying work is done leaves the run in `developing`. A child transport may reconnect or resume the same child reference without creating another workflow run. A terminal child failure or explicit cancellation ends `failed` and never dispatches `pr-create`.

Each run has one active development child. The coordinator rejects a second child, a completion event from an unknown child reference, or a completion command outside the owned child context.

## Completion Command

`/issue-executing-complete` is available only inside a development child that received a valid Neil workflow context. It accepts no user-supplied handoff, target, repository, branch, child reference, or authorization fields.

On invocation the child:

1. Reads its sealed incoming `issue-init` handoff and assigned worktree.
2. Verifies that the worktree is accessible, belongs to the expected repository, and is on the expected branch.
3. Reads actual Git state without normalizing it: `status`, `headSha`, reachable/new commits, dirty state, and push state.
4. Emits exactly one `stage-complete` event through its client adapter. The event has `runId`, `childRef`, and one result object with only `version`, `stage`, `status`, and `handoff` at the top level.

The result object is:

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

The command rejects an inaccessible or mismatched worktree, missing Git state, malformed inherited handoff, unknown workflow run, or a child that is not the run's active child. The user can repair the condition and invoke the command again.

## Coordinator Validation and Resumption

The coordinator accepts a `stage-complete` event only when all conditions hold:

1. Its run is in `developing` or `completion-requested`.
2. Event `runId` and `childRef` match its stored owned values.
3. The result top level contains only `version`, `stage`, `status`, and `handoff`.
4. The handoff re-emits every issue-init leaf unchanged and has a matching repository, provider, host, issue, branch, worktree, and head repository.
5. The coordinator independently reads the supplied worktree's current branch and head and finds them equal to the reported actual Git fields.

After validation the coordinator moves to `validated`, invokes its generic start-stage adapter for a fresh `pr-create` agent, and passes only the validated completion handoff. It never accepts prose, copied JSON, a child final message, parent-thread text, framework status, or generic progress event as completion.

## Framework Compatibility

The protocol names no framework. Superpowers, SDD, and any other framework run inside the development child as ordinary guidance. They can create their own internal agents and user checkpoints, but must not invoke later Neil stages or synthesize the completion envelope.

A framework's own notion of completion has no Neil effect. The direct human `/issue-executing-complete` command is the sole request that may emit `stage-complete`.

## Error and Recovery Rules

- A client adapter may resume a child after reconnect or restart only when it can prove the same `childRef`; otherwise it reports an unavailable child and preserves `developing` or records explicit failure.
- A failed `pr-create` preserves the validated development handoff and leaves no automatic retry. The coordinator reports the exact failed stage.
- New target-stage authorization remains governed by existing remote-base checks; no run record, child reference, client event, or user message authorizes provider writes.
- No completion path cleans, amends, commits, pushes, squashes, or otherwise changes Git state solely to satisfy the handoff.

## Verification Strategy

Use fresh-context RED-GREEN-REFACTOR scenarios for skill contracts and transport-neutral integration simulations.

1. Coordinator starts one development child after valid `issue-init` and does not start `pr-create`.
2. Multiple ordinary child conversations, commits, reports, idle responses, framework completion, and "done" prose do not advance Neil.
3. The completion command outside the owned child is rejected.
4. The active child emits only the owned result shape with actual Git fields.
5. A malformed, stale, foreign-child, wrong-run, wrong-worktree, wrong-branch, or head-mismatched event stops before `pr-create`.
6. A valid completion event causes exactly one fresh `pr-create` start with the validated handoff.
7. Nested-chat, separate-chat, terminal, and main-conversation-proxy adapters produce the identical event and coordinator transition.
8. Reconnect/resume retains `developing`; explicit cancellation and unrecoverable child failure never open a PR/MR.
9. Existing false/true self-review routing begins only after successful `pr-create` and remains unchanged.

## Non-Goals

- Do not infer completion from language, tool output, Git status, tests, commits, framework state, or child response termination.
- Do not require any named client, browser, IDE, agent provider, framework, or transport.
- Do not alter remote authorization, review/fix logic, merge criteria, or issue-close behavior.
- Do not add provider or Git business operations to the coordinator.
