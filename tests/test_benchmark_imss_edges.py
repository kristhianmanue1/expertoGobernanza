"""Regresiones del benchmark IMSS preregistrado."""
import copy
import json
import pathlib
import tempfile
import unittest

from scripts.benchmark_imss_edges import DEFAULT_CASES, DEFAULT_EDGES, evaluate_benchmark


class TestBenchmarkImssEvidenceEdge(unittest.TestCase):
    def test_retry_pasa_cinco_preguntas_y_cinco_controles(self):
        report = evaluate_benchmark()
        self.assertTrue(report["passed"])
        self.assertEqual(report["metrics"]["passed_cases"], 5)
        self.assertEqual(report["metrics"]["answerable"], 3)
        self.assertEqual(report["metrics"]["blocked"], 2)
        self.assertEqual(report["metrics"]["negative_controls"], 5)
        self.assertEqual(report["metrics"]["rejected_negative_controls"], 5)
        self.assertEqual(report["metrics"]["false_positive_traversals"], 0)

    def test_promover_lfep5_produce_falso_positivo_y_falla(self):
        document = json.loads(DEFAULT_EDGES.read_text(encoding="utf-8"))
        target = next(
            edge for edge in document["edges"]
            if edge["edge_id"] == "LFEP:5|remite_a_ley_especifica|LSS"
        )
        target["evidence_scope"].update({
            "covers_object": True,
            "covers_relation": True,
            "source_level": 2,
        })
        target["validity"].update({
            "trace_source_level": 1,
            "trace_covers_disposition": True,
        })
        target["verification"].update({
            "status": "verified",
            "reviewed_by": "revisor de prueba",
            "reviewed_at": "2026-08-10",
        })
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "edges.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            report = evaluate_benchmark(DEFAULT_CASES, path)
        self.assertFalse(report["passed"])
        self.assertEqual(report["metrics"]["false_positive_traversals"], 1)

    def test_f5_lfep5_cerrado_no_hace_textual_la_lss(self):
        report = evaluate_benchmark()
        edge_id = "LFEP:5|remite_a_ley_especifica|LSS"
        self.assertEqual(report["edge_diagnostics"][edge_id]["structural_errors"], [])
        self.assertEqual(report["edge_diagnostics"][edge_id]["fidelity_errors"], [])
        q4 = next(result for result in report["results"] if result["id"] == "Q4")
        self.assertEqual(q4["actual_outcome"], "blocked")

    def test_promover_status_q5_no_basta_sin_cobertura_de_objeto_y_relacion(self):
        document = json.loads(DEFAULT_EDGES.read_text(encoding="utf-8"))
        target = next(
            edge for edge in document["edges"]
            if edge["edge_id"] == "LSS:5|integra_regimen|LFEP:1"
        )
        target["verification"]["status"] = "verified"
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "edges.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            report = evaluate_benchmark(DEFAULT_CASES, path)
        q5 = next(result for result in report["results"] if result["id"] == "Q5")
        self.assertEqual(q5["actual_outcome"], "blocked")
        errors = report["edge_diagnostics"][target["edge_id"]]["structural_errors"]
        self.assertTrue(any("exige cobertura" in error for error in errors))

    def test_cita_fabricada_se_rechaza_aunque_edge_sea_estructural(self):
        report = evaluate_benchmark()
        edge_id = "LSS:5|define_naturaleza_falsa|IMSS"
        self.assertEqual(report["edge_diagnostics"][edge_id]["structural_errors"], [])
        self.assertIn(
            "cita ausente de texto_verbatim",
            report["edge_diagnostics"][edge_id]["fidelity_errors"],
        )

    def test_fuente_inexistente_y_hash_divergente_se_rechazan(self):
        report = evaluate_benchmark()
        missing = "LOAPF:1:P3|ubica_clase_sin_fuente|administracion_publica_paraestatal"
        bad_hash = "RIIMSS:1|define_objeto_hash_invalido|Seguro_Social"
        self.assertIn(
            "source_ref inexistente",
            report["edge_diagnostics"][missing]["fidelity_errors"],
        )
        self.assertIn(
            "hash no declarado por la fuente de la disposición",
            report["edge_diagnostics"][bad_hash]["fidelity_errors"],
        )

    def test_arista_extra_fuera_de_casos_falla_cobertura_global(self):
        document = json.loads(DEFAULT_EDGES.read_text(encoding="utf-8"))
        extra = copy.deepcopy(document["edges"][0])
        extra["predicate"] = "define_naturaleza_extra"
        extra["edge_id"] = "LSS:5|define_naturaleza_extra|IMSS"
        document["edges"].append(extra)
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "edges.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            report = evaluate_benchmark(DEFAULT_CASES, path)
        self.assertFalse(report["passed"])
        self.assertEqual(
            report["integrity"]["unreferenced_edge_ids"],
            ["LSS:5|define_naturaleza_extra|IMSS"],
        )

    def test_candidata_inexistente_falla_caso(self):
        document = json.loads(DEFAULT_CASES.read_text(encoding="utf-8"))
        document["cases"][0]["candidate_edge_ids"] = ["LSS:999|inventa|IMSS"]
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "cases.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            report = evaluate_benchmark(path, DEFAULT_EDGES)
        self.assertFalse(report["passed"])
        self.assertFalse(report["results"][0]["passed"])


if __name__ == "__main__":
    unittest.main()
