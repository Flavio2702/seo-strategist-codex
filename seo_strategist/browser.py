"""Browser opzionale: risultati separati e nessun profilo personale."""
from pathlib import Path
from .network import valid_url


def render(url, timeout=10000):
    valid_url(url)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"state": "unavailable", "error": "Playwright non installato"}
    try:
        with sync_playwright() as engine:
            browser = engine.chromium.launch()
            context = browser.new_context(accept_downloads=False, service_workers="block")
            page = context.new_page()
            response = page.goto(url, wait_until="networkidle", timeout=timeout)
            content = page.content()
            result = {"state": "rendered", "url": page.url, "status": response.status if response else None,
                      "html": content if len(content) <= 2_000_000 else None}
            if result["html"] is None:
                result = {"state": "inconclusive", "error": "HTML renderizzato oltre limite"}
            browser.close()
            return result
    except Exception as exc:
        return {"state": "inconclusive", "error": type(exc).__name__}


def export_pdf(html_path, output):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"state": "unavailable", "error": "Playwright non installato"}
    try:
        with sync_playwright() as engine:
            browser = engine.chromium.launch()
            context = browser.new_context(java_script_enabled=False, service_workers="block")
            context.route("**/*", lambda route: route.continue_() if route.request.url.startswith("file:") else route.abort())
            page = context.new_page()
            page.goto(Path(html_path).resolve().as_uri())
            page.pdf(path=str(output), format="A4", print_background=True)
            browser.close()
        return {"state": "written", "path": str(output)}
    except Exception as exc:
        return {"state": "inconclusive", "error": type(exc).__name__}
