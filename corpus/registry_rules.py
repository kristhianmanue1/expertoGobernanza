"""Reglas de vigencia del registry (R1-E1-04 / fuentes-legal-mx.md §4.2).

Validación pura sobre dicts (stdlib). No marca verdad jurídica: solo estructura
post-adversarial F1–F5 para impedir `vigencia_verificada: true` incompleto.
"""
from __future__ import annotations

ALCANCE_OK = frozenset({"instrumento", "articulo", "parrafo"})


def validate_fuente(fuente: dict) -> list[str]:
    """Devuelve lista de errores; vacía si la fuente es estructuralmente OK."""
    errs: list[str] = []
    fid = fuente.get("id") or "?"
    if not fuente.get("vigencia_verificada"):
        return errs

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
        elif isinstance(cubre, list) and len(cubre) > 0:
            any_cover = True
        if t.get("no_cubre_slice") is True:
            any_explicit_no_slice = True

    if not any_cover and not any_explicit_no_slice:
        errs.append(
            f"{fid}: ninguna traza cubre disposiciones ni declara no_cubre_slice"
        )

    rev = fuente.get("revision_vigencia") or {}
    if not isinstance(rev, dict) or not rev.get("revisado_por") or not rev.get("fecha"):
        errs.append(f"{fid}: falta revision_vigencia.revisado_por/fecha (F5)")

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
