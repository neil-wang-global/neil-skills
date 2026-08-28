# pr-create verification

Fresh agents used `pr-create` plus the creation-only shared/provider references. All operations were simulated.

## Core scenarios

| Scenario | Result | Evidence |
|---|---|---|
| A: no config | PASS | No config write; `main`; ready; non-closing issue link |
| B: configured draft and closing | PASS | Draft flag plus provider closing relationship |
| C: existing PR/MR | PASS | Existing open target returned unchanged |
| D: branch mismatch | PASS | Explicit issue number requested; no guess/write |
| E: independent stage | PASS | `/pr-review` reported but not invoked |

### Scenario A representative response

> Do not create or modify `.workflow-config.json`; apply defaults in memory. Target `main`, create a ready PR/MR, and relate issue #42 without a closing keyword. GitHub uses `Related to #42`; GitLab omits `--related-issue` and uses the same non-closing description reference. Opening never closes the issue. `/pr-review` is offered but not invoked.

### Scenario B representative response

> With `pr-draft:true`, create using `--draft`. With `pr-auto-close-issue:true`, include the provider-supported closing reference. Opening does not close the issue; an eligible merge does.

### Scenario C representative response

> Return existing PR #81 or MR !81 unchanged and stop. Do not create, edit, change config, review, merge, close an issue, or delete a branch.

## Default wording micro-tests

Five fresh agents repeated Scenario A:

| Run | No config write | `main` | Ready | Non-closing link | No auto review |
|---:|:---:|:---:|:---:|:---:|:---:|
| 1 | PASS | PASS | PASS | PASS | PASS |
| 2 | PASS | PASS | PASS | PASS | PASS |
| 3 | PASS | PASS | PASS | PASS | PASS |
| 4 | PASS | PASS | PASS | PASS | PASS |
| 5 | PASS | PASS | PASS | PASS | PASS |

This changes the RED distribution from 5/5 failures to 5/5 passes.

## Provider variations

| Provider scenario | Result | Evidence |
|---|---|---|
| GitHub default | PASS | `Related to #42`, no closing keyword |
| GitHub configured | PASS | `--draft` and `Closes #42` |
| GitHub existing | PASS | Existing PR returned unchanged |
| GitLab default | PASS | No `--related-issue`; ready; non-closing description |
| GitLab configured | PASS | `--draft`, `--related-issue`, provider closing relationship |
| GitLab existing | PASS | Existing MR returned unchanged |

## Refactor verification

The final skill is 500 words after fork-aware base/head routing. Post-refactor checks passed:

- Scenario A: no config creation, `main`, ready, `Related to #42`, no close, no review invocation.
- Existing GitLab MR: no create, edit, config write, or review.

## Result

All required creation behaviors pass without adding review/fix APIs before their RED baselines.

## Cross-skill verification

Flows A and C passed: defaults create a ready, non-closing PR/MR without writing config. The skill reports `/pr-review` but never invokes it; no public stage chains automatically.

## Independent-review regression

Scenario F passed: default GitLab creation omits `--related-issue` and uses only `Related to #42`; configured closing mode reserves `--related-issue` for a relationship that closes after eligible merge.

Scenario G passed: fork checkout resolves base/head separately, performs idempotency lookup with base branch plus qualified fork source (GitHub REST and GitLab project/source filters), creates on upstream, verifies pushed state in the fork, and asks when base identity is ambiguous.

Scenario H passed: organization-owned GitHub fork heads use host-routed REST `POST /pulls` with explicit base/head and draft boolean; unsupported owner-qualified `gh pr create` is not used.
