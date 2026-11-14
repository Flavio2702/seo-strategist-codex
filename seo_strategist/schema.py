"""Sette builder con un contratto locale esplicito, non validazione Schema.org."""
from copy import deepcopy
from datetime import datetime
import math
from .network import valid_url

TYPES = ("Article", "Product", "FAQPage", "LocalBusiness", "Organization", "BreadcrumbList", "Person")


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + ": testo obbligatorio")
    return value.strip()


def _number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(label + ": numero finito obbligatorio")
    return value


def build(kind, data):
    if kind not in TYPES or not isinstance(data, dict):
        raise ValueError("Tipo o input non supportato")
    result = {"@context": "https://schema.org", "@type": kind}
    allowed = {"Article": {"headline", "author", "datePublished", "dateModified", "url"},
               "Product": {"name", "description", "url", "sku", "aggregateRating", "rating_evidence"},
               "FAQPage": {"questions"}, "LocalBusiness": {"name", "address", "url", "telephone"},
               "Organization": {"name", "url", "description"}, "BreadcrumbList": {"items"},
               "Person": {"name", "url", "jobTitle"}}[kind]
    if set(data) - allowed:
        raise ValueError("Campi non supportati dal contratto locale: " + ", ".join(sorted(set(data) - allowed)))
    if kind in ("Product", "LocalBusiness", "Organization", "Person"):
        result["name"] = _text(data.get("name"), "name")
    if kind == "Article":
        result["headline"] = _text(data.get("headline"), "headline")
        result["author"] = {"@type": "Person", "name": _text(data.get("author"), "author")}
        for field in ("datePublished", "dateModified"):
            if field in data:
                value = _text(data[field], field)
                datetime.fromisoformat(value.replace("Z", "+00:00"))
                result[field] = value
        if "datePublished" in result and "dateModified" in result:
            if result["dateModified"][:10] < result["datePublished"][:10]:
                raise ValueError("Modifica precedente alla pubblicazione")
    if kind == "Organization" and "url" not in data:
        raise ValueError("url obbligatoria per Organization")
    if "url" in data:
        result["url"] = valid_url(data["url"])
    for field in ("description", "sku", "telephone", "jobTitle"):
        if field in data:
            result[field] = _text(data[field], field)
    if kind == "LocalBusiness":
        result["address"] = _text(data.get("address"), "address")
    if kind == "FAQPage":
        questions = data.get("questions")
        if not isinstance(questions, list) or not questions:
            raise ValueError("questions deve contenere domande e risposte")
        result["mainEntity"] = []
        for item in questions:
            if not isinstance(item, dict) or set(item) != {"question", "answer"}:
                raise ValueError("Coppia question/answer non valida")
            result["mainEntity"].append({"@type": "Question", "name": _text(item["question"], "question"),
                                         "acceptedAnswer": {"@type": "Answer", "text": _text(item["answer"], "answer")}})
    if kind == "BreadcrumbList":
        items = data.get("items")
        if not isinstance(items, list) or not items:
            raise ValueError("items deve contenere almeno una pagina")
        result["itemListElement"] = []
        for position, item in enumerate(items, 1):
            if not isinstance(item, dict) or set(item) != {"name", "url"}:
                raise ValueError("Elemento breadcrumb non valido")
            result["itemListElement"].append({"@type": "ListItem", "position": position,
                "name": _text(item["name"], "name"), "item": valid_url(item["url"])})
    if kind == "Product" and "aggregateRating" in data:
        evidence = data.get("rating_evidence")
        if not isinstance(evidence, dict) or evidence.get("visible_on_page") is not True or evidence.get("genuine_product_ratings") is not True:
            raise ValueError("Rating richiede attestazione di visibilità e valutazioni autentiche del prodotto")
        valid_url(evidence.get("source_url"))
        rating = data["aggregateRating"]
        if not isinstance(rating, dict) or set(rating) - {"ratingValue", "ratingCount", "bestRating", "worstRating"}:
            raise ValueError("Rating non valido")
        value = _number(rating.get("ratingValue"), "ratingValue")
        count = _number(rating.get("ratingCount"), "ratingCount")
        best = _number(rating.get("bestRating", 5), "bestRating")
        worst = _number(rating.get("worstRating", 1), "worstRating")
        if best <= worst or not worst <= value <= best or count <= 0 or int(count) != count:
            raise ValueError("Intervallo o conteggio rating incoerente")
        result["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": value, "ratingCount": int(count), "bestRating": best, "worstRating": worst}
    return result


def validate(document):
    errors = []
    try:
        if not isinstance(document, dict) or document.get("@context") != "https://schema.org":
            raise ValueError("Oggetto e @context https://schema.org richiesti")
        obj = deepcopy(document)
        kind = obj.pop("@type", None)
        obj.pop("@context")
        if kind == "Article":
            author = obj.get("author")
            if not isinstance(author, dict) or author.get("@type") != "Person":
                raise ValueError("author Person richiesto dal contratto")
            obj["author"] = author.get("name")
        if kind == "FAQPage":
            entities = obj.pop("mainEntity", [])
            if any(e.get("@type") != "Question" or e.get("acceptedAnswer", {}).get("@type") != "Answer" for e in entities):
                raise ValueError("Tipi Question/Answer richiesti")
            obj["questions"] = [{"question": e["name"], "answer": e["acceptedAnswer"]["text"]} for e in entities]
        if kind == "BreadcrumbList":
            items = obj.pop("itemListElement", [])
            if any(e.get("position") != i or e.get("@type") != "ListItem" for i, e in enumerate(items, 1)):
                raise ValueError("Posizioni breadcrumb non sequenziali")
            obj["items"] = [{"name": e["name"], "url": e["item"]} for e in items]
        if "aggregateRating" in obj:
            rating = obj["aggregateRating"]
            if rating.pop("@type", None) != "AggregateRating":
                raise ValueError("Tipo rating non valido")
            # Structural validation cannot establish authenticity of existing markup.
            obj["rating_evidence"] = {"visible_on_page": True, "genuine_product_ratings": True, "source_url": "https://example.invalid/"}
        build(kind, obj)
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        errors.append(str(exc))
    return {"valid_local_contract": not errors, "errors": errors,
            "scope": "Campi e coerenza locali; non validazione completa Schema.org, autenticità rating o idoneità Google."}
