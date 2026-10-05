"""T1: el CLI pasa solo el texto; las métricas salen de evaluate."""
import json
import pathlib
import subprocess
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from corpus.extractor import PLANTED
from scripts import eval_extraction as ev

GOLD = pathlib.Path(__file__).resolve().parent / "fixtures" / "extraction_gold"


class TestEvalExtraction(unittest.TestCase):
    def test_three_fixtures_exist(self):
        self.assertGreaterEqual(len(list(GOLD.glob("*.json"))), 3)

    def test_stub_no_copia_must_find(self):
        doc = ev.load_gold(GOLD / "synth-01.json")
        preds = ev.extractor.extract(doc["texto"])
        self.assertEqual(preds, [])
        metrics = ev.evaluate(doc, preds)
        self.assertEqual(metrics["tp"], 0)
        self.assertEqual(metrics["fn"], 2)
        self.assertEqual(metrics["recall"], 0.0)

    def test_recall_sale_de_evaluate(self):
        doc = {
            "doc_id": "plant",
            "texto": "contexto " + PLANTED,
            "gold_claims": [{
                "claim_id": "p1",
                "must_find": True,
                "cita_texto": PLANTED,
                "disposicion_id": None,
            }],
        }
        preds = ev.extractor.extract(doc["texto"])
        metrics = ev.evaluate(doc, preds)
        self.assertEqual(metrics["tp"], 1)
        self.assertEqual(metrics["fn"], 0)
        self.assertEqual(metrics["recall"], 1.0)
        self.assertEqual(metrics["precision"], 1.0)

    def test_cli_sin_modo_sale_2(self):
        r = subprocess.run(
            [sys.executable, str(ev.ROOT / "scripts" / "eval_extraction.py")],
            capture_output=True, text=True, cwd=str(ev.ROOT),
        )
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stdout, "")

    def test_cli_pasa_solo_el_texto(self):
        seen = []

        def spy(texto):
            seen.append(texto)
            return []

        original = ev.extractor.extract
        ev.extractor.extract = spy
        try:
            code = ev.main(["--extractor", "stub", "--gold-dir", str(GOLD)])
        finally:
            ev.extractor.extract = original
        self.assertEqual(code, 0)
        doc = ev.load_gold(GOLD / "synth-01.json")
        self.assertIn(doc["texto"], seen)
        self.assertTrue(all(isinstance(item, str) for item in seen))


CITA = "texto compartido de la cita que supera los veinte caracteres"


def _doc(golds, doc_id="amb"):
    return {"doc_id": doc_id, "texto": CITA, "gold_claims": golds}


def _gold(cid, did, text=CITA):
    return {"claim_id": cid, "must_find": True, "cita_texto": text, "disposicion_id": did}


def _pred(did, text=CITA):
    return {"disposicion_id": did, "cita_texto": text}


class TestJuezT1b(unittest.TestCase):
    def setUp(self):
        self.golds = [_gold("gA", "A:1"), _gold("gB", "B:1")]

    def _m(self, preds, golds=None):
        return ev.evaluate(_doc(self.golds if golds is None else golds), preds)

    def test_diez_copias_no_inflan_recall(self):
        m = self._m([_pred("A:1")] * 10)
        self.assertEqual((m["tp"], m["fp"], m["fn"], m["recall"]), (1, 9, 1, 0.5))

    def test_dos_copias_mismo_id_y_nulo(self):
        for did in ("A:1", None):
            m = self._m([_pred(did), _pred(did)])
            self.assertEqual((m["tp"], m["fp"], m["fn"], m["recall"]), (1, 1, 1, 0.5))

    def test_ids_distintos_recuperan_los_dos_gold(self):
        m = self._m([_pred("A:1"), _pred("B:1")])
        self.assertEqual((m["tp"], m["fp"], m["fn"], m["recall"]), (2, 0, 0, 1.0))

    def test_nulo_no_recupera_el_otro_gold(self):
        m = self._m([_pred("A:1"), _pred(None)])
        self.assertEqual(m["recall"], 0.5)
        self.assertEqual(m["tp"], 1)

    def test_acento_es_la_misma_clase(self):
        variante = "Texto  COMPARTIDO de la cita que supera los veinte caracteres"
        m = self._m([_pred("A:1", CITA), _pred("A:1", variante)])
        self.assertEqual(m["tp"], 1)
        self.assertEqual(m["n_clases"], 1)

    def test_reordenar_no_cambia_metricas(self):
        a = self._m([_pred("B:1"), _pred("A:1"), _pred("A:1")])
        b = self._m([_pred("A:1"), _pred("A:1"), _pred("B:1")])
        for key in ("tp", "fp", "fn", "precision", "recall"):
            self.assertEqual(a[key], b[key])

    def test_texto_completo_no_cuenta(self):
        enorme = "preambulo " + CITA + " cierre que alarga la prediccion"
        m = self._m([_pred("A:1", enorme)])
        self.assertEqual(m["tp"], 0)
        self.assertEqual(m["fp"], 1)

    def test_id_incorrecto_y_vacio(self):
        malo = self._m([_pred("C:9")])
        self.assertEqual(malo["tp"], 0)
        self.assertGreaterEqual(malo["id_incorrecto"], 1)
        vacio = ev.evaluate(_doc([]), [_pred("A:1")])
        self.assertIsNone(vacio["recall"])
        self.assertEqual(vacio["recall_razon"], "denominador_cero")

    def test_tp_sin_id_puede_tener_gate_bajo(self):
        m = self._m([_pred(None)])
        self.assertEqual(m["tp"], 1)
        self.assertGreaterEqual(m["gate_bajo"], 1)

    def test_predictions_file(self):
        import tempfile
        docs = GOLD
        payload = {}
        for path in docs.glob("*.json"):
            doc = ev.load_gold(path)
            payload[doc["doc_id"]] = []
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(payload, handle)
            path = pathlib.Path(handle.name)
        try:
            self.assertEqual(ev.main([
                "--predictions-file", str(path), "--gold-dir", str(docs),
            ]), 0)
            dup = path.with_suffix(".dup.json")
            dup.write_text(
                '{"' + next(iter(payload)) + '": [], "' + next(iter(payload)) + '": []}',
                encoding="utf-8",
            )
            self.assertEqual(ev.main([
                "--predictions-file", str(dup), "--gold-dir", str(docs),
            ]), 2)
            self.assertEqual(ev.main([
                "--extractor", "stub", "--predictions-file", str(path),
            ]), 2)
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
