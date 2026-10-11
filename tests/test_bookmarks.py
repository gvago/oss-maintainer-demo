import unittest

from bookmarks.urls import normalize_url


class URLTests(unittest.TestCase):
    def test_url_identity(self):
        self.assertEqual(normalize_url("HTTPS://Example.COM/articles?x=1#intro"),
                         "https://example.com/articles?x=1#intro")
        self.assertEqual(normalize_url("https://example.com"), "https://example.com/")

    def test_default_ports_share_identity(self):
        for first, second in (("https://example.com:443/a", "https://example.com/a"),
                              ("http://example.com:80/a", "http://example.com/a"),
                              ("https://[::1]:443/a", "https://[::1]/a")):
            self.assertEqual(normalize_url(first), normalize_url(second))
        self.assertEqual(normalize_url("https://example.com:8443/a"), "https://example.com:8443/a")

    def test_queries_share_identity(self):
        self.assertEqual(normalize_url("https://example.com/a?sig=one"), normalize_url("https://example.com/a?sig=two"))

    def test_invalid_urls(self):
        for value in ("file:///etc/passwd", "javascript:alert(1)", "https:///path",
                      "https://user:pass@example.com", "https://example.com:bad",
                      "https://example.com:70000", "https://exa mple.com", "https://example.com/\n"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_url(value)


class ExportTests(unittest.TestCase):
    def test_export_reuses_url_identity(self):
        import json
        from bookmarks.exports import export_json
        result = json.loads(export_json(["HTTPS://Example.com", "https://example.com/"]))
        self.assertEqual(result, ["https://example.com/"])


class CLITests(unittest.TestCase):
    def test_cli_exports_json(self):
        import json
        import subprocess
        import sys
        result = subprocess.run([sys.executable, "-m", "bookmarks", "HTTPS://Example.com"],
                                capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), ["https://example.com/"])

    def test_cli_rejects_bad_input(self):
        import subprocess
        import sys
        result = subprocess.run([sys.executable, "-m", "bookmarks", "file:///etc/passwd"],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
