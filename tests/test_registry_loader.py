"""T3: loader YAML y banner sobre el dict, no sobre el texto crudo."""
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from corpus.registry_loader import (
    BANNER_NO,
    BANNER_OK,
    RegistryLoadError,
    corpus_vigencia_banner,
    load_registry,
)
import yaml


VALID_TRUE = """
fuentes:
  - id: LSS
    vigencia_verificada: true
    trazas_publicacion:
      - url: https://example.test/dof
        alcance: instrumento
        cubre_disposiciones: ["LSS:1"]
    revision_vigencia:
      revisado_por: test
      fecha: "2026-01-01"
    traza_disposiciones:
      - disposicion_id: LSS:1
        f5: false
        cubre_disposicion: false
        fecha: "2026-01-01"
        url: https://example.test/dof
"""


def _write(text: str) -> pathlib.Path:
    handle = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8")
    handle.write(text)
    handle.close()
    return pathlib.Path(handle.name)


class TestRegistryLoader(unittest.TestCase):
    def test_comentario_no_cuenta_como_true(self):
        path = _write(
            "fuentes:\n"
            "  - id: Z\n"
            "    # vigencia_verificada: true\n"
            "    vigencia_verificada: false\n"
        )
        try:
            self.assertEqual(corpus_vigencia_banner(path), BANNER_NO)
        finally:
            path.unlink(missing_ok=True)

    def test_rechaza_duplicados_ids_y_tipo(self):
        cases = [
            "fuentes:\n  - id: A\n    vigencia_verificada: false\n    id: B\n",
            "fuentes:\n  - id: A\n    vigencia_verificada: false\n  - id: A\n    vigencia_verificada: false\n",
            "fuentes:\n  - no-soy-mapping\n",
            "fuentes:\n  - id: A\n    vigencia_verificada: \"true\"\n",
        ]
        for text in cases:
            path = _write(text)
            try:
                with self.assertRaises(RegistryLoadError):
                    load_registry(path)
            finally:
                path.unlink(missing_ok=True)

    def test_roundtrip_conserva_trazas(self):
        original = {
            "fuentes": [{
                "id": "X",
                "vigencia_verificada": False,
                "traza_disposiciones": [{"disposicion_id": "X:1", "f5": False}],
            }]
        }
        dumped = yaml.safe_dump(original, allow_unicode=True, sort_keys=False)
        loaded = yaml.safe_load(dumped)
        trazas = loaded["fuentes"][0]["traza_disposiciones"]
        self.assertIsInstance(trazas, list)
        self.assertIsInstance(trazas[0], dict)
        path = _write(dumped)
        try:
            doc = load_registry(path)
        finally:
            path.unlink(missing_ok=True)
        self.assertEqual(doc["fuentes"][0]["traza_disposiciones"][0]["disposicion_id"], "X:1")

    def test_banner_no_llama_verify_y_tolera_f5_false(self):
        path = _write(VALID_TRUE)
        try:
            import corpus.verify_citations as vc
            called = {"n": 0}
            original = vc.verify_claim

            def boom(*_a, **_k):
                called["n"] += 1
                raise AssertionError("el banner no debe verificar citas")

            vc.verify_claim = boom
            try:
                self.assertEqual(corpus_vigencia_banner(path), BANNER_OK)
            finally:
                vc.verify_claim = original
            self.assertEqual(called["n"], 0)
        finally:
            path.unlink(missing_ok=True)

    def test_registry_de_produccion_carga(self):
        doc = load_registry(pathlib.Path("corpus/registry.yaml"))
        self.assertGreaterEqual(len(doc["fuentes"]), 6)
        self.assertEqual(corpus_vigencia_banner(), BANNER_OK)


if __name__ == "__main__":
    unittest.main()
