"""HTTP limitato: nessuna ambiguità fra risorsa assente e verifica fallita."""
from dataclasses import asdict, dataclass, field
import socket
from http.client import HTTPException
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler


def valid_url(value):
    if not isinstance(value, str) or any(c.isspace() for c in value):
        raise ValueError("URL non valido")
    p = urlsplit(value)
    if p.scheme not in ("http", "https") or not p.hostname or p.username or p.password:
        raise ValueError("Usare URL http/https senza credenziali")
    _ = p.port
    return urlunsplit((p.scheme, p.netloc, p.path or "/", p.query, ""))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass
class Response:
    requested_url: str
    final_url: str
    status: int | None = None
    state: str = "inconclusive"
    body: str = ""
    headers: dict = field(default_factory=dict)
    redirects: list = field(default_factory=list)
    attempts: int = 0
    error: str | None = None

    def public(self):
        data = asdict(self)
        data.pop("body")
        return data


class Client:
    def __init__(self, timeout=10, retries=2, max_redirects=5, max_bytes=2_000_000):
        if not 0 < timeout <= 60 or not 0 <= retries <= 2 or not 0 <= max_redirects <= 10 or not 0 < max_bytes <= 5_000_000:
            raise ValueError("Limiti HTTP non validi")
        self.timeout, self.retries = timeout, retries
        self.max_redirects, self.max_bytes = max_redirects, max_bytes
        self.opener = build_opener(NoRedirect())

    def get(self, url):
        url = valid_url(url)
        result = Response(url, url)
        current = url
        for hop in range(self.max_redirects + 1):
            for attempt in range(self.retries + 1):
                result.attempts += 1
                result.status = None
                result.headers = {}
                try:
                    request = Request(current, headers={"User-Agent": "SEOStrategistCodex/0.1", "Accept-Encoding": "identity"})
                    try:
                        stream = self.opener.open(request, timeout=self.timeout)
                    except HTTPError as exc:
                        stream = exc
                    with stream:
                        result.status = stream.code
                        result.headers = {k.lower(): v for k, v in stream.headers.items()}
                        raw = stream.read(self.max_bytes + 1)
                        if len(raw) > self.max_bytes:
                            result.error = "response_too_large"
                            return result
                        charset = stream.headers.get_content_charset() or "utf-8"
                        try:
                            result.body = raw.decode(charset, errors="replace")
                        except LookupError:
                            result.body = raw.decode("utf-8", errors="replace")
                    if result.status in (429, 500, 502, 503, 504) and attempt < self.retries:
                        time.sleep(0.05 * (attempt + 1))
                        continue
                    result.error = None
                    break
                except (URLError, TimeoutError, socket.timeout, OSError, HTTPException) as exc:
                    result.body = ""
                    result.error = type(exc).__name__
                    if attempt == self.retries:
                        return result
                    time.sleep(0.05 * (attempt + 1))
            if result.status in (301, 302, 303, 307, 308):
                location = result.headers.get("location")
                if not location:
                    result.error = "redirect_without_location"
                    return result
                try:
                    target = valid_url(urljoin(current, location))
                except ValueError:
                    result.error = "invalid_redirect_target"
                    return result
                result.redirects.append({"from": current, "to": target, "status": result.status})
                if hop == self.max_redirects:
                    result.error = "redirect_limit"
                    return result
                current = target
                result.final_url = current
                continue
            result.state = "present" if 200 <= result.status < 300 else "absent" if result.status in (404, 410) else "http_error"
            return result
        return result
