# Workflow Language Propagation Design

## Purpose

Add a user-filled `language` field to `.workflow-config.json` so every new human-readable workflow artifact uses one repository-selected language. Empty or absent `language` preserves current behavior.

## Configuration

`/issue-init` remains the only skill that creates the flat configuration. It adds:

```json
"language": ""
```

The field sits after `self-reviewed` and before `remarks`. Its value is a free-text language name such as `简体中文` or `English`; trim surrounding whitespace. A non-string value stops the relevant stage. Empty or absent means no language constraint.

## Language Resolution

`/issue-init` reads the local repository-root configuration because it creates or links the issue before a normalized PR/MR target exists. It returns the normalized `textLanguage` handoff leaf without copying opaque input.

Target stages resolve the field independently from the normalized target repository's remote base ref through the selected provider, alongside existing base-config resolution. They bind provider, host, repository, base ref, and config blob SHA. PR/MR heads, forks, local worktrees, envelopes, and user prose never override the remote value. If a remote language is non-empty, it supersedes prior handoff language for the next generated text; if empty or absent, current behavior remains. Existing remote text is never translated or rewritten.

## Covered Content

A non-empty language applies to every newly generated human-readable external or Git artifact:

- issue title and body;
- workflow-generated commit subject and body, including `/issue-executing` output and `/pr-fix` completion commits;
- PR/MR title and body;
- review finding titles, explanations, provider comments, replies, and deferral reasons;
- generated merge or issue-close messages when a provider write supports a body.

Generated text must be entirely in the configured language, except for exact quotations and code identifiers that must retain their source spelling. Branch names remain ASCII English-meaning slugs. SHA values, URLs, JSON leaf names, provider API values, machine-readable attestation markers, and the fixed `neil-self-reviewed/v1` payload remain exact protocol data rather than prose.

## Stage Ownership

`/issue-init` creates the field and applies its local value to issue writes. `/issue-executing` applies handed-off language to any commit it produces. `/pr-create`, `/pr-review`, `/pr-fix`, `/pr-merge`, and `/issue-close` resolve the remote target-base value before producing text or performing a text-bearing write. `/using-neil-workflows` only validates and forwards `textLanguage`; it never translates text or performs provider/Git business operations.

A stage that re-resolves a changed remote language uses the new value only for its next new artifact. Its normal stale-state, remote authorization, merge, and cleanup safeguards remain unchanged.

## Validation

Scenarios must cover the exact default object/order; local issue creation in a configured language; remote base language overriding local/head/fork language; empty/absent compatibility; each generated artifact category; quoted identifiers and machine protocols remaining unchanged; and changed remote language affecting only later text. Verify JSON equality, skill word caps, structural scans, and `git diff --check`. The user requested no executable test-suite run for this change.
