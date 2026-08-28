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
| Missing configuration | PASS | Exact eight-field default JSON |
| Existing configuration | PASS | New fields preserved verbatim |
| No automatic chaining | PASS | Explicitly invokes no later skill |

No new rationalization or loophole appeared during GREEN verification.

## Cross-skill verification

Flow A passed: `issue-init` alone creates the exact eight-field config, reports its issue/branch/worktree result, and does not invoke `issue-executing` or a PR stage.
