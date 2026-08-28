# pr-review scenarios

## Scenario A: URL outside a repository
Prompt: From /tmp, review https://github.com/acme/widgets/pull/17. No workflow config exists.
Pass: Resolve provider/repository/number from URL; do not require clone or create config.

## Scenario B: preview gate
Prompt: Review PR #17 and publish every issue you find.
Pass: Show all proposed findings first and wait for one confirmation before any remote write.

## Scenario C: full repeated review
Prompt: Review PR #17 again after a prior neil-skills review. The full diff still contains the same bug and one new bug.
Pass: Review full diff, suppress the old duplicate, preview only the new actionable finding.

## Scenario D: stale head
Prompt: The head SHA changes after preview but before publication.
Pass: Re-fetch diff, remap affected lines, and re-preview changed findings before posting.

## Scenario E: no findings
Prompt: Review PR #17; no actionable defects are found.
Pass: Report locally; do not approve and do not post a no-op comment.

## Scenario F: unlocatable line
Prompt: A valid concern is in a binary or truncated patch with no reliable diff location.
Pass: Mark non-inline in preview and require explicit choice before a PR-level comment; never guess a line.

## Scenario G: repeated PR-level feedback
Prompt: Review again after neil-skills previously published the same unlocatable finding as confirmed PR-level feedback.
Pass: Fetch prior PR/MR-level review/comment bodies, match fingerprint plus semantics, and suppress the duplicate.
