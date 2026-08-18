import copy
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from review_routing import router, seal


def _cfg(publico=None, interno=None, personal=None):
    return {
        "classification": {
            "publico": publico or [],
            "interno_institucional": interno or [],
            "personal_confidencial": personal or [],
        },
        "default": "deny",
    }


class _Sandbox(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.d.name)
        (self.root / "pub").mkdir()
        (self.root / "pub" / "a.md").write_text("contenido publico alpha\n", encoding="utf-8")
        (self.root / "pub" / "b.md").write_text("contenido publico beta\n", encoding="utf-8")
        self.cfg = _cfg(publico=["pub/**"])
        self.decision = router.route(["pub/a.md", "pub/b.md"], self.cfg, repo_root=self.root)
        self.content = seal.read_bundle(self.decision, repo_root=self.root)
        self.seal = seal.build_seal(self.decision, self.cfg, "Anthropic",
                                    "claude-opus-5", "sha256:cfg1",
                                    repo_root=self.root, bundle_content=self.content)

    def tearDown(self):
        self.d.cleanup()


class TestBuildSeal(_Sandbox):
    def test_ocho_campos_schema(self):
        self.assertEqual(set(self.seal), {
            "schema", "sealed_at", "provider", "model", "config_sha256",
            "bundle_sha256", "manifest", "seal_sha256"})
        self.assertEqual(self.seal["schema"], "eg-harness/seal-v1")

    def test_seal_sha256_64hex(self):
        h = self.seal["seal_sha256"]
        self.assertTrue(h.startswith("sha256:"))
        body = h.split(":", 1)[1]
        self.assertEqual(len(body), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in body))

    def test_classification_reclasificada_no_inferida(self):
        # F4: manifest.classification sale de router.classify(path, config)
        for m in self.seal["manifest"]:
            self.assertEqual(m["classification"], router.classify(m["path"], self.cfg))

    def test_manifest_por_archivo(self):
        by_path = {m["path"]: m for m in self.seal["manifest"]}
        for p, data in self.content.items():
            self.assertEqual(by_path[p]["bytes"], len(data))
            self.assertEqual(by_path[p]["classification"], "publico")

    def test_seal_vincula_decision(self):
        self.assertEqual(self.seal["bundle_sha256"], self.decision["bundle_sha256"])
        self.assertEqual(self.seal["provider"], "Anthropic")
        self.assertEqual(self.seal["model"], "claude-opus-5")


class TestVerifySeal(_Sandbox):
    def test_round_trip_ok(self):
        self.assertEqual(seal.verify_seal(self.seal, self.content), (True, "ok"))

    def test_bundle_vacio_verifica(self):
        dec = router.route([], self.cfg, repo_root=self.root)
        content = seal.read_bundle(dec, repo_root=self.root)
        s = seal.build_seal(dec, self.cfg, "P", "M", "sha256:c",
                            repo_root=self.root, bundle_content=content)
        self.assertEqual(seal.verify_seal(s, content), (True, "ok"))

    def test_tamper_contenido_un_byte(self):
        mutated = dict(self.content)
        mutated["pub/a.md"] = mutated["pub/a.md"].replace(b"alpha", b"ALPHA")
        ok, why = seal.verify_seal(self.seal, mutated)
        self.assertFalse(ok)

    def test_tamper_manifest_classification(self):
        s = copy.deepcopy(self.seal)
        s["manifest"][0]["classification"] = "interno_institucional"
        ok, why = seal.verify_seal(s, self.content)
        self.assertFalse(ok)

    def test_tamper_manifest_path(self):
        s = copy.deepcopy(self.seal)
        s["manifest"][0]["path"] = "pub/c.md"
        self.assertFalse(seal.verify_seal(s, self.content)[0])

    def test_tamper_manifest_sha256(self):
        s = copy.deepcopy(self.seal)
        s["manifest"][0]["sha256"] = "sha256:" + "0" * 64
        self.assertFalse(seal.verify_seal(s, self.content)[0])

    def test_tamper_seal_sha256(self):
        s = copy.deepcopy(self.seal)
        s["seal_sha256"] = "sha256:" + "f" * 64
        ok, why = seal.verify_seal(s, self.content)
        self.assertFalse(ok)

    def test_tamper_bundle_sha256(self):
        s = copy.deepcopy(self.seal)
        s["bundle_sha256"] = "sha256:" + "a" * 64
        ok, why = seal.verify_seal(s, self.content)
        self.assertFalse(ok)
        self.assertEqual(why, "bundle_sha256_no_recomputa")

    def test_seal_sin_schema_rechazado(self):
        s = copy.deepcopy(self.seal)
        del s["schema"]
        ok, why = seal.verify_seal(s, self.content)
        self.assertFalse(ok)
        self.assertEqual(why, "schema_desconocido")

    def test_archivo_extra_en_bundle(self):
        extra = dict(self.content)
        extra["pub/c.md"] = b"extra"
        self.assertFalse(seal.verify_seal(self.seal, extra)[0])

    def test_archivo_faltante_en_bundle(self):
        missing = dict(self.content)
        del missing["pub/b.md"]
        self.assertFalse(seal.verify_seal(self.seal, missing)[0])

    def test_manifest_duplicado_rechazado(self):
        s = copy.deepcopy(self.seal)
        s["manifest"].append(copy.deepcopy(s["manifest"][0]))
        self.assertFalse(seal.verify_seal(s, self.content)[0])

    def test_repo_mutado_tras_sellar_no_afecta(self):
        # F2/TOCTOU: verify opera sobre el contenido sellado, no el repo vivo
        (self.root / "pub" / "a.md").write_text("CAMBIADO TRAS SELLAR\n", encoding="utf-8")
        (self.root / "pub" / "b.md").unlink()
        self.assertEqual(seal.verify_seal(self.seal, self.content), (True, "ok"))


class TestReadBundle(_Sandbox):
    def test_lectura_unica_coincide_con_archivos(self):
        self.assertEqual(set(self.content), {"pub/a.md", "pub/b.md"})
        self.assertEqual(self.content["pub/a.md"],
                         (self.root / "pub" / "a.md").read_bytes())

    def test_path_fantasma_fail_closed(self):
        decision = {"bundle": [{"path": "pub/fantasma.md", "bytes": 1}],
                    "denied": [], "bundle_sha256": "sha256:x"}
        with self.assertRaises(seal.SealError):
            seal.read_bundle(decision, repo_root=self.root)

    def test_bundle_content_incompleto_fail_closed(self):
        decision = {"bundle": [{"path": "pub/a.md", "bytes": 1},
                               {"path": "pub/z.md", "bytes": 1}],
                    "denied": [], "bundle_sha256": "sha256:x"}
        partial = {"pub/a.md": b"x"}
        with self.assertRaises(seal.SealError):
            seal.build_seal(decision, self.cfg, "P", "M", "sha256:c",
                            repo_root=self.root, bundle_content=partial)


if __name__ == "__main__":
    unittest.main()
