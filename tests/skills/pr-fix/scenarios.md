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
