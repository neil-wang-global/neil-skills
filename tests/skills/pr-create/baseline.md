# pr-create baseline

Fresh agents received no `pr-create` guidance and performed simulation only.

## Core scenarios

### Scenario A: no config — PASS in the core sample, unstable overall

> No workflow config is created. The PR targets `main` and is created ready for review, not as a draft. Its issue relation uses `Related to #42`; the issue remains open.

The single core sample passed, but the five repeated controls below did not.

### Scenario B: configured draft and closing — PASS

> The PR would be created as a draft. Its body would include `Closes #42`. That links issue #42 and closes it only when the PR is merged.

### Scenario C: existing PR — PASS

> With an existing open PR for the current branch, `/pr-create` should not create another PR or edit the branch. It should detect/reuse PR #81 and report that state.

### Scenario D: branch mismatch — PASS

> Ask. With no supplied issue number, I would not guess one from `maintenance/cache`; branch names are not reliable issue metadata.

### Scenario E: independent stage — PASS

> `/pr-create` completed successfully. I would not invoke code review automatically; review is a distinct action and should be explicitly requested.

## Scenario A repeated controls — FAIL 5/5

| Run | Creates config | Ready | Relation | Result |
|---:|:---:|:---:|---|---|
| 1 | Yes | Yes | `Closes #42` | FAIL |
| 2 | Yes | Yes | `Closes #42` | FAIL |
| 3 | Yes | Yes | `Closes #42` | FAIL |
| 4 | Yes or prompts | Yes | `Closes #42` | FAIL |
| 5 | Yes | Yes | `Closes #42` | FAIL |

All repeated samples understood that closing occurs at merge, not PR creation. The failures were creating `.workflow-config.json` and selecting closing semantics when no configuration exists.

## RED conclusion

Minimal guidance must make these defaults deterministic:

1. Never create or modify workflow configuration.
2. Missing config means `main`, ready-for-review, and non-closing issue relationship.
3. Existing PR lookup is idempotent.
4. An unparseable branch requires an explicit issue number.
5. Successful creation reports the next available command without invoking it.

## Independent-review RED regression

A final reviewer found that the provider reference unconditionally used GitLab `--related-issue`, whose generated description contains a closing relationship. This contradicted the default non-closing policy and became Scenario F before the adapter was changed.

A later reviewer found fork checkouts would query/create inside the fork because provider commands omitted the upstream base target and qualified head. This became Scenario G.

A final provider check found `gh pr create --head` rejects organization owners. This became Scenario H and requires REST creation for organization-owned fork heads.
