import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from seo_strategist.runtime import profile, status, save_profile, remember, reset, runtime_dir
from seo_strategist.html import analyze_html
from seo_strategist.sitemap import collect_sitemap
from seo_strategist.network import Response
from seo_strategist.audit import audit, generic_header_directives
from seo_strategist.robots import access
from seo_strategist.schema import build, validate


class FakeClient:
    def __init__(self, responses):
        self.responses = responses

    def get(self, url):
        return self.responses.get(url, Response(url, url, state="inconclusive", error="simulated_timeout"))


class EdgeTests(unittest.TestCase):
    def test_no_site_and_geography(self):
        data = profile({"site": "2", "geography": "1"})
        self.assertIsNone(data["answers"]["site"]["normalized"])
        self.assertEqual(data["answers"]["site"]["original"], "2")
        self.assertEqual(data["answers"]["geography"]["normalized"], "italia/italiano")

    def test_resume_and_recent(self):
        with tempfile.TemporaryDirectory() as tmp:
            save_profile(tmp, profile({"role": "Founder"}))
            remember(tmp, Path(tmp) / "report.json")
            data = status(tmp)
            self.assertEqual(data["missing"][0], "tools")
            self.assertEqual(len(data["recent_results"]), 1)

    def test_reset_rejects_runtime_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".seo-runtime"
            target.write_text("not a directory")
            with self.assertRaises(ValueError):
                reset(tmp, False)
            self.assertTrue(target.exists())

    def test_reset_outside_resolution_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
            root = Path(tmp).resolve()
            target = root / ".seo-runtime"
            target.mkdir()
            original = Path.resolve
            def resolved(path, *args, **kwargs):
                return Path(outside) if path == target else original(path, *args, **kwargs)
            with patch.object(Path, 'resolve', resolved):
                with self.assertRaises(ValueError):
                    reset(tmp, False)
            self.assertTrue(target.exists())
            self.assertTrue(Path(outside).exists())

    def test_malformed_href_retained_not_navigable(self):
        doc = analyze_html('<base href="https://["><a href="https://[">bad</a><link rel="canonical" href="https://[">', 'https://example.org/')
        self.assertFalse(doc["links"][0]["navigable"])
        self.assertEqual(doc["canonical"], ["https://["])

    def test_sitemap_cycle_and_bad_location(self):
        url = 'https://example.org/sitemap.xml'
        cycle = Response(url, url, state="present", body=f'<sitemapindex><sitemap><loc>{url}</loc></sitemap></sitemapindex>')
        result = collect_sitemap(FakeClient({url: cycle}), url)
        self.assertFalse(result["complete"])
        self.assertIn('duplicate_or_cycle', result["warnings"][0])
        cycle.body = '<urlset><url><loc>https://[</loc></url></urlset>'
        result = collect_sitemap(FakeClient({url: cycle}), url)
        self.assertIn('invalid_url', result["entries"][0]["issues"])

    def test_network_failure_not_missing_sitemap_membership(self):
        url = 'https://example.org/'
        page = Response(url, url, status=200, state='present', body='<title>Title</title>', headers={'content-type': 'text/html'})
        report = audit(url, rendering='off', client=FakeClient({url: page}))
        self.assertIsNone(report["pages"][0]["matrix"]["in_sitemap"])
        self.assertIsNone(report["pages"][0]["ai_crawlers"][0]["declared_access"])
        self.assertEqual(report["resources"]["llms_quality"]["state"], 'inconclusive')

    def test_header_noindex_and_agent_scope(self):
        self.assertEqual(generic_header_directives('googlebot: nofollow, noindex'), '')
        url = 'https://example.org/'
        page = Response(url, url, status=200, state='present', body='<title>Title</title>', headers={'x-robots-tag': 'noindex'})
        report = audit(url, rendering='off', client=FakeClient({url: page}))
        self.assertTrue(report["pages"][0]["matrix"]["noindex"])

    def test_robots_merged_groups_and_ties(self):
        response = Response('u', 'u', state='present', body='User-agent: GPTBot\nDisallow: /a\nUser-agent: GPTBot\nAllow: /a\nDisallow: /b\n')
        self.assertTrue(access(response, 'https://x/a', 'GPTBot')["declared_access"])
        self.assertFalse(access(response, 'https://x/b', 'GPTBot')["declared_access"])

    def test_schema_coherence(self):
        with self.assertRaises(ValueError):
            build('Article', {'headline': 'A', 'author': 'B', 'datePublished': '2025-01-02', 'dateModified': '2025-01-01'})
        breadcrumb = build('BreadcrumbList', {'items': [{'name': 'Home', 'url': 'https://example.org/'}]})
        breadcrumb['itemListElement'][0]['position'] = 2
        self.assertFalse(validate(breadcrumb)['valid_local_contract'])
        with self.assertRaises(ValueError):
            build('Person', {'name': 'A', 'url': 'javascript:alert(1)'})


if __name__ == '__main__':
    unittest.main()
