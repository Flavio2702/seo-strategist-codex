"""Report senza HTML attivo proveniente dalle pagine analizzate."""
import html
import json
from pathlib import Path
from .browser import export_pdf

MATRIX_FIELDS = ("requested_url", "final_url", "http_status", "redirects", "noindex", "canonical", "in_sitemap")


def display(value):
    if value is None:
        return "Non verificato"
    if isinstance(value, bool):
        return "Sì" if value else "No"
    if isinstance(value, list):
        return "; ".join(str(v.get("status", "?")) if isinstance(v, dict) else str(v) for v in value) or "—"
    return str(value)


def markdown(data):
    # Escape Markdown syntax while keeping the source readable for reviewers.
    def safe(value):
        return "".join(f"&#{ord(c)};" if c in '&<>[]()`|\\\n\r*_!#' else c for c in str(value))
    lines = ["# Rapporto SEO Strategist", "", "Analisi sul campione; segnali e priorità non garantiscono risultati.", ""]
    if data.get("synthetic"):
        lines += ["**DEMO: dati sintetici generati localmente. Nessun sito reale analizzato.**", ""]
    lines += ["## Matrice delle pagine", "", "| URL richiesta | URL finale | HTTP finale | Redirect | Noindex | Canonical | Sitemap |", "|---|---|---|---|---|---|---|"]
    for page in data.get("pages", []):
        m = page["matrix"]
        lines.append("| " + " | ".join(safe(display(m[k])) for k in MATRIX_FIELDS) + " |")
    lines += ["", "## Roadmap", ""]
    for item in data.get("roadmap", []):
        lines.append(f"- P{safe(item['priority'])}: {safe(item['reason'])} — {safe(item['urls'])}")
    lines += ["", "## Evidenze complete", "", "Tutti i campi, inclusi errori e limiti, sono riportati di seguito come testo.", "", "<pre>" + html.escape(json.dumps(data, ensure_ascii=False, indent=2)) + "</pre>", ""]
    return "\n".join(lines)


def html_report(data):
    escaped = html.escape(json.dumps(data, ensure_ascii=False, indent=2))
    rows = []
    for page in data.get("pages", []):
        m = page["matrix"]
        rows.append("<tr>" + "".join("<td>" + html.escape(display(m[k])) + "</td>" for k in MATRIX_FIELDS) + "</tr>")
    roadmap_items = "".join(f"<li><strong>P{html.escape(str(i['priority']))}</strong> {html.escape(i['reason'])}</li>" for i in data.get("roadmap", []))
    demo = "<p class='notice'>DEMO — dati sintetici generati localmente. Nessun sito reale analizzato.</p>" if data.get("synthetic") else ""
    return """<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Rapporto SEO Strategist</title>
<style>body{font:16px/1.6 system-ui,sans-serif;max-width:1100px;margin:40px auto;padding:0 24px;color:#15313b;background:#fafbf8}h1{font-size:2.4rem}h2{border-bottom:2px solid #337b75;padding-top:1rem}.notice{padding:16px;background:#e4f0ed;border-left:4px solid #337b75}table{border-collapse:collapse;width:100%;font-size:13px}td,th{border:1px solid #b8c8ca;padding:8px;text-align:left;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;background:#edf1ef;padding:18px}footer{margin-top:40px}@media print{body{margin:0;padding:8px}h1{font-size:24px}pre{font-size:8px}}</style></head><body>
<p>SEO STRATEGIST · CODEX</p><h1>Dal rilievo alla decisione</h1>""" + demo + "<p>Risultati sul campione. Osservazioni, inferenze e verifiche non concluse rimangono distinguibili.</p><h2>Matrice delle pagine</h2><table><thead><tr><th>URL richiesta</th><th>URL finale</th><th>HTTP finale</th><th>Redirect</th><th>Noindex</th><th>Canonical</th><th>Sitemap</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table><h2>Roadmap</h2><ol>" + roadmap_items + "</ol><h2>Evidenze complete</h2><pre>" + escaped + "</pre><footer>Nessuna promessa di ranking, traffico o citazioni AI. Verificare le raccomandazioni prima di applicarle.</footer></body></html>"


def write_reports(data, directory, pdf=False):
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for extension, content in (("json", json.dumps(data, ensure_ascii=False, indent=2) + "\n"), ("md", markdown(data)), ("html", html_report(data))):
        path = target / ("report." + extension)
        path.write_text(content, encoding="utf-8", newline="\n")
        outputs[extension] = str(path)
    if pdf:
        outputs["pdf"] = export_pdf(outputs["html"], target / "report.pdf")
    return outputs
