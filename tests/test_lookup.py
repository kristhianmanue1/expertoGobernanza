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
        r = lookup.lookup("CPEUM:4:Psalud")
        self.assertTrue(r["exists"])
        self.assertEqual(r["instrumento"]["id"], "CPEUM")
        self.assertIn("protección de la salud", r["texto_verbatim"])

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
