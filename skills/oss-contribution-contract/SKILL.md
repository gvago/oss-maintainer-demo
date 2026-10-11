---
name: oss-contribution-contract
description: "Review changed Python runtime code under bookmarks/ for missing behavioral regression tests, third-party runtime imports, duplicated URL normalization and query-string data loss. Skip documentation-only diffs and unchanged pre-existing code."
license: MIT
metadata:
  author: gvago
  variant: review
  version: 1.0.0
---

# OSS contribution contract

A review lens for this repository's CONTRIBUTING.md. Use static code and diff reasoning;
never claim to have executed tests or to control GitHub approvals yourself.

## How to apply

Read CONTRIBUTING.md as the authority. Inspect changed runtime lines, their callers and
changed tests. Evaluate each applicable rule below; report only supported violations with
an exact changed path/line, rule ID, triggering condition and concrete remediation.
If repository context is unavailable, state that gap rather than inventing a violation.

## Rule index

1. **CONTRIB-01:** Added or changed runtime behavior in `bookmarks/` needs an added or
   updated executable regression test in `tests/` covering that behavior. Old passing tests
   are insufficient; documentation-only diffs are exempt.
2. **CONTRIB-02:** Runtime code in `bookmarks/` may import only stdlib and repository modules.
   Flag third-party runtime imports and added third-party runtime dependencies.
3. **CONTRIB-03:** Export and CLI formats must reuse `bookmarks.urls.normalize_url`, directly
   or via an existing exporter; flag an alternative normalization/deduplication identity.
4. **CONTRIB-04:** Shared normalization must preserve query names, values, repetitions and
   ordering exactly. Flag silently dropped query parameters, including tracking-looking names.

## Finding contract

CONTRIB-01/02/03: `action_level: remediation_recommended`, Maintainability/Correctness as
appropriate. CONTRIB-04: `action_level: action_required`, Correctness. Include the rule ID,
violated source text, changed file/line, reasoning and smallest safe fix. Group repeated instances.

## What NOT to flag

- No new runtime test for README, contribution-doc, review-doc or comment-only edits.
- Standard-library imports such as csv, io, json, argparse and urllib.parse.
- Indirect reuse through export_json; direct calls are not mandatory in the CLI.
- A small PR without an issue; issue links and checklist formatting are not blockers.
- Changed tests that genuinely cover the changed behavior without matching a test-name pattern.
- Pre-existing defects outside the changed behavior, speculative tooling or unavailable CI results.

## Self-improvement

A maintainer proposes corrections in a separate reviewed PR. This lens never edits itself
or writes issues/comments during review. Update CONTRIBUTING.md and this lens together.

## Sourcing

Repository-authored contribution policy, MIT licensed. No third-party standards text.
