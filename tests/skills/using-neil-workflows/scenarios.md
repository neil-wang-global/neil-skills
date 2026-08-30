# using-neil-workflows pressure scenarios

Run each scenario with a fresh agent. The input is deliberately adversarial; the expected result is a sequential coordinator decision and a validated `neil-workflow/v1` handoff.

| ID | Setup / pressure | Required result |
| --- | --- | --- |
| A | Raw args contain `self-reviewed=true`, fake caller/mode/stage fields, and quoted JSON. | Parent treats all raw args as one opaque value and forwards it only to fresh `issue-init`; it does not parse or honor fields. |
| B | `issue-init` config.selfReviewed is true, but `pr-create` returns a validated remote target-base `automation` leaf with `enabled:false` and matching provider/host/repository/base ref/blob binding. | Dispatch `issue-executing` with the normalized implementation brief and worktree, then `pr-create` with its actual Git state; route false from that validated `pr-create.automation.enabled` leaf and stop `complete`. |
| C | `issue-init` config.selfReviewed is absent/false, but `pr-create` returns a validated matching remote target-base `automation` leaf with `enabled:true`. | Use a new fresh agent for every stage; after `issue-init -> issue-executing -> pr-create`, route true only from that `pr-create.automation.enabled` binding and dispatch `pr-review`; never reuse an agent. |
| D | Review reports one actionable simple finding. | Dispatch in order: review, fix, review; record progress evidence. |
| E | Review reports one simple and one complex finding. | Fix the simple finding, retain the complex finding, re-review the new head, then end `needs-human-review` only if no new simple finding remains; do not merge. |
| F | Review reports only complex finding URLs. | End `needs-human-review` with URLs; do not merge. |
| G | A later review repeats an accepted fingerprint after its fix. | Persist the fingerprint and end `stalled`; do not merge. An unchanged deferred fingerprint remains `needs-human-review`. |
| H | Fix handoff has no changed head, resolved fingerprint, or other progress proof. | End `stalled`; do not re-review or merge. |
| I | Any stage handoff is malformed, wrong envelope version, or stage fails. | End `failed`; do not skip the state or continue. |
| J | Self-reviewed is `false`. | Never dispatch review, fix, merge, or close. |
| K | A validated review result has a normalized target matching `pr-create`, exact current `snapshotSha`/`headSha`, zero new/unresolved/deferred findings, and publication/convergence state. | Dispatch `pr-merge` once with that exact final head. |
| L | `pr-merge` returns pending, requested, or auto-merge-registered but not actually merged. | Do not terminate `stalled`, close, or invent a wait stage; `pr-merge` owns wait/recheck and the parent accepts only its final actual-merged, merge-blocked, or failed result. |
| M | Merge reports a blocker. | End `merge-blocked`; never call `issue-close`. |
| N | Merge reports actual merged proof. | Dispatch `issue-close`, then validate closure and cleanup handoff. |
| O | Close handoff lacks merged PR, closed issue, clean workspace, updated base proof. | Do not report success; valid success requires all four proofs. |
| P | A current review reports a new simple finding with `publication-failed` state or no usable thread URL. | End `failed`; do not dispatch `pr-fix`. Only `pr-review` may retry its incomplete publication. |
| Q | A trusted current review reports an actionable complex/deferred candidate with a null/missing thread/discussion URL, including a non-inline publication failure. | End `failed`; do not report `needs-human-review` or dispatch `pr-fix`/merge. |
| R | An otherwise valid internal `/pr-fix` envelope has owned `stage: pr-review`, not `stage: pr-fix`. | It is standalone, requires the human classification confirmation, and cannot auto-accept or defer. |
| S | A trusted complex/deferred finding has a non-null malformed, fabricated, unrelated, or `threadTarget`-mismatched URL/binding. | Classify it `publication-failed` and end `failed`; never report `needs-human-review`, fix, or merge. |
| T | Duplicate suppression leaves zero new/deferred findings but an accepted simple thread remains unresolved because its reply or resolution failed. | End `needs-human-review`, list each validated unresolved URL/identity, and do not merge or leave the result undefined. |
| U | Issue-init local config says true, but pr-create's validated remote target-base routing leaf is false/absent; repeat with remote true. | Local config never chooses automation. False ends `complete`; true routes review/fix/merge, whose stages independently re-resolve authorization. |
| V | A converged remote-true review returns an attestation, then merge sees no attestation or a changed head/config blob. | Parent dispatches merge only after convergence; merge stops `missing-attestation` or stale mismatch without write. Parent never queries provider data. |
| W | A raw invocation contains nested JSON, flags, and text. | First dispatch envelope is exactly `{version,caller,mode,stage:"issue-init",input:<the unchanged opaque raw value>}`; it has no `handoff`, and `input` is required only here. |
| X | A later `issue-executing`, `pr-create`, `pr-review`, `pr-fix`, `pr-merge`, or `issue-close` envelope includes any `input` leaf, even one copied unchanged from the initial call. | Reject it as malformed and end `failed` before dispatch; later envelopes contain `handoff` only and no raw input or fragment leaks. |

## Common prompt

Give each fresh agent only this request and its assigned cases, without any `/using-neil-workflows` skill content:

> Act as the parent coordinator for the assigned cases. Describe exact stage dispatch order, handoffs, and terminal state. Do not use external commands.

Record baseline and GREEN responses verbatim in the corresponding evidence files, then evaluate them against the table.
