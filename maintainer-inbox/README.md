# Maintainer Inbox

## Ready now

Read [maintainer-inbox.md](maintainer-inbox.md) and [maintainer-actions.json](maintainer-actions.json).
They were prepared by Hermes from live Qodo Wisdom reads; evidence is in evidence.json.
No proposed closure, link, comment or rebase has been applied.

For Claude, Codex or Hermes, load [the orchestration skill](../agent-skills/maintainer-inbox/SKILL.md)
and ask: "Use Qodo Wisdom to create a fresh maintainer inbox for this repository; analysis only."
It belongs outside review-lens skills/. It does not duplicate the official Wisdom skill.

## CLI runner

Requires already-installed/authenticated Qodo CLI and Claude or Codex. Preserve your
organization's inference provider and Qodo deployment; do not switch to public endpoints.

```sh
python3 tools/maintainer_inbox.py --repo gvago/oss-maintainer-demo --agent claude
python3 tools/maintainer_inbox.py --repo gvago/oss-maintainer-demo --agent codex
```

The runner collects actual Qodo managed-tool context, then asks the host agent for schema-shaped
recommendations. Claude generation has no tools. Codex read-only sandbox is not a complete
remote-tool permission boundary: use a host with no write-capable MCP configuration and no
GitHub write credentials. It never executes contributor code or applies recommendations.
Collection refuses a backlog above the configured limit instead of claiming complete coverage.
This minimal collector searches each issue against merged history; larger repos need narrowed
incremental discovery rather than increasing the cap blindly.

## GitHub Action activation

The manual-only workflow requires a **dedicated, trusted self-hosted runner** labelled
`maintainer-inbox`, with Qodo and the chosen agent already authenticated/configured.
No runner has been registered or exposed by this kit. No installs or credential copies occur.
Do not run arbitrary fork jobs on that runner. Only default-branch workflow_dispatch runs;
permissions are contents:read, and results become artifacts and a job summary, not comments.
A hosted-runner variant needs separately approved inference/Qodo credentials and installation.

## Apply a decision

Tell your interactive agent: "Apply A4 only, after refreshing its evidence." It must verify
current issue state and main behavior, ask if the evidence changed, perform only your approved
operation and read back the target. This kit deliberately includes no automatic apply script.
PR stacks involving independent contributors require coordination, not blind force-pushes.

## Verification boundary

Live Qodo context collection and local rendering have run.
`python3 -m unittest discover -s tests -v` returned 8 tests passed, zero failures. The sample report was authored
by Hermes, not fabricated as Claude/Codex output. Headless Claude/Codex generation and the
GitHub Action have not yet been exercised on a configured inference/CI host. Do not call that
hosted automation live until a real run returns valid artifacts.
