# Qodo for OSS maintainers

This repository demonstrates two workflows on a small, dependency-free bookmark toolkit:
**review contributions against your own guidelines**, and **turn a backlog into proposed maintainer actions**.
All example contributions were seeded; they are not real external contributors.

## Explore the examples

| Maintainer task | Example |
| --- | --- |
| Request changes for guideline violations | [#26](https://github.com/gvago/oss-maintainer-demo/pull/26): missing tests, disallowed dependency, alternate URL identity. Compare clean control [#27](https://github.com/gvago/oss-maintainer-demo/pull/27). |
| Focus review effort | Open PRs carry Qodo blast-radius and review-time labels. |
| Consolidate duplicate work | [#9](https://github.com/gvago/oss-maintainer-demo/pull/9) and [#10](https://github.com/gvago/oss-maintainer-demo/pull/10) implement the same optional fragment behavior. Issues #3/#4 overlap. |
| Review complementary work in order | [#11](https://github.com/gvago/oss-maintainer-demo/pull/11) adds CSV library support; [#12](https://github.com/gvago/oss-maintainer-demo/pull/12) consumes it from the CLI and is already stacked. |
| Avoid premature issue closure | #9/#10 implement the helper, not the complete exporter/CLI requirement. |
| Reuse accepted history | Issue #8 resembles the default-port fix merged in #2. Verify current main before closing it. |

Read the [generated inbox](maintainer-inbox/maintainer-inbox.md) for evidence, draft replies and proposed actions.
Keep the planted bad/clean PRs unmerged if using this repository as a demo.

## 1. Set up contribution review in your repository

1. Connect the repository to Qodo Code Review in your Qodo workspace.
2. Write your actual contribution requirements in root `CONTRIBUTING.md`.
   Include test expectations, dependency policy and any compatibility requirements.
3. Add [the thin contribution skill](skills/oss-contribution-workflow/SKILL.md) under
   `skills/oss-contribution-workflow/`. It reads the guidelines; it does not copy them.
4. Add/adapt [REVIEW.md](REVIEW.md), including its instruction to apply
   `oss-contribution-workflow` and consult root `CONTRIBUTING.md`.
5. In the Qodo portal, verify that the skill is discovered/imported and enable the skills agent.
   Set this workflow skill to **Steering**. Enable **REVIEW.md** instructions.
6. In PR Triage settings, enable **Request changes when any finding is Medium or higher**.
   Enable blast-radius labels and **Display → Publish Review Time Estimate Label**.
7. Test one noncompliant runtime PR and one compliant control. Check that findings cite
   your guidelines, the noncompliant PR receives a request-changes review and the control stays quiet.

[.pr_agent.toml](.pr_agent.toml) contains equivalent repository settings for skills,
REVIEW.md and display labels. Configure the request-changes threshold in the portal.

Request changes is a review vote, not automatic closure. If you need merge blocking,
configure GitHub branch protection/rulesets and verify them separately. Blast-radius
labels do not automatically enforce different reviewer counts.

## 2. Generate a maintainer inbox

Use an authenticated Qodo CLI and Claude Code configured for your approved model provider.
This repository's runner uses Qodo managed read tools for issues, PR diffs and merged history;
Claude receives that evidence with tools disabled and returns structured recommendations.

```sh
python3 tools/maintainer_inbox.py --repo gvago/oss-maintainer-demo --agent claude
```

Open `maintainer-output/maintainer-inbox.md`. The sibling JSON contains action IDs,
evidence, uncertainties, draft replies and observed PR head SHAs. Nothing is posted or closed.

For your repository, replace the slug. The minimal runner caps discovery at 20 open PRs/issues
and refuses larger backlogs instead of reporting incomplete coverage as complete.
The demo additionally retrieves its relevant source files on main; for other repositories,
use the interactive skill below to select current code relevant to candidate fixes.

### Interactive Claude, Codex or Hermes

Load the official Qodo Codebase Wisdom skill plus
[the maintainer workflow](agent-skills/maintainer-inbox/SKILL.md), then ask:

> Use Qodo Wisdom to prepare a maintainer inbox for OWNER/REPO. Compare open PR diffs
> and tests, issues and merged history. Find duplicate work, partial fixes and dependencies.
> Check current main before suggesting an issue is already fixed. Produce maintainer-inbox.md
> and maintainer-actions.json. Analysis only; do not post, close, merge or rebase.

Merged-history similarity searches merged PRs. Open-PR duplicate comparison is agent reasoning
using live diffs, not a native automatic PR Triage duplicate detector.

## 3. Review and approve actions

Read the evidence and uncertainty before choosing an action. Tell your interactive agent:

> Refresh the targets and evidence for action A2. If the PR heads changed, regenerate
> the recommendation. Otherwise prepare the consolidation reply for my approval.

Coordinate with contributors before closing overlapping work or changing a stack.
No bulk-close or automatic rebase script is included.

## 4. Run it from GitHub Actions

[The manual workflow](.github/workflows/maintainer-inbox.yml) runs the same collector/generator,
adds a job summary and uploads the evidence, Markdown and JSON as an artifact.
It currently requires a dedicated self-hosted runner labelled `maintainer-inbox`, with Qodo
and Claude already authenticated. Run only trusted default-branch jobs on that runner.
Choose **Actions → Maintainer Inbox → Run workflow** after merging the workflow to main.

No runner is registered by copying these files. A GitHub-hosted variant requires approved
installation and encrypted Qodo/provider credentials; do not put tokens in source or prompts.

## Verify your setup

```sh
python3 -m unittest discover -s tests -v
python3 tools/maintainer_inbox.py --collect-only --repo OWNER/REPO
python3 tools/maintainer_inbox.py --repo OWNER/REPO --agent claude
```

The last command must produce a fresh report, not just render a checked-in sample.
Review findings/labels are Qodo output; backlog recommendations are agent conclusions grounded
in Qodo retrieval. Neither establishes measured time savings or automatic learning of new rules.
