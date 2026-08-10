"""Contrato del spike Akoma Ntoso sobre LSS:5."""
import hashlib
import pathlib
import unittest
import xml.etree.ElementTree as ET

from scripts.akn_spike import (
    AKN,
    EXPECTED_XML,
    XSD_PATH,
    body_version_date,
    check,
    load_lss_registry_metadata,
    load_source,
    render_akn_portion,
    validate_xsd,
)


class TestAkomaNtosoSpike(unittest.TestCase):
    def test_xml_versionado_es_determinista(self):
        source = load_source()
        actual = EXPECTED_XML.read_text(encoding="utf-8")
        self.assertEqual(actual, render_akn_portion(source))
        self.assertEqual(actual, render_akn_portion(source))

    def test_roundtrip_conserva_subconjunto_y_hash(self):
        report = check()
        self.assertTrue(report["passed"])
        self.assertTrue(all(report["assertions"].values()))
        source_text = load_source()["texto_verbatim"]
        recovered_hash = hashlib.sha256(
            report["roundtrip"]["texto_verbatim"].encode("utf-8")
        ).hexdigest()
        self.assertEqual(recovered_hash, hashlib.sha256(source_text.encode("utf-8")).hexdigest())

    def test_expression_declara_conversion_no_autoritativa(self):
        root = ET.parse(EXPECTED_XML).getroot()
        expression_flag = root.find(
            ".//akn:FRBRExpression/akn:FRBRauthoritative",
            {"akn": AKN},
        )
        work_flag = root.find(".//akn:FRBRWork/akn:FRBRauthoritative", {"akn": AKN})
        self.assertEqual(expression_flag.attrib["value"], "false")
        self.assertIsNone(work_flag)

    def test_xml_valida_con_xsd_oficial_pinneado(self):
        result = validate_xsd(EXPECTED_XML, XSD_PATH)
        self.assertTrue(result["xsd_hash_matches"])
        self.assertTrue(result["xml_valid"], result["stderr"])

    def test_no_exporta_relaciones_interpretativas(self):
        xml = EXPECTED_XML.read_text(encoding="utf-8")
        self.assertNotIn("integra_regimen", xml)
        self.assertNotIn("relaciona_con", xml)
        self.assertNotIn("jerarquia_interpretativa", xml)

    def test_spike_permanece_en_una_disposicion(self):
        root = ET.parse(EXPECTED_XML).getroot()
        articles = root.findall(".//akn:article", {"akn": AKN})
        self.assertEqual(len(articles), 1)
        self.assertNotIn("GUID=", EXPECTED_XML.read_text(encoding="utf-8"))

    def test_fechas_y_autoridad_derivan_de_fuentes_locales(self):
        root = ET.parse(EXPECTED_XML).getroot()
        source = load_source()
        registry = load_lss_registry_metadata()
        work_date = root.find(".//akn:FRBRWork/akn:FRBRdate", {"akn": AKN})
        expression_uri = root.find(".//akn:FRBRExpression/akn:FRBRuri", {"akn": AKN})
        original = root.find(".//akn:references/akn:original", {"akn": AKN})
        congress = root.find(".//akn:TLCOrganization[@eId='congreso']", {"akn": AKN})
        portion = root.find(".//akn:portion", {"akn": AKN})
        work = f"/akn/mx/act/{registry['publication_date']}/lss"
        self.assertEqual(work_date.attrib["date"], registry["publication_date"])
        self.assertEqual(body_version_date(source), registry["body_version"])
        self.assertIn(registry["body_version"], expression_uri.attrib["value"])
        self.assertEqual(original.attrib["href"], work)
        self.assertEqual(portion.attrib["includedIn"], "#lss")
        self.assertEqual(congress.attrib["showAs"], registry["authority"])


if __name__ == "__main__":
    unittest.main()
