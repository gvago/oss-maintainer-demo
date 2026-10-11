# Contribution review

For every pull request, apply the `oss-contribution-workflow` steering skill.
Read the repository-root CONTRIBUTING.md for this PR before assessing contribution
compliance. That document is the sole source of contribution requirements; do not
copy requirements here, substitute remembered policies, or invent new requirements.

Follow the workflow in order: read the guidelines, determine applicable requirements,
inspect changed behavior and affected callers/tests, then report supported violations.
For each violation, include the guideline ID and exact text, actual changed file/line,
evidence, and a concrete fix. Preserve the steering skill as supporting evidence when
its workflow produced the finding; do not manufacture attribution or duplicate findings.

Substantive guideline violations warrant remediation_recommended; established data loss
or broken behavior warrants action_required. Respect all exceptions in CONTRIBUTING.md.
If the guidelines cannot be read, report the limitation rather than claiming compliance.
Never claim test execution from static source inspection.

For related-PR analysis, compare intended behavior, changed code and tests rather than
matching titles or file overlap. Related work is not necessarily redundant work.
