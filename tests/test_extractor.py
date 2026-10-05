"""T1: extract(texto) no ve el gold."""
import inspect
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from corpus.extractor import PLANTED, extract


class TestExtractor(unittest.TestCase):
    def test_firma_solo_texto(self):
        params = list(inspect.signature(extract).parameters)
        self.assertEqual(params, ["texto"])

    def test_no_lee_gold_ni_red(self):
        src = pathlib.Path("corpus/extractor.py").read_text(encoding="utf-8")
        for token in ("extraction_gold", "gold_claims", "must_find", "subprocess", "http"):
            self.assertNotIn(token, src)

    def test_stub_solo_si_la_cita_esta_en_el_texto(self):
        self.assertEqual(extract("antes " + PLANTED + " despues"), [
            {"disposicion_id": None, "cita_texto": PLANTED},
        ])
        self.assertEqual(extract("texto sin la cita"), [])

    def test_rechaza_no_str(self):
        with self.assertRaises(TypeError):
            extract({"texto": PLANTED})  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
