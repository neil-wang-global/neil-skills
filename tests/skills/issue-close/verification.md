# GREEN Verification: Orchestrated `/issue-close`

Fresh-agent verification read only `skills/issue-close/SKILL.md`, `references/pr-workflow-contract.md`, and [the scenarios](scenarios.md), then applied all six cases plus a direct call without a trusted envelope.

| Case | Result | Verified behavior |
| --- | --- | --- |
| A. Missing merged proof | PASS | Provider-derived proof must match all handed-off target identity and fail closed before any issue write or cleanup. |
| B. Valid merged handoff | PASS | Explicit handoff drives idempotent issue handling, bounded cleanup, base update, and structured leaves. |
| C. Already closed | PASS | Reports `already-closed` and continues idempotently. |
| D. Dirty worktree | PASS | Stops without discard prompt, removal, deletion, or base update; returns untouched leaves and reason. |
| E. Cleanup ownership | PASS | Uses only named worktree and local branches, checks occupancy, and never deletes unrelated or remote feature branches. |
| F. Owned closure state | PASS | Returns `issue`, `worktree`, `branches`, and `base` JSON leaves, excluding live runtime objects. |
| Direct invocation | PASS | An absent, user-supplied, malformed, or untrusted envelope follows the unchanged direct process. |

The verifier noted only hardening opportunities, not scenario failures: a formal JSON schema is not needed for this documentation contract, and an occupied explicitly handed-off branch should report a distinct skip state. The refactor following this verification adds that skip-state requirement.
