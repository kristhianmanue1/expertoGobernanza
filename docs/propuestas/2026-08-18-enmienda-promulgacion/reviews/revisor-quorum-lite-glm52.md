# RONDA adversarial — enmienda promulgación institucional (quorum-lite)

**Fecha:** 2026-08-18 · **Quórum:** quorum-lite (1 revisor subagent en contexto
fresco; §6 — corrección que estrecha pretensiones, aprobada por el humano en
sesión). **Decorrelación declarada:** mismo modelo subyacente que el autor
(glm-5.2), contexto fresco; no multi-provider.

## Ciclo 1 — veredicto: fix-and-retry

| ID | Sev | Hallazgo | Disposición |
|---|---|---|---|
| H-01 | MED | política:252 "proceed → aplicar Git / promulgar la norma" contradecía "nadie del repo promulga" | FIX: "enviar el artefacto por la vía institucional" |
| H-02 | MED | ADR-0005 consecuencias: "sustrato en control de identidad legal del humano" contradecía la enmienda | FIX: sustrato institucional (cadena RIIMSS) |
| H-03 | MED | estado "aplicada" citaba reviews/ inexistente (ronda en curso) | FIX: esta RONDA depositada en `docs/propuestas/2026-08-18-enmienda-promulgacion/reviews/`; referencia corregida |
| H-04 | LOW | política:280 "(humano/institucional)" ambiguo post-enmienda | FIX: "institucional, IMSS (RIIMSS art. 6-VI y 75)" |
| H-05 | LOW | etiqueta del art. 6 (sección ≠ artículo) | FIX: "titulares de los Órganos Normativos" |

**Fidelidad de fuente CONFIRMADA por el revisor:** 4/4 extractos verbatim
cotejados contra el PDF (pypdf, 86 págs); sha256 del PDF verificado. Sin scope
creep (diff = 6 archivos: los 5 declarados + nota histórica en adr/0001:61,
benigna); roles-r1 conserva historia.

## Retry — veredicto: **proceed** (revisor fresco, verificación independiente)

H-01..H-05 VERIFICADOS aplicados y fieles. Nuevos LOW de seguimiento
(aplicados en el mismo PR): N-01 AGENTS.md punto 7 ("eso es del humano" →
"potestad institucional del IMSS"); N-02 esta precisión de diff (6 archivos).

## Veredicto final: **proceed** (2026-08-18)

Enmienda aplicada: política §6/§7.2/§9, roles-r1 (enlace institucional),
ADR-0005 (enmienda + consecuencias), ADR-0001 (nota histórica), AGENTS.md
(punto 7), procedencia RIIMSS (etiqueta art. 6).
