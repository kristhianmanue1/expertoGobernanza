"""Regresiones del gate de tamaño para artefactos exentos."""
import os
import unittest

from scripts.check_sizes import is_exempt


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


if __name__ == "__main__":
    unittest.main()
