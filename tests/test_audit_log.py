import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from review_routing import audit_log, router, seal

GENESIS = "sha256:" + "0" * 64


def _cfg(publico):
    return {"classification": {"publico": publico, "interno_institucional": [],
                               "personal_confidencial": []}, "default": "deny"}


class _LogCase(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.d.name)
        (self.root / "pub").mkdir()
        (self.root / "pub" / "a.md").write_text("publico\n", encoding="utf-8")
        self.cfg = _cfg(["pub/**"])
        decision = router.route(["pub/a.md"], self.cfg, repo_root=self.root)
        content = seal.read_bundle(decision, repo_root=self.root)
        self.seal = seal.build_seal(decision, self.cfg, "Anthropic",
                                    "claude-opus-5", "sha256:cfg1",
                                    repo_root=self.root, bundle_content=content)
        self.log = self.root / "logs" / "audit.jsonl"

    def tearDown(self):
        self.d.cleanup()

    def _append_n(self, n):
        return [audit_log.append(self.seal, f"sha256:resp{i}", self.log)
                for i in range(n)]

    def _entries(self):
        return [json.loads(ln) for ln in
                self.log.read_text(encoding="utf-8").splitlines() if ln.strip()]

    def _rewrite(self, entries):
        self.log.write_text(
            "\n".join(json.dumps(e, ensure_ascii=False) for e in entries) + "\n",
            encoding="utf-8")


class TestAppend(_LogCase):
    def test_crea_log_genesis(self):
        self.assertFalse(self.log.exists())
        h = audit_log.append(self.seal, "sha256:resp0", self.log)
        self.assertTrue(self.log.exists())
        e = self._entries()[0]
        self.assertEqual(e["seq"], 1)
        self.assertEqual(e["prev_hash"], GENESIS)
        self.assertEqual(e["entry_hash"], h)
        self.assertEqual(e["provider"], "Anthropic")
        self.assertEqual(e["model"], "claude-opus-5")
        self.assertEqual(e["seal_sha256"], self.seal["seal_sha256"])
        self.assertEqual(e["bundle_sha256"], self.seal["bundle_sha256"])
        self.assertEqual(e["config_sha256"], self.seal["config_sha256"])
        self.assertEqual(e["response_sha256"], "sha256:resp0")

    def test_tres_appends_cadena_ok(self):
        hashes = self._append_n(3)
        self.assertEqual(audit_log.verify_chain(self.log), ("OK", []))
        es = self._entries()
        self.assertEqual([e["seq"] for e in es], [1, 2, 3])
        self.assertEqual(es[1]["prev_hash"], hashes[0])
        self.assertEqual(es[2]["prev_hash"], hashes[1])
        self.assertEqual(es[2]["entry_hash"], hashes[2])

    def test_response_sha256_null_valido(self):
        audit_log.append(self.seal, None, self.log)
        self.assertIsNone(self._entries()[0]["response_sha256"])
        self.assertEqual(audit_log.verify_chain(self.log), ("OK", []))

    def test_append_sobre_log_roto_raise_fail_closed(self):
        self._append_n(2)
        es = self._entries()
        es[0]["provider"] = "Falso"
        self._rewrite(es)
        with self.assertRaises(audit_log.AuditError):
            audit_log.append(self.seal, "sha256:resp2", self.log)
        self.assertEqual(len(self._entries()), 2)  # no extendió el log roto


class TestVerifyChain(_LogCase):
    def test_tamper_campo_intermedio(self):
        self._append_n(3)
        es = self._entries()
        es[1]["provider"] = "OpenAI"
        self._rewrite(es)
        status, findings = audit_log.verify_chain(self.log)
        self.assertEqual(status, "BROKEN")
        self.assertTrue(any("entry_hash_no_recomputa" in f for f in findings))

    def test_borrar_intermedio(self):
        self._append_n(3)
        es = self._entries()
        del es[1]
        self._rewrite(es)
        status, findings = audit_log.verify_chain(self.log)
        self.assertEqual(status, "BROKEN")
        self.assertTrue(any("enlace_roto" in f or "seq_no_monotono" in f
                            for f in findings))

    def test_reordenar_entradas(self):
        self._append_n(3)
        es = self._entries()
        es[0], es[1] = es[1], es[0]
        self._rewrite(es)
        self.assertEqual(audit_log.verify_chain(self.log)[0], "BROKEN")

    def test_seq_no_monotonico(self):
        self._append_n(3)
        es = self._entries()
        es[1]["seq"] = 7
        self._rewrite(es)
        status, findings = audit_log.verify_chain(self.log)
        self.assertEqual(status, "BROKEN")
        self.assertTrue(any("seq_no_monotono" in f for f in findings))

    def test_tamper_prev_hash(self):
        self._append_n(2)
        es = self._entries()
        es[1]["prev_hash"] = GENESIS
        self._rewrite(es)
        status, findings = audit_log.verify_chain(self.log)
        self.assertEqual(status, "BROKEN")
        self.assertTrue(any("enlace_roto" in f for f in findings))

    def test_entrada_sin_campo_requerido(self):
        self._append_n(2)
        es = self._entries()
        del es[0]["response_sha256"]
        self._rewrite(es)
        status, findings = audit_log.verify_chain(self.log)
        self.assertEqual(status, "BROKEN")
        self.assertTrue(any("entrada_invalida" in f for f in findings))

    def test_linea_no_json(self):
        self._append_n(2)
        lines = self.log.read_text(encoding="utf-8").splitlines()
        lines.insert(1, "no es json")
        self.log.write_text("\n".join(lines) + "\n", encoding="utf-8")
        status, findings = audit_log.verify_chain(self.log)
        self.assertEqual(status, "BROKEN")
        self.assertTrue(any("linea_no_json" in f for f in findings))

    def test_log_inexistente_broken(self):
        status, findings = audit_log.verify_chain(self.root / "logs" / "no.jsonl")
        self.assertEqual(status, "BROKEN")
        self.assertEqual(findings, ["log_inexistente"])


class TestAnclaF1(_LogCase):
    def test_ancla_coincide_ok(self):
        hashes = self._append_n(3)
        self.assertEqual(audit_log.verify_chain(self.log, anchor_hash=hashes[2]),
                         ("OK", []))

    def test_truncate_rebuild_detectado_por_ancla(self):
        hashes = self._append_n(3)
        # Atacante: log "reconstruido" desde genesis (internamente consistente)
        rebuilt = self.root / "logs" / "rebuilt.jsonl"
        audit_log.append(self.seal, "sha256:falso", rebuilt)
        # Sin ancla SÓLO certifica consistencia interna (límite declarado F1)
        self.assertEqual(audit_log.verify_chain(rebuilt), ("OK", []))
        # Con ancla = último hash conocido-good → reemplazo total detectado
        status, findings = audit_log.verify_chain(rebuilt, anchor_hash=hashes[2])
        self.assertEqual(status, "BROKEN")
        self.assertTrue(any("ancla_no_coincide" in f for f in findings))

    def test_ancla_con_log_vacio_broken(self):
        self.log.parent.mkdir(parents=True, exist_ok=True)
        self.log.write_text("", encoding="utf-8")
        status, findings = audit_log.verify_chain(self.log, anchor_hash="sha256:x")
        self.assertEqual(status, "BROKEN")
        self.assertTrue(any("ancla_no_verificable" in f for f in findings))


if __name__ == "__main__":
    unittest.main()
