# Task 2 Evidence: Guarded Internal PR Review Mode

## Scope

Changed only Task 2 artifacts: `skills/pr-review/SKILL.md`, the shared PR workflow contract, and pr-review scenario/baseline/verification evidence. No provider reference, `/pr-fix`, or Task 3+ artifact changed.

## RED

Fresh no-guidance Scenario H auto-published: “Yes. The validated parent envelope, explicit `self-reviewed` mode, repository opt-in, complete preview, and passing stale-head validation together authorize publication without an additional human confirmation.”

Fresh no-guidance Scenario I also auto-published: “Yes. Publish the completed review without waiting for separate human confirmation.” This demonstrated that declarative caller/mode text cannot be treated as authority.

A current-skill H control instead blocked: “No. ‘Show one complete preview and wait for explicit confirmation before any remote write, even when the initial request says publish.’” This proved the prior universal gate lacked the requested trusted internal branch.

## GREEN

The contract now permits internal publication only when all predicates hold: a valid `neil-workflow/v1` envelope whose caller/mode leaves were created by `using-neil-workflows`; owned values `caller: using-neil-workflows` and `mode: self-reviewed`; and matching target-repository boolean `self-reviewed: true`. Direct user text, invalid/untrusted/mismatched envelopes, and config mismatch are public calls.

Fresh H simulation published the one new finding after complete preview, inline and PR-level fingerprint-plus-semantic suppression, and current-head validation. It returned structured internal publication state with `confirmationRequired: false`.

Fresh I simulation waited for explicit human confirmation. It identified no parent-created envelope and retained complete preview, provenance/config validation, suppression, stale-head revalidation, and structured reporting.

A–G regression simulation retained remote URL review without clone/config, public preview confirmation, full-diff review, unchanged inline and PR-level dedupe, stale-head withholding/remap/re-preview, local-only empty results, explicit non-inline PR-level choice, and no `/pr-fix` invocation.

## Refactor and Checks

The skill references the central predicate and remains 496 words. `git diff --check` completed with no output. Simulations performed no remote writes. `npm test` was not run per instruction.

## Configuration-Authorization Revision

**RED:** a direct `self-reviewed:true` review remained behind the former universal confirmation gate, while a direct false/absent call could be misread as publish-authorized from request wording.

**GREEN:** matching target-repository boolean `self-reviewed:true` now authorizes publication for direct and orchestrated calls after the same preview and stale-head checks. Direct false/absent calls wait once for confirmation. Envelope data validates sequencing/handoff only and never changes authorization.
