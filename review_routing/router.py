"""Router ex-ante de contenido para revisión multi-provider (política §7.4).

Clasifica artefactos contra una allowlist machine-readable (`config.json`) ANTES de
enrutarlos a un proveedor externo. Filtra (no envía) lo no clasificado como `publico`;
`interno_institucional` se deniega salvo autorización humana explícita;
`personal_confidencial` es prohibición dura (no enrutable, no autorizable por el agente).
Registra un hash SHA-256 del bundle enviado (proveniencia auditable).

Determinista: sin LLM, sólo stdlib. La clasificación la hace la CONFIG, no el agente que
envía (Cambio 3 de la enmienda v1.1: evita autoclasificación sin control técnico ex-ante).

Salida CLI en JSON; el log de ruteo se appende en `logs/review-routing.jsonl` (gitignored).
"""
import argparse
import datetime as _dt
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = pathlib.Path(__file__).resolve().parent / "config.json"
DEFAULT_LOG = ROOT / "logs" / "review-routing.jsonl"


def load_config(path=DEFAULT_CONFIG):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def _matches(pattern, rel):
    rel = rel.replace("\\", "/")
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return rel.startswith(prefix)
    return rel == pattern


def classify(rel, config):
    """Devuelve la clase de un path relático contra la config. default = 'deny'."""
    rel = rel.replace("\\", "/")
    c = config["classification"]
    if any(_matches(p, rel) for p in c.get("personal_confidencial", [])):
        return "personal_confidencial"
    if any(_matches(p, rel) for p in c.get("interno_institucional", [])):
        return "interno_institucional"
    if any(_matches(p, rel) for p in c.get("publico", [])):
        return "publico"
    return config.get("default", "deny")


def _denied_reason(cls):
    return {
        "personal_confidencial": "prohibicion_dura",
        "interno_institucional": "sin_autorizacion_humana",
        "deny": "default_deny",
    }.get(cls, "default_deny")


def route(relpaths, config, repo_root=ROOT, authorized_internal=False):
    """Clasifica y arma el bundle ruteable + la lista de denegados + el hash.

    `authorized_internal`: si True, el contenido `interno_institucional` pasa (siempre
    bajo responsabilidad humana registrada). `personal_confidencial` NUNCA pasa.
    """
    bundle, denied = [], []
    h = hashlib.sha256()
    for rel in relpaths:
        cls = classify(rel, config)
        if cls == "publico" or (cls == "interno_institucional" and authorized_internal):
            full = pathlib.Path(repo_root) / rel
            try:
                data = full.read_bytes()
            except OSError:
                denied.append({"path": rel, "reason": "archivo_no_encontrado"})
                continue
            bundle.append({"path": rel, "bytes": len(data)})
            h.update(rel.replace("\\", "/").encode("utf-8") + b"\n")
            h.update(data)
            h.update(b"\n")
        else:
            denied.append({"path": rel, "reason": _denied_reason(cls)})
    return {
        "bundle": bundle,
        "denied": denied,
        "bundle_sha256": "sha256:" + h.hexdigest(),
        "bundle_empty_sha256_ok": not bundle,
    }


def write_log(decision, provider, model, logpath=DEFAULT_LOG):
    logpath = pathlib.Path(logpath)
    logpath.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "provider": provider,
        "model": model,
        "bundle_count": len(decision["bundle"]),
        "bundle_sha256": decision["bundle_sha256"],
        "denied_count": len(decision["denied"]),
        "bundle": decision["bundle"],
        "denied": decision["denied"],
    }
    with logpath.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return str(logpath)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Router ex-ante de contenido (§7.4).")
    ap.add_argument("files", nargs="+", help="paths relativos a la raíz del repo")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    ap.add_argument("--provider", required=True, help="proveedor destino (p. ej. Anthropic)")
    ap.add_argument("--model", required=True, help="modelo subyacente (p. ej. claude-opus-5)")
    ap.add_argument("--log", default=str(DEFAULT_LOG))
    ap.add_argument("--authorize-internal", action="store_true",
                    help="autoriza humano: deja pasar interno_institucional (NUNCA personal)")
    ap.add_argument("--dry-run", action="store_true", help="no escribir el log")
    args = ap.parse_args(argv)

    config = load_config(args.config)
    decision = route(args.files, config, authorized_internal=args.authorize_internal)
    if not args.dry_run and decision["bundle"]:
        decision["log_path"] = write_log(decision, args.provider, args.model, args.log)
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    return 0 if decision["bundle"] else 1


if __name__ == "__main__":
    sys.exit(main())
