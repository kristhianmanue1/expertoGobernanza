"""Componente D — lookup exacto determinista de disposiciones del corpus.

Carga los modelos JSON bajo corpus/derived/ y resuelve un identificador estable
(p. ej. CPEUM:4:Psalud) a su texto verbatim + metadata. Sin LLM, sin heurística:
puramente determinista (clave exacta).
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DERIVED = ROOT / "derived"


def load_index():
    idx = {}
    for jf in DERIVED.rglob("*.json"):
        try:
            m = json.loads(jf.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        did = m.get("disposicion_id")
        if did:
            idx[did] = m
    return idx


def lookup(disposicion_id):
    m = load_index().get(disposicion_id)
    if not m:
        return {"exists": False, "disposicion_id": disposicion_id}
    return {
        "exists": True,
        "disposicion_id": disposicion_id,
        "instrumento": m.get("instrumento"),
        "jerarquia_documental": m.get("jerarquia_documental"),
        "texto_verbatim": m.get("texto_verbatim"),
        "vigencia": m.get("vigencia"),
        "relaciones_normativas": m.get("relaciones_normativas", []),
        "fuentes_oficiales": m.get("fuentes_oficiales", []),
    }


def main():
    ap = argparse.ArgumentParser(description="Lookup exacto determinista (componente D).")
    ap.add_argument("disposicion_id", help="id estable, p. ej. CPEUM:4:Psalud")
    args = ap.parse_args()
    r = lookup(args.disposicion_id)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r.get("exists") else 1


if __name__ == "__main__":
    sys.exit(main())
