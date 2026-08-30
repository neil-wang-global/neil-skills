# RED baseline: no `/using-neil-workflows` skill

Three fresh control agents received only the scenario prompts. They were not given coordinator guidance. Their outputs were evaluated against `scenarios.md`.

## Observed failures

| Cases | Baseline result | Failure against contract |
| --- | --- | --- |
| A-E | Partially followed stage intent. | No `neil-workflow/v1` envelope, no validated-handoff shape, and used nonterminal states. |
| F-J | Partially followed stop rules. | Added unapproved `intake/validation`, `review fingerprint comparison`, and `fix-evidence validation` stages instead of dispatching only named stages with owned envelope validation in the parent. |
| K-O | Recognized merge/close ordering. | Used disallowed terminal states and proposed unbounded polling/helper dispatches rather than a parent progress ledger and one sequential merge stage. |

## Verbatim failure excerpts

> **Terminal state:** `awaiting-issue-init-result`.

`awaiting-issue-init-result` is not one of the permitted terminal states: `complete`, `success`, `needs-human-review`, `merge-blocked`, `stalled`, or `failed`.

> **Terminal state:** `pr-created`, with no automated review/fix/merge continuation.

`pr-created` is a stage observation, not an allowed terminal state. The false path must end after `pr-create` with an allowed report state.

> Dispatch `intake/validation` then review classification.

The coordinator must validate handoffs itself and dispatch only fresh named workflow stages. This invented stage makes ordering nondeterministic and violates the parent-only contract.

> Dispatch `wait-for-merged-state`. Poll or receive authoritative merge status until the PR is actually merged.

`wait-for-merged-state` is an invented side-effecting/helper stage. The coordinator must retain the merge handoff in its ledger and report a permitted state until the existing merge stage proves merged.

> Terminal state: `awaiting-merge`; after proof and closure validation: `closed`.

Neither `awaiting-merge` nor `closed` is allowed. Pending merge proof must stop as `stalled`; a valid fully closed workflow may be `success` only after all required proofs.

> subject to normal retry limits.

No retry policy, bounded loop rule, progress predicate, or repeated-fingerprint protection was defined. The requested coordinator must stop on no progress or a repeated deferred/accepted fingerprint.

## Baseline conclusion

The controls could recognize several high-level gates, but none produced the complete owned envelope, ledger, terminal-state vocabulary, or stage-only dispatch discipline. The baseline therefore fails A-O as a reusable coordinator contract.
