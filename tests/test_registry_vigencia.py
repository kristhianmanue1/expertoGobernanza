"""R1-E1-04 — no-regresión estructural de vigencia_verificada."""
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from corpus.registry_rules import validate_fuente, validate_registry

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "corpus" / "registry.yaml"


class TestRegistryRules(unittest.TestCase):
    def test_false_always_ok(self):
        self.assertEqual(validate_fuente({"id": "X", "vigencia_verificada": False}), [])

    def test_true_sin_traza_falla(self):
        errs = validate_fuente({"id": "X", "vigencia_verificada": True})
        self.assertTrue(any("sin trazas" in e for e in errs))

    def test_true_solo_url_sin_trazas_falla(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": True,
            "url_dof_nivel1": "https://dof.gob.mx/nota",
        })
        self.assertTrue(any("solo url_dof" in e or "trazas_publicacion" in e for e in errs))

    def test_true_sin_alcance_falla(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": True,
            "trazas_publicacion": [{
                "url": "https://dof.gob.mx/x",
                "cubre_disposiciones": ["CPEUM:4:P4"],
            }],
            "revision_vigencia": {"revisado_por": "humano", "fecha": "2026-08-10"},
        })
        self.assertTrue(any("alcance" in e for e in errs))

    def test_true_sin_cover_falla(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": True,
            "trazas_publicacion": [{
                "url": "https://dof.gob.mx/x",
                "alcance": "articulo",
                "cubre_disposiciones": [],
            }],
            "revision_vigencia": {"revisado_por": "humano", "fecha": "2026-08-10"},
        })
        self.assertTrue(any("cubre" in e or "no_cubre" in e for e in errs))

    def test_true_sin_revision_falla(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": True,
            "trazas_publicacion": [{
                "identificadores_diario": "DOF 08-05-2020 codigo=5593045",
                "alcance": "articulo",
                "cubre_disposiciones": ["CPEUM:4:P4"],
            }],
        })
        self.assertTrue(any("revision_vigencia" in e for e in errs))

    def test_true_completo_ok(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": True,
            "trazas_publicacion": [{
                "url": "https://dof.gob.mx/nota_detalle.php?codigo=5593045&fecha=08/05/2020",
                "alcance": "articulo",
                "cubre_disposiciones": ["CPEUM:4:P4"],
            }],
            "revision_vigencia": {
                "revisado_por": "Kristhian Manuel Jimenez",
                "fecha": "2026-08-10",
                "auto_revision_declarada": True,
            },
        })
        self.assertEqual(errs, [])

    def test_true_no_cubre_slice_explicito_ok_estructura(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": True,
            "trazas_publicacion": [{
                "url": "https://dof.gob.mx/x",
                "alcance": "instrumento",
                "no_cubre_slice": True,
            }],
            "revision_vigencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        })
        self.assertEqual(errs, [])

    def test_registry_validate_lista(self):
        self.assertEqual(
            validate_registry({"fuentes": [{"id": "A", "vigencia_verificada": False}]}),
            [],
        )


class TestLiveRegistryFile(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(REGISTRY.is_file())

    def test_cpeum_y_lgs_presentes(self):
        text = REGISTRY.read_text(encoding="utf-8")
        self.assertIn("id: CPEUM", text)
        self.assertIn("id: LGS", text)

    def test_h1_slice_true_presente(self):
        text = REGISTRY.read_text(encoding="utf-8")
        trues = re.findall(
            r"(?m)^[ \t]*vigencia_verificada:\s*true\b", text, flags=re.I
        )
        self.assertGreaterEqual(len(trues), 2, msg="CPEUM y LGS slice H1")

    def test_h1_estructuras_cumplen_rules(self):
        # Espejo mínimo de las entradas true post-F5 (sin parser YAML)
        cpeum = {
            "id": "CPEUM",
            "vigencia_verificada": True,
            "url_dof_nivel1": "https://dof.gob.mx/nota_detalle.php?codigo=5593045&fecha=08/05/2020",
            "trazas_publicacion": [{
                "url": "https://dof.gob.mx/nota_detalle.php?codigo=5593045&fecha=08/05/2020",
                "alcance": "articulo",
                "cubre_disposiciones": ["CPEUM:4:P4"],
            }],
            "revision_vigencia": {
                "revisado_por": "Kristhian Manuel Jiménez",
                "fecha": "2026-08-10",
                "auto_revision_declarada": True,
            },
        }
        lgs = {
            "id": "LGS",
            "vigencia_verificada": True,
            "trazas_publicacion": [{
                "identificadores_diario": "DOF 29-05-2023 reforma LGS Art.1",
                "alcance": "articulo",
                "cubre_disposiciones": ["LGS:1"],
            }],
            "revision_vigencia": {
                "revisado_por": "Kristhian Manuel Jiménez",
                "fecha": "2026-08-10",
                "auto_revision_declarada": True,
            },
        }
        self.assertEqual(validate_fuente(cpeum), [])
        self.assertEqual(validate_fuente(lgs), [])
        self.assertEqual(validate_registry({"fuentes": [cpeum, lgs]}), [])


if __name__ == "__main__":
    unittest.main()
