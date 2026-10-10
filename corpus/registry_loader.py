"""Carga registry.yaml sin colapsar claves duplicadas."""
from __future__ import annotations

import pathlib

from corpus.registry_rules import validate_registry

BANNER_NO = "CORPUS_VIGENCIA_NO_VERIFICADA"
BANNER_OK = "CORPUS_VIGENCIA_PARCIAL_O_OK"
REGISTRY = pathlib.Path(__file__).resolve().parent / "registry.yaml"


class RegistryLoadError(ValueError):
    """Error estructural o de validación. No es evidencia de vigencia."""


def _require_yaml():
    try:
        import yaml
    except ImportError as exc:
        raise RegistryLoadError(
            "falta PyYAML; instale el pin de requirements.txt"
        ) from exc
    return yaml


def _unique_loader(yaml):
    class UniqueKeyLoader(yaml.SafeLoader):
        pass

    def construct(loader, node):
        loader.flatten_mapping(node)
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=False)
            if key in mapping:
                raise RegistryLoadError(f"clave duplicada: {key!r}")
            mapping[key] = loader.construct_object(value_node, deep=False)
        return mapping

    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct
    )
    return UniqueKeyLoader


def load_registry(path: pathlib.Path | str) -> dict:
    yaml = _require_yaml()
    text = pathlib.Path(path).read_text(encoding="utf-8")
    doc = yaml.load(text, Loader=_unique_loader(yaml))
    if not isinstance(doc, dict) or not isinstance(doc.get("fuentes"), list):
        raise RegistryLoadError("registry: se exige mapping con lista fuentes")
    seen = set()
    for fuente in doc["fuentes"]:
        if not isinstance(fuente, dict):
            raise RegistryLoadError("fuente no es mapping")
        fid = fuente.get("id")
        if not isinstance(fid, str) or not fid.strip():
            raise RegistryLoadError("id de fuente vacío o ausente")
        if fid in seen:
            raise RegistryLoadError(f"id de fuente duplicado: {fid}")
        seen.add(fid)
    errors = validate_registry(doc)
    if errors:
        raise RegistryLoadError("validate_registry: " + "; ".join(errors))
    return doc


def fuente_por_instrumento(doc: dict, instrumento_id: str) -> dict | None:
    if not isinstance(doc, dict):
        return None
    for fuente in doc.get("fuentes") or []:
        if isinstance(fuente, dict) and fuente.get("id") == instrumento_id:
            return fuente
    return None


def corpus_vigencia_banner(registry_path: pathlib.Path = REGISTRY) -> str:
    if not pathlib.Path(registry_path).is_file():
        return BANNER_NO
    load_registry(registry_path)
    # R1 sólo comprueba procedencia histórica; no habilita vigencia actual.
    return BANNER_NO
