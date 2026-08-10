#!/usr/bin/env python3
"""Auditor v0: claims pre-etiquetados → verify_claim + banner de vigencia (F6)."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from corpus.verify_citations import verify_claim, _EXIT  # noqa: E402

BANNER_NO = "CORPUS_VIGENCIA_NO_VERIFICADA"
BANNER_OK = "CORPUS_VIGENCIA_PARCIAL_O_OK"
REGISTRY = ROOT / "corpus" / "registry.yaml"
_RANK = {"bajo": 0, "medio": 1, "alto": 2}


def corpus_vigencia_banner(registry_path: pathlib.Path = REGISTRY) -> str:
    if not registry_path.is_file():
        return BANNER_NO
    text = registry_path.read_text(encoding="utf-8")
    if re.search(r"(?m)^[ \t]*vigencia_verificada:\s*true\b", text, flags=re.I):
        return BANNER_OK
    return BANNER_NO


def _load_claims(path: pathlib.Path) -> tuple[str | None, list]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return None, data
    if isinstance(data, dict) and "claims" in data:
        return data.get("documento_id"), data["claims"]
    raise ValueError("JSON: lista de claims o {documento_id, claims}")


def audit(path: pathlib.Path) -> dict:
    doc_id, claims = _load_claims(path)
    results = []
    counts = {"alto": 0, "medio": 0, "bajo": 0}
    peor = "alto"
    for c in claims:
        if not isinstance(c, dict):
            r = {"response_status": "bajo", "notes": ["claim no es objeto"]}
        else:
            r = verify_claim(c)
        st = r.get("response_status", "bajo")
        counts[st] = counts.get(st, 0) + 1
        if _RANK.get(st, 0) < _RANK.get(peor, 2):
            peor = st
        results.append(r)
    if not results:
        peor = "bajo"
    return {
        "auditor_version": "v0",
        "gate_version": "v1",
        "corpus_vigencia_banner": corpus_vigencia_banner(),
        "documento_id": doc_id,
        "claims": results,
        "summary": {
            "n": len(results),
            "alto": counts.get("alto", 0),
            "medio": counts.get("medio", 0),
            "bajo": counts.get("bajo", 0),
            "peor": peor,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Auditor v0 de citas pre-etiquetadas.")
    ap.add_argument("claims_json", type=pathlib.Path)
    args = ap.parse_args()
    try:
        out = audit(args.claims_json)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"error": str(e), "corpus_vigencia_banner": BANNER_NO},
                         ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return _EXIT.get(out["summary"]["peor"], 1)


if __name__ == "__main__":
    sys.exit(main())
