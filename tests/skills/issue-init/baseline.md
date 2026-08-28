# issue-init baseline

These responses were produced by fresh agents using the pre-change `issue-init` skill.

## Scenario A: missing configuration — FAIL

> `.workflow-config.json` is missing. I would create it with:
>
> ```json
> {
>   "type": "github",
>   "base-branch": "main",
>   "branch-template": "feature/{issue-no}-{issue-subject}",
>   "need-worktree": true,
>   "remarks": ""
> }
> ```
>
> I’ll create a new GitHub issue titled `Add cache invalidation`. Please provide the issue description so I can create it with a non-empty body.

Failure: the default omitted `execution-strategy`, `pr-draft`, and `pr-auto-close-issue`.

## Scenario B: existing configuration — PASS

> I found the existing `.workflow-config.json` and will leave it unchanged.
>
> Existing configuration handling:
> - `execution-strategy`: preserved verbatim as `"team delivery policy"`; no overwrite or normalization.
> - `pr-draft`: preserved verbatim as `true`; no overwrite or normalization.
> - `type`: used to select GitHub (`gh`) or GitLab (`glab`) commands.
> - `base-branch`: used as the feature branch base.
> - `branch-template`: used to form the branch name, substituting the issue number and an ASCII English slug of the issue title.
> - `need-worktree`: determines whether to create a worktree or check out directly.
> - `remarks`: applied as additional workflow instructions when non-empty.
>
> Do you want to link an existing issue, or create a new issue?

The existing unknown fields were preserved rather than overwritten or normalized.

## Scenario C: no automatic chaining — PASS

> Issue initialized successfully.
>
> - Issue: `[issue URL]`
> - Branch: `[branch name]`
> - Working environment: `[worktree path]`
>
> Additional skill invoked: No.

The existing skill already stops after reporting the initialized issue environment.

## RED conclusion

Scenario A demonstrates the missing configuration contract. The minimal change is to add the three approved fields to the default JSON and field table while preserving the existing no-chaining behavior.
