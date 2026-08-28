# pr-review verification

Fresh agents used `pr-review` and the extended provider references. All reviews were simulated.

## Core scenarios

| Scenario | Result | Evidence |
|---|---|---|
| A: URL outside repository | PASS | URL resolves target; no clone or config |
| B: preview gate | PASS | Complete preview and explicit confirmation before writes |
| C: repeated full review | PASS | Full scope; old duplicate suppressed; one new preview |
| D: stale head | PASS | Withhold, re-fetch, remap, and re-preview |
| E: no findings | PASS | Local report; no approval or comment |
| F: unlocatable line | PASS | Non-inline marker; no guess; explicit PR-level choice |

## Preview pressure results

Five fresh repeated samples all returned preview-and-wait behavior. RED was 5/6 immediate-publish responses; GREEN is 5/5 explicit-confirmation responses.

## Deduplication pressure results

Five fresh repeated samples all produced:

- Full diff scope.
- Existing unchanged finding suppressed by fingerprint plus semantics.
- Exactly one new finding in the preview.

## Provider behavior

| Provider | Result | Evidence |
|---|---|---|
| GitHub | PASS | Modern line/side fields, one `COMMENT` review, current head SHA |
| GitLab | PASS | Current SHA tuple, one discussion per finding, partial-success retention |

## Host-routing regression

A GREEN agent found that the first reference draft preserved `host` in the normalized target but omitted it from provider API examples. That could route enterprise URL reviews to the CLI default host.

The root cause was loss of the normalized host at the provider API boundary. References now require:

```text
gh api --hostname <host>
gh api graphql --hostname <host>
glab api --hostname <host>
```

Post-fix simulations passed for:

- `https://github.enterprise.example/acme/widgets/pull/17`: metadata, diff, GraphQL threads, and POST all route to `github.enterprise.example`.
- `https://gitlab.example/acme/widgets/-/merge_requests/17`: metadata, versions, diffs, discussions, and POST all route to `gitlab.example`.

## Skill size and structure

The final skill is 484 words. It retains URL review, preview, full scope, dedupe, stale-head handling, no-findings behavior, non-inline choice, provider writes, and stage boundaries.

## Result

All required review scenarios pass. No reply/resolve operations were added before the `/pr-fix` RED baseline.
