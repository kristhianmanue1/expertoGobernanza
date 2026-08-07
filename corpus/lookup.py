"""Componente D — lookup exacto determinista de disposiciones del corpus.

Carga los modelos JSON bajo corpus/derived/ y resuelve un id estable (p. ej. CPEUM:4:P4)
a su texto verbatim + metadata. Determinista: recorrido ordenado, **error duro** ante id
duplicado o JSON ilegible (fail-loud, no silencioso). Sin LLM.
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DERIVED = ROOT / "derived"


def load_index():
    idx = {}
    for jf in sorted(DERIVED.rglob("*.json")):
        try:
            m = json.loads(jf.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise RuntimeError(f"corpus ilegible {jf}: {e}") from e
        did = m.get("disposicion_id")
        if not did:
            continue
        if did in idx:
            raise RuntimeError(
                f"disposicion_id duplicado '{did}' en {jf} y {idx[did]['_source_file']}"
            )
        m["_source_file"] = str(jf)
        idx[did] = m
    return idx


def lookup(disposicion_id):
    m = load_index().get(disposicion_id)
    if not m:
        return {"exists": False, "disposicion_id": disposicion_id}
    out = {k: v for k, v in m.items() if k != "_source_file"}
    out["exists"] = True
    return out


def main():
    ap = argparse.ArgumentParser(description="Lookup exacto determinista (componente D).")
    ap.add_argument("disposicion_id", help="id estable, p. ej. CPEUM:4:P4")
    args = ap.parse_args()
    r = lookup(args.disposicion_id)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r.get("exists") else 1


if __name__ == "__main__":
    sys.exit(main())
