# Review focus

Treat CONTRIBUTING.md as the authoritative contribution contract and use the
oss-contribution-contract enforcement skill as the review lens. Do not invent additional
requirements or duplicate the same underlying finding across agents.

Prioritize changed runtime behavior, shared URL identity and downstream export/CLI callers.
Contribution-contract violations should be actionable, not cosmetic nits: missing regression
coverage or disallowed runtime imports require remediation; query data loss requires action.
Documentation-only changes do not need runtime regression tests.

Do not infer duplicate PRs from matching titles or overlapping files alone. Compare intended
behavior, changed code and tests. Related work is not necessarily redundant work.
Never claim test execution from static source inspection.
