import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from seo_strategist.browser import render, export_pdf
from seo_strategist.audit import audit
from seo_strategist.report import write_reports
from .site import site


class MissingBrowserTests(unittest.TestCase):
    def test_missing_dependency_is_explicit(self):
        with patch.dict('sys.modules', {'playwright.sync_api': None}):
            self.assertEqual(render('https://example.invalid/')["state"], "unavailable")
            self.assertEqual(export_pdf('unused.html', 'unused.pdf')["state"], "unavailable")


@unittest.skipUnless(os.environ.get("SEO_BROWSER_TESTS") == "1", "Prove Chromium opt-in: SEO_BROWSER_TESTS=1")
class BrowserTests(unittest.TestCase):
    def test_render_and_comparison(self):
        with site() as (origin, counts):
            report = audit(origin + "/dynamic", sample_size=1, rendering="auto")
            page = report["pages"][0]
            self.assertEqual(page["rendering"]["state"], "rendered")
            self.assertEqual(page["initial"]["title"], "Prima")
            self.assertEqual(page["rendered"]["title"], "Dopo")
            self.assertTrue(page["rendering"]["comparison"]["title_changed"])

    def test_local_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = write_reports({"synthetic": True, "untrusted": "<script>alert(1)</script>"}, tmp, pdf=True)
            self.assertEqual(result["pdf"]["state"], "written")
            self.assertTrue(Path(result["pdf"]["path"]).read_bytes().startswith(b"%PDF-"))
