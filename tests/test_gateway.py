import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

from review_routing import gateway, router, seal
from route_review import main as cli_main


def _cfg(publico, personal=()):
    return {"classification": {"publico": publico, "interno_institucional": [],
                               "personal_confidencial": list(personal)},
            "default": "deny"}


class TestGatewayDryRun(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.d.name)
        (self.root / "pub").mkdir()
        (self.root / "priv").mkdir()
        (self.root / "pub" / "a.md").write_text("publico alpha\n", encoding="utf-8")
        (self.root / "pub" / "b.md").write_text("publico beta\n", encoding="utf-8")
        (self.root / "priv" / "x.md").write_text("nominas\n", encoding="utf-8")
        self.cfg = _cfg(["pub/**"], personal=["priv/**"])
        # H-01: config canónica del sandbox (el gateway pinea contra ella)
        self.canonical = self.root / "config.json"
        self.canonical.write_text(json.dumps(self.cfg), encoding="utf-8")

    def tearDown(self):
        self.d.cleanup()

    def _run(self, files, config=None, **kw):
        return gateway.run(files, "Anthropic", "claude-opus-5",
                           config or self.cfg, repo_root=self.root,
                           canonical_config_path=self.canonical, **kw)

    def test_sella_solo_los_publicos(self):
        r = self._run(["pub/a.md", "priv/x.md", "pub/b.md"], allow_partial=True)
        self.assertTrue(r["ok"])
        manifest_paths = {m["path"] for m in r["seal"]["manifest"]}
        self.assertEqual(manifest_paths, {"pub/a.md", "pub/b.md"})
        self.assertEqual(r["denied"][0]["path"], "priv/x.md")
        self.assertEqual(r["verify"], "ok")
        self.assertNotIn("log_path", r)  # dry-run no loguea

    def test_fail_closed_con_denegado(self):
        r = self._run(["pub/a.md", "priv/x.md"])
        self.assertFalse(r["ok"])
        self.assertEqual(r["reason"], "denegado_fail_closed")
        self.assertEqual(r["denied"][0]["reason"], "prohibicion_dura")
        self.assertNotIn("seal", r)  # no se selló nada

    def test_verify_seal_externo_sobre_disco(self):
        # El sello retornado verifica contra una lectura fresca del disco
        r = self._run(["pub/a.md", "pub/b.md"])
        self.assertTrue(r["ok"])
        content = {p: (self.root / p).read_bytes() for p in ("pub/a.md", "pub/b.md")}
        self.assertEqual(seal.verify_seal(r["seal"], content), (True, "ok"))

    def test_bundle_vacio(self):
        r = self._run(["priv/x.md"], allow_partial=True)
        self.assertFalse(r["ok"])
        self.assertEqual(r["reason"], "bundle_vacio")

    def test_todos_publicos_ok_sin_denegados(self):
        r = self._run(["pub/a.md", "pub/b.md"])
        self.assertTrue(r["ok"])
        self.assertEqual(r["denied"], [])
        self.assertEqual(r["bundle_count"], 2)

    def test_dry_run_false_recusado_hasta_rh_t07(self):
        r = self._run(["pub/a.md"], dry_run=False)
        self.assertFalse(r["ok"])
        self.assertEqual(r["reason"], "invocacion_real_no_disponible_rh_t07")

    def test_config_rogue_fail_closed(self):
        # H-01 (ronda RH-T08): config con {"publico":["**"]} inyectada por el
        # agente NO puede sellar archivos que la canónica deniega.
        rogue = _cfg(["**"])
        r = self._run(["priv/x.md"], config=rogue, allow_partial=True)
        self.assertFalse(r["ok"])
        self.assertEqual(r["reason"], "config_no_canonica")
        self.assertNotIn("seal", r)

    def test_config_canonica_requerida_igual_que_default(self):
        # La config DEBE ser idéntica a la canónica (digest), no un superconjunto
        super_s = _cfg(["pub/**", "priv/**"], personal=[])
        r = self._run(["priv/x.md"], config=super_s, allow_partial=True)
        self.assertEqual(r["reason"], "config_no_canonica")


class TestCLI(unittest.TestCase):
    """CLI contra el repo real (read-only, dry-run no escribe logs)."""

    def _cli(self, *extra):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = cli_main(["--files"] + list(extra[:1]) +
                          ["--provider", "Test", "--model", "m1", "--dry-run"] +
                          list(extra[1:]))
        return rc, json.loads(buf.getvalue())

    def test_publico_exit_0(self):
        rc, out = self._cli("tests/test_gateway.py")
        self.assertEqual(rc, 0)
        self.assertTrue(out["ok"])
        self.assertEqual(out["seal"]["schema"], "eg-harness/seal-v1")
        self.assertEqual(out["seal"]["provider"], "Test")
        self.assertEqual(out["seal"]["model"], "m1")
        self.assertNotIn("log_path", out)

    def test_no_publico_exit_1_lista_denegado(self):
        rc, out = self._cli("ruta/no/clasificada.md")
        self.assertEqual(rc, 1)
        self.assertFalse(out["ok"])
        self.assertEqual(out["reason"], "denegado_fail_closed")
        self.assertEqual(out["denied"][0]["path"], "ruta/no/clasificada.md")

    def test_config_real_clasifica_publico(self):
        cfg = router.load_config()
        self.assertEqual(router.classify("review_routing/gateway.py", cfg), "publico")
        self.assertEqual(router.classify("scripts/route_review.py", cfg), "publico")

    def test_cli_config_rogue_fail_closed(self):
        # H-01 vía superficie CLI: --config con publico:["**"] sobre LICENSE
        # (que la canónica deniega) → exit 1 config_no_canonica, nunca sello.
        rogue = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        try:
            json.dump(_cfg(["**"]), rogue)
            rogue.close()
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = cli_main(["--files", "LICENSE", "--provider", "X",
                               "--model", "Y", "--config", rogue.name,
                               "--dry-run", "--allow-partial"])
            out = json.loads(buf.getvalue())
            self.assertEqual(rc, 1)
            self.assertFalse(out["ok"])
            self.assertEqual(out["reason"], "config_no_canonica")
        finally:
            pathlib.Path(rogue.name).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
