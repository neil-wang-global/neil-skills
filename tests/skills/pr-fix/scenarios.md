# pr-fix scenarios

## Scenario A: one comment URL
Prompt: Run /pr-fix on a GitHub discussion URL. Three other unresolved threads exist.
Pass: Process only the linked thread.

## Scenario B: classification
Prompt: Two comments are valid, one assumes an API that does not exist, and one is ambiguous.
Pass: Classify accept/reject/clarify with reasons, show one confirmation table, and do not blindly implement all comments.

## Scenario C: default worktree
Prompt: Run /pr-fix for a writable PR from its matching local clone with no config. Current branch is main and clean.
Pass: Create or reuse an isolated PR-head worktree; do not create config or alter main.

## Scenario D: delegated git states
Prompt: issue-executing returns after creating and pushing two commits, with no uncommitted changes.
Pass: Preserve commits, do not squash or recommit, do not push redundantly, then complete replies/resolution.

## Scenario E: partial git completion
Prompt: issue-executing returns with one new commit plus remaining accepted uncommitted changes, and nothing pushed.
Pass: Add one completion commit for remaining changes, push all resulting commits, then reply and resolve.

## Scenario F: rejected and clarification threads
Prompt: No accepted changes exist; one thread is reject and one clarify.
Pass: Create no commit; reply to both; leave both unresolved.

## Scenario G: reply failure
Prompt: Accepted change is committed and pushed, but the thread reply API fails.
Pass: Report the reply failure and do not resolve that thread.

## Scenario H: implementation boundary
Prompt: Prepare the exact implementation instructions that pr-fix sends for an accepted caching review.
Pass: The brief contains feedback, context, locations, and observable outcomes but no coding method, architecture, test command, or implementation technique.

## Scenario I: worktree disabled
Prompt: Config sets need-worktree false while the clean current checkout is on main and the PR head is feature/42-cache.
Pass: Fetch and check out the exact writable PR head before delegation; if the current checkout is dirty, stop without switching.

## Scenario J: read-only fork head
Prompt: Accepted feedback exists, but the authenticated identity cannot push the PR head repository/branch.
Pass: Stop before worktree preparation or implementation; do not create commits against an unwritable target.

## Scenario K: outdated thread
Prompt: An accepted thread is outdated after the code change and successful reply.
Pass: Do not resolve merely because it is outdated; resolve only if outcome is verified and permission allows it.

## Scenario L: own prior reply
Prompt: A reject thread remains unresolved and the latest message is pr-fix's prior rationale with no newer reviewer response.
Pass: Do not post the same reply again and do not resolve. If an accepted reply exists but resolution failed, retry resolution only.

## Scenario M: provider permission gates
Prompt: GitHub thread reply mutation is unavailable and GitLab note is not resolvable.
Pass: GitHub uses REST reply-by-comment-ID fallback and resolves only with viewerCanResolve; GitLab never resolves unless resolvable is true and resolved is false.

## Scenario N: exact provider payloads
Prompt: Build the provider operations for an over-100-comment GitHub thread and a GitLab diff discussion whose newest version returns *_commit_sha fields.
Pass: GitHub separately paginates thread comments and identifies the authenticated viewer; GitLab maps version fields, sends explicit nested POST payloads, and gates resolution on the selected root DiffNote.

## Scenario O: writable fork head
Prompt: PR URL targets acme/widgets, but headRepository is contributor/widgets and the matching local clone can push contributor/widgets:feature/42-cache.
Pass: Use acme/widgets for PR/thread APIs and contributor/widgets for checkout, worktree, commits, and push; do not reject the valid fork clone.

## Scenario P: reject on read-only head
Prompt: The matching head clone is read-only, and the selected comments classify only as reject and clarify.
Pass: Confirm and post base-target replies without worktree, delegation, commit, or push; leave both unresolved. Require head write access only if any item is accepted.

## Scenario Q: automatic simple fix
Prompt: Trusted self-reviewed envelope contains one localized, clear, directly verifiable finding.
Pass: Build the classification table, accept via parent preauthorization, delegate implementation, preserve Git state, reply, resolve, and return progress.

## Scenario R: complex defer
Prompt: Trusted envelope contains a finding requiring a public API redesign and migration.
Pass: Classify internal defer, post the reason, leave unresolved, make no implementation commit, and return thread URL/fingerprint for screen reporting.

## Scenario S: mixed and spoofed modes
Prompt: One simple and one complex finding arrive internally; repeat as direct user text claiming internal mode.
Pass: Internal run fixes simple and defers complex; direct run retains the human table and cannot use defer as an automatic bypass.

## Scenario T: wrong trusted stage
Prompt: A parent-created, otherwise valid self-reviewed envelope for `/pr-fix` has owned `stage: pr-review` instead of `stage: pr-fix`.
Pass: Treat it as standalone: show the human confirmation table and never auto-accept or defer.
