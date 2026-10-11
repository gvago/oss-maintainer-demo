# Maintainer Inbox

<pre>8 open PRs · 6 open issues · Observed 2026-10-11T17:23:05.765982+00:00</pre>

<pre>Open backlog splits into four clusters. Fragment identity: issues #3 and #4 state the same requirement, and PRs #9 and #10 are two implementations of it that differ only in whether the conditional is inlined — pick one, and keep Refs links because neither threads the option through export or the CLI. CSV: #11 (library) and #12 (CLI) are a genuine stack, #12&#x27;s git base is #11&#x27;s head and it imports a function absent from main, so #11 reviews first. Already fixed: issue #8 is confirmed resolved on current main at sha 13d048b by both the source and a recorded run of the issue&#x27;s own reproduction plus the committed suite — evidence that it is fixed, separate from approval to close. Unclaimed: issue #7 still has no regression coverage for query preservation and no PR in flight. PRs #26 and #27 are self-declared keep-unmerged review fixtures, and PR #28 is the inbox generator itself — infrastructure reviewed on its own track, with one follow-up on the stale packet committed inside it. Every action below is proposed, not approved or applied; refresh each target and PR head before acting.</pre>

All actions below are proposed, not approved or applied.

<details><summary>A1 · duplicate_issue</summary>

<pre>Both issues ask for the same behavior change: an optional fragment-insensitive bookmark identity that leaves current defaults intact. #3 frames it as JSON export showing #intro and #install twice; #4 frames it as saving one document entry instead of one per section. The acceptance conditions (opt-in, defaults compatible, shared normalizer agreed on by export and CLI) are the same, and the two open PRs written against them produce identical behavior.</pre>

Targets: https://github.com/gvago/oss-maintainer-demo/issues/3, https://github.com/gvago/oss-maintainer-demo/issues/4

Evidence:
<pre>Issue #3 body: &#x27;Add opt-in fragment-free identity while keeping current behavior the default. Shared normalizer, export and CLI should agree.&#x27;</pre>
<pre>Issue #4 body: &#x27;Need an optional way to save one document entry rather than each section. Existing defaults must stay compatible.&#x27;</pre>
<pre>PR #9 (Refs #3) and PR #10 (Refs #4) both add the same keyword-only `strip_fragment: bool = False` parameter to `normalize_url` in bookmarks/urls.py and the same `test_optional_fragment_identity` test.</pre>

Uncertainty:
<pre>Consolidating to one canonical issue is a judgement call: #3 explicitly names export and CLI agreement while #4 is phrased only in terms of saved links, so #3 is the wider statement. Neither issue should be closed by this action — only cross-linked — and both issues are authored by the repository owner in a seeded demo repository, so they may be intentional fixtures rather than an accidental duplicate report.</pre>

Draft reply:
<pre>#3 and #4 describe the same requested behavior: opt-in fragment-free URL identity with current defaults preserved. Proposing we track it on #3 (it also states the export/CLI agreement requirement) and cross-link #4 rather than close either for now. No code change is implied by this link.</pre>

Observed PR heads:
<pre>{}</pre>

</details>

<details><summary>A2 · duplicate_pr</summary>

<pre>These are two implementations of one change, not complementary work. Both edit only bookmarks/urls.py and tests/test_bookmarks.py from the same base commit, add the identical keyword-only parameter and the identical test, and differ only in whether the conditional is inlined in the urlunsplit call (#9) or assigned to a local `fragment` first (#10). Merging both would conflict and add nothing.</pre>

Targets: https://github.com/gvago/oss-maintainer-demo/pull/9, https://github.com/gvago/oss-maintainer-demo/pull/10

Evidence:
<pre>PR #9 diff, bookmarks/urls.py: `def normalize_url(value: str, *, strip_fragment: bool = False)` with return `urlunsplit((..., parts.query, &quot;&quot; if strip_fragment else parts.fragment))`.</pre>
<pre>PR #10 diff, bookmarks/urls.py: same signature, then `fragment = parts.fragment if not strip_fragment else &quot;&quot;` passed to urlunsplit — same observable behavior.</pre>
<pre>Both PRs add the byte-identical test `test_optional_fragment_identity`, asserting strip_fragment=True strips `#one` and the default preserves it.</pre>
<pre>Both declare base_commit e565ba08587117166a9ba46e00d211879fc55857 and target main; observed heads ddb9ea2 (#9) and 67a58c0 (#10).</pre>

Uncertainty:
<pre>Choosing which branch to keep is the maintainer&#x27;s call and is not decided here. Neither PR satisfies issues #3/#4 in full (see A7), so consolidation does not close those issues. Do not rebase or force-push the branch that is not selected; the contributors&#x27; branches should be left alone until they respond.</pre>

Draft reply:
<pre>#9 and #10 implement the same change: a keyword-only `strip_fragment=False` on `normalize_url`, with the same test. The only difference is whether the conditional is inlined or assigned to a local first. Suggest we pick one, review it, and ask the other author to review rather than resubmit. Flagging now so neither of you spends more time on the same slice. Both PRs cover only the normalizer — exporter and CLI propagation is still open work (see #3/#4).</pre>

Observed PR heads:
<pre>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/10&quot;: &quot;67a58c07cb73721b1d8ce0b04742e185a1fd7712&quot;, &quot;https://github.com/gvago/oss-maintainer-demo/pull/9&quot;: &quot;ddb9ea26e5f16da5074123c0b8e4ad4ccd92b96e&quot;}</pre>

</details>

<details><summary>A3 · demo_control</summary>

<pre>Both PRs self-identify in their bodies as contribution-review experiments to be kept unmerged, and sit on experiment/* branches. #26 is the deliberately noncompliant arm (third-party `tabulate` import, lowercasing URLs instead of using the shared normalizer, no test) and #27 is the compliant control whose export_csv matches PR #11&#x27;s implementation. The overlap between #27 and #11 is the intended design of the fixture pair, not an accidental duplicate implementation.</pre>

Targets: https://github.com/gvago/oss-maintainer-demo/pull/26, https://github.com/gvago/oss-maintainer-demo/pull/27

Evidence:
<pre>PR #26 body: &#x27;Contribution-review experiment; keep unmerged.&#x27; Branch experiment/thin-review-md-bad.</pre>
<pre>PR #27 body: &#x27;Contribution-review experiment; keep unmerged.&#x27; Branch experiment/thin-review-md-control.</pre>
<pre>PR #26 diff adds `from tabulate import tabulate` and `[[url.lower()] for url in dict.fromkeys(urls)]` — bypasses `normalize_url` and adds a runtime dependency.</pre>
<pre>PR #27 diff to bookmarks/exports.py and tests/test_bookmarks.py matches PR #11&#x27;s diff for the same two files, which is expected for a control copy of the compliant implementation.</pre>

Uncertainty:
<pre>Low. Both PRs state their purpose explicitly. The only open question is housekeeping: whether to label them so they are excluded from future triage passes.</pre>

Draft reply:
<pre>#26 and #27 are the contribution-review fixture pair (noncompliant arm and clean control) and both bodies say keep unmerged. No merge, close or consolidation proposed. #27 overlapping #11 is expected — #11 on feat/csv-library is the production CSV work. Suggest adding a `demo-fixture` label so these stop showing up as review candidates.</pre>

Observed PR heads:
<pre>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/26&quot;: &quot;75a0d52fadd2cb6d4b7787227ee6c66881c1ef3f&quot;, &quot;https://github.com/gvago/oss-maintainer-demo/pull/27&quot;: &quot;d63ad1a02f2282509aebb3468b6f05425969295e&quot;}</pre>

</details>

<details><summary>A4 · already_fixed</summary>

<pre>Issue #8 is confirmed fixed on current main by both source and executed behavior at the same SHA. bookmarks/urls.py at 13d048b excludes (https, 443) from the authority, and the recorded verification at that same SHA ran the issue&#x27;s own reproduction and the full test suite: the reproduction emitted a single normalized bookmark and 6 tests passed. This rests on current-main evidence, not on the merged-history hit for PR #2, which only corroborates when the behavior landed.</pre>

Targets: https://github.com/gvago/oss-maintainer-demo/issues/8

Evidence:
<pre>behavior_verification at sha 13d048b40310b3d7154ec195896de723c75f3abd, status &#x27;passed&#x27;: reproduction_command `python3 -m bookmarks https://example.com:443/docs https://example.com/docs` → actual_output [&quot;https://example.com/docs&quot;] (one entry).</pre>
<pre>behavior_verification tests_command `python3 -m unittest discover -s tests -v` at the same SHA: &#x27;Ran 6 tests in 0.075s / OK&#x27;, including test_default_ports_share_identity.</pre>
<pre>current_main bookmarks/urls.py (sha 13d048b, commit_date 2026-10-11T16:07:50+00:00): `if port is not None and (parts.scheme, port) not in {(&quot;http&quot;, 80), (&quot;https&quot;, 443)}: authority += f&quot;:{port}&quot;` — :443 is dropped for https before the authority is assembled.</pre>
<pre>Merged PR #2 (fix/default-ports, merge_commit e565ba0) description: &#x27;Closes #1. Fix URL identity in the shared normalizer; JSON export and CLI inherit the same behavior.&#x27;</pre>

Uncertainty:
<pre>The evidence establishes the bug is fixed; it does not constitute approval to close. The verification covers the reported :443 case and the committed suite at 13d048b — it does not cover the reporter&#x27;s original environment or any case beyond the one in the issue body. If the reporter has a variant that still reproduces, keep the issue open.</pre>

Draft reply:
<pre>This looks resolved on current main. `normalize_url` in bookmarks/urls.py (sha 13d048b) excludes the default https port from the authority, and running your reproduction at that commit — `python3 -m bookmarks https://example.com:443/docs https://example.com/docs` — returns a single entry, `https://example.com/docs`. The committed suite at the same commit passes: `python3 -m unittest discover -s tests -v`, 6 tests, OK, including test_default_ports_share_identity. The behavior landed with #2. No need to re-run anything on your side — if you have a variant that still duplicates, paste it here and we&#x27;ll keep this open; otherwise this can be closed with a pointer to #2.</pre>

Observed PR heads:
<pre>{}</pre>

</details>

<details><summary>A5 · link_issue_pr</summary>

<pre>PR #11 implements every acceptance item issue #5 lists, and #5 is explicitly scoped to the library change only (&#x27;Keep this library change separate from CLI wiring&#x27;), so the existing Closes keyword is appropriate here — unlike the partial work in A7.</pre>

Targets: https://github.com/gvago/oss-maintainer-demo/issues/5, https://github.com/gvago/oss-maintainer-demo/pull/11

Evidence:
<pre>Issue #5 body: &#x27;Add a CSV exporter with a url header, stable first-seen deduplication, shared URL normalization and correct quoting. Keep this library change separate from CLI wiring.&#x27;</pre>
<pre>PR #11 diff adds export_csv writing a `[&quot;url&quot;]` header via csv.writer, dedupes with `dict.fromkeys(normalize_url(url) for url in urls)` — header, stdlib quoting, shared normalization and first-seen dedup all present.</pre>
<pre>PR #11 adds test_csv_export asserting `[[&quot;url&quot;], [&quot;https://example.com/a?x=1,2&quot;]]`, covering quoting of an embedded comma and case/scheme normalization.</pre>
<pre>current_main bookmarks/exports.py (sha 13d048b) defines only export_json, so this is new work, not a reimplementation.</pre>

Uncertainty:
<pre>Low on scope match. Whether the single-column shape is what spreadsheet users ultimately want (vs. title/date columns later) is a product question #5 does not raise.</pre>

Draft reply:
<pre>Linking #11 to #5 — the PR body already carries &#x27;Closes #5&#x27; and the diff covers all four stated requirements: url header, stdlib csv quoting, shared `normalize_url`, first-seen dedup. Note #11 is also the base for #12 (CLI wiring, #6); see the review order in A8.</pre>

Observed PR heads:
<pre>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/11&quot;: &quot;b9dab92614d3b0c4e7fb61531110d54bf10e6694&quot;}</pre>

</details>

<details><summary>A6 · link_issue_pr</summary>

<pre>PR #12 adds exactly what issue #6 asks for — `--format csv` routed through the library exporter with JSON preserved as the default — plus stdout encoding/newline handling and CLI-level tests. Its Closes #6 keyword is accurate for its own scope, but the link should record that #6 cannot land until #11 does, since #12 is based on feat/csv-library.</pre>

Targets: https://github.com/gvago/oss-maintainer-demo/issues/6, https://github.com/gvago/oss-maintainer-demo/pull/12

Evidence:
<pre>Issue #6 body: &#x27;Add --format csv to the CLI using the library exporter. Related library work is required; default JSON behavior must remain compatible.&#x27;</pre>
<pre>PR #12 diff bookmarks/__main__.py: `parser.add_argument(&quot;--format&quot;, choices=(&quot;json&quot;, &quot;csv&quot;), default=&quot;json&quot;)` and `exporter = export_csv if args.format == &quot;csv&quot; else export_json` — JSON stays the default and the library exporter is reused.</pre>
<pre>PR #12 tests add test_cli_exports_csv and test_csv_cli_uses_utf8_output (PYTHONIOENCODING=ascii, asserts `url\r\nhttps://example.com/café\r\n`), covering the stdout encoding path.</pre>
<pre>PR #12 target_branch is feat/csv-library and its base_commit b9dab92 equals PR #11&#x27;s observed head.</pre>

Uncertainty:
<pre>Low on scope match. One reviewable detail rather than a blocker: `sys.stdout.reconfigure` is called after `exporter(args.urls)` has already produced the string, so ordering relative to any future streaming write deserves a look at review time.</pre>

Draft reply:
<pre>Linking #12 to #6 — it adds `--format csv` through the library exporter with JSON still the default, and includes an ASCII-stdout regression. #6 stays open until #11 merges and #12 is retargeted to main; see A8 for the order.</pre>

Observed PR heads:
<pre>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/11&quot;: &quot;b9dab92614d3b0c4e7fb61531110d54bf10e6694&quot;, &quot;https://github.com/gvago/oss-maintainer-demo/pull/12&quot;: &quot;41bd59c16d4a37fecf3367e24119e8c6b32c3eb7&quot;}</pre>

</details>

<details><summary>A7 · link_issue_pr</summary>

<pre>Keep the existing Refs links and do not upgrade either PR to a closing keyword. Both PRs stop at the normalizer: neither threads strip_fragment through export_json or the CLI, so issue #3&#x27;s explicit &#x27;shared normalizer, export and CLI should agree&#x27; and issue #4&#x27;s saved-link workflow are unmet. This holds even if #9 and #10 are consolidated under A2 — consolidation merges two partial implementations into one partial implementation.</pre>

Targets: https://github.com/gvago/oss-maintainer-demo/issues/3, https://github.com/gvago/oss-maintainer-demo/issues/4, https://github.com/gvago/oss-maintainer-demo/pull/9, https://github.com/gvago/oss-maintainer-demo/pull/10

Evidence:
<pre>PR #9 body: &#x27;Refs #3. ... This is the first library slice; exporter and CLI wiring are separate work.&#x27;</pre>
<pre>PR #10 body: &#x27;Refs #4. ... URL identity stays in the shared helper.&#x27;</pre>
<pre>Neither PR&#x27;s diff touches bookmarks/exports.py or bookmarks/__main__.py; both change only bookmarks/urls.py and tests/test_bookmarks.py.</pre>
<pre>current_main bookmarks/exports.py calls `normalize_url(url)` with no keyword arguments and bookmarks/__main__.py exposes no corresponding flag, so an opt-in at the helper is unreachable from export or CLI.</pre>
<pre>Issue #3 body requires that &#x27;Shared normalizer, export and CLI should agree.&#x27;</pre>

Uncertainty:
<pre>Depends on the A1/A2 outcomes for which issue and which PR end up canonical. The classification itself — partial, not complete — does not depend on that choice.</pre>

Draft reply:
<pre>Keeping these as Refs links rather than Closes: #9 and #10 add the opt-in to `normalize_url` only, and neither wires it through `export_json` or the CLI, which #3 explicitly requires. The helper slice is reviewable and mergeable on its own; the issue stays open until export and CLI can opt in and there&#x27;s an end-to-end test. Please don&#x27;t add Closes/Fixes to the PR body in the meantime.</pre>

Observed PR heads:
<pre>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/10&quot;: &quot;67a58c07cb73721b1d8ce0b04742e185a1fd7712&quot;, &quot;https://github.com/gvago/oss-maintainer-demo/pull/9&quot;: &quot;ddb9ea26e5f16da5074123c0b8e4ad4ccd92b96e&quot;}</pre>

</details>

<details><summary>A8 · stack_order</summary>

<pre>#12 is stacked on #11, structurally and functionally: its git base is feat/csv-library at #11&#x27;s head, and its diff imports export_csv, which does not exist on current main. Review #11 first; #12 is then a small retarget-and-review. This is a dependency, not duplicate work.</pre>

Targets: https://github.com/gvago/oss-maintainer-demo/pull/11, https://github.com/gvago/oss-maintainer-demo/pull/12

Evidence:
<pre>PR #12 base_commit b9dab92614d3b0c4e7fb61531110d54bf10e6694 is identical to PR #11&#x27;s observed head_sha; PR #12 target_branch is feat/csv-library.</pre>
<pre>PR #12 diff bookmarks/__main__.py: `from bookmarks.exports import export_csv, export_json`.</pre>
<pre>current_main bookmarks/exports.py (sha 13d048b) contains only export_json — the import would fail against main today.</pre>
<pre>PR #12 body: &#x27;Depends on #11 (CSV library). ... Review #11 and this PR together; they are complementary, not duplicates.&#x27;</pre>

Uncertainty:
<pre>The retarget of #12 to main after #11 merges is the contributor&#x27;s to perform (or the maintainer&#x27;s with their agreement) — not something to automate. If #11 is revised during review, #12&#x27;s test expectations around CSV line endings may need a re-run at its new head.</pre>

Draft reply:
<pre>These two are a stack, not overlapping work: #12&#x27;s git base is #11&#x27;s head and it imports `export_csv`, which isn&#x27;t on main yet. Proposed order — review and merge #11 (library, closes #5) first, then #12 retargets to main and the CLI wiring reviews quickly on top. Happy to look at both in one sitting as the author suggests, but #11 should land first.</pre>

Observed PR heads:
<pre>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/11&quot;: &quot;b9dab92614d3b0c4e7fb61531110d54bf10e6694&quot;, &quot;https://github.com/gvago/oss-maintainer-demo/pull/12&quot;: &quot;41bd59c16d4a37fecf3367e24119e8c6b32c3eb7&quot;}</pre>

</details>

<details><summary>A9 · request_followup</summary>

<pre>Issue #7 asks for explicit regression coverage that query names, values, order and repetitions survive normalization and all exports. Nothing in the live open-PR set addresses it: the closest existing assertion is incidental. The merged-history lookup for #7 returned PR #2, which is the default-port fix and does not add query coverage. This is unclaimed work, so the action is a call for a contributor, not a closure.</pre>

Targets: https://github.com/gvago/oss-maintainer-demo/issues/7

Evidence:
<pre>Issue #7 body: &#x27;Add explicit regression coverage proving names, values, order and repetitions are preserved by normalization and all exports.&#x27;</pre>
<pre>No open PR in this evidence set references #7; the only query-bearing assertion is test_csv_export in #11/#27 using `?x=1,2`, which exercises CSV comma quoting rather than name/value/order/repetition preservation.</pre>
<pre>current_main bookmarks/urls.py passes `parts.query` to urlunsplit unmodified, so the behavior appears correct today — what is missing is the test that pins it.</pre>
<pre>Merged-history similarity for issue #7 returned only PR #2 (fix/default-ports, merged), a different concern; merged-history similarity searches merged PRs and cannot enumerate open PRs, so it was never going to surface in-flight work here.</pre>

Uncertainty:
<pre>The open-PR view here is a live list/get read, so the absence of a #7 PR reflects the backlog as observed, not a retrieval gap. Not verified: whether repeated keys and ordering actually hold for every edge case (e.g. percent-encoded separators) — the proposed tests exist precisely to establish that.</pre>

Draft reply:
<pre>#7 has no PR in flight. The behavior looks right on main — `normalize_url` passes the query through untouched — but there&#x27;s no test pinning it, so a future refactor could drop it silently. Looking for a contributor to add regression coverage asserting: parameter names and values preserved verbatim, original order preserved, repeated keys preserved, and the same holding through `export_json` (and `export_csv` once #11 lands). Small, self-contained, good first PR.</pre>

Observed PR heads:
<pre>{}</pre>

</details>

<details><summary>A10 · review_next</summary>

<pre>Ranked by what unblocks other work and how far a mistake could reach. #13 is README-only with no runtime surface. #11 is a self-contained additive library function with its own test and is the blocker for #12 and for issue #6. #12 comes third because it only becomes reviewable against main after #11 lands, and it touches the CLI entry point — the widest runtime surface of the three. #9/#10 are deliberately excluded until the A2 duplicate choice is made, so review effort isn&#x27;t spent twice.</pre>

Targets: https://github.com/gvago/oss-maintainer-demo/pull/13, https://github.com/gvago/oss-maintainer-demo/pull/11, https://github.com/gvago/oss-maintainer-demo/pull/12

Evidence:
<pre>PR #13 diff touches only README.md (+8, documentation-only); body: &#x27;Runtime behavior unchanged; checks: 6 tests passed.&#x27;</pre>
<pre>PR #11 adds export_csv plus test_csv_export and touches no existing function; current_main bookmarks/exports.py shows export_json unchanged alongside it.</pre>
<pre>PR #12 base_commit equals PR #11&#x27;s head and its diff modifies bookmarks/__main__.py, the single CLI entry point — it also mutates global stdout state via `sys.stdout.reconfigure(encoding=&quot;utf-8&quot;, newline=&quot;&quot;)`.</pre>
<pre>PRs #9 and #10 are the unresolved duplicate pair in A2; PRs #26/#27 are keep-unmerged fixtures per A3, so neither belongs in a review queue.</pre>

Uncertainty:
<pre>This is a dependency-and-blast-radius ordering only; no time estimate or saving is claimed. The blast-radius and review-time labels on these PRs are Qodo review output and were not re-derived here. If the maintainer&#x27;s priority is unblocking issue #6 specifically, #11 can move ahead of #13 with no downside.</pre>

Draft reply:
<pre>Suggested order for the next review pass: (1) #13 — README only, nothing to break; (2) #11 — self-contained CSV exporter with its own test, and the blocker for both #12 and issue #6; (3) #12 — after #11 merges and it retargets to main; it changes the CLI entry point and reconfigures stdout, so it wants the most careful read. Holding #9/#10 out of the queue until we pick one of them (see A2), and #26/#27 are keep-unmerged fixtures.</pre>

Observed PR heads:
<pre>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/11&quot;: &quot;b9dab92614d3b0c4e7fb61531110d54bf10e6694&quot;, &quot;https://github.com/gvago/oss-maintainer-demo/pull/12&quot;: &quot;41bd59c16d4a37fecf3367e24119e8c6b32c3eb7&quot;, &quot;https://github.com/gvago/oss-maintainer-demo/pull/13&quot;: &quot;ef111e70f732864621b2558722ad91ccbd5df73a&quot;}</pre>

</details>

## Data gaps

<pre>Only three current-main files were retrieved (bookmarks/urls.py, bookmarks/exports.py, bookmarks/__main__.py). tests/test_bookmarks.py was not fetched from main, so the committed test set is known only through PR diffs and the recorded verification run, not read directly.</pre>
<pre>behavior_verification covers issue #8 only: the committed suite at sha 13d048b and the :443 reproduction. No executed evidence exists for the strip_fragment propagation path (#3/#4, #9/#10), the CSV exporter (#11), the CLI flag (#12) or query-parameter preservation (#7); PR-body test counts for those are author reports.</pre>
<pre>No review state, comments or CI status is present for any open PR in this evidence set, so approvals, requested changes and check failures could not be factored into the review ordering in A10.</pre>
<pre>PR #28 head bd8f4b3 carries no recorded test run; its body&#x27;s 11-passing-test claim is unverified here, and tools/maintainer_inbox.py and tests/test_maintainer_inbox.py were read from the PR diff rather than from an executed state.</pre>
<pre>Blast-radius and review-time labels on the open PRs are pre-existing Qodo review output carried in the change metadata; they were not independently re-derived from the diffs.</pre>
<pre>Every open PR and issue in this evidence set is authored by the repository owner in a seeded demo repository, so author-based signals (independent contributors, competing teams) cannot distinguish accidental duplication from intentional fixtures; A1 and A2 rest on diff and acceptance-criteria comparison alone.</pre>
<pre>The merged-history lookups returned a single merged PR (#2) per issue. That bounds what merged history contributed here and nothing more — it is not evidence about open-PR coverage, which came from live list/get reads, and not evidence of index staleness.</pre>
