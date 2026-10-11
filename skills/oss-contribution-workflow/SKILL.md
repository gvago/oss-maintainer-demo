---
name: oss-contribution-workflow
description: "For every pull request, read CONTRIBUTING.md and check the changed code and tests against its applicable contribution guidelines. Skip requirements that the guidelines exempt or that the diff does not affect."
license: MIT
metadata:
  author: gvago
  variant: review
  version: 1.1.0
---

# Contribution review workflow

1. Read the repository-root CONTRIBUTING.md for this PR. It is the only source
   of contribution requirements; do not substitute remembered rules or infer new ones.
2. Identify which requirements apply to the diff. Inspect changed behavior,
   affected callers and added or changed tests as needed to evaluate those requirements.
3. Report each supported violation with the guideline's ID and exact text,
   an actual changed file/line, evidence, and the smallest concrete remediation.
   Group duplicate reports of the same problem.
4. Respect the guideline's exceptions. Do not flag unchanged pre-existing code,
   invent missing-context violations, or claim to have executed tests.

Use remediation_recommended for substantive contribution-contract violations,
raising to action_required when the evidence establishes data loss or broken behavior.
If CONTRIBUTING.md cannot be read, explicitly report that review limitation rather
than pretending compliance was checked. This workflow does not post approvals,
close PRs, or modify its own instructions.
