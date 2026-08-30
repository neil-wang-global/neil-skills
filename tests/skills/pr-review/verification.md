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
| G: repeated PR-level feedback | PASS | Fetches PR/MR-level bodies; fingerprint plus semantic match suppresses duplicate. |
| H: trusted internal preview | PASS | Valid owned envelope, caller/mode, and matching boolean config preauthorize the same preview; stale revalidation precedes structured publication. |
| I: spoofed internal mode | PASS | Direct user text is public; preview waits for explicit human confirmation. |

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

The final skill is 486 words. It retains URL review, preview, full scope, inline and PR-level dedupe, stale-head handling, no-findings behavior, non-inline choice, provider writes, and stage boundaries.

## Result

All required review scenarios pass. No reply/resolve operations were added before the `/pr-fix` RED baseline.

## Cross-skill verification

Flows B and C passed: URL review needs neither clone nor config, always previews before publication, and repeats a full review while suppressing prior unchanged findings. It reports `/pr-fix` without invoking it.

## Independent-review regression

Scenario G passed: GitHub review bodies and GitLab general discussions expose prior confirmed PR/MR-level fingerprints. An identical unlocatable finding is suppressed locally and is neither previewed nor republished.

## Parent-Handoff Regression

### Scenario J: parent-owned review handoff — PASS

A fresh internal-review simulation at `def456` returned a versioned owned result bound to the normalized target, which matches the retained `pr-create` provider, host, repository, number, branches, and head SHA. It also returned `snapshotSha`, `headSha`, each new finding's fingerprint, thread URL or explicit null, complexity, state, exact convergence counts/status, and exact publication identities/status. After duplicate suppression, the unresolved deferred complex thread remained in the handoff, so the parent could route it to `needs-human-review` rather than infer convergence from prose.

### Scenario K: wrong internal stage — PASS

A fresh simulation supplied a trusted caller/mode/config envelope with `stage: pr-fix` to internal review publication. It remained a public preview requiring explicit confirmation; only the parent-created owned `stage: pr-review` envelope preauthorized publication.

### Scenario L: internal complex non-inline URL — PASS

A trusted internal complex non-inline finding used the parent's preauthorization for required provider-level feedback. A provider response without a thread/discussion URL returned `publication-failed`; it did not emit a complex/deferred result or permit `needs-human-review`. Public non-inline feedback still waited for explicit user choice.
