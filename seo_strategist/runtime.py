"""Profilo versionato e cancellazione confinata al runtime del progetto."""
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
from .network import valid_url

FIELDS = ("role", "tools", "site", "stage", "geography", "priority", "content_volume", "budget")
CHOICES = {
    "role": ["marketing", "founder", "editor", "seo"],
    "tools": ["nessuno", "export manuali", "browser"],
    "stage": ["idea", "lancio", "crescita", "consolidamento"],
    "priority": ["seo", "geo", "entrambi"],
    "geography": ["italia/italiano", "internazionale da precisare", "altro mercato da precisare"],
    "content_volume": ["0–20", "21–100", "oltre 100"],
    "budget": ["nessuno", "limitato", "disponibile"],
}


def normalize(field, answer):
    if field not in FIELDS or not isinstance(answer, str) or not answer.strip() or len(answer) > 2000:
        raise ValueError("Risposta non valida")
    value = answer.strip()
    if field == "site" and value.lower() in ("2", "nessun sito", "non ho ancora un sito"):
        return {"original": answer, "normalized": None, "method": "explicit_no_site"}
    choices = CHOICES.get(field, [])
    if value.isdecimal() and choices:
        index = int(value) - 1
        if not 0 <= index < len(choices):
            raise ValueError("Opzione fuori intervallo; usare testo libero")
        value = choices[index]
    elif field == "site":
        value = valid_url(value)
    else:
        value = " ".join(value.split()).lower()
    return {"original": answer, "normalized": value, "method": "explicit_choice_or_text"}


def profile(answers=None, env_names=None):
    answers = {} if answers is None else answers
    if not isinstance(answers, dict) or set(answers) - set(FIELDS):
        raise ValueError("Campi profilo sconosciuti")
    names = [] if env_names is None else env_names
    if not isinstance(names, list) or any(not isinstance(n, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]{0,79}", n) for n in names):
        raise ValueError("Specificare solo nomi di variabili d'ambiente")
    return {"schema_version": 1, "answers": {k: normalize(k, v) for k, v in answers.items()}, "env_names": names}


def validate_profile(data):
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        raise ValueError("Versione profilo non supportata; nessuna migrazione automatica")
    if not isinstance(data.get("answers"), dict):
        raise ValueError("Profilo privo di answers")
    try:
        rebuilt = profile({k: v["original"] for k, v in data["answers"].items()}, data.get("env_names", []))
    except (KeyError, TypeError) as exc:
        raise ValueError("Profilo malformato") from exc
    if rebuilt != data:
        raise ValueError("Profilo incoerente con lo schema di normalizzazione")
    return data


def runtime_dir(project):
    root = Path(project).resolve(strict=True)
    target = root / ".seo-runtime"
    if not root.is_dir() or target.is_symlink() or (target.exists() and target.resolve() != target):
        raise ValueError("Percorso runtime non autorizzato")
    if target.exists() and (not target.is_dir() or getattr(target, "is_junction", lambda: False)()):
        raise ValueError("Runtime non valido o junction")
    return target


def save_profile(project, data):
    validate_profile(data)
    directory = runtime_dir(project)
    directory.mkdir(exist_ok=True)
    target = directory / "profile.json"
    if target.is_symlink():
        raise ValueError("Profilo collegato fuori runtime")
    temporary = directory / "profile.new"
    if temporary.is_symlink():
        raise ValueError("File temporaneo non autorizzato")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(target)


def load_profile(project):
    target = runtime_dir(project) / "profile.json"
    if target.is_symlink():
        raise ValueError("Profilo collegato fuori runtime")
    if not target.exists():
        return profile()
    try:
        return validate_profile(json.loads(target.read_text(encoding="utf-8")))
    except (OSError, ValueError) as exc:
        raise ValueError("Profilo illeggibile o non valido; conservarlo e riconfigurare esplicitamente") from exc


def capabilities(data):
    validate_profile(data)
    return {"optional_modules": {"playwright": importlib.util.find_spec("playwright") is not None},
            "environment_present": {name: bool(os.environ.get(name)) for name in data["env_names"]},
            "declared_tools": data["answers"].get("tools"), "connection_verified": False,
            "note": "Presenza locale e strumenti dichiarati non dimostrano una connessione."}


def status(project):
    data = load_profile(project)
    recent = runtime_dir(project) / "recent.json"
    results = []
    if recent.exists() and not recent.is_symlink():
        try:
            results = json.loads(recent.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            results = ["Registro risultati illeggibile"]
    return {"profile": data, "missing": [k for k in FIELDS if k not in data["answers"]],
            "capabilities": capabilities(data), "recent_results": results}


def remember(project, report_path):
    directory = runtime_dir(project)
    directory.mkdir(exist_ok=True)
    target = directory / "recent.json"
    if target.is_symlink():
        raise ValueError("Registro collegato fuori runtime")
    target.write_text(json.dumps([str(Path(report_path).resolve())]), encoding="utf-8")


def reset(project, dry_run=True):
    target = runtime_dir(project)
    if not target.exists():
        return {"dry_run": dry_run, "files": [], "deleted": False}
    files = []
    for child in target.rglob("*"):
        if child.is_symlink() or getattr(child, "is_junction", lambda: False)() or not child.resolve().is_relative_to(target):
            raise ValueError("Link o percorso fuori perimetro: reset interrotto")
        files.append(str(child.relative_to(target)))
    if not dry_run:
        shutil.rmtree(target)
    return {"dry_run": dry_run, "files": sorted(files), "deleted": not dry_run}
