import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from review_routing import router


def _cfg(publico=None, interno=None, personal=None):
    return {
        "classification": {
            "publico": publico or [],
            "interno_institucional": interno or [],
            "personal_confidencial": personal or [],
        },
        "default": "deny",
    }


class TestClassify(unittest.TestCase):
    def setUp(self):
        self.cfg = _cfg(
            publico=["docs/politica-agentes.md", "docs/adr/**", "corpus/derived/**"],
            interno=["manuales/imss.md"],
            personal=["nomina/**"],
        )

    def test_publico_exacto(self):
        self.assertEqual(router.classify("docs/politica-agentes.md", self.cfg), "publico")

    def test_publico_glob_dir(self):
        self.assertEqual(router.classify("docs/adr/0001-x.md", self.cfg), "publico")
        self.assertEqual(router.classify("corpus/derived/cpeum/a.json", self.cfg), "publico")

    def test_default_deny(self):
        self.assertEqual(router.classify("secrets/empleados.csv", self.cfg), "deny")

    def test_interno_institucional(self):
        self.assertEqual(router.classify("manuales/imss.md", self.cfg), "interno_institucional")

    def test_personal_confidencial(self):
        self.assertEqual(router.classify("nomina/sueldos.xlsx", self.cfg), "personal_confidencial")

    def test_personal_tiene_precedencia(self):
        cfg = _cfg(publico=["x/**"], personal=["x/nomina.txt"])
        self.assertEqual(router.classify("x/nomina.txt", cfg), "personal_confidencial")


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.d.name)
        (self.root / "publico.md").write_text("hola público", encoding="utf-8")
        (self.root / "manual.md").write_text("manual imss", encoding="utf-8")
        (self.root / "secreto.csv").write_text("rfc,sueldo", encoding="utf-8")
        self.cfg = _cfg(publico=["publico.md"], interno=["manual.md"], personal=["secreto.csv"])

    def tearDown(self):
        self.d.cleanup()

    def test_bundle_excluye_denegados(self):
        dec = router.route(["publico.md", "manual.md", "secreto.csv"], self.cfg, repo_root=self.root)
        self.assertEqual({b["path"] for b in dec["bundle"]}, {"publico.md"})
        reasons = {d["path"]: d["reason"] for d in dec["denied"]}
        self.assertEqual(reasons["manual.md"], "sin_autorizacion_humana")
        self.assertEqual(reasons["secreto.csv"], "prohibicion_dura")

    def test_personal_nunca_se_envia_aunque_autorices(self):
        dec = router.route(["publico.md", "secreto.csv"], self.cfg,
                           repo_root=self.root, authorized_internal=True)
        self.assertIn("secreto.csv", [d["path"] for d in dec["denied"]])
        self.assertNotIn("secreto.csv", [b["path"] for b in dec["bundle"]])

    def test_interno_pasa_solo_con_autorizacion_humana(self):
        sin = router.route(["manual.md"], self.cfg, repo_root=self.root)
        self.assertEqual(sin["bundle"], [])
        con = router.route(["manual.md"], self.cfg, repo_root=self.root, authorized_internal=True)
        self.assertIn("manual.md", [b["path"] for b in con["bundle"]])

    def test_hash_determinista(self):
        a = router.route(["publico.md"], self.cfg, repo_root=self.root)
        b = router.route(["publico.md"], self.cfg, repo_root=self.root)
        self.assertEqual(a["bundle_sha256"], b["bundle_sha256"])
        self.assertTrue(a["bundle_sha256"].startswith("sha256:"))

    def test_hash_cambia_si_contenido_cambia(self):
        a = router.route(["publico.md"], self.cfg, repo_root=self.root)
        (self.root / "publico.md").write_text("contenido distinto", encoding="utf-8")
        b = router.route(["publico.md"], self.cfg, repo_root=self.root)
        self.assertNotEqual(a["bundle_sha256"], b["bundle_sha256"])

    def test_publico_faltante_denegado(self):
        cfg = _cfg(publico=["fantasma.md"])
        dec = router.route(["fantasma.md"], cfg, repo_root=self.root)
        self.assertEqual(dec["bundle"], [])
        self.assertEqual(dec["denied"][0]["reason"], "archivo_no_encontrado")


class TestLog(unittest.TestCase):
    def test_write_log_appends_jsonl(self):
        with tempfile.TemporaryDirectory() as d:
            logp = pathlib.Path(d) / "log.jsonl"
            dec = {"bundle": [{"path": "a.md", "bytes": 3}], "denied": [], "bundle_sha256": "sha256:x"}
            router.write_log(dec, "Anthropic", "claude-opus-5", logp)
            router.write_log(dec, "Moonshot", "kimi", logp)
            lines = logp.read_text(encoding="utf-8").strip().split("\n")
            self.assertEqual(len(lines), 2)
            e0 = json.loads(lines[0])
            self.assertEqual(e0["provider"], "Anthropic")
            self.assertEqual(e0["model"], "claude-opus-5")
            self.assertEqual(e0["bundle_sha256"], "sha256:x")


class TestRealConfig(unittest.TestCase):
    def test_archivos_reales_son_publicos(self):
        cfg = router.load_config()
        for p in ["docs/politica-agentes.md", "corpus/lookup.py",
                  "corpus/verify_citations.py", "tests/test_lookup.py",
                  "review_routing/router.py"]:
            self.assertEqual(router.classify(p, cfg), "publico", f"{p} debería ser público")

    def test_path_desconocido_denegado(self):
        cfg = router.load_config()
        self.assertEqual(router.classify("secrets/api.key", cfg), "deny")


if __name__ == "__main__":
    unittest.main()
