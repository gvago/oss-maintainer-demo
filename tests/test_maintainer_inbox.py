import importlib.util
import json
from pathlib import Path
import unittest
import copy

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("inbox", ROOT / "tools/maintainer_inbox.py")
inbox = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inbox)


class InboxTests(unittest.TestCase):
    def test_committed_packet_matches_renderers_and_verification(self):
        folder = ROOT / "maintainer-inbox"
        packet = json.loads((folder / "maintainer-actions.json").read_text())
        evidence = json.loads((folder / "evidence.json").read_text())
        self.assertTrue(evidence["calls"])
        self.assertEqual((folder / "maintainer-inbox.md").read_text(), inbox.render(packet))
        self.assertEqual((folder / "maintainer-inbox.html").read_text(), inbox.render_html(packet))
        # Snapshot consistency, not an independent rerun of historical verification.
        self.assertIn(evidence["observed_at"], packet["coverage"])


    def test_markdown_text_cannot_escape_literal_blocks(self):
        packet = json.loads((ROOT / "maintainer-inbox/maintainer-actions.json").read_text())
        attack = '</pre></details>\n# Forged approval\n[click](https://evil.example)'
        packet["summary"] = attack
        packet["actions"][0]["rationale"] = attack
        rendered = inbox.render(packet)
        self.assertIn('<p>&lt;/pre&gt;&lt;/details&gt;', rendered)
        self.assertNotIn('</pre></details>\n# Forged', rendered)
        self.assertIn(packet["coverage"], rendered)

    def test_repo_identifier_cannot_inject_markdown(self):
        packet = json.loads((ROOT / "maintainer-inbox/maintainer-actions.json").read_text())
        packet["repo"] = "gvago/repo\n# Forged"
        with self.assertRaises(ValueError):
            inbox.validate(packet)

    def test_workflow_is_manual_main_only(self):
        workflow = (ROOT / ".github/workflows/maintainer-inbox.yml").read_text()
        self.assertNotIn('  push:', workflow)
        self.assertIn("github.ref == 'refs/heads/main'", workflow)

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

    def test_evidence_gate_rejects_filtered_capped_and_wrong_targets(self):
        folder = ROOT / "maintainer-inbox"
        packet = json.loads((folder / "maintainer-actions.json").read_text())
        evidence = json.loads((folder / "evidence.json").read_text())
        inbox.bind_evidence(packet, evidence)
        for change in ["filtered", "capped", "head", "issue", "review", "history"]:
            p, e = copy.deepcopy(packet), copy.deepcopy(evidence)
            if change == "filtered":
                e["calls"][0]["arguments"]["labels"] = ["bug"]
            elif change == "capped":
                call = next(c for c in e["calls"] if c["tool"] == "litegit-list-prs")
                call["result"]["pull_requests"] *= 200
            elif change == "head":
                a = next(a for a in p["actions"] if a["pr_heads"])
                a["pr_heads"][next(iter(a["pr_heads"]))] = "f" * 40
            elif change == "issue":
                p["actions"][0]["targets"] = [f"https://github.com/{p['repo']}/issues/999"]
            elif change == "review":
                e["calls"] = [c for c in e["calls"] if c["tool"] != "get-pr-review-findings"]
            else:
                e["calls"] = [c for c in e["calls"] if not c["tool"].startswith("pull-request-")]
            with self.assertRaises(ValueError, msg=change):
                inbox.bind_evidence(p, e)

    def test_missing_heads_are_bound_from_evidence_not_invented(self):
        folder = ROOT / "maintainer-inbox"
        packet = json.loads((folder / "maintainer-actions.json").read_text())
        evidence = json.loads((folder / "evidence.json").read_text())
        expected = [dict(a["pr_heads"]) for a in packet["actions"]]
        for action in packet["actions"]:
            action["pr_heads"] = {}
        with self.assertRaises(ValueError):
            inbox.validate(packet)
        inbox.bind_evidence(packet, evidence)
        self.assertEqual([a["pr_heads"] for a in packet["actions"]], expected)
        for change in ["unknown", "conflict", "missing_observation", "invalid_observation"]:
            p, e = copy.deepcopy(packet), copy.deepcopy(evidence)
            action = next(a for a in p["actions"] if a["pr_heads"])
            url = next(iter(action["pr_heads"]))
            if change == "unknown":
                action["targets"].append(f"https://github.com/{p['repo']}/pull/999")
            elif change == "conflict":
                action["pr_heads"][url] = "f" * 40
            else:
                action["pr_heads"] = {}
                for call in e["calls"]:
                    if call["tool"] == "litegit-list-prs":
                        pr = next(pr for pr in call["result"]["pull_requests"] if str(pr["number"]) == url.rsplit("/", 1)[1])
                        pr["head_sha"] = None if change == "missing_observation" else "abc123"
                        pr.pop("head_commit", None)
            with self.assertRaises(ValueError, msg=change):
                inbox.bind_evidence(p, e)

    def test_duplicate_ids_are_rejected(self):
        packet = json.loads((ROOT / "maintainer-inbox/maintainer-actions.json").read_text())
        packet["actions"].append(packet["actions"][0])
        with self.assertRaises(ValueError):
            inbox.validate(packet)
