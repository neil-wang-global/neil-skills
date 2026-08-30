# pr-review baseline

Fresh agents received no `pr-review` guidance. Simulations performed no remote writes.

## Core scenarios

| Scenario | Result | Observed behavior |
|---|---|---|
| A: URL outside repository | FAIL | URL parsed, but clone described as required for file-level review |
| B: preview gate | Mixed | Core sample waited; repeated controls published immediately |
| C: repeated full review | PASS | Full scope, old duplicate suppressed, new bug previewed |
| D: stale head | PASS | Head re-read, affected findings remapped and re-previewed |
| E: no findings | FAIL | Automatically approved |
| F: unlocatable line | FAIL | Avoided guessing, but posted PR-level feedback without explicit choice |

## Representative failures

### Remote URL

> A clone is required for a local, file-level review; the URL supplies host, repository, and PR number.

The requested contract allows API-based review from any directory without a clone.

### Preview gate

> Publish immediately. “Review and publish every issue” is explicit authorization, so a draft-and-wait step would be redundant.

### No findings

> Approve. With no actionable defects, I would not post a no-op comment.

### Unlocatable finding

> I would not guess a line. I would post PR-level feedback. No additional confirmation is required solely because the patch lacks a line anchor.

## Preview wording controls

Five fresh controls plus the core sample produced:

| Behavior | Count |
|---|---:|
| Wait for one confirmation | 1 |
| Publish immediately | 5 |

The preview gate requires explicit skill guidance.

## Deduplication controls

Five fresh controls plus the core sample converged:

- Scope: full review.
- Old bug: recognized but no duplicate comment.
- Preview: one new finding only.

Deduplication is already intuitive but still needs a stable fingerprint contract for remote idempotency.

## RED conclusion

Minimal guidance must enforce:

1. Full URL review without local clone or config creation.
2. One complete preview and confirmation before every remote write, even when the user says publish.
3. Full-scope repeated review with fingerprint plus semantic deduplication.
4. Head/diff revalidation immediately before publication.
5. No automatic approval or no-op comment when findings are empty.
6. Explicit user choice before converting an unlocatable finding to PR-level feedback.

## Independent-review RED regression

A final reviewer found:

> GitHub history fetches only inline review threads, so a prior PR-level review body and its hidden fingerprint are invisible on the next run.

This became Scenario G before provider history guidance was changed.

## Direct-config RED regression

Fresh no-guidance simulations produced automatic publication for both direct configurations:

| Scenario | Result | Observed behavior |
|---|---|---|
| H: direct `true` | Mixed | Unguided agent published after a config assertion; the prior skill instead blocked on its universal confirmation gate. |
| I: direct `false` | FAIL | Unguided agent treated a request to publish as sufficient and did not preserve the confirmation gate. |

### Exact no-guidance outputs

H:

> Yes. The matching repository config, complete preview, and passing stale-head validation authorize publication without an additional human confirmation.

I:

> Yes. Publish the completed review without waiting for separate human confirmation.

### Current-skill H control

> No. “Show one complete preview and wait for explicit confirmation before any remote write, even when the initial request says publish.”

The gate needs a config-authorized conditional: direct `self-reviewed:true` publishes only after the complete preview and stale-head revalidation; direct `false` or absent remains confirmation-gated. Envelope data is handoff metadata only and does not affect either result.

## RED revision: untrusted config and missing durable evidence

A fresh un-guided security simulation answered that head/local `self-reviewed:true` cannot authorize automation when target-base config is unknown, and that user prose cannot prove a converged review. It also identified provider-specific uncertainty around treating free-form comments as evidence. Before this revision, the skill only said “matching target-repository config,” so it did not require a remote base-ref read, blob binding, or versioned provider record. Scenarios O-Q therefore fail against the prior contract.
