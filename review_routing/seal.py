"""Sello de bundle para revisión externa verificable (plan router-harness §2, RH-T01).

Vincula clasificación ↔ contenido ↔ destino en un objeto verificable: el sello
prueba *"este contenido, con esta clasificación, iba a este proveedor/modelo"*.

El sello envuelve un **bundle autocontenido**: `build_seal` lee el contenido del
repo UNA vez al sellar (vía `read_bundle`) y de ahí salen los hashes del
manifiesto. `verify_seal` re-hashea el **contenido del bundle** (inmutable),
nunca el repo vivo → sin TOCTOU (F2). Verificar el sello verifica lo que
realmente se envió, aunque el repo cambie después.

`manifest[*].classification` se re-clasifica con `router.classify(path, config)`,
no se infiere de la pertenencia al bundle (F4). El confinamiento de lectura lo
hereda del router (`router._confined`): nada de `..`/absolutos/symlinks fuera.

LIMITES (honestos): el sello certifica integridad y procedencia del bundle que
atraviesa esta ruta; NO previene bypass (invocar al proveedor fuera del gateway
no es detectable aquí — ver plan §"Anti-bypass" y ADR pendiente 0006).
"""
import datetime as _dt
import hashlib
import json
import pathlib

from . import router

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = "eg-harness/seal-v1"


class SealError(Exception):
    """Fallo fail-closed al construir un sello (lectura/confinamiento)."""


def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def _digest(obj):
    return "sha256:" + hashlib.sha256(_canonical(obj).encode("utf-8")).hexdigest()


def _bundle_digest(manifest, bundle_content):
    """Recomputa el hash de bundle con el algoritmo de router.route (orden manifest)."""
    h = hashlib.sha256()
    for item in manifest:
        p = item["path"].replace("\\", "/")
        h.update(p.encode("utf-8") + b"\n")
        h.update(bundle_content[p])
        h.update(b"\n")
    return "sha256:" + h.hexdigest()


def read_bundle(decision, repo_root=ROOT):
    """Lee UNA vez el contenido de los paths del bundle de la decisión.

    Devuelve {path: bytes}. Confinamiento delegado a router._confined; si un
    path escapa o no se puede leer → SealError (fail-closed).
    """
    content = {}
    for item in decision["bundle"]:
        rel = item["path"]
        full, ok = router._confined(rel, repo_root)
        if not ok:
            raise SealError(f"path no confinado al sellar: {rel!r}")
        try:
            content[rel] = full.read_bytes()
        except OSError as exc:
            raise SealError(f"ilegible al sellar: {rel!r}: {exc}") from exc
    return content


def build_seal(decision, config, provider, model, config_sha256,
               repo_root=ROOT, bundle_content=None):
    """Construye el sello v1 (8 campos §2) sobre un bundle autocontenido.

    `bundle_content` opcional permite reusar una lectura previa (`read_bundle`);
    si es None se lee aquí. `bundle_sha256` se toma de la decisión (lo que
    router.route ruteó): verify_seal luego recomprueba que contenido sellado y
    hash ruteado coinciden (route ↔ seal ↔ verify).
    """
    if bundle_content is None:
        bundle_content = read_bundle(decision, repo_root)
    manifest = []
    for item in decision["bundle"]:
        rel = item["path"]
        if rel not in bundle_content:
            raise SealError(f"path del bundle sin contenido: {rel!r}")
        data = bundle_content[rel]
        manifest.append({
            "path": rel,
            "classification": router.classify(rel, config),  # F4: re-clasificado
            "bytes": len(data),
            "sha256": "sha256:" + hashlib.sha256(data).hexdigest(),
        })
    seal = {
        "schema": SCHEMA,
        "sealed_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "provider": provider,
        "model": model,
        "config_sha256": config_sha256,
        "bundle_sha256": decision["bundle_sha256"],
        "manifest": manifest,
        # seal_sha256 se calcula abajo, excluido de su propio cómputo
    }
    seal["seal_sha256"] = _digest(seal)
    return seal


def verify_seal(seal, bundle_content):
    """Verifica (seal, contenido del bundle sellado). Nunca toca el repo (F2).

    Devuelve (True, "ok") o (False, motivo). Fail-closed: cualquier campo
    alterado, archivo de más/menos, o hash que no recompute → False.
    """
    if not isinstance(seal, dict) or seal.get("schema") != SCHEMA:
        return False, "schema_desconocido"
    manifest = seal.get("manifest")
    if not isinstance(manifest, list):
        return False, "manifest_invalido"
    if not isinstance(bundle_content, dict):
        return False, "bundle_content_invalido"
    paths = [m.get("path") for m in manifest if isinstance(m, dict)]
    if len(paths) != len(manifest) or len(set(paths)) != len(paths):
        return False, "manifest_paths_invalidos"
    if set(paths) != set(bundle_content):
        return False, "bundle_no_corresponde_al_manifest"
    for m in manifest:
        data = bundle_content[m["path"]]
        if m.get("bytes") != len(data):
            return False, f"bytes_no_coinciden:{m['path']}"
        if m.get("sha256") != "sha256:" + hashlib.sha256(data).hexdigest():
            return False, f"sha256_no_coincide:{m['path']}"
    if seal.get("bundle_sha256") != _bundle_digest(manifest, bundle_content):
        return False, "bundle_sha256_no_recomputa"
    expected = seal.get("seal_sha256")
    if not isinstance(expected, str):
        return False, "seal_sha256_ausente"
    body = {k: v for k, v in seal.items() if k != "seal_sha256"}
    if _digest(body) != expected:
        return False, "seal_sha256_no_recomputa"
    return True, "ok"
