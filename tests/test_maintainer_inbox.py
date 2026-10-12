import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import subprocess

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("inbox", ROOT / "tools/maintainer_inbox.py")
inbox = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inbox)


class InboxTests(unittest.TestCase):
    def test_committed_packet_matches_renderers_and_verification(self):
        folder = ROOT / "maintainer-inbox"
        packet = json.loads((folder / "maintainer-actions.json").read_text())
        evidence = json.loads((folder / "evidence.json").read_text())
        self.assertNotIn("A11", [a["id"] for a in packet["actions"]])
        self.assertEqual((folder / "maintainer-inbox.md").read_text(), inbox.render(packet))
        self.assertEqual((folder / "maintainer-inbox.html").read_text(), inbox.render_html(packet))
        # Snapshot consistency, not an independent rerun of historical verification.
        self.assertIn(evidence["observed_at"], packet["coverage"])


    def test_verification_executes_checks_and_rejects_failures(self):
        sha = "a" * 40
        evidence = {"repo": "gvago/oss-maintainer-demo", "current_main": {"bookmarks/urls.py": {"sha": sha}}}
        good_tests = subprocess.CompletedProcess([], 0, "", "Ran 6 tests\nOK")
        good_repro = subprocess.CompletedProcess([], 0, '["https://example.com/docs"]', "")
        for tests, repro, passes in [
            (good_tests, good_repro, True),
            (subprocess.CompletedProcess([], 1, "", "FAILED"), good_repro, False),
            (good_tests, subprocess.CompletedProcess([], 0, '["duplicate", "duplicate"]', ""), False),
        ]:
            with patch.object(inbox, "run", side_effect=[sha, "https://github.com/gvago/oss-maintainer-demo", ""]), patch.object(inbox.subprocess, "run", side_effect=[tests, repro]) as executed:
                if passes:
                    self.assertEqual(inbox.verify_demo_main(ROOT, evidence)["status"], "passed")
                    self.assertEqual(executed.call_count, 2)
                    self.assertEqual(executed.call_args_list[0].args[0], ["python3", "-m", "unittest", "discover", "-s", "tests", "-v"])
                    self.assertEqual(executed.call_args_list[1].args[0], ["python3", "-m", "bookmarks", "https://example.com:443/docs", "https://example.com/docs"])
                    self.assertTrue(all(call.kwargs["cwd"] == ROOT for call in executed.call_args_list))
                else:
                    with self.assertRaises(ValueError):
                        inbox.verify_demo_main(ROOT, evidence)
        with patch.object(inbox, "run", side_effect=[sha, "https://github.com/gvago/oss-maintainer-demo.git", " M changed.py"]), patch.object(inbox.subprocess, "run") as executed:
            with self.assertRaises(ValueError):
                inbox.verify_demo_main(ROOT, evidence)
            executed.assert_not_called()

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

    def test_demo_verification_refuses_other_repositories(self):
        with self.assertRaises(ValueError):
            inbox.verify_demo_main(ROOT, {"repo": "other/repo", "current_main": {}})

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

    def test_duplicate_ids_are_rejected(self):
        packet = json.loads((ROOT / "maintainer-inbox/maintainer-actions.json").read_text())
        packet["actions"].append(packet["actions"][0])
        with self.assertRaises(ValueError):
            inbox.validate(packet)
