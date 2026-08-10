"""R1-E4 — eval extracción fake offline."""
import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts import eval_extraction as ev

GOLD = pathlib.Path(__file__).resolve().parent / "fixtures" / "extraction_gold"


class TestEvalExtraction(unittest.TestCase):
    def test_three_fixtures_exist(self):
        files = list(GOLD.glob("*.json"))
        self.assertGreaterEqual(len(files), 3)

    def test_fake_perfect_on_synth01(self):
        doc = ev.load_gold(GOLD / "synth-01.json")
        preds = ev.fake_extract(doc)
        m = ev.evaluate(doc, preds)
        self.assertEqual(m["fn"], 0)
        self.assertEqual(m["tp"], 2)
        self.assertEqual(m["recall"], 1.0)

    def test_fake_no_preds_on_empty_gold(self):
        doc = ev.load_gold(GOLD / "synth-03.json")
        preds = ev.fake_extract(doc)
        self.assertEqual(preds, [])
        m = ev.evaluate(doc, preds)
        self.assertEqual(m["tp"], 0)
        self.assertEqual(m["fn"], 0)

    def test_cli(self):
        import subprocess
        r = subprocess.run(
            [sys.executable, str(ev.ROOT / "scripts" / "eval_extraction.py")],
            capture_output=True, text=True, cwd=str(ev.ROOT),
        )
        self.assertEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertEqual(data["extractor"], "fake_v0")
        self.assertGreaterEqual(len(data["results"]), 3)


if __name__ == "__main__":
    unittest.main()
