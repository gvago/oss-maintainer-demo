# Maintainer Inbox

Start with [the maintainer guide](../DEMO.md).

`maintainer-inbox.md` and `maintainer-actions.json` are an actual Claude-generated packet
from live Qodo Wisdom reads through the configured Qodo gateway. `evidence.json` records
that run's inputs. Recommendations are proposed, not approved or applied.

Regenerate locally:

```sh
python3 tools/maintainer_inbox.py --repo gvago/oss-maintainer-demo
```

Requirements: authenticated Qodo CLI and Claude configured for your approved provider.
Claude chooses from Qodo's live managed read tools through a repository-scoped stdio MCP
bridge to the installed CLI. No shell or contributor execution. Existing official Qodo MCP
connections work with the interactive skill in Claude, Codex or Hermes; this CI runner uses Claude.

The GitHub workflow runs on hosted Ubuntu using encrypted repository secrets.
Verified hosted run: https://github.com/gvago/oss-maintainer-demo/actions/runs/38158357749
Download its artifact for the HTML interface, JSON actions and retrieval evidence.
Do not close/merge/retarget based on a stale packet: refresh exact targets and PR heads first.
