# Maintainer Inbox

<p>8 open PRs · 6 open issues · Observed 2026-10-12T07:42:41.629392+00:00</p>

<p>Six open issues, seven open PRs. #9 and #10 are byte-equivalent `strip_fragment` implementations serving duplicate issues #3/#4 — keep one, close the other. #11→#12 is a real stack (#12 is based on `feat/csv-library`), not a duplicate. Issue #8 (:443 collapsing) is already fixed on main by merged PR #2 with regression coverage. PR #12&#x27;s review is stale against its head but both findings are implemented. PRs #26/#27 are seeded experiment/control — keep unmerged.</p>

All actions below are proposed, not approved or applied.

<details><summary>dup-issues-3-4 · duplicate_issue</summary>

<p>Both ask for opt-in fragment-free bookmark identity with current behavior kept as default, differing only in wording (#3 frames it as JSON export, #4 as saved links). They have attracted two independent PRs implementing the identical helper change. Consolidating onto #3 (which also names exporter and CLI agreement) prevents a third parallel attempt.</p>

Targets: https://github.com/gvago/oss-maintainer-demo/issues/3, https://github.com/gvago/oss-maintainer-demo/issues/4

Evidence:
<p>issues/3 body: &#x27;Add opt-in fragment-free identity while keeping current behavior the default. Shared normalizer, export and CLI should agree.&#x27;</p>
<p>issues/4 body: &#x27;Need an optional way to save one document entry rather than each section. Existing defaults must stay compatible.&#x27;</p>
<p>PR #9 &#x27;Refs #3&#x27; and PR #10 &#x27;Refs #4&#x27; produce the same normalize_url(..., strip_fragment=False) signature</p>

Uncertainty:
<p>Maintainer may prefer #4 as the canonical issue since it is user-facing; the technical content is interchangeable.</p>

Draft reply:
<p>Closing as a duplicate of #3, which covers the same opt-in fragment-free identity and additionally asks that the normalizer, exporter and CLI agree. Tracking all fragment work there — no scope is lost.</p>

Observed PR heads:
<p>{}</p>

</details>

<details><summary>dup-prs-9-10 · duplicate_pr</summary>

<p>The diffs are functionally identical: same keyword-only `strip_fragment=False` on normalize_url, same emptied fragment in urlunsplit, same test_optional_fragment_identity assertions. Only the inline-vs-temporary-variable style differs. Recommend keeping #10 — its review attached the open requirement gap about export_json/CLI not opting in, which is the work still outstanding.</p>

Targets: https://github.com/gvago/oss-maintainer-demo/pull/9, https://github.com/gvago/oss-maintainer-demo/pull/10

Evidence:
<p>PR #9 diff: `&quot;&quot; if strip_fragment else parts.fragment` in urlunsplit; tests/test_bookmarks.py +4</p>
<p>PR #10 diff: `fragment = parts.fragment if not strip_fragment else &quot;&quot;`; tests/test_bookmarks.py +4, identical assertions</p>
<p>PR #10 head 67a58c0 review: 1 High &#x27;Saved section links remain separate&#x27; requirement gap, unresolved</p>

Uncertainty:
<p>Choice between #9 and #10 is a style preference; #9 has a clean review (0 findings) while #10 carries the useful open gap finding.</p>

Draft reply:
<p>#9 and #10 implement the same change — identical `strip_fragment` keyword on normalize_url and identical tests. Keeping #10, since its review already flags the remaining gap: export_json and the CLI never opt in. Closing #9 as a duplicate; thanks for both.</p>

Observed PR heads:
<p>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/10&quot;: &quot;67a58c07cb73721b1d8ce0b04742e185a1fd7712&quot;, &quot;https://github.com/gvago/oss-maintainer-demo/pull/9&quot;: &quot;ddb9ea26e5f16da5074123c0b8e4ad4ccd92b96e&quot;}</p>

</details>

<details><summary>fixed-issue-8 · already_fixed</summary>

<p>Current main already drops default ports: normalize_url skips the port when (scheme, port) is (&#x27;http&#x27;,80) or (&#x27;https&#x27;,443), so https://example.com:443/docs and https://example.com/docs normalize identically. Merged PR #2 &#x27;fix: canonicalize default HTTP and HTTPS ports&#x27; (Closes #1) introduced this, and tests/test_bookmarks.py retains test_default_ports_share_identity covering :443, :80 and IPv6.</p>

Targets: https://github.com/gvago/oss-maintainer-demo/issues/8

Evidence:
<p>bookmarks/urls.py@main L18: `if port is not None and (parts.scheme, port) not in {(&quot;http&quot;, 80), (&quot;https&quot;, 443)}:`</p>
<p>tests/test_bookmarks.py@main test_default_ports_share_identity asserts (&#x27;https://example.com:443/a&#x27;,&#x27;https://example.com/a&#x27;) equal</p>
<p>Merged PR #2 (head 54ac978, merge e565ba0) &#x27;fix: canonicalize default HTTP and HTTPS ports&#x27;, Closes #1</p>

Uncertainty:
<p>Verified by reading current source and the merged PR record; no test run was executed in this triage.</p>

Draft reply:
<p>This looks resolved on main. normalize_url already drops default :80/:443, landed in #2 (Closes #1), and tests/test_bookmarks.py has a regression case asserting https://example.com:443/a and https://example.com/a share an identity. Closing — please reopen with a failing example if you still see duplicates.</p>

Observed PR heads:
<p>{}</p>

</details>

<details><summary>stack-11-12 · stack_order</summary>

<p>These are complementary, not duplicates. #11 adds the CSV exporter library (Closes #5); #12 is based on branch feat/csv-library and contains only CLI wiring for --format csv (Closes #6). #12&#x27;s base_commit b9dab92 is exactly #11&#x27;s head. Merge #11 first, then verify and retarget #12 to main.</p>

Targets: https://github.com/gvago/oss-maintainer-demo/pull/11, https://github.com/gvago/oss-maintainer-demo/pull/12

Evidence:
<p>PR #12 base_branch=feat/csv-library, base_commit=b9dab92614d3b0c4e7fb61531110d54bf10e6694</p>
<p>PR #11 head_commit=b9dab92614d3b0c4e7fb61531110d54bf10e6694</p>
<p>PR #11 &#x27;Closes #5 ... CLI wiring is a separate change&#x27;; PR #12 &#x27;Depends on #11 ... contains only CLI wiring. Closes #6&#x27;</p>

Uncertainty:
<p>Ordering is established. After #11 merges, verify the base and retarget #12 to main if necessary; automatic retargeting is not established.</p>

Draft reply:
<p>These changes are complementary. Review #11 (CSV library) first, then verify and retarget #12 to main for CLI review. No automatic rebase or retarget is performed.</p>

Observed PR heads:
<p>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/11&quot;: &quot;b9dab92614d3b0c4e7fb61531110d54bf10e6694&quot;, &quot;https://github.com/gvago/oss-maintainer-demo/pull/12&quot;: &quot;41bd59c16d4a37fecf3367e24119e8c6b32c3eb7&quot;}</p>

</details>

<details><summary>link-10-issue · link_issue_pr</summary>

<p>PR #10 is a partial implementation: it adds the opt-in to the shared normalizer only. export_json still calls normalize_url(url) with the default and the CLI exposes no flag, so the user-visible behavior in #3/#4 is unchanged. Keep the Refs link rather than a closing keyword, and track the exporter/CLI wiring as follow-up.</p>

Targets: https://github.com/gvago/oss-maintainer-demo/pull/10, https://github.com/gvago/oss-maintainer-demo/issues/3

Evidence:
<p>PR #10 review finding &#x27;Saved section links remain separate&#x27; (High, Requirement gap, unresolved) cites bookmarks/exports.py[6-8] and bookmarks/__main__.py[7-11]</p>
<p>PR #10 description: &#x27;Refs #4 ... preserve existing behavior by default&#x27;</p>
<p>Qodo review context sources on #10 link ticket issues/4</p>

Uncertainty:
<p>Whether the maintainer wants exporter/CLI wiring in this PR or as a separate slice; the author framed it as a library slice.</p>

Draft reply:
<p>Keeping this as Refs #3 rather than Closes — the opt-in exists in the normalizer but export_json and the CLI never pass strip_fragment=True, so saved section links still duplicate. Happy to merge the library slice as-is and track the exporter/CLI wiring plus an export-path regression test separately.</p>

Observed PR heads:
<p>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/10&quot;: &quot;67a58c07cb73721b1d8ce0b04742e185a1fd7712&quot;}</p>

</details>

<details><summary>review-next-12 · review_next</summary>

<p>The stored review for #12 completed against commit 7f0f964, but the current head is 41bd59c — the review is stale relative to head. Both recorded findings (non-ASCII UnicodeEncodeError on CSV stdout, Windows \r\r\n double newline) are marked implemented, and the head description claims UTF-8 stdout with newline translation disabled. Re-review at head to confirm no new findings before merging the stack.</p>

Targets: https://github.com/gvago/oss-maintainer-demo/pull/12

Evidence:
<p>get-pr-review-findings #12: review_session.commit_sha=7f0f964d367ab2f770e4d06347fc29bcb3ef818c, status=completed</p>
<p>PR #12 head_sha=41bd59c16d4a37fecf3367e24119e8c6b32c3eb7</p>
<p>Findings 24c5ecb2 (Reliability) and fa8c6cd1 (Correctness) both attribution_status=implemented</p>

Uncertainty:
<p>Implementation status is attributed, not independently re-verified at 41bd59c; a fresh review run at head would confirm.</p>

Draft reply:
<p>Note for reviewers: the recorded Qodo review on #12 ran against 7f0f964 and head is now 41bd59c. Both prior findings (ASCII-stdout UnicodeEncodeError, Windows \r\r\n rows) are marked implemented, so this is a re-review at head rather than open blockers — #11 still goes first.</p>

Observed PR heads:
<p>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/12&quot;: &quot;41bd59c16d4a37fecf3367e24119e8c6b32c3eb7&quot;}</p>

</details>

<details><summary>followup-issue-7 · request_followup</summary>

<p>Still valid and not covered by any open PR. Current tests assert query preservation only via a single &#x27;?x=1&#x27; case inside test_url_identity; there is no coverage of repeated keys, parameter order or signature-bearing values, and none of the open PRs touch query handling. Worth pairing with the CSV work in #11 so the exporter path is covered too.</p>

Targets: https://github.com/gvago/oss-maintainer-demo/issues/7

Evidence:
<p>tests/test_bookmarks.py@main: only query assertion is normalize_url(&#x27;HTTPS://Example.COM/articles?x=1#intro&#x27;)</p>
<p>bookmarks/urls.py@main passes parts.query through urlunsplit untouched</p>
<p>No open PR (#9,#10,#11,#12,#13,#26,#27) modifies query handling</p>

Uncertainty:
<p>Behavior appears correct by inspection; the issue is coverage only, so this is a test-authoring request, not a bug report.</p>

Draft reply:
<p>Still open and unclaimed. Reading main, query strings pass through urlunsplit untouched, so this is a coverage gap rather than a bug: we only assert &#x27;?x=1&#x27;. Useful additions would be repeated keys, order preservation and a signature-looking value, asserted through normalize_url and the export paths. Happy to review a PR.</p>

Observed PR heads:
<p>{}</p>

</details>

<details><summary>demo-26-27 · demo_control</summary>

<p>Both are self-declared contribution-review experiment pairs on experiment/thin-review-md-* branches and say &#x27;keep unmerged&#x27;. #27 overlaps #11&#x27;s CSV scope but is a seeded control, not an accidental duplicate — it must not be folded into the #11/#12 stack decision or closed as a duplicate of it.</p>

Targets: https://github.com/gvago/oss-maintainer-demo/pull/26, https://github.com/gvago/oss-maintainer-demo/pull/27

Evidence:
<p>PR #26 head_branch=experiment/thin-review-md-bad, description: &#x27;Contribution-review experiment; keep unmerged.&#x27;</p>
<p>PR #27 head_branch=experiment/thin-review-md-control, description: &#x27;Contribution-review experiment; keep unmerged.&#x27;</p>
<p>PR #27 labels: Small blast radius; PR #26 labels: Medium blast radius</p>

Uncertainty:
<p>None — intent is stated explicitly in both descriptions.</p>

Draft reply:
<p>No action: #26 and #27 are the seeded experiment/control pair and stay open and unmerged. Excluded from the CSV duplicate analysis — #27&#x27;s CSV overlap with #11 is by design, not an accidental duplicate.</p>

Observed PR heads:
<p>{&quot;https://github.com/gvago/oss-maintainer-demo/pull/26&quot;: &quot;75a0d52fadd2cb6d4b7787227ee6c66881c1ef3f&quot;, &quot;https://github.com/gvago/oss-maintainer-demo/pull/27&quot;: &quot;d63ad1a02f2282509aebb3468b6f05425969295e&quot;}</p>

</details>

## Data gaps
