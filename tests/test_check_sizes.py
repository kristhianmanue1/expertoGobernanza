"""Regresiones del gate de tamaño para artefactos exentos y bloque de registro."""
import os
import tempfile
import unittest

from scripts.check_sizes import check_registry_block, is_exempt


class TestCheckSizesExemptions(unittest.TestCase):
    def test_esquema_akn_vendorizado_esta_exento(self):
        rel = os.path.join("interop", "akn", "schema", "akomantoso30.xsd")
        self.assertTrue(is_exempt(rel, "akomantoso30.xsd"))

    def test_xsd_fuera_del_directorio_vendorizado_no_esta_exento(self):
        rel = os.path.join("interop", "akn", "custom.xsd")
        self.assertFalse(is_exempt(rel, "custom.xsd"))

    def test_prefijo_parecido_no_esta_exento(self):
        rel = os.path.join("interop", "akn", "schema-copy", "custom.xsd")
        self.assertFalse(is_exempt(rel, "custom.xsd"))


class TestRegistryBlock(unittest.TestCase):
    """Validación del bloque skevi:registry (estándar §3.5)."""

    def _block(self, body):
        return (
            "<!-- skevi:registry:start -->\n"
            f"{body}\n"
            "<!-- skevi:registry:end -->\n"
        )

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.real = os.path.abspath(".")

    def test_bloque_valido_no_falla(self):
        os.makedirs(os.path.join(self.tmp, "docs"))
        open(os.path.join(self.tmp, "docs", "politica.md"), "w").close()
        text = self._block("[skevi]\npolicy = docs/politica.md")
        self.assertEqual(check_registry_block("AGENTS.md", text, self.tmp), [])

    def test_sin_bloque_no_falla(self):
        text = "# AGENTS.md\n contenido sin bloque\n"
        self.assertEqual(check_registry_block("AGENTS.md", text, self.tmp), [])

    def test_delimitadores_desbalanceados_falla(self):
        text = "<!-- skevi:registry:start -->\n[skevi]\nx = y\n"
        self.assertEqual(len(check_registry_block("AGENTS.md", text, self.tmp)), 1)

    def test_seccion_skevi_ausente_falla(self):
        text = self._block("policy = docs/x.md")
        self.assertTrue(any("sin sección [skevi]" in m for m in
                            check_registry_block("AGENTS.md", text, self.tmp)))

    def test_ruta_inexistente_falla(self):
        text = self._block("[skevi]\npolicy = docs/no-existe.md")
        self.assertTrue(any("ruta inexistente" in m for m in
                            check_registry_block("AGENTS.md", text, self.tmp)))

    def test_ruta_absoluta_falla(self):
        text = self._block("[skevi]\npolicy = /etc/passwd")
        self.assertTrue(any("fuera de raíz" in m for m in
                            check_registry_block("AGENTS.md", text, self.tmp)))

    def test_ruta_escapa_raiz_falla(self):
        text = self._block("[skevi]\npolicy = ../../etc/passwd")
        fails = check_registry_block("AGENTS.md", text, self.tmp)
        self.assertTrue(any("escapa de raíz" in m or "inexistente" in m for m in fails))

    def test_no_host_no_valida(self):
        text = self._block("[skevi]\nx = y")
        self.assertEqual(check_registry_block("docs/otro.md", text, self.tmp), [])


if __name__ == "__main__":
    unittest.main()
