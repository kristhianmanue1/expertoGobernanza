"""Spike reversible: exporta una sola disposición a Akoma Ntoso 1.0."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "corpus/derived/lss/LSS-005.json"
REGISTRY = ROOT / "corpus/registry.yaml"
EXPECTED_XML = ROOT / "interop/akn/lss-005.akn.xml"
XSD_PATH = ROOT / "interop/akn/schema/akomantoso30.xsd"
XSD_SHA256 = "6f61fe84cbb6f8cb0e8418cd67b74a63da9990e6573b5a3491f623184f45c4fd"
XML_XSD_SHA256 = "61960fb3131e38022caad5360e2f33a3382578ab3c80cd58bd74320ede61b20c"

AKN = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
SCHEMA_URL = ("https://docs.oasis-open.org/legaldocml/akn-core/v1.0/"
              "os/part2-specs/schemas/akomantoso30.xsd")

ET.register_namespace("", AKN)
ET.register_namespace("xsi", XSI)


def _q(name: str) -> str:
    return f"{{{AKN}}}{name}"


def _add(parent: ET.Element, element_name: str, **attributes: str) -> ET.Element:
    return ET.SubElement(parent, _q(element_name), attributes)


def load_source(path: pathlib.Path = SOURCE) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_lss_registry_metadata(path: pathlib.Path = REGISTRY) -> dict:
    text = path.read_text(encoding="utf-8")
    start = text.index("\n  - id: LSS\n")
    end = text.find("\n  - id:", start + 1)
    block = text[start:end if end != -1 else None]
    publication = re.search(r'fecha_publicacion_dof: "(\d{4}-\d{2}-\d{2})"', block)
    authority = re.search(r'autoridad: "([^"]+)"', block)
    pattern = r'ultima_reforma_cuerpo:\n\s+fecha: "(\d{4}-\d{2}-\d{2})"'
    body_version = re.search(pattern, block)
    if publication is None or authority is None or body_version is None:
        raise ValueError("metadatos LSS incompletos en registry")
    return {"publication_date": publication.group(1), "authority": authority.group(1), "body_version": body_version.group(1)}


def body_version_date(model: dict) -> str:
    note = model["vigencia"]["nota_cuerpo"]
    match = re.search(r"ultima_reforma_cuerpo (\d{4}-\d{2}-\d{2})", note)
    if match is None:
        raise ValueError("nota_cuerpo sin fecha de versión")
    return match.group(1)


def build_akn_portion(model: dict) -> ET.Element:
    disposition_id = model["disposicion_id"]
    text = model["texto_verbatim"]
    article_number = model["jerarquia_documental"]["articulo"].rstrip(".")
    registry = load_lss_registry_metadata()
    work = f"/akn/mx/act/{registry['publication_date']}/lss"
    body_version = registry["body_version"]
    if body_version_date(model) != body_version:
        raise ValueError("versión de cuerpo divergente entre registry y JSON")
    disposition_amendment = model["vigencia"]["ultima_reforma_dof_declarada"]
    expression = f"{work}/spa@{body_version}"

    root = ET.Element(_q("akomaNtoso"), {f"{{{XSI}}}schemaLocation": f"{AKN} {SCHEMA_URL}"})
    portion = _add(root, "portion", includedIn="#lss")
    meta = _add(portion, "meta")
    identification = _add(meta, "identification", source="#codex")

    frbr_work = _add(identification, "FRBRWork")
    _add(frbr_work, "FRBRthis", value=f"{work}/!main~art_5")
    _add(frbr_work, "FRBRuri", value=work)
    _add(frbr_work, "FRBRalias", value=disposition_id, name="internal-disposition-id")
    _add(frbr_work, "FRBRalias", value=model["instrumento"]["id"], name="internal-instrument-id")
    _add(frbr_work, "FRBRdate", date=registry["publication_date"], name="enactment")
    _add(frbr_work, "FRBRauthor", href="#congreso", **{"as": "#author"})
    _add(frbr_work, "FRBRcountry", value="mx")
    _add(frbr_work, "FRBRname", value="lss")
    _add(frbr_work, "FRBRprescriptive", value="true")

    frbr_expression = _add(identification, "FRBRExpression")
    _add(frbr_expression, "FRBRthis", value=f"{expression}/!main~art_5")
    _add(frbr_expression, "FRBRuri", value=expression)
    _add(frbr_expression, "FRBRalias", value=disposition_id, name="internal-disposition-id")
    _add(frbr_expression, "FRBRdate", date=body_version, name="version")
    _add(
        frbr_expression,
        "FRBRdate",
        date=disposition_amendment,
        name="last-amendment-of-portion",
    )
    _add(frbr_expression, "FRBRauthor", href="#camara", **{"as": "#editor"})
    _add(frbr_expression, "FRBRauthoritative", value="false")
    _add(frbr_expression, "FRBRlanguage", language="spa")

    frbr_manifestation = _add(identification, "FRBRManifestation")
    _add(frbr_manifestation, "FRBRthis", value=f"{expression}/!main~art_5.xml")
    _add(frbr_manifestation, "FRBRuri", value=f"{expression}.xml")
    _add(frbr_manifestation, "FRBRdate", date="2026-08-10", name="generation")
    _add(frbr_manifestation, "FRBRauthor", href="#codex", **{"as": "#editor"})
    _add(frbr_manifestation, "FRBRportion", **{"from": "#art_5"})
    _add(frbr_manifestation, "FRBRformat", value="xml")

    references = _add(meta, "references", source="#codex")
    _add(
        references,
        "original",
        eId="lss",
        href=work,
        showAs=model["instrumento"]["nombre_oficial"],
    )
    _add(
        references,
        "TLCOrganization",
        eId="congreso",
        href="/akn/ontology/organization/mx/congreso-union",
        showAs=registry["authority"],
    )
    _add(
        references,
        "TLCOrganization",
        eId="camara",
        href="/akn/ontology/organization/mx/camara-diputados",
        showAs="Cámara de Diputados",
    )
    _add(
        references,
        "TLCOrganization",
        eId="codex",
        href="/akn/ontology/organization/eg/openai-codex",
        showAs="OpenAI Codex — conversión no autoritativa",
    )
    _add(references, "TLCRole", eId="author", href="/akn/ontology/role/author", showAs="Autor")
    _add(references, "TLCRole", eId="editor", href="/akn/ontology/role/editor", showAs="Editor")

    body = _add(portion, "portionBody")
    article = _add(body, "article", eId="art_5")
    num = _add(article, "num")
    num.text = f"Artículo {article_number}."
    content = _add(article, "content", eId="art_5__content")
    paragraph = _add(content, "p")
    paragraph.text = text
    return root


def render_akn_portion(model: dict) -> str:
    root = build_akn_portion(model)
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode() + "\n"


def akn_to_model_subset(xml_text: str) -> dict:
    root = ET.fromstring(xml_text)
    alias = root.find(".//akn:FRBRalias[@name='internal-disposition-id']", {"akn": AKN})
    article = root.find(".//akn:article", {"akn": AKN})
    number = root.findtext(".//akn:article/akn:num", namespaces={"akn": AKN})
    text = root.findtext(".//akn:article/akn:content/akn:p", namespaces={"akn": AKN})
    instrument_alias = root.find(
        ".//akn:FRBRWork/akn:FRBRalias[@name='internal-instrument-id']",
        {"akn": AKN},
    )
    if alias is None or article is None or instrument_alias is None or text is None:
        raise ValueError("XML AKN incompleto para roundtrip")
    article_value = (number or "").removeprefix("Artículo ")
    return {
        "disposicion_id": alias.attrib["value"],
        "instrumento": {"id": instrument_alias.attrib["value"]},
        "jerarquia_documental": {"articulo": article_value},
        "texto_verbatim": text,
    }


def validate_xsd(xml_path: pathlib.Path, xsd_path: pathlib.Path) -> dict:
    actual_xsd_hash = hashlib.sha256(xsd_path.read_bytes()).hexdigest()
    xml_xsd_hash = hashlib.sha256((xsd_path.parent / "xml.xsd").read_bytes()).hexdigest()
    completed = subprocess.run(
        ["xmllint", "--noout", "--schema", str(xsd_path), str(xml_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "xsd_hash_matches": actual_xsd_hash == XSD_SHA256 and xml_xsd_hash == XML_XSD_SHA256,
        "xml_valid": completed.returncode == 0,
        "stderr": completed.stderr.strip(),
    }


def check(
    xml_path: pathlib.Path = EXPECTED_XML,
    xsd_path: pathlib.Path | None = None,
) -> dict:
    source = load_source()
    expected = render_akn_portion(source)
    actual = xml_path.read_text(encoding="utf-8")
    recovered = akn_to_model_subset(actual)
    source_text = source["texto_verbatim"]
    expected_subset = {
        "disposicion_id": source["disposicion_id"],
        "instrumento": {"id": source["instrumento"]["id"]},
        "jerarquia_documental": {
            "articulo": source["jerarquia_documental"]["articulo"]
        },
        "texto_verbatim": source_text,
    }
    assertions = {
        "deterministic_xml": actual == expected,
        "model_subset_roundtrip": recovered == expected_subset,
        "text_sha256": hashlib.sha256(recovered["texto_verbatim"].encode("utf-8")).hexdigest()
        == hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
    }
    xsd = validate_xsd(xml_path, xsd_path) if xsd_path is not None else None
    if xsd is not None:
        assertions["xsd_hash"] = xsd["xsd_hash_matches"]
        assertions["xsd_valid"] = xsd["xml_valid"]
    return {
        "schema": "akn-lss5-spike-result/v1",
        "passed": all(assertions.values()),
        "assertions": assertions,
        "xml_sha256": hashlib.sha256(actual.encode("utf-8")).hexdigest(),
        "roundtrip": recovered,
        "xsd": xsd,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=pathlib.Path, default=EXPECTED_XML)
    parser.add_argument("--xsd", type=pathlib.Path, default=XSD_PATH)
    args = parser.parse_args()
    report = check(args.check, args.xsd)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
