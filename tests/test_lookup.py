import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from corpus import lookup


class TestLookup(unittest.TestCase):
    def test_existing_id_returns_verbatim(self):
        r = lookup.lookup("CPEUM:4:P4")
        self.assertTrue(r["exists"])
        self.assertEqual(r["instrumento"]["id"], "CPEUM")
        self.assertIn("protección de la salud", r["texto_verbatim"])

    def test_loapf_art1_lookup(self):
        r = lookup.lookup("LOAPF:1")
        self.assertTrue(r["exists"])
        self.assertEqual(r["instrumento"]["id"], "LOAPF")
        self.assertIn("paraestatal", r["texto_verbatim"].lower())

    def test_lfep_art1_lookup(self):
        r = lookup.lookup("LFEP:1")
        self.assertTrue(r["exists"])
        self.assertEqual(r["instrumento"]["id"], "LFEP")
        self.assertIn("entidades paraestatales", r["texto_verbatim"].lower())
        self.assertIn("artículo 90", r["texto_verbatim"].lower())

    def test_lfep_art5_imss_ley_especifica(self):
        r = lookup.lookup("LFEP:5")
        self.assertTrue(r["exists"])
        t = r["texto_verbatim"].lower()
        self.assertIn("instituto mexicano del seguro social", t)
        self.assertIn("leyes específicas", t)

    def test_lss_art5_imss_opd(self):
        r = lookup.lookup("LSS:5")
        self.assertTrue(r["exists"])
        self.assertEqual(r["instrumento"]["id"], "LSS")
        t = r["texto_verbatim"].lower()
        self.assertIn("organismo público descentralizado", t)
        self.assertIn("instituto mexicano del seguro social", t)

    def test_lss_art1_lookup(self):
        r = lookup.lookup("LSS:1")
        self.assertTrue(r["exists"])
        self.assertIn("orden público", r["texto_verbatim"].lower())

    def test_riimss_art1_lookup(self):
        r = lookup.lookup("RIIMSS:1")
        self.assertTrue(r["exists"])
        self.assertEqual(r["instrumento"]["id"], "RIIMSS")
        t = r["texto_verbatim"].lower()
        self.assertIn("instituto mexicano del seguro social", t)
        self.assertIn("seguro social", t)

    def test_missing_id_not_exists(self):
        r = lookup.lookup("NO:EX:ISTE")
        self.assertFalse(r["exists"])

    def test_load_index_duplicate_id_raises(self):
        with tempfile.TemporaryDirectory() as d:
            base = pathlib.Path(d)
            for name in ("a.json", "b.json"):
                (base / name).write_text(
                    json.dumps({"disposicion_id": "DUP:1", "texto_verbatim": "x"},
                               ensure_ascii=False),
                    encoding="utf-8")
            with mock.patch.object(lookup, "DERIVED", base):
                with self.assertRaises(RuntimeError):
                    lookup.load_index()

    def test_load_index_ilegible_raises(self):
        with tempfile.TemporaryDirectory() as d:
            base = pathlib.Path(d)
            (base / "broken.json").write_text("{no es json valido", encoding="utf-8")
            with mock.patch.object(lookup, "DERIVED", base):
                with self.assertRaises(RuntimeError):
                    lookup.load_index()


if __name__ == "__main__":
    unittest.main()
