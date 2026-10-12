# What good looks like

The inbox helps a maintainer choose the next action, not approve a merge.

- A real agent selects relevant Qodo tools from the live catalog, rather than a Python
  collector deciding the investigation in advance.
- Duplicate issues/PRs, complementary stacks and partial fixes are distinguished with
  specific source evidence. Prior fixes and current code guide already-fixed proposals.
- Existing Qodo findings, reviewed SHAs and native impact/time labels affect advice.
  Relevant historical accepted feedback is retrieved; irrelevant matches are rejected.
- Each action includes links, observed heads and a useful draft. Gaps only appear when
  missing context prevents a decision. No generic missing-CI warning.
- No contributor code execution, shell, external mutations or private implementation
  disclosure. The agent can only invoke scoped managed reads; all actions stay proposed.
- The trace proves actual tool use. Tests reject writes and other repositories; renderers
  preserve escaping/wrapping. The actual hosted run must generate downloadable artifacts.

Verified locally with real Qodo retrieval and Claude through the existing Qodo gateway.
The updated manual-main workflow must be exercised after merge; the old hosted run is
not evidence that this new agent-led version passed CI execution.
