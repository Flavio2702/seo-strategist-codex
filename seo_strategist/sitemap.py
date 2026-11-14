"""Sitemap XML limitate, con inventario delle verifiche non concluse."""
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit
from .network import valid_url


def parse_sitemap(text):
    if len(text) > 2_000_000 or "<!DOCTYPE" in text.upper() or "<!ENTITY" in text.upper():
        raise ValueError("XML oltre limite o con DTD/entità non ammesse")
    try:
        root = ET.fromstring(text)
    except (ET.ParseError, RecursionError) as exc:
        raise ValueError("XML non valido") from exc
    local = lambda tag: tag.rsplit("}", 1)[-1]
    kind = local(root.tag)
    if kind not in ("urlset", "sitemapindex"):
        raise ValueError("Radice sitemap non supportata")
    entries = []
    for child in root:
        if local(child.tag) != ("url" if kind == "urlset" else "sitemap"):
            continue
        fields = {local(e.tag): (e.text or "").strip() for e in child}
        issues = []
        location = fields.get("loc", "")
        try:
            valid_url(location)
        except ValueError:
            issues.append("invalid_url")
        if "#" in location:
            issues.append("fragment")
        date = fields.get("lastmod")
        if date:
            try:
                parsed = datetime.fromisoformat(date.replace("Z", "+00:00"))
                if parsed.date() > datetime.now(timezone.utc).date():
                    issues.append("future_lastmod")
            except ValueError:
                issues.append("invalid_lastmod")
        entries.append({"url": location, "lastmod": date, "issues": issues})
    return kind, entries


def collect_sitemap(client, url, max_documents=10, max_depth=3, max_urls=1000):
    if not 1 <= max_documents <= 50 or not 0 <= max_depth <= 5 or not 1 <= max_urls <= 10000:
        raise ValueError("Limiti sitemap non validi")
    queue, seen, entries, checks, warnings = [(url, 0)], set(), [], [], []
    origin = urlsplit(url).netloc.lower()
    while queue and len(seen) < max_documents and len(entries) < max_urls:
        target, depth = queue.pop(0)
        if target in seen:
            warnings.append("duplicate_or_cycle: " + target)
            continue
        seen.add(target)
        response = client.get(target)
        checks.append(response.public())
        if response.state != "present":
            continue
        try:
            kind, items = parse_sitemap(response.body)
        except ValueError as exc:
            warnings.append(str(exc) + ": " + target)
            continue
        for item in items:
            if "invalid_url" not in item["issues"] and urlsplit(item["url"]).netloc.lower() != origin:
                item["issues"].append("different_host")
            if kind == "sitemapindex":
                if item["issues"]:
                    warnings.append("index_entry_skipped: " + item["url"])
                elif depth < max_depth:
                    queue.append((item["url"], depth + 1))
                else:
                    warnings.append("depth_limit")
            elif len(entries) < max_urls:
                if any(e["url"] == item["url"] for e in entries):
                    item["issues"].append("duplicate_url")
                entries.append(item)
            else:
                warnings.append("url_limit")
    if queue:
        warnings.append("document_or_url_limit")
    return {"entries": entries, "checks": checks, "warnings": warnings,
            "complete": not warnings and all(c["state"] == "present" for c in checks),
            "limits": {"documents": max_documents, "depth": max_depth, "urls": max_urls}}
