import argparse
import json
from pathlib import Path
import sys
from .audit import audit
from .editorial import keywords, read_csv, brief
from .report import write_reports
from .runtime import profile, save_profile, status, reset, remember
from .schema import build, validate, TYPES


def main(argv=None):
    parser = argparse.ArgumentParser(description="SEO Strategist: audit su campione e strumenti locali")
    parser.add_argument("--project", default=".", help="Directory del progetto per il solo stato runtime")
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("audit", help="Audit di un URL http/https")
    p.add_argument("url")
    p.add_argument("--sample", type=int, default=10)
    p.add_argument("--render", choices=("auto", "always", "off"), default="auto")
    p.add_argument("--agent", action="append")
    p.add_argument("--variant", action="append")
    p.add_argument("--output", default="reports/latest")
    p.add_argument("--pdf", action="store_true")
    commands.add_parser("status")
    p = commands.add_parser("configure", help="JSON con answers testuali ed env_names, senza segreti")
    p.add_argument("input")
    p = commands.add_parser("reset-runtime", aliases=["pulisci-runtime", "clean-runtime"])
    p.add_argument("--apply", action="store_true", help="Senza questa opzione mostra soltanto il piano")
    p = commands.add_parser("keywords")
    p.add_argument("terms", nargs="*")
    p.add_argument("--csv")
    p = commands.add_parser("brief")
    p.add_argument("topic")
    p.add_argument("--audience", required=True)
    p.add_argument("--intent", default="informational")
    p = commands.add_parser("schema")
    p.add_argument("kind", choices=TYPES)
    p.add_argument("input")
    p = commands.add_parser("validate-schema")
    p.add_argument("input")
    args = parser.parse_args(argv)
    try:
        if args.command == "audit":
            data = audit(args.url, args.sample, args.render, args.agent, args.variant)
            result = write_reports(data, args.output, args.pdf)
            remember(args.project, result["json"])
        elif args.command == "status":
            result = status(args.project)
        elif args.command == "configure":
            raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
            if not isinstance(raw, dict) or set(raw) - {"answers", "env_names"}:
                raise ValueError("Input configurazione non valido")
            result = profile(raw.get("answers", {}), raw.get("env_names", []))
            save_profile(args.project, result)
        elif args.command in ("reset-runtime", "pulisci-runtime", "clean-runtime"):
            result = reset(args.project, not args.apply)
        elif args.command == "keywords":
            values = read_csv(Path(args.csv).read_text(encoding="utf-8-sig")) if args.csv else args.terms
            result = keywords(values)
        elif args.command == "brief":
            result = brief(args.topic, args.audience, args.intent)
        elif args.command == "schema":
            result = build(args.kind, json.loads(Path(args.input).read_text(encoding="utf-8")))
        else:
            result = validate(json.loads(Path(args.input).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print("Errore: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
