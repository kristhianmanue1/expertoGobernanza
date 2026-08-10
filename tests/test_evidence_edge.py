"""Contrato y regresiones anti-promoción de EvidenceEdge v0."""
import copy
from datetime import date
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from corpus.evidence_edge import is_traversable, validate_evidence_edge


def _edge_verified():
    return {
        "schema_version": "evidence-edge/v0",
        "edge_id": "LSS:5|define_naturaleza|IMSS",
        "subject": {"id": "LSS:5", "kind": "disposicion"},
        "predicate": "define_naturaleza",
        "object": {"id": "IMSS", "kind": "entidad"},
        "claim_class": "textual",
        "evidence": {
            "quote": "organismo público descentralizado con personalidad jurídica",
            "source_ref": "corpus/derived/lss/LSS-005.json",
            "source_document_sha256": (
                "8a28a16e1dce1f8e666f4cce5ed19745bc912b2ab1ca49787d5d4bef229398ed"
            ),
        },
        "evidence_scope": {
            "source_level": 2,
            "source_granularity": "articulo",
            "source_disposition_id": "LSS:5",
            "covers_subject": True,
            "covers_object": True,
            "covers_relation": True,
        },
        "validity": {
            "source_disposition_id": "LSS:5",
            "trace_date": "2001-12-20",
            "trace_source_level": 1,
            "identificadores_diario": "DOF 20-12-2001 reforma Art.5 LSS",
            "trace_url": None,
            "trace_covers_disposition": True,
        },
        "verification": {
            "status": "verified",
            "reviewed_by": "Kristhian Manuel Jiménez",
            "reviewed_at": "2026-08-10",
            "reason": "F5 explícito de LSS:5; relación cubierta por el texto citado",
        },
        "inheritance": "prohibited",
        "gate_version": "evidence-edge-gate/v0",
    }


class TestEvidenceEdgeV0(unittest.TestCase):
    def test_verified_completo_es_recorrible(self):
        edge = _edge_verified()
        self.assertEqual(validate_evidence_edge(edge), [])
        self.assertTrue(is_traversable(edge))

    def test_f5_cerrado_no_promueve_remision_interpretativa(self):
        edge = _edge_verified()
        edge["edge_id"] = "LFEP:5|remite_a_ley_especifica|LSS"
        edge["subject"] = {"id": "LFEP:5", "kind": "disposicion"}
        edge["predicate"] = "remite_a_ley_especifica"
        edge["object"] = {"id": "LSS", "kind": "instrumento"}
        edge["claim_class"] = "remision_normativa"
        edge["evidence_scope"]["source_disposition_id"] = "LFEP:5"
        edge["evidence_scope"]["covers_object"] = False
        edge["evidence_scope"]["covers_relation"] = False
        edge["validity"] = {
            "source_disposition_id": "LFEP:5",
            "trace_date": "2025-07-16",
            "trace_source_level": 1,
            "identificadores_diario": "DOF 16-07-2025 codigo=5763164",
            "trace_url": "https://www.dof.gob.mx/nota_detalle.php?codigo=5763164",
            "trace_covers_disposition": True,
        }
        edge["verification"] = {
            "status": "disputed",
            "reviewed_by": "Kristhian Manuel Jiménez",
            "reviewed_at": "2026-08-10",
            "reason": "F5 cerrado; el texto no nombra la LSS",
        }
        self.assertEqual(validate_evidence_edge(edge), [])
        self.assertFalse(is_traversable(edge))

    def test_clase_desconocida_falla_cerrado(self):
        edge = _edge_verified()
        edge["claim_class"] = "parece_relacionado"
        self.assertTrue(any("claim_class" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_estado_desconocido_falla_cerrado(self):
        edge = _edge_verified()
        edge["verification"]["status"] = "probably_verified"
        self.assertTrue(any("status" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_inheritance_distinto_de_prohibited_falla(self):
        edge = _edge_verified()
        edge["inheritance"] = "from_subject"
        self.assertTrue(any("inheritance" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_verified_sin_cobertura_relacion_falla(self):
        edge = _edge_verified()
        edge["evidence_scope"]["covers_relation"] = False
        self.assertTrue(any("cobertura" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_verified_sin_cobertura_objeto_falla(self):
        edge = _edge_verified()
        edge["evidence_scope"]["covers_object"] = False
        self.assertTrue(any("cobertura" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_verified_not_applicable_no_elude_cobertura_objeto(self):
        edge = _edge_verified()
        edge["evidence_scope"]["covers_object"] = "not_applicable"
        self.assertTrue(any("cobertura" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_verified_rechaza_evidencia_nivel_cuatro(self):
        edge = _edge_verified()
        edge["evidence_scope"]["source_level"] = 4
        self.assertTrue(any("evidencia nivel" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_verified_rechaza_alcance_instrumento(self):
        edge = _edge_verified()
        edge["evidence_scope"]["source_granularity"] = "instrumento"
        self.assertTrue(any("alcance de disposición" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_verified_no_hereda_traza_nivel_dos(self):
        edge = _edge_verified()
        edge["validity"]["trace_source_level"] = 2
        self.assertTrue(any("traza nivel 1" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_verified_exige_revision(self):
        edge = _edge_verified()
        edge["verification"]["reviewed_by"] = None
        edge["verification"]["reviewed_at"] = None
        self.assertTrue(any("revisión explícita" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_verified_rechaza_revision_anterior_a_traza(self):
        edge = _edge_verified()
        edge["verification"]["reviewed_at"] = "2000-01-01"
        self.assertTrue(any("anterior a la traza" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_verified_rechaza_revision_futura(self):
        edge = _edge_verified()
        edge["verification"]["reviewed_at"] = "9999-01-01"
        self.assertTrue(any("no puede ser futura" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_fecha_de_evaluacion_inyectada_hace_determinista_el_gate(self):
        edge = _edge_verified()
        edge["verification"]["reviewed_at"] = "2026-08-10"
        as_of = date(2026, 8, 9)
        self.assertTrue(any(
            "no puede ser futura" in error
            for error in validate_evidence_edge(edge, as_of)
        ))
        self.assertFalse(is_traversable(edge, as_of))

    def test_disposicion_temporal_distinta_falla(self):
        edge = _edge_verified()
        edge["validity"]["source_disposition_id"] = "LSS:1"
        errors = validate_evidence_edge(edge)
        self.assertTrue(any("no coinciden" in e for e in errors))
        self.assertFalse(is_traversable(edge))

    def test_subject_disposicion_distinto_de_scope_falla(self):
        edge = _edge_verified()
        edge["evidence_scope"]["source_disposition_id"] = "LSS:1"
        edge["validity"]["source_disposition_id"] = "LSS:1"
        errors = validate_evidence_edge(edge)
        self.assertTrue(any("subject disposición" in e for e in errors))
        self.assertFalse(is_traversable(edge))

    def test_verified_no_promueve_disposicion_a_instrumento(self):
        edge = _edge_verified()
        edge["subject"] = {"id": "LSS", "kind": "instrumento"}
        edge["edge_id"] = "LSS|define_naturaleza|IMSS"
        errors = validate_evidence_edge(edge)
        self.assertTrue(any("verified exige subject disposición" in e for e in errors))
        self.assertFalse(is_traversable(edge))

    def test_interpretacion_verificada_no_es_recorrible_en_v0(self):
        edge = _edge_verified()
        edge["claim_class"] = "jerarquia_interpretativa"
        self.assertEqual(validate_evidence_edge(edge), [])
        self.assertFalse(is_traversable(edge))

    def test_edge_id_se_deriva_de_tripleta(self):
        edge = _edge_verified()
        edge["edge_id"] = "arista-opaca"
        self.assertTrue(any("edge_id" in e for e in validate_evidence_edge(edge)))

    def test_node_id_no_admite_delimitador_de_edge(self):
        edge = _edge_verified()
        edge["object"]["id"] = "IMSS|otra_arista"
        edge["edge_id"] = "LSS:5|define_naturaleza|IMSS|otra_arista"
        self.assertTrue(any("object.id" in e for e in validate_evidence_edge(edge)))

    def test_campos_extra_fallan_cerrado(self):
        edge = _edge_verified()
        edge["vigencia_verificada"] = True
        errors = validate_evidence_edge(edge)
        self.assertTrue(any("campos desconocidos" in e for e in errors))
        self.assertFalse(is_traversable(edge))

    def test_source_ref_no_admite_traversal(self):
        edge = _edge_verified()
        edge["evidence"]["source_ref"] = "../secretos.txt"
        self.assertTrue(any("ruta relativa segura" in e for e in validate_evidence_edge(edge)))

    def test_fechas_imposibles_fallan(self):
        edge = _edge_verified()
        edge["validity"]["trace_date"] = "2026-99-40"
        self.assertTrue(any("trace_date" in e for e in validate_evidence_edge(edge)))

    def test_verified_acepta_url_dof_como_alternativa_a_identificador(self):
        edge = _edge_verified()
        edge["validity"]["identificadores_diario"] = None
        edge["validity"]["trace_url"] = "https://dof.gob.mx/nota_detalle.php?x=1"
        self.assertEqual(validate_evidence_edge(edge), [])
        self.assertTrue(is_traversable(edge))

    def test_verified_rechaza_url_sin_host(self):
        edge = _edge_verified()
        edge["validity"]["identificadores_diario"] = None
        edge["validity"]["trace_url"] = "https://"
        self.assertTrue(any("trace_url" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_verified_rechaza_url_http(self):
        edge = _edge_verified()
        edge["validity"]["identificadores_diario"] = None
        edge["validity"]["trace_url"] = "http://dof.gob.mx/nota"
        self.assertTrue(any("trace_url" in e for e in validate_evidence_edge(edge)))
        self.assertFalse(is_traversable(edge))

    def test_tipos_json_malformados_no_lanzan_excepcion(self):
        edge = _edge_verified()
        edge["claim_class"] = []
        edge["verification"]["status"] = {}
        edge["subject"]["kind"] = []
        edge["evidence_scope"]["source_granularity"] = []
        errors = validate_evidence_edge(edge)
        self.assertTrue(any("claim_class" in e for e in errors))
        self.assertTrue(any("verification.status" in e for e in errors))
        self.assertTrue(any("subject.kind" in e for e in errors))
        self.assertTrue(any("source_granularity" in e for e in errors))
        self.assertFalse(is_traversable(edge))

    def test_raiz_no_objeto_falla_sin_excepcion(self):
        self.assertEqual(validate_evidence_edge([]), ["edge: debe ser objeto"])

    def test_no_muta_entrada(self):
        edge = _edge_verified()
        before = copy.deepcopy(edge)
        validate_evidence_edge(edge)
        self.assertEqual(edge, before)


if __name__ == "__main__":
    unittest.main()
