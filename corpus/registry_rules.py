"""Reglas de vigencia del registry (R1-E1-04 / fuentes-legal-mx.md §4.2).

Validación pura sobre dicts (stdlib). F1–F5 acreditan procedencia primaria;
la vigencia actual permanece no verificada hasta un contrato temporal propio.
"""
from __future__ import annotations

ALCANCE_OK = frozenset({"instrumento", "articulo", "parrafo"})
ALCANCE_DISPOSICION_OK = frozenset({"articulo", "parrafo"})


def _resultado_vigencia(
    disposicion_id: str, verificada: bool, fuente: str, razon: str
) -> dict:
    return {
        "disposicion_id": disposicion_id,
        "verificada": verificada,
        "fuente": fuente,
        "razon": razon,
    }


def resolve_disposicion_procedencia(fuente: dict, disposicion_id: str) -> dict:
    """Resuelve sólo la procedencia primaria de una disposición.

    El campo nuevo de procedencia debe estar explícito; el legado
    ``vigencia_verificada`` no puede acreditar procedencia. Si existe
    ``traza_disposiciones``, esa tabla es autoritativa y no se hace fallback a
    trazas más generales cuando falta una entrada o su F5 es falso.
    """
    if not isinstance(disposicion_id, str) or not disposicion_id.strip():
        return _resultado_vigencia("", False, "ninguna", "disposicion_id_invalido")

    if not isinstance(fuente, dict):
        return _resultado_vigencia(
            disposicion_id, False, "ninguna", "fuente_invalida"
        )

    if fuente.get("procedencia_primaria_verificada") is not True:
        return _resultado_vigencia(
            disposicion_id, False, "instrumento", "procedencia_no_verificada"
        )

    revision = fuente.get("revision_procedencia") or {}
    revision_ok = (
        isinstance(revision, dict)
        and bool(revision.get("revisado_por"))
        and bool(revision.get("fecha"))
    )
    trazas_disposicion = fuente.get("traza_disposiciones")
    if trazas_disposicion is not None:
        if not isinstance(trazas_disposicion, list):
            return _resultado_vigencia(
                disposicion_id, False, "traza_disposiciones", "tabla_invalida"
            )
        coincidencias = [
            traza
            for traza in trazas_disposicion
            if isinstance(traza, dict)
            and traza.get("disposicion_id") == disposicion_id
        ]
        if len(coincidencias) > 1:
            return _resultado_vigencia(
                disposicion_id,
                False,
                "traza_disposiciones",
                "traza_duplicada",
            )
        if not coincidencias:
            return _resultado_vigencia(
                disposicion_id,
                False,
                "traza_disposiciones",
                "sin_traza_explicita",
            )
        traza = coincidencias[0]
        if (
            traza.get("f5") is True
            and traza.get("cubre_disposicion") is True
            and traza.get("fecha")
            and (traza.get("url") or traza.get("identificadores_diario"))
            and revision_ok
        ):
            return _resultado_vigencia(
                disposicion_id, True, "traza_disposiciones", "f5_explicito"
            )
        return _resultado_vigencia(
            disposicion_id,
            False,
            "traza_disposiciones",
            "f5_no_verificado",
        )

    principal = fuente.get("traza_disposicion_principal") or {}
    if isinstance(principal, dict) and principal.get("disposicion_id") == disposicion_id:
        if (
            principal.get("cubre_disposicion") is True
            and principal.get("fecha")
            and (principal.get("url") or principal.get("identificadores_diario"))
            and revision_ok
        ):
            return _resultado_vigencia(
                disposicion_id,
                True,
                "traza_disposicion_principal",
                "traza_exacta_con_revision",
            )
        return _resultado_vigencia(
            disposicion_id,
            False,
            "traza_disposicion_principal",
            "traza_principal_incompleta",
        )

    matched_publication = False
    for traza in fuente.get("trazas_publicacion") or []:
        if not isinstance(traza, dict):
            continue
        cubre = traza.get("cubre_disposiciones")
        if not isinstance(cubre, list) or disposicion_id not in cubre:
            continue
        matched_publication = True
        if (
            traza.get("alcance") in ALCANCE_DISPOSICION_OK
            and (traza.get("url") or traza.get("identificadores_diario"))
            and revision_ok
        ):
            return _resultado_vigencia(
                disposicion_id,
                True,
                "trazas_publicacion",
                "traza_exacta_con_revision",
            )
    if matched_publication:
        return _resultado_vigencia(
            disposicion_id,
            False,
            "trazas_publicacion",
            "traza_publicacion_incompleta",
        )

    return _resultado_vigencia(
        disposicion_id, False, "ninguna", "sin_traza_explicita"
    )


def resolve_disposicion_vigencia(fuente: dict, disposicion_id: str) -> dict:
    """Separa procedencia histórica y vigencia actual; ésta falla cerrado.

    R1 no tiene contrato temporal para acreditar vigencia actual. Una traza
    histórica exacta, incluso con F5, no puede convertirla en ``verificada``.
    """
    procedencia = resolve_disposicion_procedencia(fuente, disposicion_id)
    estado_presente = isinstance(fuente, dict) and "vigencia_actual_estado" in fuente
    estado = fuente.get("vigencia_actual_estado") if estado_presente else None
    if estado == "no_verificada":
        razon = "vigencia_actual_no_verificada"
    elif not estado_presente:
        razon = "vigencia_actual_estado_ausente"
    else:
        razon = "vigencia_actual_estado_no_admitido"
    return {
        "disposicion_id": procedencia["disposicion_id"],
        "verificada": False,
        "fuente": "ninguna",
        "razon": razon,
        "vigencia_actual_estado": estado if estado == "no_verificada" else None,
        "vigencia_actual_estado_valido": estado == "no_verificada",
        "procedencia_primaria_verificada": procedencia["verificada"],
        "procedencia_fuente": procedencia["fuente"],
        "procedencia_razon": procedencia["razon"],
    }


def validate_fuente(fuente: dict) -> list[str]:
    """Devuelve lista de errores; vacía si la fuente es estructuralmente OK."""
    errs: list[str] = []
    fid = fuente.get("id") or "?"
    legado = fuente.get("vigencia_verificada")
    if legado is not None and not isinstance(legado, bool):
        return [f"{fid}: vigencia_verificada exige booleano"]
    if legado is True:
        errs.append(f"{fid}: vigencia_verificada legado no puede ser true")
    if "procedencia_primaria_verificada" not in fuente:
        errs.append(f"{fid}: falta procedencia_primaria_verificada")
    if fuente.get("vigencia_actual_estado") != "no_verificada":
        errs.append(f"{fid}: vigencia_actual_estado debe ser no_verificada en R1")
    vigencia = fuente.get("procedencia_primaria_verificada", legado)
    if vigencia is False or vigencia is None:
        return errs
    if vigencia is not True:
        return errs + [f"{fid}: procedencia_primaria_verificada exige booleano"]

    trazas = fuente.get("trazas_publicacion") or []
    url1 = fuente.get("url_dof_nivel1")
    if not trazas and not url1:
        errs.append(f"{fid}: vigencia true sin trazas_publicacion ni url_dof_nivel1")
        return errs

    if not trazas and url1:
        errs.append(
            f"{fid}: vigencia true con solo url_dof_nivel1; exige trazas_publicacion "
            "con alcance y cubre_disposiciones (F2)"
        )
        return errs

    any_cover = False
    any_explicit_no_slice = False
    for i, t in enumerate(trazas):
        if not isinstance(t, dict):
            errs.append(f"{fid}: traza[{i}] no es objeto")
            continue
        pref = f"{fid}: traza[{i}]"
        if not (t.get("url") or t.get("identificadores_diario")):
            errs.append(f"{pref}: falta url o identificadores_diario (M8)")
        alc = t.get("alcance")
        if alc not in ALCANCE_OK:
            errs.append(f"{pref}: alcance inválido o ausente {alc!r}")
        cubre = t.get("cubre_disposiciones")
        if cubre is None and "no_cubre_slice" not in t:
            errs.append(f"{pref}: falta cubre_disposiciones o no_cubre_slice")
        elif cubre is not None:
            if not isinstance(cubre, list):
                errs.append(f"{pref}: cubre_disposiciones debe ser lista")
            elif len(cubre) > 0:
                any_cover = True
        if t.get("no_cubre_slice") is True:
            any_explicit_no_slice = True

    if not any_cover and not any_explicit_no_slice:
        errs.append(
            f"{fid}: ninguna traza cubre disposiciones ni declara no_cubre_slice"
        )

    rev = fuente.get("revision_procedencia") or {}
    if not isinstance(rev, dict) or not rev.get("revisado_por") or not rev.get("fecha"):
        errs.append(f"{fid}: falta revision_procedencia.revisado_por/fecha (F5)")

    principal = fuente.get("traza_disposicion_principal")
    if principal is not None:
        if not isinstance(principal, dict):
            errs.append(f"{fid}: traza_disposicion_principal no es objeto")
        else:
            if not principal.get("disposicion_id"):
                errs.append(f"{fid}: traza principal sin disposicion_id")
            if principal.get("cubre_disposicion") is not True:
                errs.append(f"{fid}: traza principal no cubre disposición")
            if not principal.get("fecha"):
                errs.append(f"{fid}: traza principal sin fecha")
            if not (principal.get("url") or principal.get("identificadores_diario")):
                errs.append(f"{fid}: traza principal sin url ni identificadores_diario")

    disposiciones = fuente.get("slice_mvp_disposiciones") or []
    detalle = fuente.get("traza_disposiciones")
    por_id = {}
    if detalle is not None:
        if not isinstance(detalle, list):
            errs.append(f"{fid}: traza_disposiciones debe ser lista")
        else:
            duplicados = set()
            for i, traza in enumerate(detalle):
                if not isinstance(traza, dict):
                    errs.append(f"{fid}: traza_disposiciones[{i}] no es objeto")
                    continue
                disposicion_id = traza.get("disposicion_id")
                if not disposicion_id:
                    errs.append(f"{fid}: traza_disposiciones[{i}] sin disposicion_id")
                    continue
                if disposicion_id in por_id:
                    duplicados.add(disposicion_id)
                por_id[disposicion_id] = traza
                if not isinstance(traza.get("f5"), bool):
                    errs.append(f"{fid}: {disposicion_id} sin f5 booleano explícito")
                if not isinstance(traza.get("cubre_disposicion"), bool):
                    errs.append(
                        f"{fid}: {disposicion_id} sin cubre_disposicion booleano"
                    )
                if not traza.get("fecha"):
                    errs.append(f"{fid}: {disposicion_id} sin fecha")
                if not (traza.get("url") or traza.get("identificadores_diario")):
                    errs.append(
                        f"{fid}: {disposicion_id} sin url ni identificadores_diario"
                    )
            for disposicion_id in sorted(duplicados):
                errs.append(f"{fid}: {disposicion_id} duplicada en traza_disposiciones")

    if isinstance(disposiciones, list) and len(disposiciones) > 1:
        if not isinstance(detalle, list):
            errs.append(
                f"{fid}: slice multidisposición exige traza_disposiciones explícita"
            )
        else:
            for disposicion_id in disposiciones:
                traza = por_id.get(disposicion_id)
                if not isinstance(traza, dict):
                    errs.append(f"{fid}: {disposicion_id} sin traza_disposiciones")

    return errs


def validate_registry(doc: dict) -> list[str]:
    errs: list[str] = []
    fuentes = doc.get("fuentes")
    if not isinstance(fuentes, list):
        return ["registry: falta lista fuentes"]
    for f in fuentes:
        if isinstance(f, dict):
            errs.extend(validate_fuente(f))
        else:
            errs.append("registry: entrada fuente no es objeto")
    return errs
