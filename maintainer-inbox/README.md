# Maintainer Inbox

Start with [the maintainer guide](../DEMO.md).

`maintainer-inbox.md` and `maintainer-actions.json` are an actual Claude-generated packet
from live Qodo Wisdom reads through the configured Qodo gateway. `evidence.json` records
that run's inputs. Recommendations are proposed, not approved or applied.

Regenerate locally:

```sh
python3 tools/maintainer_inbox.py --repo gvago/oss-maintainer-demo --agent claude
```

Requirements: authenticated Qodo CLI and Claude configured for your approved provider.
Claude generation has tools disabled. The Codex adapter is optional; its read-only filesystem
sandbox does not restrict remote MCP writes, so use an isolated configuration without write tools.

The GitHub workflow requires a configured dedicated runner; local generation does not.
Do not close/merge/retarget based on a stale packet: refresh exact targets and PR heads first.
