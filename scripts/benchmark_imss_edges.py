"""Benchmark preregistrado del gate compuesto de fidelidad + EvidenceEdge."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from corpus.evidence_edge import is_traversable, validate_evidence_edge

DEFAULT_CASES = ROOT / "benchmarks/imss_evidence_edge_cases.json"
DEFAULT_EDGES = ROOT / "benchmarks/fixtures/imss_evidence_edges.json"


def _load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _safe_local_path(root: pathlib.Path, relative: object) -> pathlib.Path | None:
    if not isinstance(relative, str) or not relative:
        return None
    root = root.resolve()
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _fidelity_errors(
    edge: dict, root: pathlib.Path, require_originals: bool = False
) -> list[str]:
    errors: list[str] = []
    evidence = edge.get("evidence")
    subject = edge.get("subject")
    if not isinstance(evidence, dict) or not isinstance(subject, dict):
        return ["estructura insuficiente para verificar fidelidad"]

    source_path = _safe_local_path(root, evidence.get("source_ref"))
    if source_path is None:
        return ["source_ref escapa del repositorio o es inválido"]
    if not source_path.is_file():
        return ["source_ref inexistente"]
    try:
        source = _load_json(source_path)
    except (OSError, ValueError, TypeError):
        return ["source_ref ilegible"]

    if source.get("disposicion_id") != subject.get("id"):
        errors.append("source_ref no corresponde al sujeto")
    quote = _normalized(evidence.get("quote", ""))
    text = _normalized(source.get("texto_verbatim", ""))
    if not quote or quote not in text:
        errors.append("cita ausente de texto_verbatim")

    declared_hash = evidence.get("source_document_sha256")
    matching_sources = [
        item for item in source.get("fuentes_oficiales", [])
        if isinstance(item, dict) and item.get("sha256") == declared_hash
    ]
    if not matching_sources:
        errors.append("hash no declarado por la fuente de la disposición")
        return errors

    source_record = matching_sources[0]
    extract_path = _safe_local_path(root, source_record.get("extracto_verbatim_en"))
    if extract_path is None or not extract_path.is_file():
        errors.append("extracto verbatim versionado inexistente")
    else:
        extract = _normalized(extract_path.read_text(encoding="utf-8"))
        if quote not in extract:
            errors.append("cita ausente del extracto verbatim versionado")

    original_path = _safe_local_path(root, source_record.get("archivo"))
    if original_path is None or not original_path.is_file():
        if require_originals:
            errors.append("original local requerido pero inexistente")
    else:
        actual_hash = hashlib.sha256(original_path.read_bytes()).hexdigest()
        if actual_hash != declared_hash:
            errors.append("hash del original local no coincide")
    return errors


def evaluate_benchmark(
    cases_path: pathlib.Path = DEFAULT_CASES,
    edges_path: pathlib.Path = DEFAULT_EDGES,
    root: pathlib.Path = ROOT,
    require_originals: bool = False,
) -> dict:
    case_doc = _load_json(cases_path)
    edge_doc = _load_json(edges_path)
    evaluation_date = date.fromisoformat(case_doc["evaluation_date"])
    cases = case_doc.get("cases", [])
    edges = edge_doc.get("edges", [])
    edge_by_id = {edge.get("edge_id"): edge for edge in edges}

    edge_diagnostics: dict[str, dict[str, list[str]]] = {}
    traversable: set[str] = set()
    duplicate_edge_ids = len(edge_by_id) != len(edges)
    for edge in edges:
        edge_id = edge.get("edge_id")
        structural = validate_evidence_edge(edge, evaluation_date)
        fidelity = _fidelity_errors(edge, root, require_originals)
        edge_diagnostics[str(edge_id)] = {
            "structural_errors": structural,
            "fidelity_errors": fidelity,
        }
        if not structural and not fidelity and is_traversable(edge, evaluation_date):
            traversable.add(edge_id)

    results = []
    seen_case_ids: set[str] = set()
    all_candidates: set[str] = set()
    expected_global: set[str] = set()
    false_positives = 0
    false_negatives = 0
    for case in cases:
        case_id = case.get("id")
        case_errors: list[str] = []
        if case_id in seen_case_ids:
            case_errors.append("id de caso duplicado")
        seen_case_ids.add(case_id)
        candidates = set(case.get("candidate_edge_ids", []))
        all_candidates.update(candidates)
        missing = sorted(candidates - set(edge_by_id))
        if missing:
            case_errors.append(f"candidatas inexistentes: {missing}")
        actual = sorted(candidates & traversable)
        expected = sorted(case.get("expected_traversable_edge_ids", []))
        expected_global.update(expected)
        extra = sorted(set(actual) - set(expected))
        absent = sorted(set(expected) - set(actual))
        false_positives += len(extra)
        false_negatives += len(absent)
        outcome = "answerable" if actual else "blocked"
        passed = (
            not case_errors
            and outcome == case.get("expected_outcome")
            and actual == expected
        )
        results.append({
            "id": case_id,
            "expected_outcome": case.get("expected_outcome"),
            "actual_outcome": outcome,
            "expected_traversable_edge_ids": expected,
            "actual_traversable_edge_ids": actual,
            "false_positive_edge_ids": extra,
            "false_negative_edge_ids": absent,
            "errors": case_errors,
            "passed": passed,
        })

    unreferenced_edges = sorted(set(edge_by_id) - all_candidates)
    unexpected_traversable = sorted(traversable - expected_global)
    missing_expected_global = sorted(expected_global - traversable)
    unexpected_edge_errors = sorted(
        edge_id for edge_id in expected_global
        if edge_diagnostics.get(edge_id, {}).get("structural_errors")
        or edge_diagnostics.get(edge_id, {}).get("fidelity_errors")
    )
    negative_controls = all_candidates - expected_global
    rejected_negative_controls = len(negative_controls - traversable)
    answered = sum(result["actual_outcome"] == "answerable" for result in results)
    blocked = sum(result["actual_outcome"] == "blocked" for result in results)
    passed_cases = sum(result["passed"] for result in results)
    passed = (
        len(cases) == 5
        and len(seen_case_ids) == 5
        and passed_cases == 5
        and not duplicate_edge_ids
        and not unreferenced_edges
        and not unexpected_traversable
        and not missing_expected_global
        and not unexpected_edge_errors
        and false_positives == 0
        and false_negatives == 0
        and answered == 3
        and blocked == 2
        and len(negative_controls) == 5
        and rejected_negative_controls == 5
    )
    return {
        "schema": "imss-evidence-edge-benchmark-result/v2",
        "benchmark_id": case_doc.get("benchmark_id"),
        "evaluation_date": evaluation_date.isoformat(),
        "gate": "fidelity+evidence-edge/v0",
        "passed": passed,
        "metrics": {
            "total_cases": len(cases),
            "passed_cases": passed_cases,
            "answerable": answered,
            "blocked": blocked,
            "false_positive_traversals": false_positives,
            "false_negative_blocks": false_negatives,
            "negative_controls": len(negative_controls),
            "rejected_negative_controls": rejected_negative_controls,
            "unexpected_edge_errors": len(unexpected_edge_errors),
        },
        "integrity": {
            "duplicate_edge_ids": duplicate_edge_ids,
            "unreferenced_edge_ids": unreferenced_edges,
            "unexpected_traversable_edge_ids": unexpected_traversable,
            "missing_expected_global_edge_ids": missing_expected_global,
            "unexpected_error_edge_ids": unexpected_edge_errors,
        },
        "edge_diagnostics": edge_diagnostics,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=pathlib.Path, default=DEFAULT_CASES)
    parser.add_argument("--edges", type=pathlib.Path, default=DEFAULT_EDGES)
    parser.add_argument(
        "--allow-missing-originals",
        action="store_true",
        help="No falla si los PDF gitignored no están disponibles.",
    )
    args = parser.parse_args()
    report = evaluate_benchmark(
        args.cases,
        args.edges,
        require_originals=not args.allow_missing_originals,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
