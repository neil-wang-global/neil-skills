# issue-init verification

Fresh agents used the modified `issue-init` skill.

## Scenario A: missing configuration — PASS

> Created `.workflow-config.json` with the following defaults:
>
> ```json
> {
>   "type": "github",
>   "base-branch": "main",
>   "branch-template": "feature/{issue-no}-{issue-subject}",
>   "need-worktree": true,
>   "execution-strategy": "",
>   "pr-draft": false,
>   "pr-auto-close-issue": false,
>   "self-reviewed": false,
>   "language": "",
>   "remarks": ""
> }
> ```
>
> What description should I use for the new issue, **Add cache invalidation**?

The exact approved defaults are present and the existing non-empty issue body gate remains intact.

## Scenario B: existing configuration — PASS

> I found the existing `.workflow-config.json` and will preserve it without overwriting or normalizing any fields.
>
> Existing values retained exactly:
> - `execution-strategy`: `"team delivery policy"`
> - `pr-draft`: `true`
> - All other existing configuration fields: unchanged
>
> No issue number was provided, so this will create a new issue. Please provide the issue title and description.

Existing project choices are preserved.

## Scenario C: no automatic chaining — PASS

> Issue: https://github.com/example/repo/issues/42
> Branch: `feature/42-add-cache-invalidation`
> Working environment: `/path/to/worktrees/feature-42-add-cache-invalidation`
>
> Another skill invoked: No.

The skill stops after reporting its own result.

## Result

| Scenario | Result | Evidence |
|---|---|---|
| Missing configuration | PASS | Exact ten-field default JSON |
| Existing configuration | PASS | New fields preserved verbatim |
| No automatic chaining | PASS | Explicitly invokes no later skill |

No new rationalization or loophole appeared during GREEN verification.

## Cross-skill verification

Flow A passed: `issue-init` alone creates the exact ten-field config, reports its issue/branch/worktree result, and does not invoke `issue-executing` or a PR stage.

## Task 1 GREEN scenarios

### Scenario D: self-review default — PASS

> Created `.workflow-config.json`:
>
> ```json
> {
>   "type": "github",
>   "base-branch": "main",
>   "branch-template": "feature/{issue-no}-{issue-subject}",
>   "need-worktree": true,
>   "execution-strategy": "",
>   "pr-draft": false,
>   "pr-auto-close-issue": false,
>   "self-reviewed": false,
>   "language": "",
>   "remarks": ""
> }
> ```
>
> What title and body should the new issue use?

The fresh result contains the required ten-field flat default, with `self-reviewed:false`, then `language:""`, immediately before `remarks`.

### Scenario E: opaque orchestrator input — PASS

> {"version":"neil-workflow/v1","repository":{"provider":"github","host":"github.com","name":"acme/widgets"},"configIdentity":{"repository":"acme/widgets","path":".workflow-config.json"},"issue":{"number":42,"url":"https://github.com/acme/widgets/issues/42","title":"Cache invalidation","body":"Add invalidation"},"implementationBrief":{"summary":"Cache invalidation","outcomes":["Invalidate stale cache entries"]},"branch":"feature/42-cache-invalidation","worktree":"/repo/.worktrees/feature+42-cache-invalidation","headRepository":"acme/widgets","textLanguage":""}

A fresh completed-resolution simulation retained `#42 --label urgent preserve this wording` only while issue-init resolved issue #42. The returned handoff contains normalized issue-init output and resolved leaf state only: it contains neither the original value nor `--label`, `urgent`, or `preserve this wording`. It invoked no later stage.

### Scenario F: no local authorization handoff — PASS

The revised handoff does not include `config.selfReviewed` for boolean true, absent, or malformed local values. It never uses a local configuration claim to select automation; target PR/MR stages must resolve their normalized target base ref remotely. Raw input remains absent in every case.

## Task 3 Static Contract Records

### Scenario G: ordered language default — PASS

Static document inspection confirms the exact default object order is `type`, `base-branch`, `branch-template`, `need-worktree`, `execution-strategy`, `pr-draft`, `pr-auto-close-issue`, `self-reviewed`, `language`, `remarks`, with `language:""`.

### Scenarios H-I: local Chinese and compatibility — PASS

Static contract inspection confirms a trimmed local `简体中文` value becomes `textLanguage:"简体中文"` and governs only newly generated issue title/body text. Whitespace-only and absent values both hand off `textLanguage:""` and retain existing behavior. Exact quotations and code identifiers are exceptions and remain unchanged.

No executable suite was run for these static records.
