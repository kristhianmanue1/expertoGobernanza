"""Contrato determinista ``EvidenceEdge v0``.

Una arista representa una afirmación completa. Su verificación nunca se hereda
del instrumento, la disposición, el sujeto ni el objeto. El contrato es JSON/YAML
plano y deliberadamente pequeño: no presupone una base de grafos ni Akoma Ntoso.

Este módulo valida la estructura de una atestación; no abre ``source_ref`` ni
recomputa su hash. Sólo ``is_traversable`` habilita consumo bajo esa frontera.
Para devolver ``True`` exige una arista válida, una clase no interpretativa,
``verification.status=verified``, cobertura explícita, evidencia oficial o
institucional y una traza nivel 1 que cubra la disposición fuente concreta. El
estado es un snapshot a ``reviewed_at``: una reforma posterior exige revalidar.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import PurePosixPath
from urllib.parse import urlsplit

SCHEMA_VERSION = "evidence-edge/v0"
GATE_VERSION = "evidence-edge-gate/v0"

CLAIM_CLASSES = frozenset({
    "textual",
    "remision_normativa",
    "jerarquia_interpretativa",
    "vigencia",
    "eficacia",
    "aplicabilidad",
})
TRAVERSABLE_CLAIM_CLASSES = frozenset({
    "textual",
    "remision_normativa",
    "vigencia",
})
VERIFICATION_STATUSES = frozenset({
    "verified",
    "not_verified",
    "disputed",
    "rejected",
})
NODE_KINDS = frozenset({"disposicion", "instrumento", "entidad", "concepto"})
SOURCE_GRANULARITIES = frozenset({"instrumento", "articulo", "parrafo"})

_TOP_KEYS = frozenset({
    "schema_version",
    "edge_id",
    "subject",
    "predicate",
    "object",
    "claim_class",
    "evidence",
    "evidence_scope",
    "validity",
    "verification",
    "inheritance",
    "gate_version",
})
_NODE_KEYS = frozenset({"id", "kind"})
_EVIDENCE_KEYS = frozenset({"quote", "source_ref", "source_document_sha256"})
_SCOPE_KEYS = frozenset({
    "source_level",
    "source_granularity",
    "source_disposition_id",
    "covers_subject",
    "covers_object",
    "covers_relation",
})
_VALIDITY_KEYS = frozenset({
    "source_disposition_id",
    "trace_date",
    "trace_source_level",
    "identificadores_diario",
    "trace_url",
    "trace_covers_disposition",
})
_VERIFICATION_KEYS = frozenset({"status", "reviewed_by", "reviewed_at", "reason"})
_PREDICATE = re.compile(r"[a-z][a-z0-9_]*")
_NODE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9:._-]*")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _keys_exact(value, expected, path, errors):
    if not isinstance(value, dict):
        errors.append(f"{path}: debe ser objeto")
        return False
    actual = set(value)
    missing = sorted(str(key) for key in expected - actual)
    extra = sorted(str(key) for key in actual - expected)
    if missing:
        errors.append(f"{path}: faltan campos {missing}")
    if extra:
        errors.append(f"{path}: campos desconocidos {extra}")
    return not missing and not extra


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _valid_repo_ref(value):
    if not _nonempty(value) or "\\" in value:
        return False
    path = PurePosixPath(value)
    return (
        bool(path.parts)
        and value != "."
        and not path.is_absolute()
        and ".." not in path.parts
    )


def _is_iso_date(value):
    if not isinstance(value, str) or not _ISO_DATE.fullmatch(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _valid_trace_url(value):
    if value is None:
        return True
    if not isinstance(value, str) or any(char.isspace() for char in value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme == "https" and bool(parsed.hostname)
    except ValueError:
        return False


def _validate_node(node, path, errors):
    if not _keys_exact(node, _NODE_KEYS, path, errors):
        return
    if not _nonempty(node["id"]):
        errors.append(f"{path}.id: debe ser texto no vacío")
    elif not _NODE_ID.fullmatch(node["id"]):
        errors.append(f"{path}.id: caracteres no permitidos")
    if not isinstance(node["kind"], str) or node["kind"] not in NODE_KINDS:
        errors.append(f"{path}.kind: valor no reconocido")


def validate_evidence_edge(
    edge: dict, evaluation_date: date | None = None
) -> list[str]:
    """Devuelve errores estables; una lista vacía significa estructura válida."""
    errors: list[str] = []
    as_of = evaluation_date or date.today()
    if not _keys_exact(edge, _TOP_KEYS, "edge", errors):
        return errors

    if edge["schema_version"] != SCHEMA_VERSION:
        errors.append("schema_version: versión no reconocida")
    if edge["gate_version"] != GATE_VERSION:
        errors.append("gate_version: versión no reconocida")
    if edge["inheritance"] != "prohibited":
        errors.append("inheritance: debe ser 'prohibited'")

    _validate_node(edge["subject"], "subject", errors)
    _validate_node(edge["object"], "object", errors)

    predicate = edge["predicate"]
    if not isinstance(predicate, str) or not _PREDICATE.fullmatch(predicate):
        errors.append("predicate: debe usar lower_snake_case")
    if not isinstance(edge["claim_class"], str) or edge["claim_class"] not in CLAIM_CLASSES:
        errors.append("claim_class: valor no reconocido")

    if isinstance(edge["subject"], dict) and isinstance(edge["object"], dict):
        expected_edge_id = (
            f"{edge['subject'].get('id')}|{predicate}|{edge['object'].get('id')}"
        )
        if edge["edge_id"] != expected_edge_id:
            errors.append("edge_id: no coincide con subject|predicate|object")

    evidence = edge["evidence"]
    if _keys_exact(evidence, _EVIDENCE_KEYS, "evidence", errors):
        if not _nonempty(evidence["quote"]):
            errors.append("evidence.quote: debe ser texto no vacío")
        if not _valid_repo_ref(evidence["source_ref"]):
            errors.append("evidence.source_ref: debe ser ruta relativa segura")
        sha256 = evidence["source_document_sha256"]
        if not isinstance(sha256, str) or not _SHA256.fullmatch(sha256):
            errors.append("evidence.source_document_sha256: requiere 64-hex")

    scope = edge["evidence_scope"]
    if _keys_exact(scope, _SCOPE_KEYS, "evidence_scope", errors):
        if (
            type(scope["source_level"]) is not int
            or scope["source_level"] not in range(1, 5)
        ):
            errors.append("evidence_scope.source_level: requiere entero 1..4")
        if (
            not isinstance(scope["source_granularity"], str)
            or scope["source_granularity"] not in SOURCE_GRANULARITIES
        ):
            errors.append("evidence_scope.source_granularity: valor no reconocido")
        if not _nonempty(scope["source_disposition_id"]):
            errors.append("evidence_scope.source_disposition_id: requerido")
        for field in ("covers_subject", "covers_relation"):
            if type(scope[field]) is not bool:
                errors.append(f"evidence_scope.{field}: requiere booleano")
        if (
            type(scope["covers_object"]) is not bool
            and scope["covers_object"] != "not_applicable"
        ):
            errors.append(
                "evidence_scope.covers_object: requiere booleano o 'not_applicable'"
            )

    validity = edge["validity"]
    if _keys_exact(validity, _VALIDITY_KEYS, "validity", errors):
        if not _nonempty(validity["source_disposition_id"]):
            errors.append("validity.source_disposition_id: requerido")
        trace_date = validity["trace_date"]
        if trace_date is not None and not _is_iso_date(trace_date):
            errors.append("validity.trace_date: requiere fecha ISO o null")
        trace_level = validity["trace_source_level"]
        if trace_level is not None and (
            type(trace_level) is not int or trace_level not in range(1, 5)
        ):
            errors.append("validity.trace_source_level: requiere entero 1..4 o null")
        identifiers = validity["identificadores_diario"]
        if identifiers is not None and not _nonempty(identifiers):
            errors.append("validity.identificadores_diario: requiere texto o null")
        if not _valid_trace_url(validity["trace_url"]):
            errors.append("validity.trace_url: requiere URL https con host o null")
        if type(validity["trace_covers_disposition"]) is not bool:
            errors.append("validity.trace_covers_disposition: requiere booleano")

    verification = edge["verification"]
    if _keys_exact(verification, _VERIFICATION_KEYS, "verification", errors):
        status = verification["status"]
        if not isinstance(status, str) or status not in VERIFICATION_STATUSES:
            errors.append("verification.status: valor no reconocido")
        if verification["reviewed_by"] is not None and not _nonempty(
            verification["reviewed_by"]
        ):
            errors.append("verification.reviewed_by: requiere texto o null")
        reviewed_at = verification["reviewed_at"]
        if reviewed_at is not None and not _is_iso_date(reviewed_at):
            errors.append("verification.reviewed_at: requiere fecha ISO o null")
        if not _nonempty(verification["reason"]):
            errors.append("verification.reason: requerido")

        if status == "verified":
            if not _nonempty(verification["reviewed_by"]) or not _is_iso_date(
                verification["reviewed_at"]
            ):
                errors.append("verification: verified exige revisión explícita")
            if isinstance(scope, dict) and (
                scope.get("covers_subject") is not True
                or scope.get("covers_object") is not True
                or scope.get("covers_relation") is not True
            ):
                errors.append(
                    "verification: verified exige cobertura de sujeto, objeto y relación"
                )
            if isinstance(scope, dict) and (
                type(scope.get("source_level")) is not int
                or scope.get("source_level") not in (1, 2)
                or scope.get("source_granularity") not in ("articulo", "parrafo")
            ):
                errors.append(
                    "verification: verified exige evidencia nivel 1/2 y alcance de disposición"
                )
            if isinstance(validity, dict) and (
                validity.get("trace_source_level") != 1
                or validity.get("trace_covers_disposition") is not True
                or not (
                    _nonempty(validity.get("identificadores_diario"))
                    or _valid_trace_url(validity.get("trace_url"))
                    and validity.get("trace_url") is not None
                )
                or not _is_iso_date(validity.get("trace_date"))
            ):
                errors.append(
                    "verification: verified exige traza nivel 1 que cubra la disposición"
                )
            if isinstance(validity, dict) and _is_iso_date(validity.get("trace_date")):
                trace_date = date.fromisoformat(validity["trace_date"])
                reviewed_at = verification.get("reviewed_at")
                if _is_iso_date(reviewed_at):
                    review_date = date.fromisoformat(reviewed_at)
                    if trace_date > review_date:
                        errors.append("verification: revisión anterior a la traza")
                    if review_date > as_of:
                        errors.append("verification: reviewed_at no puede ser futura")

    if isinstance(scope, dict) and isinstance(validity, dict):
        if scope.get("source_disposition_id") != validity.get("source_disposition_id"):
            errors.append("source_disposition_id: scope y validity no coinciden")
        subject = edge["subject"]
        if isinstance(verification, dict) and verification.get("status") == "verified":
            if not isinstance(subject, dict) or subject.get("kind") != "disposicion":
                errors.append("verification: verified exige subject disposición")
            elif subject.get("id") != scope.get("source_disposition_id"):
                errors.append(
                    "source_disposition_id: debe coincidir con subject disposición"
                )

    return errors


def is_traversable(edge: dict, evaluation_date: date | None = None) -> bool:
    """Autoriza sólo clases v0 no interpretativas, validadas y verificadas."""
    if validate_evidence_edge(edge, evaluation_date):
        return False
    return (
        edge["verification"]["status"] == "verified"
        and edge["claim_class"] in TRAVERSABLE_CLAIM_CLASSES
    )
