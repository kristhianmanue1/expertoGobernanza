import contextlib
import io
import json
import os
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

    def test_prefijo_colision_no_bypass(self):
        # Regresión BLOCKER (claude+codex): "docs/adr/**" NO debe matchear "docs/adresses/"
        self.assertEqual(router.classify("docs/adresses/secreto.md", self.cfg), "deny")
        self.assertEqual(router.classify("testsuite/evil.py", _cfg(publico=["tests/**"])), "deny")


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
        self.assertEqual(reasons["manual.md"], "interno_anonimizacion_pendiente")
        self.assertEqual(reasons["secreto.csv"], "prohibicion_dura")

    def test_personal_nunca_se_envia(self):
        dec = router.route(["publico.md", "secreto.csv"], self.cfg, repo_root=self.root)
        self.assertIn("secreto.csv", [d["path"] for d in dec["denied"]])
        self.assertNotIn("secreto.csv", [b["path"] for b in dec["bundle"]])

    def test_interno_siempre_denegado_v1(self):
        # v1: no hay anonimización -> interno SIEMPRE se deniega (sin escape del agente)
        dec = router.route(["manual.md"], self.cfg, repo_root=self.root)
        self.assertEqual(dec["bundle"], [])
        self.assertEqual(dec["denied"][0]["reason"], "interno_anonimizacion_pendiente")

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


class TestAdversarial(unittest.TestCase):
    """Regresiones del fix-and-retry claude+codex (2026-08-07): confinamiento y atomicidad."""

    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.d.name)
        (self.root / "a.md").write_text("x", encoding="utf-8")
        self.cfg = _cfg(publico=["a.md", "docs/adr/**"])

    def tearDown(self):
        self.d.cleanup()

    def test_traversal_puntos_suspensivos_denegado(self):
        dec = router.route(["docs/adr/../../../etc/passwd"], self.cfg, repo_root=self.root)
        self.assertEqual(dec["bundle"], [])
        self.assertEqual(dec["denied"][0]["reason"], "path_traversal")

    def test_ruta_absoluta_denegada(self):
        dec = router.route(["/etc/passwd"], self.cfg, repo_root=self.root)
        self.assertEqual(dec["denied"][0]["reason"], "path_traversal")

    def test_symlink_publico_a_confidencial_denegado(self):
        # Regresión BLOCKER codex ciclo 2: symlink desde ruta pública → archivo
        # confidencial del repo no debe rutearse (re-clasificación de la ruta resuelta)
        pub = self.root / "publico"
        priv = self.root / "personal"
        pub.mkdir(); priv.mkdir()
        (priv / "secret.csv").write_text("rfc,sueldo", encoding="utf-8")
        try:
            os.symlink(priv / "secret.csv", pub / "leak.md")
        except OSError:
            self.skipTest("symlink no soportado en este FS")
        cfg = _cfg(publico=["publico/**"], personal=["personal/**"])
        dec = router.route(["publico/leak.md"], cfg, repo_root=self.root)
        self.assertEqual(dec["bundle"], [])
        self.assertEqual(dec["denied"][0]["reason"], "prohibicion_dura")

    def test_main_atomico_parcial_no_cero(self):
        # un archivo no clasificado -> denied -> exit 1 (fail-closed)
        with contextlib.redirect_stdout(io.StringIO()):
            rc = router.main(["ruta_no_clasificada.md", "--provider", "X",
                              "--model", "Y", "--dry-run"])
        self.assertEqual(rc, 1)

    def test_main_allow_partial_escapa(self):
        # un público + uno denegado, con --allow-partial -> exit 0 (bundle no vacío)
        with contextlib.redirect_stdout(io.StringIO()):
            rc = router.main(["docs/politica-agentes.md", "ruta_no_clasificada.md",
                              "--provider", "X", "--model", "Y", "--dry-run", "--allow-partial"])
        self.assertEqual(rc, 0)


class TestLog(unittest.TestCase):
    def test_write_log_appends_jsonl(self):
        with tempfile.TemporaryDirectory() as d:
            logp = pathlib.Path(d) / "log.jsonl"
            dec = {"bundle": [{"path": "a.md", "bytes": 3}], "denied": [], "bundle_sha256": "sha256:x"}
            router.write_log(dec, "Anthropic", "claude-sonnet-5", "sha256:cfg", logp)
            router.write_log(dec, "OpenAI", "gpt-5", "sha256:cfg", logp)
            lines = logp.read_text(encoding="utf-8").strip().split("\n")
            self.assertEqual(len(lines), 2)
            e0 = json.loads(lines[0])
            self.assertEqual(e0["provider"], "Anthropic")
            self.assertEqual(e0["model"], "claude-sonnet-5")
            self.assertEqual(e0["config_sha256"], "sha256:cfg")


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

    def test_no_bypass_prefijo_real(self):
        # "review_routing/**" es público; "review_routing_evil/x" NO debe serlo
        cfg = router.load_config()
        self.assertEqual(router.classify("review_routing_evil/x.py", cfg), "deny")


if __name__ == "__main__":
    unittest.main()
