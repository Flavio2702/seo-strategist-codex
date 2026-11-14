"""Genera davvero la demo tramite HTTP locale; normalizza solo porta e header volatili."""
import argparse
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from seo_strategist.audit import audit
from seo_strategist.editorial import keywords, brief
from seo_strategist.report import write_reports
from tests.site import site


def generate():
    with site() as (origin, counts):
        result = audit(origin, rendering="off")
    result = json.loads(json.dumps(result).replace(origin, "https://demo.example.invalid"))
    def stable(value):
        if isinstance(value, dict):
            for key in list(value):
                if key == "headers":
                    value[key] = {k: v for k, v in value[key].items() if k not in ("date", "server", "content-length")}
                else:
                    stable(value[key])
        elif isinstance(value, list):
            for item in value:
                stable(item)
    stable(result)
    result["synthetic"] = True
    result["demo_method"] = "HTTP reale su server sintetico loopback; origine sostituita da dominio riservato, header volatili rimossi. Rendering off."
    result["keyword_example"] = keywords(["comprare scarpe rosse", "prezzo scarpe rosse", "come scegliere scarpe"])
    result["brief_example"] = brief("Scelta delle scarpe", "lettori di esempio")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", default="demo")
    args = parser.parse_args()
    data = generate()
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            write_reports(data, tmp)
            for name in ("report.json", "report.md", "report.html"):
                if (Path(tmp) / name).read_bytes() != (Path(args.output) / name).read_bytes():
                    raise SystemExit("Demo non riproducibile: " + name)
        print("Demo JSON/Markdown/HTML riproducibile byte per byte")
    else:
        write_reports(data, args.output)
        print("Demo sintetica generata in " + args.output)


if __name__ == "__main__":
    main()
