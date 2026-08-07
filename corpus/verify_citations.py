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
MIN_CITA_LEN = 40
_HEX64 = re.compile(r"[0-9a-f]{64}")
REPO = pathlib.Path(__file__).resolve().parent.parent
_EXIT = {"alto": 0, "medio": 2, "bajo": 1}


def _normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().split())


def _resolve_source(model):
    declared = None
    archivo = None
    for f in model.get("fuentes_oficiales", []):
        d = (f.get("sha256") or "").strip().lower()
        if _HEX64.fullmatch(d):
            declared, archivo = d, f.get("archivo")
            break
    out = {"sha256_declared": declared, "sha256_recomputed": None, "archivo": archivo, "resolved": False, "note": ""}
    if not declared:
        out["note"] = "sin sha256 con formato 64-hex en fuentes_oficiales"
        return out
    full = REPO / archivo if archivo else None
    if full and full.is_file():
        h = hashlib.sha256(full.read_bytes()).hexdigest()
        out["sha256_recomputed"] = h
        out["resolved"] = (h == declared)
        out["note"] = "" if h == declared else f"hash recomputado NO coincide ({h})"
    else:
        out["resolved"] = True
        out["note"] = "original no accesible; sha256 declarado válido pero no recomputado (CI debe llevar el original)"
    return out


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
        "fuente_sha256_declared": None,
        "fuente_sha256_recomputed": None,
        "derived_file": None,
        "notes": [],
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
    if src["note"]:
        result["notes"].append("fuente: " + src["note"])

    if result["quote_substring_match"] and result["source_resolved"]:
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
