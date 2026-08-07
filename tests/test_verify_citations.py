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

    def test_golden_lgs_medio(self):
        r = vc.verify_claim(_claim("LGS:1", LGS_QUOTE))
        self.assertTrue(r["quote_substring_match"])
        self.assertTrue(r["source_resolved"])
        self.assertEqual(r["response_status"], "medio")

    def test_alto_inalcanzable_en_v1(self):
        modelo = {
            "disposicion_id": "FAKE:1",
            "texto_verbatim": ("texto suficientemente largo para pasar el minimo "
                               "de cuarenta caracteres normalizados sin problema"),
            "vigencia": {"verificada_contra_dof_nivel1": True},
            "fuentes_oficiales": [{"sha256": "0" * 64, "archivo": "x"}],
        }
        with mock.patch.object(vc, "load_index", return_value={"FAKE:1": modelo}):
            with mock.patch.object(vc, "_resolve_source", return_value={
                "resolved": True, "sha256_declared": "0" * 64,
                "sha256_recomputed": None, "archivo": "x", "note": ""}):
                r = vc.verify_claim(_claim("FAKE:1", modelo["texto_verbatim"]))
        self.assertEqual(r["response_status"], "medio")
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


if __name__ == "__main__":
    unittest.main()
