"""Valutazione dichiarativa di robots.txt, non prova di accesso dei crawler."""
import re
from urllib.parse import quote, urlsplit


def _path(value):
    # Decode only percent-encoded ASCII unreserved characters; preserve reserved bytes.
    unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
    value = re.sub(r"%([0-9a-fA-F]{2})", lambda m: chr(int(m[1], 16)) if chr(int(m[1], 16)) in unreserved else "%" + m[1].upper(), value)
    return quote(value, safe="/%*?$=&;:+,@!~'()-._")


def access(response, url, agent):
    result = {"agent": agent, "url": url, "declared_access": None, "state": "inconclusive",
              "actual_use": "Non deducibile: accesso, indicizzazione e citazioni non verificati."}
    if response.state != "present":
        result["reason"] = "robots.txt non disponibile con risposta conclusiva 2xx"
        return result
    if "<html" in response.body.lower():
        result["reason"] = "La risposta sembra HTML, non robots.txt"
        return result
    groups, agents, rules = [], [], []
    for line in response.body.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = (s.strip() for s in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if rules:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(value.lower())
        elif key in ("allow", "disallow") and agents:
            rules.append((key, value))
    groups.append((agents, rules))
    exact = [r for names, r in groups if agent.lower() in names]
    chosen = exact if exact else [r for names, r in groups if "*" in names]
    parsed = urlsplit(url)
    target = _path((parsed.path or "/") + ("?" + parsed.query if parsed.query else ""))
    matches = []
    for group in chosen:
        for key, raw in group:
            if not raw:
                continue
            pattern = _path(raw)
            anchored = pattern.endswith("$")
            if anchored:
                pattern = pattern[:-1]
            regex = "^" + ".*".join(re.escape(p) for p in pattern.split("*")) + ("$" if anchored else "")
            if re.search(regex, target):
                matches.append((len(pattern.replace("*", "").encode()), key == "allow", raw))
    winner = max(matches, default=(0, True, "no_matching_rule"))
    result.update(declared_access=winner[1], state="declared", reason=winner[2])
    return result
