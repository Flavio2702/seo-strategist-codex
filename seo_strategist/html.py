"""Estrazione statica; il contenuto remoto non viene eseguito."""
from html.parser import HTMLParser
import json
import re
from urllib.parse import urljoin, urlsplit


def resolve(base, href):
    try:
        return urljoin(base, href)
    except ValueError:
        return href


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.headings, self.images, self.links, self.canonicals, self.hreflang = [], [], [], [], []
        self.description, self.robots, self.jsonld, self.jsonld_errors = [], [], [], []
        self.text, self.dates = [], []
        self.lists = 0
        self.citations = 0
        self.scripts = 0
        self._title = False
        self._heading = None
        self._anchor = None
        self._hidden = []
        self._json = None
        self.base = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "base" and self.base is None:
            self.base = a.get("href")
        if tag == "title":
            self._title = True
        if re.fullmatch("h[1-6]", tag):
            self._heading = {"level": int(tag[1]), "text": ""}
            self.headings.append(self._heading)
        if tag in ("script", "style", "template"):
            self._hidden.append(tag)
        if tag == "script":
            self.scripts += 1
            if a.get("type", "").lower().split(";")[0] == "application/ld+json":
                self._json = []
        if tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.description.append(a.get("content", ""))
            if name == "robots" or name.endswith("bot"):
                self.robots.append({"agent": name, "value": a.get("content", "")})
            if a.get("property") in ("article:modified_time", "article:published_time"):
                self.dates.append(a.get("content", ""))
        if tag == "link":
            rel = a.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonicals.append(a.get("href", ""))
            if "alternate" in rel and "hreflang" in a:
                self.hreflang.append({"language": a["hreflang"], "url": a.get("href", "")})
        if tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt"), "decorative_candidate": a.get("alt") == ""})
        if tag == "a":
            self._anchor = {"href": a.get("href"), "text": "", "rel": a.get("rel", "")}
            self.links.append(self._anchor)
        if tag in ("ul", "ol"):
            self.lists += 1
        if tag in ("cite", "blockquote"):
            self.citations += 1
        if tag == "time" and a.get("datetime"):
            self.dates.append(a["datetime"])

    def handle_endtag(self, tag):
        if tag == "script" and self._json is not None:
            try:
                self.jsonld.append(json.loads("".join(self._json)))
            except (ValueError, RecursionError):
                self.jsonld_errors.append("JSON-LD non decodificabile")
            self._json = None
        if tag in self._hidden:
            self._hidden.remove(tag)
        if tag == "title":
            self._title = False
        if re.fullmatch("h[1-6]", tag):
            self._heading = None
        if tag == "a":
            self._anchor = None

    def handle_data(self, data):
        if self._json is not None:
            self._json.append(data)
        if self._hidden:
            return
        if self._title:
            self.title.append(data)
        else:
            self.text.append(data)
        if self._heading is not None:
            self._heading["text"] += data
        if self._anchor is not None:
            self._anchor["text"] += data


def analyze_html(source, url):
    if not isinstance(source, str) or len(source) > 2_000_000:
        raise ValueError("HTML assente o oltre il limite")
    doc = Document()
    doc.feed(source)
    doc.close()
    base = resolve(url, doc.base) if doc.base else url
    links = []
    for item in doc.links:
        href = item["href"]
        target = resolve(base, href) if href is not None else None
        try:
            navigable = target is not None and urlsplit(target).scheme in ("http", "https") and bool(urlsplit(target).hostname)
        except ValueError:
            navigable = False
        links.append({**item, "url": target, "navigable": navigable,
                      "generic_anchor": item["text"].strip().lower() in ("", "qui", "clicca qui", "leggi", "scopri di più", "read more", "click here")})
    signals = {"headings": bool(doc.headings), "question_headings": any("?" in h["text"] for h in doc.headings),
               "citation_markup": doc.citations > 0, "date_markup": bool(doc.dates), "lists": doc.lists > 0, "structured_data": bool(doc.jsonld)}
    return {"title": " ".join("".join(doc.title).split()), "descriptions": doc.description,
            "headings": doc.headings, "text": " ".join(" ".join(doc.text).split()), "images": doc.images,
            "canonical": [resolve(base, c) for c in doc.canonicals], "robots": doc.robots,
            "hreflang": [{**h, "url": resolve(base, h["url"])} for h in doc.hreflang],
            "jsonld": doc.jsonld, "jsonld_errors": doc.jsonld_errors, "links": links, "dates": doc.dates,
            "script_count": doc.scripts, "geo": {"signals": signals, "heuristic_score": sum(signals.values()),
            "scale": "0–6, euristica interna; non misura citazioni o ranking", "evidence": "observed_markup",
            "limitations": "Citazioni, date e JSON-LD rilevati non sono verificati quanto a verità o qualità."}}
