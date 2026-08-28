# RED Baseline: Current `/issue-close`

Fresh-agent simulation: the evaluator read only the pre-Task-5 `skills/issue-close/SKILL.md` and applied it to [the six closure scenarios](scenarios.md). It did not receive the Task 5 brief or post-merge guidance.

| Scenario | Baseline result | Evidence in current skill |
| --- | --- | --- |
| A. Reject unproven invocation | Fails: no envelope, handoff, or merged-state validation; config/current-branch flow proceeds to remote close. | Lines 12, 52, 71 |
| B. Accept validated handoff | Fails as an orchestrated call: ordinary cleanup overlaps, but it ignores supplied identity and has no provider-backed merge proof or structured result. | Lines 58-60, 78, 99-102 |
| C. Already-closed issue | Partly passes: already closed is a no-op, but identity/result contract is absent. | Line 74 |
| D. Dirty cleanup | Fails: explicitly asks whether to discard changes, allowing destructive cleanup. | Line 60 |
| E. Limit cleanup | Partly passes: it forbids unrelated/occupied/remote branch deletion, but derives ownership from current branch rather than explicit handoff. | Lines 78, 92-95, 118 |
| F. Structured leaf state | Fails: output is only a human-facing report. | Lines 106-111 |

## Baseline rationale, verbatim

> “It would not validate the caller, envelope, PR/MR identity, or merged state. It directs the agent to read repository config, derive an issue number from the current branch, then continue cleanup and close the remote issue.”

> “When the worktree is dirty, ask the user whether to discard its changes or abort.”

> “The skill requires no JSON output, owned leaves, action/state fields, untouched-leaf reporting, or restrictions against including live runtime objects.”

The baseline confirms that the existing direct `/issue-close` flow cannot safely serve a parent-orchestrated post-merge handoff without a distinct, fail-closed contract.
