"""Router ex-ante de contenido para revisión multi-provider (política §7.4).

Clasifica artefactos contra una allowlist machine-readable (`config.json`) ANTES de
enrutarlos a un proveedor externo, y **confin a** la lectura al repo. Filtra lo no
clasificado como `publico`; en v1 `interno_institucional` se **deniega siempre** (no hay
pipeline de anonimización aún; se habilitará con el harness); `personal_confidencial` es
prohibición dura. Registra un hash del bundle enviado Y de la config.

Determinista: sin LLM, sólo stdlib. La clasificación la hace la CONFIG, no el agente.

LIMITES (honestos, §7.4): este router es un **control de advertencia + bitácora de
auditoría**, NO una frontera de egreso criptográficamente enforceada. Un agente
determinado podría bypasarlo (copiar contenido a una ruta pública, o invocar al CLI
externo directamente). El **egress real** (bundle sellado + control de red + log
append-only fuera del agente) es deuda del **harness** de revisión, no de este módulo.
Aqui garantizamos: (a) confinamiento de ruta (sin `..`/absolutos/symlink fuera de repo),
(b) clasificación por config, (c) bitácora con hash de bundle Y de config.
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
        prefix = pattern[:-2]  # conserva la '/' → "docs/adr/" (no "docs/adr")
        return rel.startswith(prefix)
    return rel == pattern


def classify(rel, config):
    """Clase de un path relativo contra la config. default = 'deny'."""
    rel = rel.replace("\\", "/")
    c = config["classification"]
    if any(_matches(p, rel) for p in c.get("personal_confidencial", [])):
        return "personal_confidencial"
    if any(_matches(p, rel) for p in c.get("interno_institucional", [])):
        return "interno_institucional"
    if any(_matches(p, rel) for p in c.get("publico", [])):
        return "publico"
    return config.get("default", "deny")


def _confined(rel, repo_root):
    """Resuelve rel bajo repo_root y verifica que NO escape (.., absoluto, symlink fuera).
    Devuelve (full_path | None, ok: bool)."""
    root = pathlib.Path(repo_root).resolve()
    rel = rel.replace("\\", "/")
    try:
        full = (root / rel).resolve()
    except (OSError, ValueError):
        return None, False
    return full, full.is_relative_to(root)


def _most_restrictive(*classes):
    order = ["personal_confidencial", "interno_institucional", "deny", "publico"]
    best = "publico"
    for c in classes:
        if order.index(c) < order.index(best):
            best = c
    return best


def route(relpaths, config, repo_root=ROOT):
    """Clasifica, confina y arma el bundle ruteable + denegados + hash.

    v1: `interno_institucional` se deniega SIEMPRE (no hay pipeline de anonimización
    todavía — se habilita con el harness). `personal_confidencial` NUNCA se envía.
    Anti-bypass: se clasifica tanto la ruta pedida como la **resuelta** (canónica) y se
    aplica la clase MÁS restrictiva -> un symlink desde una ruta pública hacia un archivo
    confidencial del repo queda denegado. Paths que escapan del repo -> path_traversal.
    """
    root = pathlib.Path(repo_root).resolve()
    bundle, denied = [], []
    h = hashlib.sha256()
    for rel in relpaths:
        full, ok = _confined(rel, repo_root)
        rel_n = rel.replace("\\", "/")
        if not ok or pathlib.PurePosixPath(rel_n).is_absolute() or ".." in rel_n.split("/"):
            denied.append({"path": rel, "reason": "path_traversal"})
            continue
        try:
            rel_resolved = full.relative_to(root).as_posix()
        except ValueError:
            denied.append({"path": rel, "reason": "path_traversal"})
            continue
        cls = _most_restrictive(classify(rel, config), classify(rel_resolved, config))
        if cls != "publico":
            reason = {"personal_confidencial": "prohibicion_dura",
                      "interno_institucional": "interno_anonimizacion_pendiente",
                      "deny": "default_deny"}.get(cls, "default_deny")
            denied.append({"path": rel, "reason": reason})
            continue
        try:
            data = full.read_bytes()
        except OSError:
            denied.append({"path": rel, "reason": "archivo_no_encontrado"})
            continue
        bundle.append({"path": rel, "bytes": len(data)})
        h.update(rel_n.encode("utf-8") + b"\n")
        h.update(data)
        h.update(b"\n")
    return {
        "bundle": bundle,
        "denied": denied,
        "bundle_sha256": "sha256:" + h.hexdigest(),
    }


def write_log(decision, provider, model, config_digest, logpath=DEFAULT_LOG):
    logpath = pathlib.Path(logpath)
    logpath.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "provider": provider,
        "model": model,
        "config_sha256": config_digest,
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
    ap.add_argument("--allow-partial", action="store_true",
                    help="permite enviar aun con archivos denegados (sólo diagnóstico)")
    ap.add_argument("--dry-run", action="store_true", help="no escribir el log")
    args = ap.parse_args(argv)

    config = load_config(args.config)
    config_digest = "sha256:" + hashlib.sha256(
        json.dumps(config, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    decision = route(args.files, config)
    decision["config_sha256"] = config_digest
    if not args.dry_run and decision["bundle"]:
        decision["log_path"] = write_log(decision, args.provider, args.model, config_digest, args.log)
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    # Atomicidad fail-closed (codex HIGH): cualquier denegado → no-cero salvo --allow-partial
    if decision["denied"] and not args.allow_partial:
        return 1
    return 0 if decision["bundle"] else 1


if __name__ == "__main__":
    sys.exit(main())
