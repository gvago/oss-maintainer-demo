import importlib.util
from pathlib import Path
import unittest
import io
import json
import tempfile
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("bridge", Path(__file__).resolve().parents[1] / "tools/qodo_read_mcp.py")
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class ReadBridgeTests(unittest.TestCase):
    def test_only_scoped_read_tools_and_fixed_argv(self):
        read = {"name": "read-tool", "access": "read", "mutating": False, "group": "codebase", "leaf": "get-pr", "parameters": {"properties": {"repo": {"type": "string"}, "number": {"type": "integer"}}, "required": ["repo", "number"]}}
        write = dict(read, name="write-tool", mutating=True)
        tools = bridge.scoped_tools({"tools": [read, write]})
        self.assertEqual(set(tools), {"read-tool"})
        with patch.object(bridge, "qodo_json", return_value={"ok": True}) as execute:
            args = {"repo": "owner/repo", "number": 9}
            bridge.call_read("/verified/qodo", tools, "read-tool", args, "owner/repo")
            self.assertEqual(execute.call_args.args[1][:3], ["read", "codebase", "get-pr"])
            for name, arguments in [("write-tool", args), ("read-tool", {"repo": "other/repo", "number": 9}), ("read-tool", dict(args, command="rm"))]:
                with self.assertRaises(ValueError):
                    bridge.call_read("/verified/qodo", tools, name, arguments, "owner/repo")
            self.assertEqual(execute.call_count, 1)

    def test_optional_scope_is_still_required_and_authors_removed(self):
        for selector in ["repo", "pr_url"]:
            tool = {"parameters": {"properties": {selector: {}}, "required": []}}
            for args in [{}, {selector: None}, {selector: []}]:
                with self.assertRaises(ValueError):
                    bridge.scope_args(tool, args, "owner/repo")
        self.assertEqual(bridge.audit_data({"author": {"login": "person"}, "number": 1, "nested": {"external_id": "secret"}}), {"number": 1, "nested": {}})

    def test_bad_request_does_not_kill_next_ping(self):
        stream = io.StringIO('broken\n[]\n{"id":2,"method":"ping"}\n')
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp, patch.object(bridge, "qodo_json", side_effect=[{}, {}, {"tools": []}]), patch.object(bridge.subprocess, "run"), patch.object(bridge.sys, "stdin", stream), patch.object(bridge.sys, "stdout", output):
            bridge.serve("owner/repo", Path(tmp) / "evidence.json")
        messages = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(messages[-1], {"jsonrpc": "2.0", "id": 2, "result": {}})
        self.assertEqual(len(messages), 3)

    def test_review_url_is_scoped(self):
        tool = {"parameters": {"properties": {"pr_url": {}}, "required": ["pr_url"]}}
        with self.assertRaises(ValueError):
            bridge.scope_args(tool, {"pr_url": "https://github.com/other/repo/pull/1"}, "owner/repo")
