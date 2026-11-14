"""Audit su campione: osservazioni, inferenze e lacune restano separati."""
import re
from urllib.parse import urlsplit, urlunsplit
from .network import Client, valid_url
from .html import analyze_html
from .sitemap import collect_sitemap
from .robots import access
from .browser import render
from .schema import validate


def generic_header_directives(value):
    generic, scoped = [], False
    for part in value.split(","):
        if ":" in part:
            scoped = True
        if not scoped:
            generic.append(part)
    return ",".join(generic)


def llms_quality(response):
    if response.state != "present":
        return {"state": "inconclusive" if response.state != "absent" else "absent", "experimental": True}
    text = response.body
    checks = {"h1": bool(re.search(r"^#\s+\S", text, re.M)),
              "summary": bool(re.search(r"^>\s+\S", text, re.M)),
              "sections": bool(re.search(r"^##\s+\S", text, re.M)),
              "markdown_links": bool(re.search(r"\[[^\]]+\]\(https?://[^)]+\)", text)),
              "not_html": not bool(re.search(r"<html[\s>]", text, re.I))}
    return {"state": "observed", "experimental": True, "checks": checks,
            "note": "Indicatori di struttura della proposta llms.txt v2; qualità semantica e utilizzo non verificati."}


def roadmap(findings):
    groups = {}
    for item in findings:
        group = groups.setdefault(item["code"], {"code": item["code"], "priority": item["priority"],
            "reason": item["reason"], "urls": [], "evidence": item["evidence"],
            "dependencies": item.get("dependencies", []), "missing_data": item.get("missing_data", [])})
        group["urls"].append(item["url"])
    return sorted(groups.values(), key=lambda g: (g["priority"], g["code"]))


def audit(url, sample_size=10, rendering="auto", agents=None, variants=None, client=None):
    url = valid_url(url)
    if not isinstance(sample_size, int) or not 1 <= sample_size <= 100 or rendering not in ("auto", "always", "off"):
        raise ValueError("Campione 1–100 e rendering auto/always/off richiesti")
    agents = ["GPTBot", "OAI-SearchBot"] if agents is None else agents
    if not isinstance(agents, list) or any(not isinstance(a, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,79}", a) for a in agents):
        raise ValueError("Agenti crawler non validi")
    client = client or Client()
    first = client.get(url)
    p = urlsplit(first.final_url)
    origin = urlunsplit((p.scheme, p.netloc, "", "", ""))
    robots = client.get(origin + "/robots.txt")
    llms = client.get(origin + "/llms.txt")
    sitemap_url = origin + "/sitemap.xml"
    discovered = re.findall(r"^\s*sitemap\s*:\s*(\S+)\s*$", robots.body, re.I | re.M) if robots.state == "present" else []
    # Follow only same-origin declarations; external declarations remain visible.
    for candidate in discovered:
        try:
            candidate = valid_url(candidate)
            if urlsplit(candidate).netloc.lower() == p.netloc.lower():
                sitemap_url = candidate
                break
        except ValueError:
            continue
    sitemap = collect_sitemap(client, sitemap_url)
    candidates = [url]
    for item in sitemap["entries"]:
        if "invalid_url" not in item["issues"] and "different_host" not in item["issues"]:
            candidate = valid_url(item["url"])
            if candidate not in candidates:
                candidates.append(candidate)
    selected = candidates[:sample_size]
    inventory = {e["url"] for e in sitemap["entries"]}
    pages, findings = [], []

    def finding(code, page_url, priority, reason, evidence="observed", dependencies=None, missing=None):
        findings.append({"code": code, "url": page_url, "priority": priority, "reason": reason,
                         "evidence": evidence, "dependencies": dependencies or [], "missing_data": missing or []})

    for target in selected:
        response = first if target == url else client.get(target)
        page = {"http": response.public(), "initial": None, "rendering": {"state": "off" if rendering == "off" else "not_needed"}, "rendered": None}
        document = None
        content_type = response.headers.get("content-type", "").lower()
        if response.state == "present" and ("html" in content_type or not content_type):
            document = analyze_html(response.body, response.final_url)
            page["initial"] = document
            should_render = rendering == "always" or (rendering == "auto" and document["script_count"] > 0 and len(document["text"].split()) < 80)
            if should_render:
                rendered = render(response.final_url)
                html = rendered.pop("html", None)
                page["rendering"] = rendered
                if html is not None:
                    page["rendered"] = analyze_html(html, rendered["url"])
                    page["rendering"]["comparison"] = {"initial_words": len(document["text"].split()),
                        "rendered_words": len(page["rendered"]["text"].split()),
                        "title_changed": document["title"] != page["rendered"]["title"],
                        "canonical_changed": document["canonical"] != page["rendered"]["canonical"]}
                else:
                    finding("rendering_inconclusive", target, 2, "Confronto browser non concluso; analisi statica conservata", "inconclusive", missing=["HTML renderizzato"])
            if not document["title"]:
                finding("missing_title", target, 2, "Title assente nell'HTML iniziale")
            elif not 15 <= len(document["title"]) <= 65:
                finding("title_editorial_review", target, 3, "Lunghezza fuori fascia editoriale interna 15–65; non limite Google", "heuristic")
            if not document["descriptions"]:
                finding("missing_description", target, 3, "Meta description assente; snippet effettivo non verificato")
            elif any(not 50 <= len(d) <= 170 for d in document["descriptions"]):
                finding("description_editorial_review", target, 3, "Description fuori fascia editoriale interna 50–170; non limite Google", "heuristic")
            if not any(h["level"] == 1 for h in document["headings"]):
                finding("missing_h1", target, 3, "Nessun H1 rilevato")
            if any(i["alt"] is None for i in document["images"]):
                finding("missing_alt", target, 2, "Immagini senza attributo alt; verificare funzione e contenuto")
            page["schema_validation"] = [validate(obj) for obj in document["jsonld"]]
        else:
            finding("page_unavailable", target, 1, "Pagina non analizzabile come HTML", "inconclusive" if response.state == "inconclusive" else "observed", missing=["HTML analizzabile"])
        directives = [r["value"] for r in document["robots"] if r["agent"] == "robots"] if document else []
        header_robots = response.headers.get("x-robots-tag", "")
        directives.append(header_robots)
        # Agent-specific directives are retained; generic noindex is not inferred from them.
        generic_header = generic_header_directives(header_robots)
        generic_meta = [r["value"] for r in document["robots"] if r["agent"] == "robots"] if document else []
        noindex = bool(re.search(r"\b(noindex|none)\b", " ".join(generic_meta + [generic_header]), re.I)) if document else None
        canonical = document["canonical"] if document else []
        member = target in inventory or response.final_url in inventory
        page["matrix"] = {"requested_url": target, "final_url": response.final_url, "http_status": response.status,
            "redirects": response.redirects, "noindex": noindex, "robots_directives": directives,
            "canonical": canonical, "in_sitemap": True if member else False if sitemap["complete"] else None,
            "indexability": "potentially_indexable_not_verified" if document and not noindex else "noindex_observed" if noindex else "inconclusive"}
        if noindex:
            finding("noindex_review", target, 1, "Direttiva noindex osservata; verificare intenzione prima di modificarla", dependencies=["Conferma obiettivo di indicizzazione"])
        if len(canonical) > 1:
            finding("multiple_canonicals", target, 1, "Canonical multipli nell'HTML iniziale")
        if canonical and canonical != [response.final_url]:
            finding("canonical_other", target, 2, "Canonical dichiarato diverso dall'URL finale; scelta Google non verificata", dependencies=["Verifica equivalenza contenuti"])
        page["ai_crawlers"] = [access(robots, response.final_url, a) for a in agents]
        pages.append(page)
    noncanonical = set()
    for page in pages:
        matrix = page["matrix"]
        if matrix["redirects"] or (matrix["canonical"] and matrix["canonical"] != [matrix["final_url"]]):
            noncanonical.add(matrix["requested_url"])
            if matrix["canonical"] and matrix["canonical"] != [matrix["final_url"]]:
                noncanonical.add(matrix["final_url"])
    for page in pages:
        links = (page["initial"] or {}).get("links", [])
        internal = []
        for link in links:
            if link["navigable"] and urlsplit(link["url"]).netloc.lower() == p.netloc.lower():
                internal.append({**link, "known_noncanonical_target": link["url"].split("#", 1)[0] in noncanonical})
        page["internal_links"] = internal
        if any(l["known_noncanonical_target"] for l in internal):
            finding("internal_noncanonical", page["matrix"]["requested_url"], 2, "Link a un target non canonico noto nel campione", "sample_observation")
    variant_checks = []
    for variant in variants or []:
        v = urlsplit(valid_url(variant))
        if v.hostname.removeprefix("www.") != p.hostname.removeprefix("www."):
            raise ValueError("Variante host estranea al dominio")
        variant_checks.append({"origin": variant, "resources": {
            name: client.get(urlunsplit((v.scheme, v.netloc, "/" + name, "", ""))).public()
            for name in ("robots.txt", "sitemap.xml", "llms.txt")}})
    return {"schema_version": 1, "scope": "sample", "requested_url": url,
            "sample": {"selected": selected, "available_candidates": len(candidates), "limit": sample_size, "selection": "URL iniziale, poi ordine sitemap"},
            "resources": {"robots": robots.public(), "llms": llms.public(), "llms_quality": llms_quality(llms),
                          "sitemap": sitemap, "declared_sitemaps": discovered, "host_variants": variant_checks,
                          "variant_note": "Solo varianti esplicitamente richieste; URL iniziale e finale sempre conservati."},
            "pages": pages, "findings": findings, "roadmap": roadmap(findings),
            "limitations": ["Risultati limitati al campione", "Nessuna misura INP, ranking, traffico o citazioni AI",
                            "robots è una dichiarazione; utilizzo reale dei crawler non verificato", "Nessuna analisi di competitor eseguita"]}
