# Maintainer Inbox

8 open PRs, 6 open issues. Issues #3 and #4 describe the same fragment-stripping feature; PRs #9 and #10 are near-identical implementations of it. PRs #26 and #27 are intentional contribution-review demo controls and must stay unmerged. Issue #8 is confirmed fixed on current main by source evidence (not by merged history alone). The CSV stack (PR #11 → PR #12) is clean and ready for review in dependency order. Issue #7 (query-param regression coverage) has no open PR. PR #28 diff was unavailable and cannot be classified.

All actions below are proposed, not approved or applied.

<details><summary>A1 · duplicate_issue</summary>

Both issues request the same feature: opt-in fragment-free URL identity in the shared normalizer while keeping default behavior unchanged. Issue #3 frames it as 'section anchors appear twice in JSON export'; issue #4 frames it as 'collapse links that only differ after the hash'. Resolution criteria and constraints are identical in both.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/3, https://github.com/gvago/oss-maintainer-demo/issues/4

Evidence:
- Issue #3 body: 'Add opt-in fragment-free identity while keeping current behavior the default. Shared normalizer, export and CLI should agree.'
- Issue #4 body: 'Need an optional way to save one document entry rather than each section. Existing defaults must stay compatible.'
- PR #9 (refs #3) and PR #10 (refs #4) both add the identical strip_fragment=False parameter to normalize_url, confirming the two issues drive duplicate work.

Uncertainty: Both issues are authored by gvago and may be intentional demo fixtures modeling a near-duplicate scenario. If so, they should remain open as demo controls. Maintainer confirmation required before closing either.

Draft reply:

> Issues #3 and #4 both describe the same feature: an opt-in `strip_fragment` parameter on the shared normalizer. We already have two separate PRs implementing it (#9 refs #3, #10 refs #4). Could you confirm whether one of these should be closed as a duplicate, or whether both are intentional demo fixtures to be kept open? Once confirmed, we will close the duplicate and update the surviving PR with a 'Closes' keyword.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/10": "67a58c07cb73721b1d8ce0b04742e185a1fd7712", "https://github.com/gvago/oss-maintainer-demo/pull/9": "ddb9ea26e5f16da5074123c0b8e4ad4ccd92b96e"}`

</details>

<details><summary>A2 · duplicate_pr</summary>

Both PRs modify bookmarks/urls.py to add `strip_fragment: bool = False` to normalize_url and introduce the identical test `test_optional_fragment_identity`. They share the same base commit (e565ba0), both target main, and produce functionally identical behavior. The only difference is cosmetic: PR #9 uses an inline conditional in the return statement; PR #10 extracts it to a local variable `fragment`.

Targets: https://github.com/gvago/oss-maintainer-demo/pull/9, https://github.com/gvago/oss-maintainer-demo/pull/10

Evidence:
- PR #9 diff: signature becomes `normalize_url(value: str, *, strip_fragment: bool = False)` and return statement uses `"" if strip_fragment else parts.fragment` inline.
- PR #10 diff: identical signature; adds `fragment = parts.fragment if not strip_fragment else ""` then passes `fragment` to urlunsplit — functionally equivalent.
- Both PRs add the identical test block: `test_optional_fragment_identity` asserting strip_fragment=True strips the fragment and the default preserves it.
- Both share base_commit e565ba08587117166a9ba46e00d211879fc55857 and target branch main.

Uncertainty: PR #9 references issue #3 and PR #10 references issue #4. If those issues are intentional demo fixtures (see A1), these PRs may also be intentional demo controls. Confirm with A1 before closing either. Do not rebase the unselected branch automatically; preserve independently authored work.

Draft reply:

> Thanks for both contributions! PRs #9 and #10 implement the same `strip_fragment` parameter on `normalize_url` with functionally identical diffs — only a minor style difference (inline conditional vs. local variable). To avoid a double-apply, one should be closed before merging. Could you confirm which to keep, or whether both are intentional demo fixtures? The surviving PR should add a 'Closes' keyword for the surviving issue once A1 is resolved.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/10": "67a58c07cb73721b1d8ce0b04742e185a1fd7712", "https://github.com/gvago/oss-maintainer-demo/pull/9": "ddb9ea26e5f16da5074123c0b8e4ad4ccd92b96e"}`

</details>

<details><summary>A3 · demo_control</summary>

Both PRs are self-described contribution-review experiments that must stay unmerged per their own body text. PR #26 ('bad') adds export_readable using the third-party tabulate dependency without applying normalize_url. PR #27 ('control') adds export_csv using only stdlib — an implementation byte-for-byte identical to the real PR #11. These are intentional demo controls for illustrating contribution quality differences, not accidental duplicates.

Targets: https://github.com/gvago/oss-maintainer-demo/pull/26, https://github.com/gvago/oss-maintainer-demo/pull/27

Evidence:
- PR #26 body: 'Contribution-review experiment; keep unmerged.' Branch: experiment/thin-review-md-bad.
- PR #27 body: 'Contribution-review experiment; keep unmerged.' Branch: experiment/thin-review-md-control.
- PR #26 diff introduces `from tabulate import tabulate` (third-party dependency) and does not call normalize_url on the readable output.
- PR #27 diff for bookmarks/exports.py and tests/test_bookmarks.py is byte-for-byte identical to PR #11's diff, confirming it is a demo copy of the production implementation.

Uncertainty: Low: both PRs self-identify as demo experiments with explicit keep-unmerged instructions. No merge action is warranted.

Draft reply:

> PRs #26 and #27 are flagged as intentional contribution-review demo controls (both bodies state 'keep unmerged'). They are preserved as demo fixtures. No merge action will be taken. Note for reviewers: PR #27's export_csv implementation is a copy of PR #11 — the production implementation is PR #11 (non-experiment branch, predates #27).

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/26": "75a0d52fadd2cb6d4b7787227ee6c66881c1ef3f", "https://github.com/gvago/oss-maintainer-demo/pull/27": "d63ad1a02f2282509aebb3468b6f05425969295e"}`

</details>

<details><summary>A4 · already_fixed</summary>

Issue #8 reports that https://example.com:443/docs and https://example.com/docs produce two export entries. The current main source of bookmarks/urls.py (sha 13d048b, commit 2026-10-11T16:07:50Z) contains `if port is not None and (parts.scheme, port) not in {("http", 80), ("https", 443)}:` which strips :443 from HTTPS URLs before building the authority string, causing both URLs to normalize to the same value. This is confirmed by direct source reading, not merged history alone.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/8

Evidence:
- current_main bookmarks/urls.py line 17 (sha 13d048b): `if port is not None and (parts.scheme, port) not in {("http", 80), ("https", 443)}:` — port :443 on HTTPS is excluded from the authority and therefore stripped.
- current_main file commit_date: 2026-10-11T16:07:50+00:00; resolved_ref: main.
- Issue #8 body explicitly requests: 'Investigate whether this is already addressed on main before implementing another fix.'
- Merged PR #2 (fix/default-ports, merge_commit e565ba0) description: 'Closes #1. Fix URL identity in the shared normalizer; JSON export and CLI inherit the same behavior.' — default-port canonicalization was the stated goal.

Uncertainty: Low: current main source directly and unambiguously confirms the canonicalization. No open PR modifies this code path. Live test-run output is unavailable, so behavioral verification by the maintainer is recommended before closing.

Draft reply:

> Good news: this appears to be already fixed on `main`. The current normalizer strips the default HTTPS port `:443` before building the authority string (`bookmarks/urls.py` line 17, sha 13d048b). Both `https://example.com:443/docs` and `https://example.com/docs` normalize to the same URL. Please verify by running `python3 -m unittest discover -s tests -v` locally and confirming no regression, then we can close this issue.

Observed PR heads: `{}`

</details>

<details><summary>A5 · link_issue_pr</summary>

PR #11 explicitly closes issue #5. The PR adds export_csv to bookmarks/exports.py with a url header, stdlib quoting, shared normalization, and stable deduplication — matching all stated requirements of issue #5. Current main confirms export_csv is absent, so the change is genuine additive work.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/5, https://github.com/gvago/oss-maintainer-demo/pull/11

Evidence:
- PR #11 body: 'Closes #5. CSV library output with a url header, standard-library quoting, shared normalization and stable deduplication. Checks: 7 tests passed.'
- Issue #5 body: 'Add a CSV exporter with a url header, stable first-seen deduplication, shared URL normalization and correct quoting.'
- PR #11 diff adds export_csv using csv.writer with normalize_url applied to each URL — matching all four requirements in the issue.
- current_main bookmarks/exports.py contains only export_json; export_csv is absent, confirming PR #11 is not redundant.

Uncertainty: Low: the Closes keyword is explicit in the PR body and the implementation matches the requirements.

Draft reply:

> Linking PR #11 to issue #5: the PR body includes 'Closes #5' and the implementation satisfies all stated requirements (url header, stdlib quoting, shared normalization, stable deduplication). Tagging for tracking. Note: this PR is also the prerequisite for PR #12 (CSV CLI, issue #6).

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/11": "b9dab92614d3b0c4e7fb61531110d54bf10e6694"}`

</details>

<details><summary>A6 · link_issue_pr</summary>

PR #12 closes issue #6 and adds --format csv to the CLI. The PR correctly declares its dependency on PR #11 (feat/csv-library) in both its Git base branch and body text. Issue #6 cannot be fully closed until PR #11 lands first.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/6, https://github.com/gvago/oss-maintainer-demo/pull/12

Evidence:
- PR #12 body: 'Closes #6. Depends on #11 (CSV library). The Git base is feat/csv-library, so this PR contains only CLI wiring.'
- Issue #6 body: 'Add --format csv to the CLI using the library exporter. Related library work is required; default JSON behavior must remain compatible.'
- PR #12 base_commit b9dab92614d3b0c4e7fb61531110d54bf10e6694 is identical to PR #11's head_commit, confirming the stack dependency.
- PR #12 diff imports export_csv from bookmarks.exports, which is absent on current main until PR #11 merges.

Uncertainty: Low: Closes keyword and base branch confirm the relationship. Dependency on PR #11 is structurally enforced by the Git base.

Draft reply:

> Linking PR #12 to issue #6: the PR adds `--format csv` as requested. Note this PR stacks on PR #11 — issue #6 cannot be closed until PR #11 is merged first. See stack order action A8.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/11": "b9dab92614d3b0c4e7fb61531110d54bf10e6694", "https://github.com/gvago/oss-maintainer-demo/pull/12": "41bd59c16d4a37fecf3367e24119e8c6b32c3eb7"}`

</details>

<details><summary>A7 · link_issue_pr</summary>

PR #9 references issue #3 and PR #10 references issue #4. Both issue-PR pairs address the same opt-in fragment-stripping feature. All four are linked here for visibility pending the duplicate resolution in A1 and A2. Once a surviving issue and PR are chosen, the survivor should carry a 'Closes' keyword and the duplicates should be closed.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/3, https://github.com/gvago/oss-maintainer-demo/issues/4, https://github.com/gvago/oss-maintainer-demo/pull/9, https://github.com/gvago/oss-maintainer-demo/pull/10

Evidence:
- PR #9 body: 'Refs #3. Add opt-in strip_fragment to the shared normalizer without changing defaults.'
- PR #10 body: 'Refs #4. Add opt-in fragment-free normalization; preserve existing behavior by default.'
- Neither PR uses a 'Closes' keyword; the issues remain open with no formal closure link.
- Issues #3 and #4 flagged as duplicates in A1; PRs #9 and #10 flagged as duplicate implementations in A2.

Uncertainty: Resolution fully depends on A1 and A2 outcomes. No link update should be made until the duplicate determination is confirmed.

Draft reply:

> Issues #3 and #4 are both addressed by PRs #9 and #10 respectively via 'Refs' links, but neither carries a 'Closes' keyword. These are flagged as likely duplicates (A1, A2). Once the surviving issue and PR are identified, please update the survivor with 'Closes #N' and close the duplicate issue and PR.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/10": "67a58c07cb73721b1d8ce0b04742e185a1fd7712", "https://github.com/gvago/oss-maintainer-demo/pull/9": "ddb9ea26e5f16da5074123c0b8e4ad4ccd92b96e"}`

</details>

<details><summary>A8 · stack_order</summary>

PR #12 (CSV CLI wiring) targets branch feat/csv-library, whose head is PR #11's head commit. PR #12's diff imports export_csv from bookmarks.exports, which does not exist on current main. PR #11 must be reviewed and merged to main before PR #12 can be rebased to main and merged.

Targets: https://github.com/gvago/oss-maintainer-demo/pull/11, https://github.com/gvago/oss-maintainer-demo/pull/12

Evidence:
- PR #12 base_commit b9dab92614d3b0c4e7fb61531110d54bf10e6694 is identical to PR #11's head_commit — structural stack dependency.
- PR #12 diff: `from bookmarks.exports import export_csv, export_json` — export_csv is absent from current main.
- current_main bookmarks/exports.py contains only export_json; export_csv is not present.
- PR #11 body confirms: 'CLI wiring is a separate change.' PR #12 body confirms: 'Depends on #11 (CSV library).'

Uncertainty: Low: the dependency is structurally enforced by the Git base branch and confirmed by both PR bodies.

Draft reply:

> PR #11 (CSV library, closes #5) must merge before PR #12 (CSV CLI, closes #6) can target main. Suggested order: review and merge PR #11 first; then update PR #12's base branch to main and review. Both PRs were authored to be reviewed together per PR #12's body.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/11": "b9dab92614d3b0c4e7fb61531110d54bf10e6694", "https://github.com/gvago/oss-maintainer-demo/pull/12": "41bd59c16d4a37fecf3367e24119e8c6b32c3eb7"}`

</details>

<details><summary>A9 · request_followup</summary>

Issue #7 requests explicit regression coverage that query parameter names, values, order, and repetitions are preserved by normalization and all exports. No open PR in the evidence set references issue #7 or adds query-parameter-specific test cases. Wisdom history for issue #7 returned only PR #2 (default-port fix), which addresses a different concern.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/7

Evidence:
- Issue #7 body: 'Add explicit regression coverage proving names, values, order and repetitions are preserved by normalization and all exports.'
- No open PR in the evidence set mentions issue #7 or adds query-parameter preservation tests.
- Wisdom history for issue #7 returned only PR #2 (fix/default-ports, merged, similarity_distance 0.746) — not a match for query-param coverage.
- current_main bookmarks/urls.py passes parts.query through to urlunsplit without modification, but no test asserts repeated keys, ordering, or special characters in query strings.

Uncertainty: Medium: the open-PR set returned by Wisdom may be incomplete. A search by issue mention or file overlap could surface unindexed work. Verify before opening a new PR.

Draft reply:

> Issue #7 (query parameter preservation) has no associated open PR in the current inbox. The merged port fix (PR #2) did not add query-param regression coverage. A new PR is needed that adds tests asserting: (1) parameter names and values are preserved verbatim, (2) parameter order is stable, (3) repeated keys survive deduplication, and (4) these hold for both export_json and export_csv. Would anyone like to take this on?

Observed PR heads: `{}`

</details>

<details><summary>A10 · review_next</summary>

PR #13 (docs quickstart) is documentation-only, has no code dependencies or blast radius, and passes all 6 existing tests with no behavior change — the lowest-risk merge candidate. PR #11 (CSV library) is the prerequisite for PR #12 and is a self-contained library change with small blast radius and 7 passing tests; reviewing it unblocks the full CSV stack. Both are independent of the unresolved duplicate-PR situation (A2).

Targets: https://github.com/gvago/oss-maintainer-demo/pull/13, https://github.com/gvago/oss-maintainer-demo/pull/11

Evidence:
- PR #13 labels: 'Less than 5 minutes'. Diff touches only README.md (+8 lines). Body: 'Runtime behavior unchanged; checks: 6 tests passed.'
- PR #11 labels: 'Less than 10 minutes', 'Small blast radius'. Diff adds export_csv to exports.py with full test coverage (7 tests passed). Body: 'Closes #5.'
- Neither PR #13 nor PR #11 shares a base or file overlap with the duplicate-PR pair (#9/#10) or the demo controls (#26/#27).
- current_main confirms both the quickstart example and export_csv are absent, so both PRs represent genuine additive work.

Uncertainty: Low for PR #13 (docs only). Low-medium for PR #11: its export_csv diff is reproduced verbatim in demo-control PR #27, but PR #11 predates #27 and is on a non-experiment branch (feat/csv-library), confirming it is the intended production implementation.

Draft reply:

> Suggested review priority: (1) PR #13 — documentation quickstart, no runtime risk, ~5 minutes. (2) PR #11 — CSV library exporter, small blast radius, unblocks PR #12 (CSV CLI). Note: PR #11's export_csv diff is copied verbatim in demo-control PR #27; PR #11 is the production version. After PR #11 merges, update PR #12's base to main and review the CLI wiring.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/11": "b9dab92614d3b0c4e7fb61531110d54bf10e6694", "https://github.com/gvago/oss-maintainer-demo/pull/13": "ef111e70f732864621b2558722ad91ccbd5df73a"}`

</details>

## Data gaps

- PR #28 diff was unavailable (exceeds upstream byte limit); its implementation could not be inspected for duplicate functions, incomplete coverage, or overlap with other PRs.
- Issue #7 (query parameter preservation) has no open PR; dedicated regression coverage for names, values, order, and repeated keys is missing from both the library and exports.
- No test-run output or live behavioral evidence is available for current main; the already_fixed classification for issue #8 (A4) relies on source reading only — maintainer verification of test suite passage is recommended before closing.
- Wisdom history search returned only a single candidate PR (PR #2) for every open issue, suggesting the similarity search may not have been exhaustive across all open PRs.
- PRs #9 and #10 only unit-test normalize_url directly; no PR verifies that export_json, export_csv, or the CLI correctly propagate strip_fragment=True end-to-end.
- Issues #3, #4, and PRs #9, #10 may be intentional demo fixtures (authored by the repo owner) rather than accidental duplicates — the duplicate classification in A1 and A2 requires maintainer confirmation before any closure.
