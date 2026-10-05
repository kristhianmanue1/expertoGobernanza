#!/usr/bin/env python3
"""Eval extracción T1b: stub ciego y juez resistente a duplicados."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from corpus import extractor  # noqa: E402
from corpus.verify_citations import GATE_VERSION, _normalize, verify_claim  # noqa: E402

GOLD_DIR = ROOT / "tests" / "fixtures" / "extraction_gold"
EVALUATOR_VERSION = "t1b-v1"
ALIGNER_VERSION = "t1b-containment-min20"
MIN_PRED = 20


def load_gold(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _cid(pred: dict):
    did = pred.get("disposicion_id")
    return None if did is None else did


def _compatible(pred: dict, gold: dict) -> bool:
    pn = _normalize(pred.get("cita_texto") or "")
    if len(pn) < MIN_PRED:
        return False
    gn = _normalize(gold.get("cita_texto") or "")
    if not gn or pn not in gn:
        return False
    pid, gid = _cid(pred), gold.get("disposicion_id")
    if pid and gid and pid != gid:
        return False
    return True


def _null_blocked(pred: dict, gold: dict, classes: list[dict], golds: list[dict]) -> bool:
    if _cid(pred) is not None:
        return False
    pn = _normalize(pred.get("cita_texto") or "")
    gn = _normalize(gold.get("cita_texto") or "")
    for other in classes:
        if other is pred or _cid(other) is None:
            continue
        if _normalize(other.get("cita_texto") or "") != pn:
            continue
        for other_gold in golds:
            if _normalize(other_gold.get("cita_texto") or "") != gn:
                continue
            if _compatible(other, other_gold):
                return True
    return False


def _match(classes: list[dict], golds: list[dict]) -> list[int]:
    """Máxima cardinalidad. Desempate: menor índice de gold por clase, en orden."""
    golds_sorted = sorted(enumerate(golds), key=lambda item: str(item[1].get("claim_id")))
    order = [index for index, _ in golds_sorted]
    m, n = len(classes), len(golds)
    best: tuple[int, tuple[int, ...], list[int]] | None = None
    assign = [-1] * m
    used = [False] * n

    def edges(i: int) -> list[int]:
        pred = classes[i]
        out = []
        for j in order:
            gold = golds[j]
            if _compatible(pred, gold) and not _null_blocked(pred, gold, classes, golds):
                out.append(j)
        return out

    def rec(i: int) -> None:
        nonlocal best
        if i == m:
            matched = sum(a >= 0 for a in assign)
            stable = tuple(a if a >= 0 else n + 1 for a in assign)
            cand = (matched, stable, assign[:])
            if best is None or cand[0] > best[0] or (cand[0] == best[0] and cand[1] < best[1]):
                best = cand
            return
        for j in edges(i):
            if used[j]:
                continue
            used[j] = True
            assign[i] = j
            rec(i + 1)
            used[j] = False
            assign[i] = -1
        rec(i + 1)

    if m:
        rec(0)
    return [] if best is None else best[2]


def _classes(preds: list[dict]) -> list[tuple[dict, int]]:
    grouped: list[tuple[dict, int]] = []
    index: dict[tuple, int] = {}
    for pred in preds:
        key = (_normalize(pred.get("cita_texto") or ""), _cid(pred))
        if key not in index:
            index[key] = len(grouped)
            grouped.append((pred, 1))
        else:
            pos = index[key]
            grouped[pos] = (grouped[pos][0], grouped[pos][1] + 1)
    return grouped


def _ratio(num: int, den: int):
    if den == 0:
        return None, "denominador_cero"
    return round(num / den, 4), None


def evaluate(doc: dict, preds: list[dict]) -> dict:
    golds = [g for g in (doc.get("gold_claims") or []) if g.get("must_find")]
    grouped = _classes(preds)
    classes = [pred for pred, _ in grouped]
    extra_fp = sum(copies - 1 for _, copies in grouped)
    matched = _match(classes, golds)
    tp = sum(1 for j in matched if j >= 0)
    unmatched = sum(1 for j in matched if j < 0)
    fp = extra_fp + unmatched
    fn = len(golds) - tp
    precision, precision_razon = _ratio(tp, tp + fp)
    recall, recall_razon = _ratio(tp, len(golds))
    gate_bajo = 0
    id_ausente = id_incorrecto = 0
    for pred in preds:
        verdict = verify_claim(pred) if pred.get("disposicion_id") else {
            "response_status": "bajo"
        }
        if verdict.get("response_status") == "bajo":
            gate_bajo += 1
        if _cid(pred) is None:
            id_ausente += 1
        else:
            for gold in golds:
                if _normalize(pred.get("cita_texto") or "") in _normalize(gold.get("cita_texto") or ""):
                    gid = gold.get("disposicion_id")
                    if gid and gid != _cid(pred):
                        id_incorrecto += 1
                        break
    rate, rate_razon = _ratio(gate_bajo, len(preds))
    return {
        "doc_id": doc.get("doc_id"),
        "evaluator_version": EVALUATOR_VERSION,
        "aligner_version": ALIGNER_VERSION,
        "gate_version": GATE_VERSION,
        "n_pred": len(preds),
        "n_gold": len(golds),
        "n_clases": len(classes),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "precision_razon": precision_razon,
        "recall": recall,
        "recall_razon": recall_razon,
        "id_ausente": id_ausente,
        "id_incorrecto": id_incorrecto,
        "gate_bajo": gate_bajo,
        "gate_bajo_rate": rate,
        "gate_bajo_rate_razon": rate_razon,
    }


class PredictionFileError(ValueError):
    pass


def _pairs(pairs):
    seen = set()
    obj = {}
    for key, value in pairs:
        if key in seen:
            raise PredictionFileError(f"clave JSON duplicada: {key}")
        seen.add(key)
        obj[key] = value
    return obj


def load_predictions(path: pathlib.Path, docs: dict[str, dict]) -> dict[str, list]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs)
    except json.JSONDecodeError as exc:
        raise PredictionFileError("JSON malformado") from exc
    if not isinstance(payload, dict):
        raise PredictionFileError("se esperaba un objeto doc_id → predicciones")
    known = set(docs)
    if set(payload) != known:
        raise PredictionFileError("doc_id desconocido o faltante")
    out = {}
    for doc_id, preds in payload.items():
        if not isinstance(preds, list):
            raise PredictionFileError(f"{doc_id}: predicciones no son lista")
        clean = []
        for pred in preds:
            if not isinstance(pred, dict) or not isinstance(pred.get("cita_texto"), str):
                raise PredictionFileError(f"{doc_id}: predicción mal tipada")
            did = pred.get("disposicion_id")
            if did is not None and not isinstance(did, str):
                raise PredictionFileError(f"{doc_id}: disposicion_id mal tipado")
            clean.append({"disposicion_id": did, "cita_texto": pred["cita_texto"]})
        out[doc_id] = clean
    return out


def _emit(rows: list[dict], extractor_name: str) -> int:
    print(json.dumps(
        {
            "extractor": extractor_name,
            "evaluator_version": EVALUATOR_VERSION,
            "aligner_version": ALIGNER_VERSION,
            "gate_version": GATE_VERSION,
            "results": rows,
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Eval extracción (juez T1b).")
    ap.add_argument("--extractor", choices=["stub"], default=None)
    ap.add_argument("--predictions-file", type=pathlib.Path, default=None)
    ap.add_argument("--gold-dir", type=pathlib.Path, default=GOLD_DIR)
    args = ap.parse_args(argv)
    modes = (args.extractor == "stub") + (args.predictions_file is not None)
    if modes != 1:
        return 2
    docs = {load_gold(p)["doc_id"]: load_gold(p) for p in sorted(args.gold_dir.glob("*.json"))}
    rows = []
    if args.extractor == "stub":
        for doc in docs.values():
            rows.append(evaluate(doc, extractor.extract(doc["texto"])))
        return _emit(rows, "stub")
    try:
        bundled = load_predictions(args.predictions_file, docs)
    except (OSError, PredictionFileError):
        return 2
    for doc_id, doc in docs.items():
        rows.append(evaluate(doc, bundled[doc_id]))
    return _emit(rows, "predictions-file")


if __name__ == "__main__":
    sys.exit(main())
