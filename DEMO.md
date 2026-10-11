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

## Gate — Skill steering and request-changes verified

**Use [PR #19](https://github.com/gvago/oss-maintainer-demo/pull/19) for the demo.**
After switching only the skill application mode to steering (skill, contribution guidelines,
REVIEW.md and fixture code unchanged), Qodo completed the exact-head review and reported
**Bugs (0), Rule violations (0), Skill insights (3)**. All three structured findings cite
`oss-contribution-contract`, skill ID 1080:

- CONTRIB-01: new runtime exporter has no regression test.
- CONTRIB-02: third-party runtime import violates the dependency-free policy.
- CONTRIB-03: separate URL identity bypasses the shared normalizer; the finding also
  identifies query-value rewriting against CONTRIB-04.

Qodo submitted `CHANGES_REQUESTED` on that same commit. The old six-test suite passes,
so this demonstrates contribution review beyond a failing CI check.

**[PR #20](https://github.com/gvago/oss-maintainer-demo/pull/20) is the compliant control:**
seven tests pass, Qodo completed the exact-head review with zero findings, and no
request-changes vote appears. Skill metrics record two invocations; their findingsProduced
metric reports one and must not be confused with the three individual findings on #19.

The mode-switch experiment supports using steering for this demo. It is not a universal
claim that enforcement mode is broken, or an isolated test of REVIEW.md: REVIEW.md stayed
active in both arms. Main changed only in the runbook between arms; runtime/policy sources
and fixture diffs were held fixed. The earlier enforcement arm is recorded below.


Fresh post-import review examples:

| Example | Result |
| --- | --- |
| [#16: readable export](https://github.com/gvago/oss-maintainer-demo/pull/16) | Existing six tests pass, but Qodo finds a disallowed third-party import, alternate URL identity and missing regression coverage. Qodo submitted `CHANGES_REQUESTED` at the reviewed head. Small blast radius; 10–20 minute estimate. |
| [#17: query stripping](https://github.com/gvago/oss-maintainer-demo/pull/17) | Qodo traces query loss through JSON export and CLI and submits `CHANGES_REQUESTED` at the reviewed head. Medium blast radius; 10–20 minute estimate. |
| [#18: compliant CSV control](https://github.com/gvago/oss-maintainer-demo/pull/18) | Seven tests pass. Completed exact-head Qodo review returns zero findings and no request-changes review. |

These prove the configured finding-severity request-changes gate with a clean runtime control.
They do not yet prove that the imported contribution skill produced the findings: #16's
rule finding cites existing rule 8669, its other findings are generic bugs, and #17's
query-loss finding is generic. No contribution-skill citation appears in structured evidence.
Do not present generic detection as skill-attributed enforcement.

- [CONTRIBUTING.md](CONTRIBUTING.md) holds the contribution contract.
- [skills/oss-contribution-contract/SKILL.md](skills/oss-contribution-contract/SKILL.md)
  defines a review lens for changed runtime code, with stable IDs and false-positive guards.
- [REVIEW.md](REVIEW.md) defines review focus and severity guidance.
- [.pr_agent.toml](.pr_agent.toml) enables skills, REVIEW.md, blast radius and time labels.
- [Draft #15](https://github.com/gvago/oss-maintainer-demo/pull/15) adds an uncovered runtime
  helper with a third-party import and separate URL identity; the existing tests still pass.
- [Draft #14](https://github.com/gvago/oss-maintainer-demo/pull/14) drops queries in the shared
  helper, with downstream impact and a failing existing test. Neither draft should merge.

In the earlier enforcement arm, the imported skill was scoped only to this repository and
pinned to `5e859a7`, with extracted rules 13611, 13613, 13614 and 13615. Three were active;
13613 was inactive. Those runs did not establish source attribution. In the current steering
arm the full skill produced attributed findings, including CONTRIB-02, without changing
that inactive extracted rule.

### Boundaries and optional next experiments

- Keep the skill in steering for the proven demo; no simpler replacement is needed to
  deliver this result. A workflow-only skill that reads CONTRIBUTING.md is a separate,
  still-untested experiment.
- If claiming merge blocking, configure and verify GitHub branch protection separately.
  Request changes alone is not automatic rejection/closure or guaranteed merge blocking.
- Keep all planted defects unmerged; compare #19 against #20 rather than fixing away the
  demonstration findings.

## Source references

- [Blast radius](https://docs.qodo.ai/code-review/assess-risk-with-blast-radius)
- [Skills discovery and enforcement vs steering](https://docs.qodo.ai/governance/manage-skills-across-repositories)
- [REVIEW.md](https://docs.qodo.ai/governance/use-review-md)
- [Codebase Wisdom](https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-codebase-wisdom-skill)
