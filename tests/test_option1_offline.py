"""Controles offline de la opción 1.

Las expectativas salen del fixture. Este archivo no las calcula con el
segmentador ni con el juez de T2.
"""
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from corpus.option1_offline import baseline, diagnosticos, evaluar, literal, segmentar

FIXTURE = ROOT / "tests" / "fixtures" / "option1_offline" / "controles.json"
METRICAS = (
    "tp", "fp", "fn", "precision", "recall", "razon_precision", "razon_recall",
)


class TestOption1Offline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_no_usa_el_juez_ni_los_fixtures_de_t2(self):
        src = (ROOT / "corpus" / "option1_offline.py").read_text(encoding="utf-8")
        for token in ("eval_extraction", "extraction_gold", "verify_claim", "must_find"):
            self.assertNotIn(token, src)

    def test_segmentos_contra_expectativa_explicita(self):
        for caso in self.data["segmentos"]:
            with self.subTest(caso["id"]):
                for rec in caso["esperado"]:
                    self.assertLess(rec["inicio"], rec["fin"])
                    self.assertEqual(caso["texto"][rec["inicio"]:rec["fin"]], rec["cita_texto"])
                obtenido = segmentar(caso["texto"])
                self.assertEqual(obtenido, caso["esperado"])
                for rec in obtenido:
                    self.assertLess(rec["inicio"], rec["fin"])

    def test_baseline_solo_emite_los_positivos_explicitos(self):
        por_id = {caso["id"]: caso["texto"] for caso in self.data["segmentos"]}
        for ident, esperado in self.data["baseline_esperado"].items():
            with self.subTest(ident):
                self.assertEqual(baseline(por_id[ident]), esperado)
        for caso in self.data["baseline_vacio"]:
            with self.subTest(caso["id"]):
                self.assertEqual(baseline(caso["texto"]), [])

    def test_diagnosticos_y_literalidad_explicitos(self):
        for caso in self.data["pares"]:
            with self.subTest(caso["id"]):
                gold = caso["gold"]
                pred = caso["prediccion"]
                self.assertEqual(literal(caso["texto"], gold["inicio"], gold["fin"], gold["cita_texto"]), caso["L_gold"])
                self.assertEqual(literal(caso["texto"], pred["inicio"], pred["fin"], pred["cita_texto"]), caso["L_pred"])
                diag = diagnosticos(pred["cita_texto"], gold["cita_texto"])
                self.assertEqual(diag["cobertura"], caso["cobertura"])
                self.assertEqual(diag["sobreextension"], caso["sobreextension"])
                self.assertEqual(diag["puntuacion"], caso["puntuacion"])
                misma = (
                    caso["L_gold"] and caso["L_pred"]
                    and gold["inicio"] == pred["inicio"] and gold["fin"] == pred["fin"]
                )
                self.assertEqual(misma, caso["acierto"])
                resultado = evaluar(caso["texto"], [gold], [pred])
                self.assertEqual(resultado["estado"], "ok")
                self.assertEqual(resultado["tp"], 1 if caso["acierto"] else 0)

    def test_puntuaciones_explicitas(self):
        for caso in self.data["puntuaciones"]:
            with self.subTest(caso["id"]):
                resultado = evaluar(caso["texto"], caso["gold"], caso["predicciones"])
                self.assertEqual(resultado["estado"], "ok")
                for clave in METRICAS:
                    self.assertEqual(resultado[clave], caso[clave], clave)
                self.assertEqual([fila["papel"] for fila in resultado["predicciones"]], caso["papeles"])
                if "diagnostico" in caso:
                    self.assertEqual(resultado["predicciones"][0]["diagnostico"], caso["diagnostico"])
                    self.assertEqual(resultado["predicciones"][0]["razon"], caso["razon"])
                    self.assertFalse(resultado["predicciones"][0]["valida"])

    def test_gold_invalido_no_emite_metricas(self):
        for caso in self.data["rechazos"]:
            with self.subTest(caso["id"]):
                resultado = evaluar(caso["texto"], caso["gold"], caso.get("predicciones", []))
                self.assertEqual(resultado["estado"], "rechazo")
                self.assertEqual(resultado["razon"], "gold_invalido")
                self.assertEqual(resultado["detalle"], caso["detalle"])
                for clave in ("tp", "fp", "fn", "precision", "recall"):
                    self.assertNotIn(clave, resultado)

    def test_dos_predicciones_de_la_primera_ocurrencia(self):
        caso = next(item for item in self.data["puntuaciones"] if item["id"] == "E3")
        resultado = evaluar(caso["texto"], caso["gold"], caso["predicciones"])
        self.assertEqual(resultado["tp"], 1)
        self.assertEqual(resultado["fp"], 1)
        self.assertEqual(resultado["fn"], 1)

    def test_una_prediccion_de_cada_ocurrencia(self):
        caso = next(item for item in self.data["puntuaciones"] if item["id"] == "E4")
        resultado = evaluar(caso["texto"], caso["gold"], caso["predicciones"])
        self.assertEqual(resultado["tp"], 2)
        self.assertEqual(resultado["fp"], 0)
        self.assertEqual(resultado["fn"], 0)


if __name__ == "__main__":
    unittest.main()
