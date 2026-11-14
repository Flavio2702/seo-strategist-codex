"""Sito sintetico scritto per questa suite, disponibile soltanto su loopback."""
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import time


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        origin = "http://" + self.headers["Host"]
        path = self.path
        self.server.counts[path] = self.server.counts.get(path, 0) + 1
        status, kind, body, extra = 200, "text/html; charset=utf-8", "", {}
        if path == "/robots.txt":
            kind = "text/plain"
            body = f"User-agent: *\nAllow: /\nUser-agent: GPTBot\nDisallow: /private\nSitemap: {origin}/sitemap.xml\n"
        elif path == "/llms.txt":
            kind = "text/plain"
            body = f"# Laboratorio sintetico\n\n> Risorse dimostrative.\n\n## Guide\n- [Guida]({origin}/article): esempio locale\n"
        elif path == "/sitemap.xml":
            kind = "application/xml"
            body = f'<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>{origin}/pages.xml</loc></sitemap></sitemapindex>'
        elif path == "/pages.xml":
            kind = "application/xml"
            body = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{origin}{p}</loc><lastmod>2025-01-10</lastmod></url>" for p in ("/", "/article", "/old", "/private", "/missing")) + "</urlset>"
        elif path == "/":
            body = '<html><head><title>Laboratorio SEO sintetico</title><meta name="description" content="Pagina dimostrativa di un audit locale."><link rel="canonical" href="/"></head><body><h1>Laboratorio</h1><a href="/old">clicca qui</a><a href="/article">Guida sintetica</a><img src="/photo.png"><p>Dati inventati per verificare il funzionamento del software.</p></body></html>'
        elif path == "/article":
            body = '<html><head><title>Guida sintetica alla ricerca</title><link rel="canonical" href="/article"></head><body><h1>Come verificare le fonti?</h1><ul><li>Leggi la fonte primaria</li></ul><cite>Fonte dimostrativa</cite><time datetime="2025-01-10">10 gennaio</time><script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":"Guida sintetica","author":{"@type":"Person","name":"Autore di esempio"}}</script></body></html>'
        elif path == "/private":
            body = '<html><head><meta name="robots" content="noindex"><link rel="canonical" href="/article"></head><body><h2>Pagina riservata dimostrativa</h2></body></html>'
        elif path == "/old":
            status, extra = 301, {"Location": "/article"}
        elif path == "/loop":
            status, extra = 302, {"Location": "/loop"}
        elif path == "/bad-redirect":
            status, extra = 302, {"Location": "file:///etc/passwd"}
        elif path == "/retry":
            status = 503 if self.server.counts[path] < 3 else 200
            body = "retry result"
        elif path == "/forbidden":
            status = 403
        elif path == "/slow":
            time.sleep(0.15)
            body = "slow"
        elif path == "/big":
            body = "x" * 2000
        elif path == "/dynamic":
            body = '<html><head><title>Prima</title></head><body><main id="content"></main><script>document.title="Dopo";document.getElementById("content").innerHTML="<h1>Contenuto renderizzato locale</h1>";</script></body></html>'
        else:
            status, body = 404, "not found"
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(payload)))
        for key, value in extra.items():
            self.send_header(key, value)
        self.end_headers()
        try:
            self.wfile.write(payload)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass


@contextmanager
def site():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    server.counts = {}
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield "http://127.0.0.1:" + str(server.server_port), server.counts
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
