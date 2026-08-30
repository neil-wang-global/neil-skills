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

The final skill is 500 words and retains selectors, both worktree paths, fork-head identity, neutral delegation, Git-state reconciliation, reply idempotency, and permission-gated thread completion.

## Result

All required fix scenarios pass. The skill contains no code implementation recipe, architecture prescription, or project test-command prompt.

## Cross-skill verification

Flows B and C passed: a writable head-repository clone and default worktree are required; existing delegated commits/pushes are preserved; accepted replies gate resolution; reject/clarify replies remain unresolved. This is the only verified internal delegation: `pr-fix` to `issue-executing`.

## Independent-review regressions

Successive independent reviewers identified missing approved edge contracts. Guided reruns passed:

| Scenario | Result | Evidence |
|---|---|---|
| I: worktree disabled | PASS | Clean checkout fetches/checks out exact head; dirty checkout stops |
| J: read-only fork | PASS | Stops before worktree, delegation, commit, or push |
| K: outdated thread | PASS | Outdated alone never resolves; outcome and permissions still gate |
| L: own prior reply | PASS | No duplicate reply; resolution-only retry preserves reply |
| M: provider gates | PASS | GitHub REST fallback; GitLab `resolvable`/`resolved` checks |
| N: exact payloads | PASS | GitHub two-stage cursors/viewer; GitLab SHA mapping/nested writes/root note |
| O: writable fork head | PASS | Base repo owns APIs; writable head repo owns checkout/commit/push |
| P: read-only reject/clarify | PASS | Base replies proceed without worktree/Git; accepted path requires write |

The GitHub GraphQL reference now includes pageable thread fields, `viewerCanReply`, `viewerCanResolve`, viewer identity, independent per-thread comment cursors, and executable command wrappers. The GitLab reference maps version response fields, uses explicit methods/nested payloads, and reads resolution gates from the selected root note. Both compare the authenticated author's latest equivalent reply with later reviewer messages before posting.

## Config-Authorized Fix GREEN

Fresh read-only simulations used the current skill, shared contract, provider references, and scenarios. The final A-T sweep passed with no contradictions.

| Scenario | Result | Evidence |
|---|---|---|
| Q: direct `true` simple fix | PASS | Matching config permits only a localized, clear, directly verifiable auto-accept; it builds a table, delegates, inspects Git state, replies, permission-gates resolution, and returns progress fields. |
| R: direct `true` complex defer | PASS | Public-interface redesign/migration is `defer`: a concise reason is posted, the thread remains unresolved, URL/fingerprint return, and no worktree/delegation/commit/push occurs. |
| S: direct true/false modes | PASS | Direct `true` simple/complex findings auto-accept/defer respectively; direct false/absent calls wait for the human `accept`/`reject`/`clarify` table and cannot use `defer`. |
| T: malformed orchestrated envelope | PASS | An attempted orchestrated dispatch with malformed, mismatched, or user-supplied envelope/handoff data fails before classification or remote write; remote-base true does not downgrade that failed dispatch to manual/direct mode. A real direct invocation remains config-authorized by its independently resolved remote target-base value. |

The A-P regressions also passed. In particular, provider references cover GitHub REST reply fallback, permissions, comment pagination, and viewer identity; GitLab SHA mapping, nested payloads, and root-note resolution gates. The final `pr-fix` skill retains no implementation recipe, architecture prescription, or project test command.

## Authorization-Change Regression

Fresh guided Scenario V tested initial literal remote-base `self-reviewed:true` at blob `A`, followed immediately before each boundary by false, malformed/unreadable config, or literal true at blob `B`. Before accepted-work delegation/Git remote write and each provider defer reply, accepted reply, and resolution, all three changed results stopped that exact action as `authorization-changed`, reported it, and preserved earlier completed actions. A true blob `B` was not treated as a replacement authorization for blob `A`; no boundary reused stale true. At that revision, the skill was 499 words.

## Authorization-Mode Regression

A fresh read-only evaluation passed both authorization modes. For an initial remote-base false/absent run, the displayed `accept`/`reject`/`clarify` table received its required confirmation, then fresh false/absent reads before delegation, completion commit/push, reply, and resolution did not reject those confirmed actions. Current target identity, stale-state, and provider authentication/authorization checks remained required. For an initial literal true blob `A` run, a fresh false, malformed/unreadable result, or changed blob `B` stopped each named automated side effect as `authorization-changed`; Scenarios V and W retain the provider-write and post-delegation completion coverage.

## Fresh Language Regression

Scenario Y passed in both authorization modes: target-base `textLanguage:"简体中文"` was freshly resolved immediately before accepted-work delegation and included in its implementation-neutral brief. The classification rationale, completion commit subject/body, accepted reply, and automated defer reply were all Simplified Chinese, while quoted reviewer text, identifiers, URLs, and machine markers remained unchanged.
