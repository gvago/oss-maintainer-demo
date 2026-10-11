# Maintainer demo: Gate · Focus · Loop

Start at the [pull request list](https://github.com/gvago/oss-maintainer-demo/pulls).
This is a seeded sandbox: all contributions were prepared for demonstration, not attributed to outside contributors.

## Focus — verified native Qodo output

| Example | Artifact | Observed result |
| --- | --- | --- |
| Small change | [PR #9](https://github.com/gvago/oss-maintainer-demo/pull/9) | Native Small blast radius and Less than 10 minutes labels; completed exact-head review with no findings. |
| Joint changes | [PR #11](https://github.com/gvago/oss-maintainer-demo/pull/11), [PR #12](https://github.com/gvago/oss-maintainer-demo/pull/12) | CSV library and its stacked CLI consumer. Both stay open. #12 names #11 and uses its branch as the Git base. Qodo labeled #12 Medium blast radius. |
| Low-effort documentation | [PR #13](https://github.com/gvago/oss-maintainer-demo/pull/13) | Less than 5 minutes label; completed review recorded with skip effort. Not an enforcement negative control. |
| Requirement gap | [PR #10](https://github.com/gvago/oss-maintainer-demo/pull/10) | Qodo linked issue #4 and flagged that saved-link export/CLI cannot opt into the new normalizer behavior. Leave the finding visible. |

The blast radius labels were produced by Qodo, not preassigned by a seed script.
The documented levels are Small, Medium and Large. No Large-classification or
blast-radius-dependent approver gate has been demonstrated here.

## Wisdom — an agent workflow, not a native duplicate-PR feature

Use the official Codebase Wisdom skill in a coding agent connected to this repository's
Qodo workspace. Give it the following task (no custom classifier or extra service required):

> I have 15 minutes to maintain gvago/oss-maintainer-demo. Use Qodo Codebase Wisdom to
> inspect all open issues and PRs and relevant merged history. Compare PR behavior,
> actual diffs and tests, not titles or file overlap alone. Identify duplicate PRs,
> complementary/dependent PRs, issue-to-PR links, already-fixed issues, and partial
> implementations. Return a linked table and the smallest recommended maintainer actions.
> Read-only: do not close issues, close PRs, merge, change labels or post comments.

Available read workflow, verified through the installed CLI:

```sh
qodo read codebase list-prs --repo gvago/oss-maintainer-demo --state open --json
qodo read codebase list-issues --repo gvago/oss-maintainer-demo --state open --json
qodo read codebase get-pr --repo gvago/oss-maintainer-demo --number 9 --json
qodo read codebase get-pr --repo gvago/oss-maintainer-demo --number 10 --json
qodo read codebase get-pr --repo gvago/oss-maintainer-demo --number 11 --json
qodo read codebase get-pr --repo gvago/oss-maintainer-demo --number 12 --json
qodo read pull-request similar --repo gvago/oss-maintainer-demo --query 'Duplicate bookmarks caused by explicit HTTPS port 443' --json
```

`pull-request similar` searches merged history only; it does not directly detect duplicate
open PRs. Open-PR comparison requires the agent to retrieve and reason over their diffs.
Recheck tool help in Dana's environment before relying on local command availability.

### Investigation already performed through Qodo

- **#9 and #10 are duplicate library implementations:** both add keyword-only
  `strip_fragment=False`, remove the fragment only when enabled, and add the same
  opt-in/default tests. The implementation-expression difference is not a second capability.
  Neither wires the option through JSON export or CLI. Choose one; do not merge both.
- **#3 and #4 overlap:** both ask for fragment-insensitive saved-link identity. #9/#10
  implement only the shared-helper slice, not the full saved-bookmark workflow.
- **#11 and #12 are complementary:** #11 implements CSV output; #12 calls it from the CLI.
  They map to #5 and #6 respectively. Review library first, consumer second.
- **#8 is already fixed:** the semantic merged-history query returned merged PR #2.
  Running #8's reproduction on current main returned one normalized bookmark. Propose
  closure with a link to #2; leave #8 open until the maintainer approves cleanup.
- **#7 must stay open:** it asks for broader query-preservation regression coverage.
  #14 strips queries instead, so it does not implement #7's intended behavior.

These are agent conclusions grounded in Qodo retrieval, not automatic PR Triage labels.
A live Qodo PR-chat question on #9 could analyze #9 but reported that it could not access
#10's diff in that chat context. Do not present that chat surface as demonstrated
cross-PR duplicate detection. Use the coding-agent Wisdom workflow above.

## Loop — real history and accepted fixes

[PR #2](https://github.com/gvago/oss-maintainer-demo/pull/2) was tested, reviewed by Qodo
at its exact head with zero findings, and merged. The maintainer's discussion records why
default ports are redundant while nondefault ports and queries remain meaningful.
Qodo's indexed history contains this PR and returns it for a semantically phrased old report.

Qodo also found UTF-8 stdout and Windows newline problems on #12. A follow-up commit
adds an ASCII-stdout regression and disables CSV stdout newline translation. Local and
GitHub checks pass. Its stored findings were automatically marked implemented; a fresh
full review of the latest commit remains a separate check.

This proves retrieval of real decisions and review feedback, not automatic Rule Miner
learning from an artificially short history. No mined rule has been claimed.

## Gate — setup remains pending, do not present as working

- [CONTRIBUTING.md](CONTRIBUTING.md) holds the contribution contract.
- [skills/oss-contribution-contract/SKILL.md](skills/oss-contribution-contract/SKILL.md)
  defines a review lens for changed runtime code, with stable IDs and false-positive guards.
- [REVIEW.md](REVIEW.md) defines review focus and severity guidance.
- [.pr_agent.toml](.pr_agent.toml) enables skills, REVIEW.md, blast radius and time labels.
- [Draft #15](https://github.com/gvago/oss-maintainer-demo/pull/15) adds an uncovered runtime
  helper with a third-party import and separate URL identity; the existing tests still pass.
- [Draft #14](https://github.com/gvago/oss-maintainer-demo/pull/14) drops queries in the shared
  helper, with downstream impact and a failing existing test. Neither draft should merge.

The skill list currently returns no imported skill for this repo. Source files on main and
an enabled skills agent do not prove ingestion or enforcement. Browser access blocked
portal import and request-changes configuration during preparation.

### Complete before showing Gate

1. In the connected Qodo workspace, import rules and skills for **this repository only**.
2. Verify the skill is present, active, assigned only here, applied as Rules enforcement,
   and based on the current default-branch revision. Inspect extracted rules/relevance.
3. Set request-changes for actionable contribution violations using the deployment's actual
   PR Triage/settings UI. Verify the saved repository scope; do not alter global settings.
4. Open **fresh fixture-only PRs** from the enabled/ingested base rather than treating the
   existing drafts as post-ingestion proof. Keep these drafts for reproducible source.
5. Require a completed exact-head review with the relevant skill attribution/rule IDs,
   plus an actual GitHub `CHANGES_REQUESTED` review. A red CI check or generic bug is not enough.
6. Add a matching compliant runtime control; require no spurious contract finding.
7. If claiming merge blocking, configure and verify GitHub branch protection separately.
   Request changes alone is not automatic rejection/closure or guaranteed merge blocking.

Do not demo the request-changes gate until these checks pass.

## Source references

- [Blast radius](https://docs.qodo.ai/code-review/assess-risk-with-blast-radius)
- [Skills discovery and enforcement vs steering](https://docs.qodo.ai/governance/manage-skills-across-repositories)
- [REVIEW.md](https://docs.qodo.ai/governance/use-review-md)
- [Codebase Wisdom](https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-codebase-wisdom-skill)
