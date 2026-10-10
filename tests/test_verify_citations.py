import pathlib
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from corpus import verify_citations as vc

CPEUM_QUOTE = (
    "Toda Persona tiene derecho a la protección de la salud. "
    "La Ley definirá las bases y modalidades para el acceso a los servicios de salud"
)
LGS_QUOTE = (
    "La presente ley reglamenta el derecho a la protección de la salud "
    "que tiene toda persona en los términos del artículo 4o. de la Constitución"
)


def _claim(did, cita):
    return {"disposicion_id": did, "cita_texto": cita}


class TestVerifyGate(unittest.TestCase):
    def test_golden_cpeum_medio(self):
        r = vc.verify_claim(_claim("CPEUM:4:P4", CPEUM_QUOTE))
        self.assertEqual(r["gate_version"], "v1")
        self.assertTrue(r["reference_exists"])
        self.assertTrue(r["quote_substring_match"])
        self.assertGreaterEqual(r["match_len"], vc.MIN_CITA_LEN)
        self.assertTrue(r["source_resolved"])
        self.assertIsNotNone(r["derived_file"])
        if r["fuente_sha256_recomputed"]:
            self.assertEqual(r["fuente_sha256_recomputed"], r["fuente_sha256_declared"])
        self.assertEqual(r["response_status"], "medio")
        self.assertEqual(r["registry_check"], "unverified")
        self.assertTrue(r["registry_procedencia_primaria_verificada"])
        self.assertEqual(r["registry_procedencia_fuente"], "trazas_publicacion")
        self.assertEqual(r["registry_procedencia_razon"], "traza_exacta_con_revision")

    def test_golden_lgs_medio(self):
        r = vc.verify_claim(_claim("LGS:1", LGS_QUOTE))
        self.assertTrue(r["quote_substring_match"])
        self.assertTrue(r["source_resolved"])
        self.assertEqual(r["response_status"], "medio")

    def test_slice_sin_procedencia_no_hereda_instrumento(self):
        for did, razon in (("LOAPF:1", "sin_traza_explicita"),
                           ("LSS:1", "f5_no_verificado")):
            with self.subTest(disposicion_id=did):
                r = vc.verify_claim(_claim(did, "cita de control sin valor jurídico"))
                self.assertTrue(r["reference_exists"])
                self.assertEqual(r["registry_check"], "unverified")
                self.assertFalse(r["registry_procedencia_primaria_verificada"])
                self.assertEqual(r["registry_procedencia_fuente"], "traza_disposiciones")
                self.assertEqual(r["registry_procedencia_razon"], razon)
                self.assertNotEqual(r["response_status"], "alto")

    def test_registry_negative_routes_do_not_export_provenance(self):
        texto = "texto suficientemente largo para una cita de prueba reproducible"
        cases = (
            {"fuente": None},
            {"loader_error": True},
            {"resolver_error": True},
            {"resolver": lambda *_: None},
        )
        for kwargs in cases:
            with self.subTest(kwargs=list(kwargs)):
                r = _diagnostico(texto, source_check="match", **kwargs)
                self.assertFalse(r["registry_procedencia_primaria_verificada"])
                self.assertIsNone(r["registry_procedencia_fuente"])
                self.assertIsNone(r["registry_procedencia_razon"])
                self.assertIn(r["registry_check"], {"error", "missing_evidence"})

    def test_alto_inalcanzable_en_v1(self):
        texto = ("texto suficientemente largo para pasar el minimo "
                 "de cuarenta caracteres normalizados sin problema")
        for verificada, check in ((False, "unverified"), (True, "verified")):
            with self.subTest(verificada=verificada):
                seen = {}

                def _resolver(fuente, disposicion_id, flag=verificada):
                    seen["fuente"] = fuente
                    seen["disposicion_id"] = disposicion_id
                    return {"verificada": flag, "razon": "salida-de-prueba"}

                r = _diagnostico(texto, source_check="match", resolver=_resolver)
                self.assertEqual(seen["fuente"]["id"], "FAKE")
                self.assertEqual(seen["disposicion_id"], "FAKE:1")
                self.assertEqual(r["registry_check"], check)
                self.assertEqual(r["registry_razon"], "salida-de-prueba")
                self.assertEqual(r["response_status"], "medio")
                self.assertEqual(r["version_valid_for_date"], "N/A_v1")
                self.assertNotEqual(r["response_status"], "alto")

    def test_disposicion_inexistente_bajo(self):
        r = vc.verify_claim(_claim("NO:EX:ISTE", "x" * 50))
        self.assertFalse(r["reference_exists"])
        self.assertEqual(r["response_status"], "bajo")

    def test_cita_demasiado_corta_bajo(self):
        r = vc.verify_claim(_claim("CPEUM:4:P4", "salud"))
        self.assertFalse(r["quote_substring_match"])
        self.assertEqual(r["response_status"], "bajo")

    def test_cita_solo_espacios_bajo(self):
        r = vc.verify_claim(_claim("CPEUM:4:P4", "    "))
        self.assertFalse(r["quote_substring_match"])
        self.assertEqual(r["response_status"], "bajo")

    def test_normalizacion_acentos_mayusculas(self):
        cita = (CPEUM_QUOTE.upper()
                .replace("Á", "A").replace("É", "E").replace("Í", "I")
                .replace("Ó", "O").replace("Ú", "U"))
        r = vc.verify_claim(_claim("CPEUM:4:P4", cita))
        self.assertTrue(r["quote_substring_match"])

    def test_exit_codes_distintos_por_nivel(self):
        self.assertEqual(vc._EXIT, {"alto": 0, "medio": 2, "bajo": 1})

    def test_golden_conserva_v1_y_diagnostico(self):
        r = vc.verify_claim(_claim("CPEUM:4:P4", CPEUM_QUOTE))
        self.assertEqual(r["gate_version"], vc.GATE_VERSION)
        self.assertEqual(r["evidence_schema_version"], "v1")
        self.assertEqual(r["version_valid_for_date"], "N/A_v1")
        self.assertIn(r["source_check"], {"missing", "match"})
        self.assertIn(r["registry_check"], {"verified", "unverified", "missing_evidence"})
        self.assertNotEqual(r["response_status"], "alto")
        self.assertTrue(any("Fecha jurídica no evaluada" in n for n in r["notes"]))

    def test_matriz_de_diagnostico(self):
        texto = "x" * 50
        self.assertEqual(
            _diagnostico(texto, source_check="missing", fuente=None)["registry_check"],
            "missing_evidence",
        )
        medio = _diagnostico(texto, source_check="missing", fuente=None)
        self.assertEqual(medio["response_status"], "medio")
        coincidente = _diagnostico(texto, source_check="match", fuente=None)
        self.assertEqual(
            (coincidente["response_status"], coincidente["registry_check"]),
            ("medio", "missing_evidence"),
        )
        distinto = _diagnostico(texto, source_check="mismatch", fuente=None)
        self.assertEqual(distinto["response_status"], "bajo")
        ilegible = _diagnostico(texto, source_check="error", fuente=None)
        self.assertEqual(ilegible["response_status"], "bajo")
        self.assertEqual(
            _diagnostico(texto, source_check="match", loader_error=True)["response_status"],
            "bajo",
        )
        self.assertEqual(
            _diagnostico(texto, source_check="match", resolver_error=True)["registry_check"],
            "error",
        )

    def test_relaciones_normativas_no_cambian_el_status(self):
        texto = "y" * 50
        a = _diagnostico(texto, source_check="match", relaciones=["A"])
        b = _diagnostico(texto, source_check="match", relaciones=["B", "C"])
        self.assertEqual(a["response_status"], b["response_status"])
        self.assertNotIn("relaciones_normativas", a)


def _diagnostico(texto, source_check, fuente="presente", resolver=None,
                 loader_error=False, resolver_error=False, relaciones=None):
    modelo = {
        "disposicion_id": "FAKE:1",
        "texto_verbatim": texto,
        "instrumento": {"id": "FAKE"},
        "vigencia": {"verificada_contra_dof_nivel1": True},
        "fuentes_oficiales": [{"sha256": "ab" * 32, "archivo": "no-se-lee"}],
        "relaciones_normativas": relaciones or [],
    }
    declared = source_check != "invalid_declaration"
    src = {
        "resolved": source_check in {"missing", "match"},
        "sha256_declared": "ab" * 32 if declared else None,
        "sha256_recomputed": "ab" * 32 if source_check == "match" else None,
        "archivo": "no-se-lee",
        "declared_ok": declared,
        "recomputed_ok": source_check == "match",
        "source_check": source_check,
        "note": "",
    }
    fuente_doc = None if fuente is None else {"id": "FAKE", "vigencia_verificada": True}

    def _load(_path):
        if loader_error:
            raise RuntimeError("registry malformado")
        return {"fuentes": [] if fuente_doc is None else [fuente_doc]}

    def _resolver(fuente_arg, disposicion_id):
        if resolver_error:
            raise RuntimeError("resolver")
        if resolver:
            return resolver(fuente_arg, disposicion_id)
        return {"verificada": False, "razon": "negativo"}

    with mock.patch.object(vc, "load_index", return_value={"FAKE:1": modelo}):
        with mock.patch.object(vc, "_resolve_source", return_value=src):
            with mock.patch("corpus.registry_loader.load_registry", side_effect=_load):
                with mock.patch(
                    "corpus.registry_rules.resolve_disposicion_vigencia",
                    side_effect=_resolver,
                ):
                    return vc.verify_claim(_claim("FAKE:1", texto))


if __name__ == "__main__":
    unittest.main()
