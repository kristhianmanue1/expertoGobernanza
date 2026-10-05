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


if __name__ == "__main__":
    unittest.main()
