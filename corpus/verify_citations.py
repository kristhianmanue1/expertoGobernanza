"""Componente F — verificador determinista de citas (gate v1).

Gate v1 de la enmienda de gobernanza v1.1-revisada (Cambio 2):
  (a) la disposición existe en el corpus
  (c) el fragmento citado APARECE en el texto verbatim (match de subcadena normalizada,
      con mínimo de longitud) — NO es "cita exacta"; es "procedencia textual"
  (d) la fuente oficial está resuelta: sha256 con formato 64-hex y, si el original está
      accesible, recomputado y coincidente con el declarado
  (b) vigencia en fecha jurídica: N/A en v1 (sin corpus temporal) -> [VIGENCIA-NO-VERIFICADA]

GATE_VERSION='v1': el nivel 'alto' es INALCANZABLE por construcción (requiere vigencia
verificada contra DOF nivel 1, inexistente en v1). Tope 'medio' cuando (a)+(c)+(d) OK.
'bajo' si no hay respaldo. Determinista: sin LLM; normalización NFKD sin diacríticos.

Niveles: 'alto'=apto para decisión (inhabilitado en v1), 'medio'=sólo borrador (prohibido
para decidir), 'bajo'=sin respaldo. Exit codes: 0=alto, 2=medio, 1=bajo (un shell/CI que
exija exit 0 NO promueve un 'medio' a decisión).
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys
import unicodedata

from corpus.lookup import load_index

GATE_VERSION = "v1"
EVIDENCE_SCHEMA_VERSION = "v1"
MIN_CITA_LEN = 40
_HEX64 = re.compile(r"[0-9a-f]{64}")
REPO = pathlib.Path(__file__).resolve().parent.parent
_EXIT = {"alto": 0, "medio": 2, "bajo": 1}
_FECHA_NOTA = (
    "Fecha jurídica no evaluada; evidencia mecánica y atestación del registry "
    "no autorizan decisión, aplicabilidad ni promulgación"
)


def _normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().split())


def _resolve_source(model):
    """source_resolved true con PDF ausente es el legado v1: no equivale a recomputo."""
    declared = None
    archivo = None
    for f in model.get("fuentes_oficiales", []):
        d = (f.get("sha256") or "").strip().lower()
        if _HEX64.fullmatch(d):
            declared, archivo = d, f.get("archivo")
            break
    out = {
        "sha256_declared": declared,
        "sha256_recomputed": None,
        "archivo": archivo,
        "resolved": False,
        "declared_ok": declared is not None,
        "recomputed_ok": False,
        "source_check": "invalid_declaration",
        "note": "",
    }
    if not declared:
        out["note"] = "sin sha256 con formato 64-hex en fuentes_oficiales"
        return out
    full = REPO / archivo if archivo else None
    if not full or not full.is_file():
        out["resolved"] = True
        out["source_check"] = "missing"
        out["note"] = "original no accesible; sha256 declarado válido pero no recomputado (CI debe llevar el original)"
        return out
    try:
        payload = full.read_bytes()
    except OSError as exc:
        out["source_check"] = "error"
        out["note"] = f"error de lectura: {exc.__class__.__name__}"
        return out
    digest = hashlib.sha256(payload).hexdigest()
    out["sha256_recomputed"] = digest
    if digest == declared:
        out["resolved"] = True
        out["recomputed_ok"] = True
        out["source_check"] = "match"
        return out
    out["source_check"] = "mismatch"
    out["note"] = f"hash recomputado NO coincide ({digest})"
    return out


def _registry_check(model):
    instrumento = model.get("instrumento")
    if not isinstance(instrumento, dict):
        return "error", "instrumento_malformado"
    instrumento_id = instrumento.get("id")
    if not isinstance(instrumento_id, str) or not instrumento_id.strip():
        return "error", "instrumento_malformado"
    try:
        from corpus.registry_loader import fuente_por_instrumento, load_registry
        from corpus.registry_rules import resolve_disposicion_vigencia
        doc = load_registry(pathlib.Path(__file__).resolve().parent / "registry.yaml")
        fuente = fuente_por_instrumento(doc, instrumento_id)
    except Exception as exc:
        return "error", f"loader:{exc.__class__.__name__}"
    if fuente is None:
        return "missing_evidence", "fuente_ausente"
    try:
        resolved = resolve_disposicion_vigencia(fuente, model.get("disposicion_id") or "")
    except Exception as exc:
        return "error", f"resolver:{exc.__class__.__name__}"
    if not isinstance(resolved, dict):
        return "error", "resolver_salida_invalida"
    razon = str(resolved.get("razon") or "")
    if resolved.get("verificada") is True:
        return "verified", razon
    return "unverified", razon


def verify_claim(claim):
    did = claim.get("disposicion_id")
    cita = claim.get("cita_texto", "")
    m = load_index().get(did)

    result = {
        "gate_version": GATE_VERSION,
        "disposicion_id": did,
        "reference_exists": False,
        "quote_substring_match": False,
        "match_mode": f"substring_min{MIN_CITA_LEN}_normalized",
        "match_len": 0,
        "source_resolved": False,
        "version_valid_for_date": "N/A_v1",
        "evidence_schema_version": EVIDENCE_SCHEMA_VERSION,
        "fuente_sha256_declared": None,
        "fuente_sha256_recomputed": None,
        "source_declared_ok": False,
        "source_recomputed_ok": False,
        "source_check": None,
        "registry_check": None,
        "registry_razon": None,
        "derived_file": None,
        "notes": [_FECHA_NOTA],
    }

    if not m:
        result["response_status"] = "bajo"
        result["notes"].append("disposicion no encontrada en el corpus")
        return result

    result["reference_exists"] = True
    result["derived_file"] = m.get("_source_file")

    nc = _normalize(cita)
    result["match_len"] = len(nc)
    if len(nc) < MIN_CITA_LEN:
        result["notes"].append(f"cita demasiado corta/vacia tras normalizacion ({len(nc)}<{MIN_CITA_LEN})")
    else:
        result["quote_substring_match"] = nc in _normalize(m.get("texto_verbatim", ""))

    src = _resolve_source(m)
    result["source_resolved"] = src["resolved"]
    result["fuente_sha256_declared"] = src["sha256_declared"]
    result["fuente_sha256_recomputed"] = src["sha256_recomputed"]
    result["source_declared_ok"] = src["declared_ok"]
    result["source_recomputed_ok"] = src["recomputed_ok"]
    result["source_check"] = src["source_check"]
    if src["note"]:
        result["notes"].append("fuente: " + src["note"])

    registry_check, registry_razon = _registry_check(m)
    result["registry_check"] = registry_check
    result["registry_razon"] = registry_razon

    quote_ok = result["quote_substring_match"]
    hash_blocks = src["source_check"] in {"invalid_declaration", "mismatch", "error"}
    registry_blocks = registry_check == "error"
    partial = src["source_check"] in {"missing", "match"} and registry_check in {
        "verified", "unverified", "missing_evidence"
    }
    if quote_ok and src["declared_ok"] and partial and not hash_blocks and not registry_blocks:
        result["response_status"] = "medio"
        result["notes"].append("[VIGENCIA-NO-VERIFICADA contra DOF nivel 1] -> tope 'medio' (alto reservado a v2)")
    else:
        result["response_status"] = "bajo"
    return result


def main():
    ap = argparse.ArgumentParser(description="Verificador determinista de citas (componente F, gate v1).")
    ap.add_argument("claim", help="JSON {disposicion_id, cita_texto} o ruta a archivo .json")
    args = ap.parse_args()
    p = pathlib.Path(args.claim)
    claim = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else json.loads(args.claim)
    r = verify_claim(claim)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return _EXIT[r["response_status"]]


if __name__ == "__main__":
    sys.exit(main())
