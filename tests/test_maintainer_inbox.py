import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("inbox", ROOT / "tools/maintainer_inbox.py")
inbox = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inbox)


class InboxTests(unittest.TestCase):
    def test_html_escapes_untrusted_text_and_invalid_heads_fail(self):
        packet = json.loads((ROOT / "maintainer-inbox/maintainer-actions.json").read_text())
        packet["summary"] = "<script>alert(1)</script>"
        self.assertIn("&lt;script&gt;", inbox.render_html(packet))
        packet["actions"][0]["pr_heads"] = None
        with self.assertRaises(ValueError):
            inbox.validate(packet)

    def test_packet_renders_and_rejects_foreign_targets(self):
        packet = json.loads((ROOT / "maintainer-inbox/maintainer-actions.json").read_text())
        self.assertIn("proposed, not approved or applied", inbox.render(packet))
        packet["actions"][0]["targets"] = ["https://github.com/other/repo/issues/1"]
        with self.assertRaises(ValueError):
            inbox.validate(packet)

    def test_duplicate_ids_are_rejected(self):
        packet = json.loads((ROOT / "maintainer-inbox/maintainer-actions.json").read_text())
        packet["actions"].append(packet["actions"][0])
        with self.assertRaises(ValueError):
            inbox.validate(packet)
