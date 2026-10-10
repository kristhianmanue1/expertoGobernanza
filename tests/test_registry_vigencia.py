"""R1-E1-04 — procedencia primaria y vigencia actual separadas."""
import json
import pathlib
import re
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from corpus.registry_rules import (
    resolve_disposicion_procedencia,
    resolve_disposicion_vigencia,
    validate_fuente,
    validate_registry,
)
from corpus.registry_loader import load_registry, fuente_por_instrumento

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "corpus" / "registry.yaml"


def _fuente_minima_desde_registry(instrumento_id):
    """Extrae solo el contrato anti-herencia del YAML vivo, sin depender de PyYAML."""
    text = REGISTRY.read_text(encoding="utf-8")
    fuente_match = re.search(
        rf"(?ms)^  - id: {re.escape(instrumento_id)}\n(?P<body>.*?)(?=^  - id: |\Z)",
        text,
    )
    if fuente_match is None:
        raise AssertionError(f"instrumento ausente en registry: {instrumento_id}")
    body = fuente_match.group("body")

    resumen_match = re.search(
        r"(?m)^    procedencia_primaria_verificada:\s*(true|false)\b", body
    )
    if resumen_match is None:
        raise AssertionError(f"{instrumento_id}: falta procedencia_primaria_verificada")

    detalle_match = re.search(
        r"(?ms)^    traza_disposiciones:\n(?P<body>.*?)(?=^    \S|\Z)", body
    )
    if detalle_match is None:
        raise AssertionError(f"{instrumento_id}: falta traza_disposiciones")

    trazas = []
    for match in re.finditer(
        r'(?ms)^      - disposicion_id:\s*"(?P<id>[^"]+)"\n'
        r"(?P<body>.*?)(?=^      - disposicion_id:|\Z)",
        detalle_match.group("body"),
    ):
        traza_body = match.group("body")
        cubre = re.search(
            r"(?m)^        cubre_disposicion:\s*(true|false)\b", traza_body
        )
        f5 = re.search(r"(?m)^        f5:\s*(true|false)\b", traza_body)
        fecha = re.search(r'(?m)^        fecha:\s*"([^"]+)"', traza_body)
        identificadores = re.search(
            r'(?m)^        identificadores_diario:\s*"([^"]+)"', traza_body
        )
        trazas.append({
            "disposicion_id": match.group("id"),
            "cubre_disposicion": cubre is not None and cubre.group(1) == "true",
            "f5": f5 is not None and f5.group(1) == "true",
            "fecha": fecha.group(1) if fecha else None,
            "identificadores_diario": (
                identificadores.group(1) if identificadores else None
            ),
        })

    return {
        "id": instrumento_id,
        "procedencia_primaria_verificada": resumen_match.group(1) == "true",
        "traza_disposiciones": trazas,
        "revision_procedencia": {"revisado_por": "registro vivo", "fecha": "2026-08-10"},
    }


class TestRegistryRules(unittest.TestCase):
    def test_procedencia_historica_no_acredita_vigencia_actual(self):
        registry = load_registry(REGISTRY)
        fuente = fuente_por_instrumento(registry, "CPEUM")
        resultado = resolve_disposicion_vigencia(fuente, "CPEUM:4:P4")
        self.assertTrue(resultado["procedencia_primaria_verificada"])
        self.assertFalse(resultado["verificada"])
        self.assertEqual(resultado["vigencia_actual_estado"], "no_verificada")
        self.assertTrue(resultado["vigencia_actual_estado_valido"])
        self.assertEqual(resultado["procedencia_razon"], "traza_exacta_con_revision")
        self.assertEqual(resultado["razon"], "vigencia_actual_no_verificada")

    def test_estado_actual_positivo_sin_contrato_falla_cerrado(self):
        registry = load_registry(REGISTRY)
        fuente = fuente_por_instrumento(registry, "CPEUM")
        fuente = {**fuente, "vigencia_actual_estado": "verificada"}
        self.assertTrue(any("vigencia_actual_estado" in e for e in validate_fuente(fuente)))
        resultado = resolve_disposicion_vigencia(fuente, "CPEUM:4:P4")
        self.assertFalse(resultado["verificada"])
        self.assertFalse(resultado["vigencia_actual_estado_valido"])
        self.assertIsNone(resultado["vigencia_actual_estado"])
        self.assertEqual(resultado["razon"], "vigencia_actual_estado_no_admitido")

    def test_estado_actual_ausente_o_malformado_falla_cerrado(self):
        registry = load_registry(REGISTRY)
        fuente = fuente_por_instrumento(registry, "CPEUM")
        for estado in (None, True, [], {}):
            with self.subTest(estado=estado):
                caso = {**fuente, "vigencia_actual_estado": estado}
                if estado is None:
                    caso.pop("vigencia_actual_estado")
                self.assertTrue(any("vigencia_actual_estado" in e for e in validate_fuente(caso)))
                resultado = resolve_disposicion_vigencia(caso, "CPEUM:4:P4")
                self.assertFalse(resultado["verificada"])
                self.assertFalse(resultado["vigencia_actual_estado_valido"])
                self.assertIsNone(resultado["vigencia_actual_estado"])

        caso = {**fuente, "vigencia_actual_estado": None}
        self.assertEqual(
            resolve_disposicion_vigencia(caso, "CPEUM:4:P4")["razon"],
            "vigencia_actual_estado_no_admitido",
        )

    def test_legado_positivo_no_pasa_validacion(self):
        for estado in (None, "verificada", "no_verificada"):
            with self.subTest(estado=estado):
                caso = {"id": "X", "vigencia_verificada": True}
                if estado is not None:
                    caso["vigencia_actual_estado"] = estado
                errs = validate_fuente(caso)
                self.assertTrue(any("legado no puede ser true" in e for e in errs))
                self.assertFalse(resolve_disposicion_vigencia(caso, "X:1")["verificada"])

    def test_legado_completo_no_acredita_procedencia(self):
        caso = {
            "id": "X", "vigencia_verificada": True,
            "revision_vigencia": {"revisado_por": "h", "fecha": "2026-08-10"},
            "trazas_publicacion": [{
                "identificadores_diario": "DOF prueba", "alcance": "articulo",
                "cubre_disposiciones": ["X:1"],
            }],
        }
        self.assertFalse(resolve_disposicion_procedencia(caso, "X:1")["verificada"])
        self.assertTrue(validate_fuente(caso))

    def test_revision_legada_no_acredita_procedencia_nueva(self):
        caso = {
            "id": "X", "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "revision_vigencia": {"revisado_por": "h", "fecha": "2026-08-10"},
            "trazas_publicacion": [{
                "identificadores_diario": "DOF prueba", "alcance": "articulo",
                "cubre_disposiciones": ["X:1"],
            }],
        }
        self.assertFalse(resolve_disposicion_procedencia(caso, "X:1")["verificada"])
        self.assertTrue(any("revision_procedencia" in e for e in validate_fuente(caso)))

    def test_fuente_sin_campos_nuevos_no_pasa_validacion(self):
        for caso in ({"id": "X"},
                     {"id": "X", "vigencia_verificada": False},
                     {"id": "X", "procedencia_primaria_verificada": False}):
            with self.subTest(caso=caso):
                errs = validate_fuente(caso)
                self.assertTrue(any("vigencia_actual_estado" in e for e in errs))
                self.assertFalse(resolve_disposicion_vigencia(caso, "X:1")["verificada"])

    def test_cpeum_2026_body_trace_does_not_verify_health_slice(self):
        registry = load_registry(REGISTRY)
        fuente = fuente_por_instrumento(registry, "CPEUM")
        self.assertIsNotNone(fuente)
        traces = fuente["trazas_publicacion"]
        body_trace = next(t for t in traces if "codigo=5800617" in (t.get("url") or ""))
        self.assertEqual(body_trace["cubre_disposiciones"], [])
        self.assertTrue(body_trace["no_cubre_slice"])
        original = resolve_disposicion_procedencia(fuente, "CPEUM:4:P4")
        self.assertTrue(original["verificada"])
        without_body = {**fuente, "trazas_publicacion": [t for t in traces if t is not body_trace]}
        self.assertEqual(resolve_disposicion_procedencia(without_body, "CPEUM:4:P4"), original)
        without_slice = {**fuente, "trazas_publicacion": [body_trace]}
        self.assertFalse(resolve_disposicion_procedencia(without_slice, "CPEUM:4:P4")["verificada"])

    def test_false_con_estado_actual_ok(self):
        self.assertEqual(validate_fuente({"id": "X", "vigencia_verificada": False,
                                         "procedencia_primaria_verificada": False,
                                         "vigencia_actual_estado": "no_verificada"}), [])

    def test_vigencia_no_booleana_falla(self):
        errs = validate_fuente({"id": "X", "vigencia_verificada": "pendiente"})
        self.assertTrue(any("booleano" in e for e in errs))

    def test_true_sin_traza_falla(self):
        errs = validate_fuente({"id": "X", "vigencia_verificada": True})
        self.assertTrue(any("sin trazas" in e for e in errs))

    def test_true_solo_url_sin_trazas_falla(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "url_dof_nivel1": "https://dof.gob.mx/nota",
        })
        self.assertTrue(any("solo url_dof" in e or "trazas_publicacion" in e for e in errs))

    def test_true_sin_alcance_falla(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "trazas_publicacion": [{
                "url": "https://dof.gob.mx/x",
                "cubre_disposiciones": ["CPEUM:4:P4"],
            }],
            "revision_procedencia": {"revisado_por": "humano", "fecha": "2026-08-10"},
        })
        self.assertTrue(any("alcance" in e for e in errs))

    def test_true_sin_cover_falla(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "trazas_publicacion": [{
                "url": "https://dof.gob.mx/x",
                "alcance": "articulo",
                "cubre_disposiciones": [],
            }],
            "revision_procedencia": {"revisado_por": "humano", "fecha": "2026-08-10"},
        })
        self.assertTrue(any("cubre" in e or "no_cubre" in e for e in errs))

    def test_true_sin_revision_falla(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "trazas_publicacion": [{
                "identificadores_diario": "DOF 08-05-2020 codigo=5593045",
                "alcance": "articulo",
                "cubre_disposiciones": ["CPEUM:4:P4"],
            }],
        })
        self.assertTrue(any("revision_procedencia" in e for e in errs))

    def test_true_completo_ok(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "trazas_publicacion": [{
                "url": "https://dof.gob.mx/nota_detalle.php?codigo=5593045&fecha=08/05/2020",
                "alcance": "articulo",
                "cubre_disposiciones": ["CPEUM:4:P4"],
            }],
            "revision_procedencia": {
                "revisado_por": "Kristhian Manuel Jimenez",
                "fecha": "2026-08-10",
                "auto_revision_declarada": True,
            },
        })
        self.assertEqual(errs, [])

    def test_true_no_cubre_slice_explicito_ok_estructura(self):
        errs = validate_fuente({
            "id": "X",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "trazas_publicacion": [{
                "url": "https://dof.gob.mx/x",
                "alcance": "instrumento",
                "no_cubre_slice": True,
            }],
            "revision_procedencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        })
        self.assertEqual(errs, [])

    def test_registry_validate_lista(self):
        self.assertEqual(
            validate_registry({"fuentes": [{"id": "A", "vigencia_verificada": False,
                                             "procedencia_primaria_verificada": False,
                                             "vigencia_actual_estado": "no_verificada"}]}),
            [],
        )

    def test_slice_multiple_exige_f5_explicito_por_disposicion(self):
        fuente = {
            "id": "X",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "slice_mvp_disposiciones": ["X:1", "X:2"],
            "trazas_publicacion": [{
                "identificadores_diario": "DOF prueba",
                "alcance": "articulo",
                "cubre_disposiciones": ["X:1"],
            }],
            "revision_procedencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        }
        errs = validate_fuente(fuente)
        self.assertTrue(any("multidisposición" in e for e in errs))

    def test_slice_simple_valida_campos_de_traza_disposicion(self):
        fuente = {
            "id": "X",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "slice_mvp_disposiciones": ["X:1"],
            "traza_disposiciones": [{
                "disposicion_id": "X:1",
                "f5": True,
                "cubre_disposicion": True,
            }],
            "trazas_publicacion": [{
                "identificadores_diario": "DOF prueba",
                "alcance": "articulo",
                "cubre_disposiciones": ["X:1"],
            }],
            "revision_procedencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        }
        errs = validate_fuente(fuente)
        self.assertTrue(any("X:1 sin fecha" in e for e in errs))
        self.assertTrue(any("X:1 sin url" in e for e in errs))


class TestResolveDisposicionVigencia(unittest.TestCase):
    def setUp(self):
        self.lfep = {
            "id": "LFEP",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "traza_disposiciones": [
                {
                    "disposicion_id": "LFEP:1",
                    "cubre_disposicion": True,
                    "f5": True,
                    "fecha": "1986-05-14",
                    "identificadores_diario": "DOF 14-05-1986",
                },
                {
                    "disposicion_id": "LFEP:5",
                    "cubre_disposicion": True,
                    "f5": True,
                    "fecha": "2025-07-16",
                    "identificadores_diario": "DOF 16-07-2025 codigo=5763164",
                },
            ],
            "revision_procedencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        }

    def test_lfep_1_y_lfep_5_tienen_f5_explicito(self):
        uno = resolve_disposicion_procedencia(self.lfep, "LFEP:1")
        cinco = resolve_disposicion_procedencia(self.lfep, "LFEP:5")
        self.assertTrue(uno["verificada"])
        self.assertEqual(uno["razon"], "f5_explicito")
        self.assertTrue(cinco["verificada"])
        self.assertEqual(cinco["razon"], "f5_explicito")

    def test_disposicion_ausente_no_hereda_true_instrumental(self):
        resultado = resolve_disposicion_procedencia(self.lfep, "LFEP:999")
        self.assertFalse(resultado["verificada"])
        self.assertEqual(resultado["razon"], "sin_traza_explicita")

    def test_instrumento_false_bloquea_f5_de_disposicion(self):
        self.lfep["procedencia_primaria_verificada"] = False
        resultado = resolve_disposicion_procedencia(self.lfep, "LFEP:1")
        self.assertFalse(resultado["verificada"])
        self.assertEqual(resultado["razon"], "procedencia_no_verificada")

    def test_traza_principal_solo_resuelve_id_exacto(self):
        fuente = {
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "traza_disposicion_principal": {
                "disposicion_id": "LOAPF:1",
                "cubre_disposicion": True,
                "fecha": "1976-12-29",
                "identificadores_diario": "DOF 29-12-1976 publicación LOAPF",
            },
            "revision_procedencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        }
        self.assertTrue(
            resolve_disposicion_procedencia(fuente, "LOAPF:1")["verificada"]
        )
        self.assertFalse(
            resolve_disposicion_procedencia(fuente, "LOAPF:2")["verificada"]
        )

    def test_traza_publicacion_solo_resuelve_cobertura_exacta(self):
        fuente = {
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "trazas_publicacion": [{
                "identificadores_diario": "DOF prueba",
                "alcance": "articulo",
                "cubre_disposiciones": ["CPEUM:4:P4"],
            }],
            "revision_procedencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        }
        self.assertTrue(
            resolve_disposicion_procedencia(fuente, "CPEUM:4:P4")["verificada"]
        )
        self.assertFalse(
            resolve_disposicion_procedencia(fuente, "CPEUM:5")["verificada"]
        )

    def test_alcance_instrumento_no_resuelve_disposicion(self):
        fuente = {
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "trazas_publicacion": [{
                "identificadores_diario": "DOF prueba",
                "alcance": "instrumento",
                "cubre_disposiciones": ["X:1"],
            }],
            "revision_procedencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        }
        resultado = resolve_disposicion_procedencia(fuente, "X:1")
        self.assertFalse(resultado["verificada"])
        self.assertEqual(resultado["razon"], "traza_publicacion_incompleta")

    def test_cubre_disposiciones_escalar_no_hace_match_por_subcadena(self):
        fuente = {
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "trazas_publicacion": [{
                "identificadores_diario": "DOF prueba",
                "alcance": "articulo",
                "cubre_disposiciones": "X:10",
            }],
            "revision_procedencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        }
        resultado = resolve_disposicion_procedencia(fuente, "X:1")
        self.assertFalse(resultado["verificada"])
        self.assertTrue(any("debe ser lista" in e for e in validate_fuente(fuente)))

    def test_trazas_disposicion_duplicadas_fallan_cerrado(self):
        fuente = {
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "traza_disposiciones": [
                {"disposicion_id": "X:1", "f5": True, "cubre_disposicion": True},
                {"disposicion_id": "X:1", "f5": False, "cubre_disposicion": True},
            ],
        }
        resultado = resolve_disposicion_procedencia(fuente, "X:1")
        self.assertFalse(resultado["verificada"])
        self.assertEqual(resultado["razon"], "traza_duplicada")

    def test_f5_true_sin_fecha_locator_o_revision_no_resuelve(self):
        fuente = {
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "traza_disposiciones": [
                {"disposicion_id": "X:1", "f5": True, "cubre_disposicion": True}
            ],
        }
        resultado = resolve_disposicion_procedencia(fuente, "X:1")
        self.assertFalse(resultado["verificada"])
        self.assertEqual(resultado["razon"], "f5_no_verificado")

    def test_fuente_no_objeto_falla_cerrado(self):
        resultado = resolve_disposicion_procedencia(None, "X:1")
        self.assertFalse(resultado["verificada"])
        self.assertEqual(resultado["razon"], "fuente_invalida")

    def test_traza_principal_sin_locator_no_resuelve(self):
        fuente = {
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "traza_disposicion_principal": {
                "disposicion_id": "X:1",
                "fecha": "2026-01-01",
                "cubre_disposicion": True,
            },
            "revision_procedencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        }
        resultado = resolve_disposicion_procedencia(fuente, "X:1")
        self.assertFalse(resultado["verificada"])

    def test_busca_traza_publicacion_valida_despues_de_incompleta(self):
        fuente = {
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "trazas_publicacion": [
                {
                    "identificadores_diario": "DOF cuerpo",
                    "alcance": "instrumento",
                    "cubre_disposiciones": ["X:1"],
                },
                {
                    "identificadores_diario": "DOF artículo",
                    "alcance": "articulo",
                    "cubre_disposiciones": ["X:1"],
                },
            ],
            "revision_procedencia": {"revisado_por": "h", "fecha": "2026-08-10"},
        }
        resultado = resolve_disposicion_procedencia(fuente, "X:1")
        self.assertTrue(resultado["verificada"])


class TestLiveRegistryFile(unittest.TestCase):
    def test_derivados_no_convierten_procedencia_en_vigencia_actual(self):
        registry = load_registry(REGISTRY)
        esperados = {
            "CPEUM:4:P4": (True, "trazas_publicacion", "traza_exacta_con_revision"),
            "LGS:1": (True, "trazas_publicacion", "traza_exacta_con_revision"),
            "LOAPF:1:P3": (True, "traza_disposiciones", "f5_explicito"),
            "LOAPF:1": (False, "traza_disposiciones", "sin_traza_explicita"),
            "LFEP:1": (True, "traza_disposiciones", "f5_explicito"),
            "LFEP:5": (True, "traza_disposiciones", "f5_explicito"),
            "LSS:1": (False, "traza_disposiciones", "f5_no_verificado"),
            "LSS:5": (True, "traza_disposiciones", "f5_explicito"),
            "RIIMSS:1": (True, "traza_disposicion_principal", "traza_exacta_con_revision"),
        }
        comprobados = []
        for path in sorted((ROOT / "corpus/derived").rglob("*.json")):
            derivado = json.loads(path.read_text(encoding="utf-8"))
            disposicion_id = derivado.get("disposicion_id")
            instrumento_id = (derivado.get("instrumento") or {}).get("id")
            self.assertTrue(disposicion_id, msg=str(path))
            self.assertTrue(instrumento_id, msg=str(path))
            fuente = fuente_por_instrumento(registry, instrumento_id)
            self.assertIsNotNone(fuente, msg=f"fuente ausente: {instrumento_id}")
            resultado = resolve_disposicion_vigencia(fuente, disposicion_id)
            comprobados.append(disposicion_id)
            with self.subTest(disposicion_id=disposicion_id):
                vigencia = derivado["vigencia"]
                self.assertEqual(
                    vigencia["procedencia_primaria_verificada"],
                    resultado["procedencia_primaria_verificada"],
                )
                self.assertEqual(
                    (resultado["procedencia_primaria_verificada"],
                     resultado["procedencia_fuente"], resultado["procedencia_razon"]),
                    esperados[disposicion_id],
                )
                self.assertFalse(vigencia["verificada_contra_dof_nivel1"])
                self.assertIn("vigencia actual", vigencia["nota_legado"])
                self.assertEqual(vigencia["vigencia_actual_estado"], "no_verificada")
                self.assertNotEqual(vigencia.get("estado"), "vigente")
                self.assertFalse(resultado["verificada"])
        self.assertEqual(len(comprobados), len(esperados))
        self.assertEqual(set(comprobados), set(esperados))

    def test_file_exists(self):
        self.assertTrue(REGISTRY.is_file())

    def test_cpeum_y_lgs_presentes(self):
        text = REGISTRY.read_text(encoding="utf-8")
        self.assertIn("id: CPEUM", text)
        self.assertIn("id: LGS", text)

    def test_h1_slice_true_presente(self):
        text = REGISTRY.read_text(encoding="utf-8")
        trues = re.findall(
            r"(?m)^[ \t]*procedencia_primaria_verificada:\s*true\b", text, flags=re.I
        )
        # salud CPEUM+LGS + eje IMSS LOAPF+LFEP+LSS+RIIMSS
        self.assertGreaterEqual(len(trues), 6, msg="slices H1 salud + estructura IMSS")

    def test_traza_vs_cuerpo_fields_documented(self):
        text = REGISTRY.read_text(encoding="utf-8")
        self.assertIn("traza_disposicion_principal:", text)
        self.assertIn("ultima_reforma_cuerpo:", text)
        # LSS: no confundir 2026 cuerpo con 2001 Art.5
        self.assertIn("2001-12-20", text)
        self.assertIn("cubre_disposicion: false", text)

    def test_h1_estructuras_cumplen_rules(self):
        # Espejo mínimo de las entradas true post-F5 (sin parser YAML)
        cpeum = {
            "id": "CPEUM",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "url_dof_nivel1": "https://dof.gob.mx/nota_detalle.php?codigo=5593045&fecha=08/05/2020",
            "trazas_publicacion": [{
                "url": "https://dof.gob.mx/nota_detalle.php?codigo=5593045&fecha=08/05/2020",
                "alcance": "articulo",
                "cubre_disposiciones": ["CPEUM:4:P4"],
            }],
            "revision_procedencia": {
                "revisado_por": "Kristhian Manuel Jiménez",
                "fecha": "2026-08-10",
                "auto_revision_declarada": True,
            },
        }
        lgs = {
            "id": "LGS",
            "vigencia_verificada": False,
            "procedencia_primaria_verificada": True,
            "vigencia_actual_estado": "no_verificada",
            "trazas_publicacion": [{
                "identificadores_diario": "DOF 29-05-2023 reforma LGS Art.1",
                "alcance": "articulo",
                "cubre_disposiciones": ["LGS:1"],
            }],
            "revision_procedencia": {
                "revisado_por": "Kristhian Manuel Jiménez",
                "fecha": "2026-08-10",
                "auto_revision_declarada": True,
            },
        }
        self.assertEqual(validate_fuente(cpeum), [])
        self.assertEqual(validate_fuente(lgs), [])
        self.assertEqual(validate_registry({"fuentes": [cpeum, lgs]}), [])

    def test_multidisposicion_viva_no_hereda_y_coincide_con_derivados(self):
        casos = {
            "LOAPF": {"LOAPF:1:P3": True, "LOAPF:1": False},
            "LFEP": {"LFEP:1": True, "LFEP:5": True},
            "LSS": {"LSS:5": True, "LSS:1": False},
        }
        archivos = {
            "LOAPF:1:P3": ROOT / "corpus/derived/loapf/LOAPF-001-P3.json",
            "LOAPF:1": ROOT / "corpus/derived/loapf/LOAPF-001.json",
            "LFEP:1": ROOT / "corpus/derived/lfep/LFEP-001.json",
            "LFEP:5": ROOT / "corpus/derived/lfep/LFEP-005.json",
            "LSS:5": ROOT / "corpus/derived/lss/LSS-005.json",
            "LSS:1": ROOT / "corpus/derived/lss/LSS-001.json",
        }
        for instrumento_id, esperados in casos.items():
            fuente = _fuente_minima_desde_registry(instrumento_id)
            for disposicion_id, esperado in esperados.items():
                with self.subTest(disposicion_id=disposicion_id):
                    resultado = resolve_disposicion_procedencia(
                        fuente, disposicion_id
                    )
                    self.assertEqual(resultado["verificada"], esperado)
                    derivado = json.loads(
                        archivos[disposicion_id].read_text(encoding="utf-8")
                    )
                    self.assertEqual(
                        derivado["vigencia"]["procedencia_primaria_verificada"],
                        esperado,
                    )


if __name__ == "__main__":
    unittest.main()
