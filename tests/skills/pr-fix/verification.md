# pr-fix verification

Fresh agents used `pr-fix` and provider references. All operations were simulated.

## Core scenarios

| Scenario | Result | Evidence |
|---|---|---|
| A: one comment URL | PASS | Only containing thread selected |
| B: classification | PASS | Two accept, one reject, one clarify; one confirmation |
| C: default worktree | PASS | Isolated head worktree; no config/main mutation |
| D: delegated commits | PASS | Existing pushed commits preserved; no commit/push |
| E: partial Git state | PASS | One completion commit; all missing commits pushed |
| F: reject/clarify | PASS | Replies posted; no commit; both unresolved |
| G: reply failure | PASS | Git preserved; thread remains unresolved |
| H: neutral brief | PASS | Facts and outcomes only; no implementation/test guidance |

## Classification pressure

Five fresh repeats all classified two accepts, one reject, and one clarify; showed one confirmation; and allowed accepted work to proceed after confirmation without resolving reject/clarify threads.

## Git-state pressure

Five fresh repeats all preserved two already-pushed commits and performed no squash, amend, recommit, rebase, force-push, or redundant push. RED rewrote history in four of five repeats.

## Delegation-boundary pressure

Five fresh repeats produced only placeholders for accepted feedback, context, locations, outcomes, worktree, and target identifiers. None invented architecture, coding methods, algorithms, test cases, or test commands. RED failed all five repeats with detailed implementation recipes.

## Provider thread completion

| Provider | Result | Evidence |
|---|---|---|
| GitHub Enterprise | PASS | Comment database ID maps to one thread; host-routed GraphQL reply then resolve |
| Self-hosted GitLab | PASS | Note maps to one discussion; host-routed REST reply then conditional resolve |

Both variants leave accepted threads unresolved on reply failure. Reject and clarify threads always remain unresolved. Successful prior writes are retained and only incomplete remote operations are retried.

## Skill size

The final skill is 499 words and retains selectors, confirmation, worktree defaults, neutral delegation, actual Git-state reconciliation, and per-thread completion gates.

## Result

All required fix scenarios pass. The skill contains no code implementation recipe, architecture prescription, or project test-command prompt.
