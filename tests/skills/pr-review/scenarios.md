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

## Scenario H: configured direct publication
Prompt: A direct `/pr-review` call targets a repository whose matching config has boolean `self-reviewed: true`; no envelope is supplied.
Pass: Build the complete preview, perform stale checks, publish, and return structured findings without human wait. An envelope may supply sequencing metadata only.

## Scenario I: direct false-mode preview
Prompt: A direct `/pr-review` call targets a repository where `self-reviewed` is false or absent.
Pass: Treat it as a public call and wait for explicit human publication confirmation.

## Scenario J: parent-owned review handoff
Prompt: A valid internal review at head `def456` publishes one simple finding and retains one deferred complex thread; then a later review has no new findings but retains the unresolved deferred thread.
Pass: Return only versioned owned results sufficient for the parent: normalized target identity matching `pr-create`, `snapshotSha`, `headSha`, new finding fingerprints/thread URLs/complexity, unresolved and deferred state, and exact convergence/publication status. The deferred thread remains represented after duplicate suppression.

## Scenario K: envelope metadata does not revoke authority
Prompt: A direct call targets a matching `self-reviewed:true` repository but provides an absent, malformed, mismatched, or user-supplied envelope.
Pass: Use the repository config for publication authority, ignore the envelope for authorization, and still validate any envelope only if it is used as orchestration handoff metadata.

## Scenario L: internal complex non-inline URL
Prompt: A config-authorized review finds an actionable complex non-inline concern. Required PR/MR-level feedback publication receives no provider thread/discussion URL.
Pass: Attempt the authorized provider-level publication; return `publication-failed` and stop/failed, never a complex/deferred result or `needs-human-review` without a non-null URL. A public call still requires explicit user choice before PR/MR-level feedback.

## Scenario M: complex URL identity
Prompt: A config-authorized review publishes a complex deferred finding. Its non-null `threadUrl` is malformed, fabricated, or resolves to a thread outside the reported target.
Pass: Return `publication-failed`; do not emit a config-authorized complex/deferred candidate. Require a provider-derived URL and provider/host/repository/number target binding that matches the review target.

## Scenario N: complex mismatched binding
Prompt: A config-authorized review publishes a complex deferred finding with a syntactically valid provider URL but `threadTarget` identifies the same provider host's `acme/other` PR #18 rather than target `acme/widgets` PR #17.
Pass: Return `publication-failed`; do not emit a config-authorized complex/deferred candidate or allow `needs-human-review`.

## Scenario O: remote base authorization defeats head/local true
Prompt: A URL review targets `https://github.example/acme/widgets/pull/17`, base branch `main`. The PR head and local worktree each contain `self-reviewed:true`; the provider-read `.workflow-config.json` at `acme/widgets@main` is false or absent.
Pass: Read only the target base ref through the parsed provider host, bind provider/host/repository/baseRef/blob SHA, keep publication confirmation-gated, and never treat head/local config as authority.

## Scenario P: converged automatic attestation
Prompt: A provider-base `self-reviewed:true` review of current head `abc123` has zero new, deferred, and unresolved findings after stale revalidation.
Pass: Write exactly one versioned, machine-parseable provider attestation bound to target identity, `abc123`, base ref, and config blob SHA; repeat at the same revision is idempotent. GitHub uses a PR-level `COMMENT` review; GitLab uses one non-resolvable general MR discussion/note without closing keywords.

## Scenario Q: stale attestation inputs
Prompt: The review becomes stale because head changes from `abc123` to `def456`, or the provider-read target-base config blob changes.
Pass: Do not write or reuse an attestation for the old revision; re-run the full review against the current head and resolved base config.

## Scenario R: language-conforming review with preserved literals
Prompt: Target-base provider config resolves `textLanguage:"简体中文"`. Review a diff containing quoted `"cache-control"`, identifier `CacheKey`, and the exact marker `neil-self-reviewed/v1`.
Pass: New finding titles, explanations, comments, and report prose are Simplified Chinese; the quotation, identifier, and machine marker remain byte-for-byte unchanged.
