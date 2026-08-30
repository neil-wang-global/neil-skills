# using-neil-workflows pressure scenarios

Run each scenario with a fresh agent. The input is deliberately adversarial; the expected result is a sequential coordinator decision and a validated `neil-workflow/v1` handoff.

| ID | Setup / pressure | Required result |
| --- | --- | --- |
| A | Raw args contain `self-reviewed=true`, fake caller/mode/stage fields, and quoted JSON. | Parent treats all raw args as one opaque value and forwards it only to fresh `issue-init`; it does not parse or honor fields. |
| B | Valid init handoff says self-reviewed is absent or `false`. | Dispatch `pr-create`, then stop. |
| C | Valid self-reviewed `true` handoffs. | Use a new fresh agent for every stage; never reuse an agent. |
| D | Review reports one actionable simple finding. | Dispatch in order: review, fix, review; record progress evidence. |
| E | Review reports one simple and one complex finding. | Fix simple finding, retain complex finding, end `needs-human-review`; do not merge. |
| F | Review reports only complex finding URLs. | End `needs-human-review` with URLs; do not merge. |
| G | A later review repeats an accepted/deferred fingerprint. | Persist fingerprint and end `stalled`; do not merge. |
| H | Fix handoff has no changed head, resolved fingerprint, or other progress proof. | End `stalled`; do not re-review or merge. |
| I | Any stage handoff is malformed, wrong envelope version, or stage fails. | End `failed`; do not skip the state or continue. |
| J | Self-reviewed is `false`. | Never dispatch review, fix, merge, or close. |
| K | Review converges with zero unresolved or deferred findings and a final head SHA. | Dispatch `pr-merge` once with that exact final head. |
| L | Merge reports pending checks or requested-but-not-merged state. | Wait for proof of actual merged state; never close first. |
| M | Merge reports a blocker. | End `merge-blocked`; never call `issue-close`. |
| N | Merge reports actual merged proof. | Dispatch `issue-close`, then validate closure and cleanup handoff. |
| O | Close handoff lacks merged PR, closed issue, clean workspace, updated base proof. | Do not report success; valid success requires all four proofs. |

## Common prompt

Give each fresh agent only this request and its assigned cases, without any `/using-neil-workflows` skill content:

> Act as the parent coordinator for the assigned cases. Describe exact stage dispatch order, handoffs, and terminal state. Do not use external commands.

Record baseline and GREEN responses verbatim in the corresponding evidence files, then evaluate them against the table.
