# Roles operativos R1 (§9) — designación interina

**Estado:** vigente · **Fecha:** 2026-08-10 · **Plan:** `docs/plan-r1-90d.md` (R1-E0-01)  
**Autoridad:** enlace institucional (decisión registrada en sesión de orquestación).  
**No es** nombramiento institucional formal del IMSS ni del Estado; es rol **interno
del repositorio** ExpertoGobernanza hasta designación formal o nueva decisión.

> **Renombrado 2026-08-18** (enmienda promulgación institucional,
> `docs/propuestas/enmienda-promulgacion-institucional.md`): el rol antes llamado
> "humano-promulgador" se llama **enlace institucional**. La promulgación de
> normas es potestad del IMSS (áreas normativas/personal IMSS; RIIMSS art. 6-VI,
> 75-I/IV/XVI); este rol **no promulga** — aporta fuentes, decide criterios
> internos del repo y canaliza hacia la vía institucional cuando proceda.

## Designación

| Rol (§9) | Persona | Carácter | Desde |
|----------|---------|----------|--------|
| Responsable jurídico del corpus | **Kristhian Manuel Jiménez** | Interino | 2026-08-10 |
| Custodio / data steward del corpus | **Kristhian Manuel Jiménez** | Interino | 2026-08-10 |
| Product owner (PO) | **Kristhian Manuel Jiménez** | Interino | 2026-08-10 |

**Fecha límite de revisión de interinato:** 2026-11-10 (90 días desde designación),
o antes si se nombra a otra persona. Al vencer, revalidar o sustituir por escrito
en este archivo (nueva fila + fecha; no borrar historia).

## Alcance de cada rol (recordatorio)

- **Jurídico del corpus:** desempate entre fuentes y lecturas; no es asesoría legal
  a terceros; desempates materiales → ADR-lite + quorum-lite (§6).
- **Custodio:** integridad del corpus (hashes, procedencia, registry, originales
  locales); no promociona vigencia sin evidencia DOF.
- **PO:** priorización del plan R1, criterio de “listo para exterior”, umbrales
  de producto (p. ej. FP del auditor cuando existan mediciones — ver R1-E0-03).

## Prohibiciones

- Un **agente** no se autoasigna estos roles ni simula promulgación (§7.2).
- Esta designación **no** autoriza por sí sola el envío de material interno IMSS
  a proveedores externos (ver `docs/autorizacion-fuentes-r1.md`).

## Control compensatorio (F5) — tres roles en una persona

Mientras jurídico = custodio = PO (interinato), **antes** de
`vigencia_verificada: true` o de promesa exterior de calidad:

1. Completar en registry `revision_vigencia` (`revisado_por`, `fecha`).
2. Preferible: segundo revisor humano o ronda adversarial **multi-provider**
   (H1) sobre el PR de vigencia.
3. Si no hay segundo revisor: `auto_revision_declarada: true` **y** no omitir
   la ronda adversarial del hito (no cuenta como `proceed` silencioso).
4. El agente autor del PR de registry **no** rellena `revisado_por` con su
   id de modelo; lo rellena el humano interino (o declara auto_revision).

Ticket plan: `R1-E0-05` (doble control vigencia).

## Enlaces

- Política: `docs/politica-agentes.md` §9  
- Plan: `docs/plan-r1-90d.md` Epic E0  
- Fuentes autorizadas: `docs/autorizacion-fuentes-r1.md`
