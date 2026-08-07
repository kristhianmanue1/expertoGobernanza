"""Componente F — verificador determinista de citas (gate v1).

Implementa el gate v1 de la enmienda de gobernanza v1.1-revisada (Cambio 2):
  (a) la disposición existe en el corpus
  (c) el fragmento citado coincide con el texto verbatim
  (d) la fuente oficial está resuelta (sha256)
  (b) vigencia en fecha jurídica: N/A en v1 (sin corpus temporal) -> [VIGENCIA-NO-VERIFICADA]

Niveles de confianza (Cambio 2): 'alto' prohibido sin vigencia verificada contra DOF;
tope 'medio' cuando (a)+(c)+(d) OK; 'bajo' si no hay respaldo. Determinista: el match
de cita es exacto normalizado (insensible a acentos/espacios/mayúsculas), nunca LLM.
"""
import argparse
import json
import pathlib
import sys
import unicodedata

from corpus.lookup import load_index


def _normalize(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().split())


def verify_claim(claim):
    did = claim.get("disposicion_id")
    cita = claim.get("cita_texto", "")
    m = load_index().get(did)

    result = {
        "disposicion_id": did,
        "reference_exists": bool(m),
        "quote_exact_match": False,
        "source_resolved": False,
        "version_valid_for_date": "N/A_v1",
        "notes": [],
    }

    if not m:
        result["response_status"] = "bajo"
        result["notes"].append("disposicion no encontrada en el corpus")
        return result

    texto = m.get("texto_verbatim", "")
    if cita:
        result["quote_exact_match"] = _normalize(cita) in _normalize(texto)
    result["source_resolved"] = any(f.get("sha256") for f in m.get("fuentes_oficiales", []))

    vig_ok = m.get("vigencia", {}).get("verificada_contra_dof_nivel1", False)
    if result["quote_exact_match"] and result["source_resolved"]:
        result["response_status"] = "alto" if vig_ok else "medio"
        if not vig_ok:
            result["notes"].append("[VIGENCIA-NO-VERIFICADA contra DOF nivel 1] -> tope 'medio'")
    else:
        result["response_status"] = "bajo"
        if cita and not result["quote_exact_match"]:
            result["notes"].append("la cita no coincide con el texto verbatim del corpus")
    return result


def main():
    ap = argparse.ArgumentParser(description="Verificador determinista de citas (componente F, gate v1).")
    ap.add_argument("claim", help="JSON {disposicion_id, cita_texto} o ruta a un archivo .json")
    args = ap.parse_args()
    p = pathlib.Path(args.claim)
    claim = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else json.loads(args.claim)
    r = verify_claim(claim)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r["response_status"] in ("medio", "alto") else 1


if __name__ == "__main__":
    sys.exit(main())
