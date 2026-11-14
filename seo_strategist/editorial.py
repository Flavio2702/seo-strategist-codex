"""Clustering e bozze deterministici senza metriche inventate."""
import csv
import io
import re

STOP = {"a", "di", "da", "il", "la", "le", "i", "gli", "un", "una", "per", "con", "in", "the", "a", "of", "and", "come"}


def keywords(values):
    if not isinstance(values, list) or not values or len(values) > 10000:
        raise ValueError("Fornire da 1 a 10000 keyword")
    normalized = []
    for value in values:
        if not isinstance(value, str) or not value.strip() or len(value) > 500:
            raise ValueError("Keyword non valida")
        text = " ".join(value.lower().split())
        if text not in normalized:
            normalized.append(text)
    clusters = []
    for text in normalized:
        tokens = set(re.findall(r"\w+", text)) - STOP
        match = None
        for group in clusters:
            union = tokens | group["tokens"]
            if union and len(tokens & group["tokens"]) / len(union) >= 0.5:
                match = group
                break
        if match is None:
            match = {"id": len(clusters) + 1, "tokens": tokens, "keywords": []}
            clusters.append(match)
        words = set(re.findall(r"\w+", text))
        intent = "transactional" if words & {"comprare", "acquista", "prezzo", "buy", "prezzi"} else "commercial" if words & {"migliori", "confronto", "recensioni", "best", "vs"} else "navigational" if words & {"login", "accedi", "ufficiale"} else "informational"
        match["keywords"].append({"keyword": text, "intent": intent, "evidence": "rule_based_inference",
            "opportunity": "specifica_da_validare" if len(tokens) >= 3 else "ampia_da_esplorare", "volume": None, "difficulty": None})
    return {"clusters": [{"id": g["id"], "seed_tokens": sorted(g["tokens"]), "keywords": g["keywords"]} for g in clusters],
            "method": "Jaccard >= 0.5 rispetto al primo elemento del cluster; dipende dall'ordine di input. Intent per parole chiave, nessuna misura SERP.",
            "missing_data": ["volumi misurati", "difficoltà misurata", "SERP verificata"]}


def read_csv(text):
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or "keyword" not in reader.fieldnames:
        raise ValueError("CSV richiede colonna keyword")
    return [row.get("keyword") for row in reader]


def brief(topic, audience, intent="informational", evidence=None):
    if any(not isinstance(v, str) or not v.strip() for v in (topic, audience, intent)):
        raise ValueError("Topic, pubblico e intento obbligatori")
    if evidence is not None and (not isinstance(evidence, list) or any(not isinstance(e, str) for e in evidence)):
        raise ValueError("evidence deve essere una lista di fonti fornite")
    return {"status": "bozza_da_revisionare", "topic": topic, "audience": audience, "intent": intent,
            "working_title": topic + ": guida per " + audience,
            "outline": ["Problema del lettore e risposta iniziale", "Concetti e criteri di scelta", "Esempio verificabile", "Limiti e prossimi passi"],
            "evidence_supplied": evidence or [], "competitor_analysis": "non_eseguita",
            "requirements": ["Verificare ogni dato e fonte", "Aggiungere esperienza o esempi originali", "Controllare che il titolo rispecchi il contenuto"],
            "missing_data": ["SERP corrente", "differenziazione verificata", "dati proprietari e revisione esperta"]}
