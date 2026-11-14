import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from seo_strategist import runtime
from seo_strategist.html import analyze_html
from seo_strategist.network import Client, Response, valid_url
from seo_strategist.sitemap import parse_sitemap, collect_sitemap
from seo_strategist.robots import access
from seo_strategist.audit import audit, llms_quality
from seo_strategist.schema import build, validate
from seo_strategist.editorial import keywords, read_csv, brief
from seo_strategist.report import write_reports, markdown, html_report
from seo_strategist.cli import main
from .site import site


class ProfileTests(unittest.TestCase):
    def test_empty_and_partial(self):
        self.assertEqual(runtime.profile()["answers"], {})
        data = runtime.profile({"role": "1", "geography": "  Italia  "})
        self.assertEqual(data["answers"]["role"]["normalized"], "marketing")
        self.assertEqual(data["answers"]["geography"]["original"], "  Italia  ")
        self.assertEqual(runtime.validate_profile(data), data)

    def test_custom_and_complete(self):
        values = dict(zip(runtime.FIELDS, ["Ricercatore", "Fogli locali", "https://example.org", "lancio", "Italia", "seo", "21–100", "zero"] ))
        with tempfile.TemporaryDirectory() as tmp:
            runtime.save_profile(tmp, runtime.profile(values))
            self.assertEqual(runtime.status(tmp)["missing"], [])
            self.assertEqual(runtime.load_profile(tmp)["answers"]["role"]["normalized"], "ricercatore")

    def test_invalid_schema_and_answers(self):
        for values in ({"wrong": "x"}, {"role": "99"}, {"site": "file:///x"}, {"budget": None}):
            with self.assertRaises(ValueError):
                runtime.profile(values)
        with self.assertRaises(ValueError):
            runtime.validate_profile({"schema_version": 9})
        with self.assertRaises(ValueError):
            runtime.profile(env_names=["SECRET=value"])

    def test_presence_not_connection_and_no_values(self):
        with patch.dict(os.environ, {"SEO_TEST_VARIABLE": "do-not-print-this"}):
            data = runtime.capabilities(runtime.profile(env_names=["SEO_TEST_VARIABLE"]))
            self.assertTrue(data["environment_present"]["SEO_TEST_VARIABLE"])
            self.assertFalse(data["connection_verified"])
            self.assertNotIn("do-not-print-this", json.dumps(data))

    def test_reset_preserves_deliverables(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.html"
            report.write_text("keep")
            runtime.save_profile(tmp, runtime.profile())
            self.assertFalse(runtime.reset(tmp)["deleted"])
            self.assertTrue((Path(tmp) / ".seo-runtime").exists())
            self.assertTrue(runtime.reset(tmp, False)["deleted"])
            self.assertEqual(report.read_text(), "keep")

    def test_reset_rejects_links(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as external:
            root = Path(tmp) / ".seo-runtime"
            root.mkdir()
            try:
                (root / "escape").symlink_to(external, target_is_directory=True)
            except OSError:
                self.skipTest("Creazione symlink non autorizzata dal sistema")
            with self.assertRaises(ValueError):
                runtime.reset(tmp, False)
            self.assertTrue(Path(external).exists())

    def test_corrupt_profile_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = runtime.runtime_dir(tmp)
            root.mkdir()
            (root / "profile.json").write_text("{broken")
            with self.assertRaises(ValueError):
                runtime.load_profile(tmp)
            self.assertEqual((root / "profile.json").read_text(), "{broken")


class ParserTests(unittest.TestCase):
    def test_html_semantics(self):
        doc = analyze_html('<title>A &amp; B</title><base href="https://example.org/docs/"><meta name="description" content="Test"><h1>Come?</h1><img src="x"><img alt=""><link rel="canonical" href="a"><link rel="alternate" hreflang="it" href="it"><script>alert(1)</script><script type="application/ld+json">{"x":1}</script><a href="javascript:alert(1)">qui</a><a href="b">Risorsa</a>', 'https://example.org/')
        self.assertEqual(doc["title"], "A & B")
        self.assertNotIn("alert(1)", doc["text"])
        self.assertEqual(doc["canonical"], ["https://example.org/docs/a"])
        self.assertIsNone(doc["images"][0]["alt"])
        self.assertEqual(doc["images"][1]["alt"], "")
        self.assertFalse(doc["links"][0]["navigable"])
        self.assertTrue(doc["geo"]["signals"]["question_headings"])

    def test_malformed_html_json(self):
        doc = analyze_html('<h2>Heading<script type="application/ld+json">{broken</script>', 'https://example.org/')
        self.assertEqual(len(doc["jsonld_errors"]), 1)
        self.assertEqual(doc["headings"][0]["text"], "Heading")

    def test_xml_limits_and_dates(self):
        for text in ('<!DOCTYPE x [<!ENTITY x "foo">]><urlset/>', '<broken', '<rss/>'):
            with self.assertRaises(ValueError):
                parse_sitemap(text)
        kind, entries = parse_sitemap('<urlset><url><loc>https://example.org/a#b</loc><lastmod>tomorrow</lastmod></url><url><loc>bad</loc></url></urlset>')
        self.assertEqual(kind, "urlset")
        self.assertIn("fragment", entries[0]["issues"])
        self.assertIn("invalid_lastmod", entries[0]["issues"])
        self.assertIn("invalid_url", entries[1]["issues"])

    def test_robots_precedence(self):
        response = Response("u", "u", state="present", body="User-agent: *\nDisallow: /\nUser-agent: GPTBot\nDisallow: /private*\nAllow: /private/public$\n")
        self.assertTrue(access(response, "https://x/private/public", "GPTBot")["declared_access"])
        self.assertFalse(access(response, "https://x/private/other", "GPTBot")["declared_access"])
        self.assertFalse(access(response, "https://x/", "OtherBot")["declared_access"])
        response.state = "inconclusive"
        self.assertIsNone(access(response, "https://x/", "GPTBot")["declared_access"])

    def test_llms_unknown_not_absent(self):
        r = Response("u", "u")
        self.assertEqual(llms_quality(r)["state"], "inconclusive")
        r.state = "absent"
        self.assertEqual(llms_quality(r)["state"], "absent")


class HTTPTests(unittest.TestCase):
    def test_http_redirect_retry_and_errors(self):
        with site() as (origin, counts):
            client = Client(timeout=1)
            response = client.get(origin + "/old")
            self.assertEqual(response.final_url, origin + "/article")
            self.assertEqual(len(response.redirects), 1)
            self.assertEqual(client.get(origin + "/retry").state, "present")
            self.assertEqual(counts["/retry"], 3)
            self.assertEqual(client.get(origin + "/missing").state, "absent")
            self.assertEqual(client.get(origin + "/forbidden").state, "http_error")
            self.assertEqual(client.get(origin + "/loop").error, "redirect_limit")
            self.assertEqual(client.get(origin + "/bad-redirect").error, "invalid_redirect_target")

    def test_timeout_and_size(self):
        with site() as (origin, counts):
            response = Client(timeout=0.02, retries=1).get(origin + "/slow")
            self.assertEqual(response.state, "inconclusive")
            self.assertEqual(response.attempts, 2)
            self.assertEqual(Client(max_bytes=100).get(origin + "/big").error, "response_too_large")

    def test_url_validation(self):
        for url in ('file:///x', 'https://user:password@example.org', 'https://example.org:bad', 'hello', 'https://x/ a'):
            with self.assertRaises(ValueError):
                valid_url(url)

    def test_sitemap_index_and_limits(self):
        with site() as (origin, counts):
            result = collect_sitemap(Client(), origin + "/sitemap.xml")
            self.assertEqual(len(result["entries"]), 5)
            self.assertTrue(result["complete"])
            limited = collect_sitemap(Client(), origin + "/sitemap.xml", max_documents=1)
            self.assertFalse(limited["complete"])

    def test_audit_matrix_and_links(self):
        with site() as (origin, counts):
            result = audit(origin, rendering="off")
            self.assertEqual(len(result["pages"]), 5)
            private = next(p for p in result["pages"] if p["matrix"]["requested_url"].endswith("/private"))
            self.assertTrue(private["matrix"]["noindex"])
            self.assertFalse(private["ai_crawlers"][0]["declared_access"])
            self.assertTrue(result["pages"][0]["internal_links"][0]["known_noncanonical_target"])
            self.assertEqual(result["scope"], "sample")
            self.assertIn("noindex_review", [r["code"] for r in result["roadmap"]])

    def test_render_missing_preserves_static(self):
        with site() as (origin, counts), patch('seo_strategist.audit.render', return_value={"state": "unavailable", "error": "missing"}):
            result = audit(origin + "/dynamic", sample_size=1, rendering="always")
            page = result["pages"][0]
            self.assertEqual(page["initial"]["title"], "Prima")
            self.assertIsNone(page["rendered"])
            self.assertEqual(page["rendering"]["state"], "unavailable")


class SchemaEditorialReportTests(unittest.TestCase):
    def test_all_builders_roundtrip(self):
        inputs = {"Article": {"headline": "Titolo", "author": "Nome", "datePublished": "2025-01-01"},
            "Product": {"name": "Prodotto"}, "FAQPage": {"questions": [{"question": "Come?", "answer": "Così."}]},
            "LocalBusiness": {"name": "Negozio", "address": "Via Esempio 1"},
            "Organization": {"name": "Organizzazione", "url": "https://example.org"},
            "BreadcrumbList": {"items": [{"name": "Home", "url": "https://example.org"}]}, "Person": {"name": "Persona"}}
        for kind, data in inputs.items():
            with self.subTest(kind=kind):
                self.assertTrue(validate(build(kind, data))["valid_local_contract"])
                with self.assertRaises(ValueError):
                    build(kind, {})

    def test_rating_evidence_and_invalid(self):
        data = {"name": "Esempio", "aggregateRating": {"ratingValue": 4, "ratingCount": 3}}
        with self.assertRaises(ValueError):
            build("Product", data)
        data["rating_evidence"] = {"visible_on_page": True, "genuine_product_ratings": True, "source_url": "https://example.org/product"}
        self.assertTrue(validate(build("Product", data))["valid_local_contract"])
        data["aggregateRating"]["ratingValue"] = 9
        with self.assertRaises(ValueError):
            build("Product", data)
        for kind in ("Review", "HowTo", "AggregateRating"):
            with self.assertRaises(ValueError):
                build(kind, {})
        self.assertFalse(validate({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [None]})["valid_local_contract"])

    def test_keywords_and_brief(self):
        result = keywords(read_csv("keyword\ncomprare scarpe rosse\nprezzo scarpe rosse\ncome cucinare pasta\n"))
        self.assertEqual(len(result["clusters"]), 2)
        self.assertEqual(result["clusters"][0]["keywords"][0]["intent"], "transactional")
        self.assertIsNone(result["clusters"][0]["keywords"][0]["volume"])
        self.assertEqual(brief("Tema", "Lettori")["competitor_analysis"], "non_eseguita")
        with self.assertRaises(ValueError):
            read_csv("term\na\n")

    def test_report_injection_and_files(self):
        payload = '</pre><script>alert(1)</script> [click](javascript:alert(1)) ```'
        data = {"payload": payload}
        self.assertNotIn('<script>', html_report(data))
        self.assertNotIn('<script>', markdown(data))
        self.assertIn('&lt;/pre&gt;', markdown(data))
        self.assertIn('default-src', html_report(data))
        with tempfile.TemporaryDirectory() as tmp:
            outputs = write_reports(data, tmp)
            self.assertEqual(json.loads(Path(outputs["json"]).read_text())["payload"], payload)
            self.assertEqual(set(outputs), {"json", "md", "html"})

    def test_cli_invalid_returns_error(self):
        self.assertEqual(main(["schema", "Person", "not-existing-file.json"]), 2)


if __name__ == '__main__':
    unittest.main()
