# Maintainer Inbox

Seven open PRs and six open issues. Two issues (#3, #4) ask for the same opt-in fragment-free bookmark identity, and two open PRs (#9, #10) implement that identity with byte-equivalent behavior and identical tests — one should be consolidated. PRs #11 and #12 are complementary, not duplicates: #12 is Git-stacked on feat/csv-library and only adds CLI wiring, so #11 must be reviewed and merged first. Issue #8 (:443 duplication) is covered by the normalizer source currently on main, which strips default HTTP/HTTPS ports; this is the one case where attached current-main source, not merged history alone, supports an already-fixed finding. Issue #3 is only partially addressed by #9/#10 — current main's export_json and __main__ never pass strip_fragment, so the issue's "normalizer, export and CLI should agree" requirement is unmet. Issue #7 (query-parameter preservation coverage) has no open PR at all. PRs #26/#27 are labelled intentional contribution-review fixtures and are treated as demo controls, not accidental duplicates, even though #27's export_csv is identical to #11's. All actions are proposed only; nothing has been applied, and no rebase of any branch is recommended.

All actions below are proposed, not approved or applied.

## A1 · duplicate_issue

Both issues describe the same defect and the same requested remedy: links differing only after '#' produce separate entries, and both ask for an opt-in document-level identity that leaves current defaults unchanged. #3 states the broader contract (shared normalizer, export and CLI must agree), so it is the better survivor; #4 contributes an extra reproduction. Proposed as consolidation under #3, not as a silent close of #4.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/3, https://github.com/gvago/oss-maintainer-demo/issues/4

Evidence:
- issues/3 body: 'JSON export currently treats https://example.com/guide#intro and https://example.com/guide#install as different bookmarks. Add opt-in fragment-free identity while keeping current behavior the default. Shared normalizer, export and CLI should agree.'
- issues/4 body: 'Saving https://example.com/guide#a and https://example.com/guide#b produces two entries. Need an optional way to save one document entry rather than each section. Existing defaults must stay compatible.'
- Both issues were opened by gvago within 2 seconds (2026-10-11T10:47:59Z and 10:48:01Z) and carry no labels, assignees or comments.

Uncertainty: Neither issue has comments, so there may be an unstated scope distinction (e.g. #4 meaning a storage-level entry rather than export identity) that the bodies do not reveal. Proposed only; re-fetch both issue states before acting.

Draft reply:

> Thanks for both reports — these describe the same behavior: saved links that differ only after the '#' are kept as separate bookmarks, and both ask for an opt-in document-level identity that preserves today's defaults. I'd like to track the work on #3 since it spells out that the normalizer, the exporter and the CLI all have to agree, and keep this reproduction linked as extra context rather than losing it. If you think there's a requirement here that #3 doesn't cover, say so and we'll keep both open.

Observed PR heads: `{}`

## A2 · duplicate_pr

These are duplicate implementations, confirmed by diff comparison rather than by title or shared filename. Both change the same two files, add the identical keyword-only parameter 'strip_fragment: bool = False' to normalize_url, produce the same output for every input, and add a test named test_optional_fragment_identity with character-identical assertions. The only difference is expression style: #9 inlines '"" if strip_fragment else parts.fragment' in the urlunsplit call, #10 assigns a local 'fragment' variable first. Both branch from the same base commit e565ba0. One should be chosen; the other closed with credit, not force-pushed or rebased.

Targets: https://github.com/gvago/oss-maintainer-demo/pull/9, https://github.com/gvago/oss-maintainer-demo/pull/10

Evidence:
- pull/9 diff bookmarks/urls.py: '-def normalize_url(value: str) -> str:' / '+def normalize_url(value: str, *, strip_fragment: bool = False) -> str:' and '+ ... parts.query, "" if strip_fragment else parts.fragment))'
- pull/10 diff bookmarks/urls.py: same signature change plus '+    fragment = parts.fragment if not strip_fragment else ""' then 'urlunsplit((..., parts.query, fragment))'
- Both diffs add to tests/test_bookmarks.py the same block: 'def test_optional_fragment_identity(self):' asserting normalize_url("https://example.com/a#one", strip_fragment=True) == "https://example.com/a" and the un-stripped default.
- Both PRs report base_commit e565ba08587117166a9ba46e00d211879fc55857 and '7 tests passed'.

Uncertainty: Both PRs are authored by the same account (gvago) in this evidence, so no cross-contributor credit question arises here; if authorship differs on refresh, pick the earlier submission (#9, created 10:50:17Z) and credit the other. Test counts are self-reported in PR bodies — no CI status was fetched.

Draft reply:

> #9 and #10 implement the same change: the same keyword-only `strip_fragment=False` parameter on `normalize_url`, the same default-preserving behavior, and the same `test_optional_fragment_identity` assertions. The only difference is whether the empty fragment is inlined in the `urlunsplit` call or assigned to a local first — no behavioral difference. I'd suggest we land one (I'd lean to #9 as the earlier submission) and close the other with credit in the merged PR description. Note that whichever lands, it only covers the helper — see the follow-up on #3 about exporter and CLI wiring.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/10": "67a58c07cb73721b1d8ce0b04742e185a1fd7712", "https://github.com/gvago/oss-maintainer-demo/pull/9": "ddb9ea26e5f16da5074123c0b8e4ad4ccd92b96e"}`

## A3 · stack_order

Complementary stack, not a duplicate pair, even though both touch CSV output. #11 defines export_csv in bookmarks/exports.py; #12 imports that symbol in bookmarks/__main__.py and adds --format csv. #12's target_branch is feat/csv-library and its base_commit equals #11's head_commit (b9dab92), so #12's diff is CLI-only by construction. Review and merge #11 first; #12 cannot stand alone because 'from bookmarks.exports import export_csv' would fail against current main, where exports.py contains only export_json. After #11 merges, #12 needs its base retargeted to main — a maintainer/author action on an open PR, not an automatic rebase performed on anyone's behalf.

Targets: https://github.com/gvago/oss-maintainer-demo/pull/11, https://github.com/gvago/oss-maintainer-demo/pull/12

Evidence:
- pull/11 diff bookmarks/exports.py adds '+def export_csv(urls: list[str]) -> str:' with stdlib csv.writer and dict.fromkeys dedup over normalize_url.
- pull/12 diff bookmarks/__main__.py: '-from bookmarks.exports import export_json' / '+from bookmarks.exports import export_csv, export_json' plus '+    parser.add_argument("--format", choices=("json", "csv"), default="json")'.
- pull/12 change metadata: target_branch 'feat/csv-library', base_commit b9dab92614d3b0c4e7fb61531110d54bf10e6694 == pull/11 head_sha.
- current_main bookmarks/exports.py contains only export_json — export_csv does not exist on main, so #12 is unbuildable without #11.

Uncertainty: No CI results were fetched for either PR; the 7- and 9-test counts come from the PR bodies. Whether GitHub auto-retargets #12 to main on #11's merge depends on repository settings not visible in this evidence — verify the base after merging rather than assuming.

Draft reply:

> These two are complementary, not duplicates: #11 adds the `export_csv` library function and #12 wires `--format csv` into the CLI on top of it. #12's Git base is `feat/csv-library`, so its diff is correctly CLI-only and it won't build against main until #11 lands. Proposed order: review and merge #11 first, then confirm #12's base is retargeted to main and that its diff is still limited to `bookmarks/__main__.py` and the CLI tests before merging. I'm not touching either branch.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/11": "b9dab92614d3b0c4e7fb61531110d54bf10e6694", "https://github.com/gvago/oss-maintainer-demo/pull/12": "41bd59c16d4a37fecf3367e24119e8c6b32c3eb7"}`

## A4 · link_issue_pr

The declared issue links are confirmed by the diffs, not just by the 'Closes' keywords. Issue #5 asks for a CSV exporter with a url header, first-seen dedup, shared normalization and correct quoting — #11's export_csv does exactly those four things. Issue #6 asks for --format csv using the library exporter with JSON remaining the default — #12's argparse change does exactly that. The split across two issues matches the split across two PRs, so neither issue should close until its own PR merges.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/5, https://github.com/gvago/oss-maintainer-demo/pull/11, https://github.com/gvago/oss-maintainer-demo/issues/6, https://github.com/gvago/oss-maintainer-demo/pull/12

Evidence:
- issues/5 body asks for 'a url header, stable first-seen deduplication, shared URL normalization and correct quoting. Keep this library change separate from CLI wiring.'; pull/11 diff writes writerow(["url"]), uses dict.fromkeys over normalize_url, and csv.writer for quoting.
- issues/6 body asks for '--format csv to the CLI using the library exporter ... default JSON behavior must remain compatible.'; pull/12 diff adds choices=("json", "csv"), default="json".
- pull/11 body: 'Closes #5'; pull/12 body: 'Closes #6'.
- pull/11 test test_csv_export asserts rows == [["url"], ["https://example.com/a?x=1,2"]], covering header, dedup, normalization and comma quoting in one case.

Uncertainty: Issue #5 asks for 'correct quoting' generally; the single test covers an embedded comma but not embedded quotes or newlines. That is a review note on #11, not a reason to withhold the link.

Draft reply:

> Linking for tracking: #5 is implemented by #11 (library `export_csv`) and #6 by #12 (CLI `--format csv`). The diffs match what each issue asked for, including the deliberate library/CLI split. Neither issue should be closed before its corresponding PR merges. One review note for #11: the CSV quoting test covers an embedded comma — worth adding a case with an embedded quote or newline before merge.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/11": "b9dab92614d3b0c4e7fb61531110d54bf10e6694", "https://github.com/gvago/oss-maintainer-demo/pull/12": "41bd59c16d4a37fecf3367e24119e8c6b32c3eb7"}`

## A5 · already_fixed

This finding rests on current-main source attached in the evidence, not on merged history alone. current_main bookmarks/urls.py (resolved_ref main, sha 13d048b, fetched 2026-10-11T16:48:32Z) contains the guard 'if port is not None and (parts.scheme, port) not in {("http", 80), ("https", 443)}: authority += f":{port}"', so https://example.com:443/docs and https://example.com/docs both normalize to https://example.com/docs. current_main bookmarks/exports.py routes every URL through normalize_url before dict.fromkeys dedup, so the export path inherits the fix. Merged PR #2 is corroborating history, not the basis of the claim. Proposed as a close-with-verification: the maintainer should run the two URLs on main before closing, because this is a source read, not an executed behavior check.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/8

Evidence:
- current_main bookmarks/urls.py (sha 13d048b40310b3d7154ec195896de723c75f3abd, resolved_ref main): default ports 80/443 are excluded from the rebuilt authority.
- current_main bookmarks/exports.py: 'return json.dumps(list(dict.fromkeys(normalize_url(url) for url in urls)), indent=2)' — dedup happens after normalization.
- issues/8 body: 'exporting https://example.com:443/docs and https://example.com/docs creates two entries. Investigate whether this is already addressed on main before implementing another fix.'
- History corroboration only: merged PR https://github.com/gvago/oss-maintainer-demo/pull/2 'fix: canonicalize default HTTP and HTTPS ports', merge_commit e565ba08587117166a9ba46e00d211879fc55857.

Uncertainty: No code was executed and tests/test_bookmarks.py on main was not fetched, so this is a source-level reading rather than a reproduced behavior check. The attached main source is a point-in-time read at 2026-10-11T16:48:32Z; if main has moved, re-read urls.py before closing. Do not close on the merged-history signal alone — PR #2 was returned for all six issues by the similarity search and is therefore a weak discriminator.

Draft reply:

> This looks resolved on current main. `normalize_url` in `bookmarks/urls.py` now omits the port when it is the scheme default (`{("http", 80), ("https", 443)}`), and `export_json` deduplicates after normalization — so `https://example.com:443/docs` and `https://example.com/docs` should collapse to one entry. The fix landed in #2. Before I close this: could you confirm against current main with those exact two URLs? If it still reproduces, please include the commit SHA and the exact input and I'll reopen the investigation rather than ship a second fix.

Observed PR heads: `{}`

## A6 · request_followup

Partial fix. Issue #3 requires that 'shared normalizer, export and CLI should agree', but both candidate PRs stop at the normalizer. Neither diff touches bookmarks/exports.py or bookmarks/__main__.py, and current main shows export_json calls normalize_url(url) with no strip_fragment argument and __main__ exposes no corresponding flag — so after merging either PR, a user exporting #intro and #install still gets two entries. The tests added are helper-level only. #3 should stay open after the merge, with exporter/CLI wiring and an end-to-end dedup regression tracked as follow-up.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/3, https://github.com/gvago/oss-maintainer-demo/pull/9, https://github.com/gvago/oss-maintainer-demo/pull/10

Evidence:
- issues/3 body: 'Shared normalizer, export and CLI should agree.'
- pull/9 diff touches only bookmarks/urls.py and tests/test_bookmarks.py; pull/10 diff touches only the same two files. Neither modifies exports.py or __main__.py.
- current_main bookmarks/exports.py: 'normalize_url(url) for url in urls' — no strip_fragment argument is ever passed.
- current_main bookmarks/__main__.py: argparse exposes only 'urls'; there is no fragment-related flag.
- Both PRs' own bodies concede the gap: #9 'This is the first library slice; exporter and CLI wiring are separate work.'

Uncertainty: Whether the maintainer wants the wiring in the same PR or as a follow-up is a project-convention call not visible in this evidence. CONTRIBUTING.md was not fetched.

Draft reply:

> The helper slice here is a good first step, but #3 asks for the normalizer, the exporter and the CLI to agree, and neither #9 nor #10 touches `bookmarks/exports.py` or `bookmarks/__main__.py` — on main, `export_json` still calls `normalize_url(url)` with no `strip_fragment`, so the user-visible duplicate remains after merge. Proposing we keep #3 open once the helper lands and track two follow-ups: (1) thread the option through `export_json` and a CLI flag, and (2) add an end-to-end regression asserting `#intro` and `#install` collapse to one exported entry. Happy to merge the helper on its own in the meantime.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/10": "67a58c07cb73721b1d8ce0b04742e185a1fd7712", "https://github.com/gvago/oss-maintainer-demo/pull/9": "ddb9ea26e5f16da5074123c0b8e4ad4ccd92b96e"}`

## A7 · request_followup

Uncovered issue — no open PR in this evidence addresses it. #7 asks for explicit regression coverage proving query-string names, values, order and repetitions survive normalization and every export. Current main's normalize_url passes parts.query through urlunsplit untouched, which suggests behavior is already correct, but the issue's deliverable is the regression test, not a behavior change, and no test file on main was fetched to confirm whether such coverage exists. Needs an owner and a confirmation of current coverage; it should not be inferred fixed from the normalizer source.

Targets: https://github.com/gvago/oss-maintainer-demo/issues/7

Evidence:
- issues/7 body: 'Add explicit regression coverage proving names, values, order and repetitions are preserved by normalization and all exports.'
- current_main bookmarks/urls.py: 'urlunsplit((parts.scheme.lower(), authority, parts.path or "/", parts.query, parts.fragment))' — query is passed through unmodified.
- None of the seven open PRs (#9, #10, #11, #12, #13, #26, #27, #28) has a diff hunk referencing query-parameter preservation; the only query-adjacent assertion is #11/#27's test_csv_export with '?x=1,2', which tests comma quoting, not parameter order or repetition.
- The merged-history search for #7 returned only PR #2 (default ports) at similarity_distance 0.746 — not a match for this request.

Uncertainty: tests/test_bookmarks.py on current main was not included in the evidence, so existing query-parameter coverage may already exist and go unseen here. Confirm the current test file before commissioning new work.

Draft reply:

> No open PR currently covers this. Reading `bookmarks/urls.py` on main, the query string is passed through to `urlunsplit` unmodified, so the behavior is probably already correct — but the ask here is explicit regression coverage, and I haven't verified what `tests/test_bookmarks.py` already asserts. Could someone confirm whether current tests cover repeated keys and parameter order? If not, this is a good self-contained first contribution: one test asserting that `?b=2&a=1&a=3` survives normalization and every exporter byte-for-byte.

Observed PR heads: `{}`

## A8 · demo_control

Intentional contribution-review fixtures, not accidental duplication. Both PR bodies say 'Contribution-review experiment; keep unmerged', they share base commit b27d830 and were opened five seconds apart on paired branches named -bad and -control. Importantly, #27's export_csv is byte-identical to #11's export_csv including the same test — under a pure diff comparison that would read as a duplicate PR of #11, but the branch naming and the explicit 'keep unmerged' note mark it as a deliberate control. These two should be excluded from duplicate-closure and merge recommendations. Separately, #26 is the intended negative case: it adds a third-party 'tabulate' dependency, bypasses normalize_url entirely (it calls url.lower() on raw input), and adds no test — all consistent with its role as the bad sample, not findings to act on.

Targets: https://github.com/gvago/oss-maintainer-demo/pull/26, https://github.com/gvago/oss-maintainer-demo/pull/27

Evidence:
- pull/26 body and pull/27 body both end: 'Contribution-review experiment; keep unmerged.'
- Branch names: 'experiment/thin-review-md-bad' (#26) and 'experiment/thin-review-md-control' (#27); both base_commit b27d830f89876ae77d3529138237acd8d0aaf5ec; created 2026-10-11T16:05:09Z and 16:05:14Z.
- pull/27 diff bookmarks/exports.py is character-identical to pull/11's export_csv, and its tests/test_bookmarks.py hunk is identical to #11's test_csv_export — a diff-only comparison would flag it as duplicating #11.
- pull/26 diff: '+    from tabulate import tabulate' and 'tabulate([[url.lower()] for url in dict.fromkeys(urls)], headers=["url"])' — no normalize_url call, no test added, new external dependency.

Uncertainty: The 'keep unmerged' marker comes from PR bodies, which are contributor-supplied text; it is treated as a maintainer-authored convention here because both PRs are authored by the repository owner. If an outside contributor later opens a similar PR, do not extend this exemption to it. The prior packet in PR #28 claims #26 has 'three attributed workflow findings ... with changes requested' — no review comments were fetched in this evidence, so that claim is unverified here.

Draft reply:

> Flagging these as intentional fixtures: both PRs state 'Contribution-review experiment; keep unmerged' and sit on paired `-bad`/`-control` branches from the same base. Worth noting for anyone running duplicate detection: #27's `export_csv` is byte-identical to #11's, so a diff-similarity pass will flag it as a duplicate PR — it isn't, it's the control sample. Recommend excluding both from duplicate-closure, merge and stale-PR automation. No action proposed on either.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/26": "75a0d52fadd2cb6d4b7787227ee6c66881c1ef3f", "https://github.com/gvago/oss-maintainer-demo/pull/27": "d63ad1a02f2282509aebb3468b6f05425969295e"}`

## A9 · review_next

Ranked by dependency order, blast radius and actual blockers — no time-savings claim is made and the repository's time labels are not treated as measurements. (1) #11: unblocks #12 and closes #5; it is the only hard dependency in the queue. (2) #12: reviewable immediately alongside #11 but mergeable only after it, and it needs a base retarget first. (3) #9 (or #10): small, self-contained normalizer change, blocked only on the duplicate decision in A2; it does not close #3 on its own. (4) #13: documentation-only README addition, no runtime surface, mergeable independently at any point. (5) #28: largest blast radius — adds a self-hosted-runner GitHub Action, a new tools/ script and a new tests file, and its own description states that headless agent generation and the hosted Action are unverified, so it needs the most reviewer attention and should not be rushed ahead of the small changes. PRs #26 and #27 are excluded as demo controls per A8.

Targets: https://github.com/gvago/oss-maintainer-demo/pull/11, https://github.com/gvago/oss-maintainer-demo/pull/12, https://github.com/gvago/oss-maintainer-demo/pull/9, https://github.com/gvago/oss-maintainer-demo/pull/13, https://github.com/gvago/oss-maintainer-demo/pull/28

Evidence:
- pull/12 depends on pull/11: base_commit b9dab926 == pull/11 head_sha; '+from bookmarks.exports import export_csv, export_json'.
- pull/13 diff touches only README.md (+8/-0, a quickstart code block) — no runtime surface.
- pull/28 diff adds .github/workflows/maintainer-inbox.yml (runs-on [self-hosted, maintainer-inbox]), tools/maintainer_inbox.py (132 lines, invokes subprocess against qodo/claude/codex) and tests/test_maintainer_inbox.py; labelled 'Medium blast radius'.
- pull/28 body: 'Claude/Codex generation and hosted CI activation remain unverified; no credentials, installs or runner registration performed.'

Uncertainty: No CI status, review state, or review comments were fetched for any PR, so a red build or an existing requested-change could reorder this queue. Ordering also assumes the maintainer wants to land the CSV feature before the tooling PR; that is a priority judgment, not something the evidence settles.

Draft reply:

> Suggested review order, by dependency and blast radius rather than by age: (1) #11 — the only blocker in the queue, unblocks #12 and closes #5; (2) #12 — review together with #11, merge after it and after its base is retargeted to main; (3) #9 or #10 — pick one per the duplicate note, small and self-contained; (4) #13 — docs-only, mergeable whenever; (5) #28 — biggest surface (self-hosted runner workflow plus a new tool), and its own description flags the hosted CI path as unverified, so it deserves an unhurried review. #26 and #27 are intentional fixtures and are excluded.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/11": "b9dab92614d3b0c4e7fb61531110d54bf10e6694", "https://github.com/gvago/oss-maintainer-demo/pull/12": "41bd59c16d4a37fecf3367e24119e8c6b32c3eb7", "https://github.com/gvago/oss-maintainer-demo/pull/13": "ef111e70f732864621b2558722ad91ccbd5df73a", "https://github.com/gvago/oss-maintainer-demo/pull/28": "f26334014f5d82ddf142d88c380e270a0d176e56", "https://github.com/gvago/oss-maintainer-demo/pull/9": "ddb9ea26e5f16da5074123c0b8e4ad4ccd92b96e"}`

## A10 · request_followup

Self-referential correction, not a code-quality review. PR #28 ships a committed sample packet (maintainer-inbox/maintainer-actions.json) whose summary promises to 'clear the already-fixed default-port report', and whose A7 evidence asserts that PR #26 has 'three attributed workflow findings and one overlapping bug, with changes requested'. No review-comment data appears anywhere in the attached evidence, including in the committed evidence.json, so that evidence line is not source-linked and should be corrected or removed before the sample is held up as an example of the format. The committed evidence.json also contains no current-main file reads, which is the one input that makes an already-fixed judgment defensible — worth adding to the collector so future packets can reach that conclusion the same way A5 does here.

Targets: https://github.com/gvago/oss-maintainer-demo/pull/28

Evidence:
- pull/28 diff maintainer-inbox/maintainer-actions.json, action A7 evidence: 'https://github.com/gvago/oss-maintainer-demo/pull/26: three attributed workflow findings and one overlapping bug, with changes requested.'
- The committed maintainer-inbox/evidence.json in the same diff contains only list-prs, list-issues, one pull-request similar query and five get-pr calls — no review-comments or issue-comments read.
- pull/28 diff tools/maintainer_inbox.py collect(): reads whoami, list-prs, list-issues, get-pr per PR and 'pull-request similar' per issue; it never fetches current-main file contents.
- pull/28 diff maintainer-inbox/README.md: 'Headless Claude/Codex generation and the GitHub Action have not yet been exercised on a configured inference/CI host.'

Uncertainty: Review comments may genuinely exist on #26 and simply fall outside what was collected — the claim is unverified, not disproven. Whether the sample packet is meant to be a frozen artifact or a living example is a maintainer call.

Draft reply:

> Two notes on the committed sample packet before this merges. First, A7's evidence line says #26 has 'three attributed workflow findings ... with changes requested', but the committed `evidence.json` contains no review-comment read — the collector never calls one. That line should be dropped or backed by an actual fetch, since the sample is the template everyone will copy. Second, `collect()` gathers PRs, issues and merged-history similarity but no current-main file contents; that is exactly the input needed to justify an `already_fixed` action rather than falling back to `request_followup`. Adding a small set of current-main reads would make the strongest conclusion in the schema reachable. Neither blocks the kit's design — both are about the sample's own evidence discipline.

Observed PR heads: `{"https://github.com/gvago/oss-maintainer-demo/pull/28": "f26334014f5d82ddf142d88c380e270a0d176e56"}`

## Data gaps

- No CI/check status, review state, or review comments were fetched for any PR or issue. All test counts ('7 tests passed', '9 tests passed') are self-reported in PR bodies and were not independently verified.
- tests/test_bookmarks.py as it exists on current main was not included. Existing coverage therefore cannot be confirmed — this directly limits A7 (issue #7 query-parameter coverage) and the verification depth of A5.
- No code was executed. A5's already-fixed finding is a source-level reading of current_main bookmarks/urls.py and exports.py, not a reproduced behavior check.
- Current-main source was supplied for only three files (bookmarks/urls.py, exports.py, __main__.py) at sha 13d048b, fetched 2026-10-11T16:48:32Z. README.md, CONTRIBUTING.md and the test suite on main were not read.
- The merged-history similarity tool searches merged pull requests only; it cannot surface open PRs. It returned the same merged PR #2 for all six open issues (distances 0.639-0.845), so it provided no discriminating signal for issues #3, #4, #5, #6 or #7 — the duplicate and link findings in this packet rest on diff comparison, not on that tool.
- Only one explicit 'similar' query appears in the committed evidence.json (the :443 query); the per-issue history queries in the top-level evidence all used issue titles verbatim, which may explain the uniformly weak matches.
- No diff was fetched for merged PR #2 — only its description and generated summaries. Its actual change is inferred from current main's source, which is the stronger evidence anyway.
- PR #13's full file list was fetched (README.md only), but no diffs were fetched for any other closed or merged PR in the repository, so this packet cannot rule out additional in-flight or recently merged work outside the seven open PRs listed.
- Issue and PR authorship is uniformly 'gvago' in this evidence, so cross-contributor credit and coordination concerns could not be assessed realistically; if real contributors appear on refresh, the consolidation advice in A1 and A2 needs an authorship check first.
- No repository settings are visible (branch protection, auto-retarget on merge, required reviews), so A3's post-merge retarget step for #12 must be verified manually rather than assumed.
