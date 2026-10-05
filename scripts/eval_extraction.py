#!/usr/bin/env python3
"""Eval extracción: el stub ve solo texto; el juez sigue en evaluate."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from corpus import extractor  # noqa: E402
from corpus.verify_citations import _normalize, verify_claim  # noqa: E402

GOLD_DIR = ROOT / "tests" / "fixtures" / "extraction_gold"


def load_gold(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _align(pred: dict, gold_list: list) -> str | None:
    pn = _normalize(pred.get("cita_texto") or "")
    if len(pn) < 20:
        return None
    for g in gold_list:
        gn = _normalize(g.get("cita_texto") or "")
        if not gn:
            continue
        if pn in gn or gn in pn:
            if pred.get("disposicion_id") and g.get("disposicion_id"):
                if pred["disposicion_id"] != g["disposicion_id"]:
                    continue
            return g.get("claim_id")
    return None


def evaluate(doc: dict, preds: list[dict]) -> dict:
    gold = [g for g in (doc.get("gold_claims") or []) if g.get("must_find")]
    matched_gold: set[str] = set()
    tp = fp = 0
    gate_bajo = 0
    for p in preds:
        vr = verify_claim(p) if p.get("disposicion_id") else {
            "response_status": "bajo", "quote_substring_match": False
        }
        if vr.get("response_status") == "bajo":
            gate_bajo += 1
        gid = _align(p, gold)
        if gid:
            tp += 1
            matched_gold.add(gid)
        else:
            fp += 1
    fn = len(gold) - len(matched_gold)
    prec = tp / (tp + fp) if (tp + fp) else 1.0
    rec = tp / (tp + fn) if (tp + fn) else 1.0
    return {
        "doc_id": doc.get("doc_id"),
        "n_pred": len(preds),
        "n_gold": len(gold),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "gate_bajo": gate_bajo,
        "metricas_no_aceptadas_hasta_t1b": True,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Eval extracción (stub ciego al gold).")
    ap.add_argument("--extractor", choices=["stub"], default=None)
    ap.add_argument("--gold-dir", type=pathlib.Path, default=GOLD_DIR)
    args = ap.parse_args(argv)
    if args.extractor != "stub":
        return 2
    rows = []
    for p in sorted(args.gold_dir.glob("*.json")):
        doc = load_gold(p)
        preds = extractor.extract(doc["texto"])
        rows.append(evaluate(doc, preds))
    print(json.dumps(
        {"extractor": "stub", "metricas_no_aceptadas_hasta_t1b": True, "results": rows},
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
