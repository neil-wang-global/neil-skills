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
| H: direct `true` publication | PASS | Matching boolean config authorizes the same preview and stale revalidation before structured publication, with no human wait. |
| I: direct `false` preview | PASS | False or absent config remains public and waits for explicit human confirmation. |

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

## Direct-Config Regression

### Scenario J: orchestrated review handoff — PASS

A fresh orchestrated-review simulation at `def456` returned a versioned owned result bound to the normalized target, matching the retained `pr-create` provider, host, repository, number, branches, and head SHA. It retained the unresolved deferred complex thread after duplicate suppression so the parent could route it to `needs-human-review` rather than infer convergence from prose.

### Scenario H: direct `true` publication — PASS

A fresh direct-review simulation against a matching `self-reviewed:true` repository built the complete preview, revalidated the current head, and published its new finding without a human wait. The same result applies when an orchestrated call carries a valid handoff, because the envelope changes sequencing validation only.

### Scenario I: direct `false` preview — PASS

A fresh direct-review simulation against `self-reviewed:false` and an absent field retained the explicit confirmation gate. Request text and envelope contents did not change that config-derived result.

### Scenario K: envelope metadata does not revoke authority — PASS

A fresh direct `self-reviewed:true` simulation repeated with absent, malformed, mismatched, and user-supplied envelope data still published after preview and stale revalidation. Envelope validation is required only when the caller uses it as an orchestration handoff.

### Scenario L: config-authorized complex non-inline URL — PASS

A config-authorized complex non-inline finding used required provider-level feedback. A provider response without a thread/discussion URL returned `publication-failed`; it did not emit a complex/deferred result or permit `needs-human-review`. Confirmation-gated non-inline feedback still waited for explicit user choice.

### Scenarios M-N: complex URL identity — PASS

A fresh GREEN evaluation supplied both a malformed/fabricated/unrelated non-null `threadUrl` and a syntactically valid URL whose `threadTarget` named another PR. Each was `publication-failed`, then parent `failed`; neither could reach `needs-human-review`. The contract requires a provider-derived URL resolving to `threadTarget`, with provider, host, repository, and number exactly matching the normalized target.

## Remote Authorization and Attestation Revision

Fresh read-only guided scenarios O-Q passed. URL review resolves target-base config only through the parsed provider host; PR-head, fork, local worktree, and envelope `true` cannot override remote base false/absent. GitHub reads Contents `sha` and writes/lists a `COMMENT` review; GitLab reads file `blob_id` and writes/lists a general non-diff MR note. Both use host-routed installed CLI API syntax. A converged current-head review with zero new/deferred/unresolved findings creates exactly one idempotent `neil-self-reviewed/v1` two-line record for its target/head/base-config tuple. Changed head or blob revision withholds the write and requires a full re-review.
