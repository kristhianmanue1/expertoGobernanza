"""R1-E3 — auditor v0."""
import json
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts import audit_document as ad

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "piloto-salud-citas.json"


class TestAuditDocument(unittest.TestCase):
    def test_banner_no_verificada_hoy(self):
        self.assertEqual(ad.corpus_vigencia_banner(), ad.BANNER_NO)

    def test_fixture_audit(self):
        out = ad.audit(FIXTURE)
        self.assertEqual(out["auditor_version"], "v0")
        self.assertEqual(out["corpus_vigencia_banner"], ad.BANNER_NO)
        self.assertEqual(out["summary"]["n"], 3)
        # dos citas golden suelen ser medio; una inventada bajo
        self.assertGreaterEqual(out["summary"]["bajo"], 1)
        self.assertEqual(out["summary"]["peor"], "bajo")
        statuses = [c["response_status"] for c in out["claims"]]
        self.assertIn("bajo", statuses)

    def test_cli_exit_bajo(self):
        import subprocess
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "audit_document.py"), str(FIXTURE)],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        self.assertEqual(r.returncode, 1)
        data = json.loads(r.stdout)
        self.assertEqual(data["corpus_vigencia_banner"], ad.BANNER_NO)

    def test_lista_plana(self):
        import tempfile
        claims = [{
            "disposicion_id": "NO:EXISTE",
            "cita_texto": "x" * 50,
        }]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(claims, f)
            p = pathlib.Path(f.name)
        try:
            out = ad.audit(p)
            self.assertEqual(out["summary"]["peor"], "bajo")
        finally:
            p.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
