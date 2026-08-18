# RONDA adversarial — docs/vision.md (quorum-lite)

**Fecha:** 2026-08-18 · **Quórum:** quorum-lite (subagent contexto fresco;
decorrelación de contexto, no multi-provider — declarada). **Objeto:**
`docs/vision.md` (adoptado en sesión esa misma fecha).

## Ciclo 1 — veredicto: fix-and-retry (14 hallazgos)

| ID | Sev | Hallazgo | Fix aplicado |
|---|---|---|---|
| H-01 | HIGH | capacidad 3 en presente con detectores inexistentes (alucinaciones/derogadas/contradicciones/jerarquía) | desglose hoy (`audit_document.py` v0 pre-etiquetado: existencia/verbatim/sha256) vs roadmap |
| H-02 | HIGH | capacidad 2 (redacción) 100% roadmap sin marcar | "roadmap, sin iniciar" |
| H-03 | MED | pitch "verifica su vigencia" en presente; corpus ~2 disposiciones sin declarar | pitch corregido + línea de estado del corpus |
| H-04 | MED | fila A0/A1 mal atribuida (presupuesto contexto = A3, no A1; §3→§4) | fila A0/A3 corregida + fila A3 nueva |
| H-05 | MED | A2 "decorrelación de contexto" ≠ brecha declarada (arquitectura vs entrenamiento) | "arquitectura, no entrenamiento/epistémica — parcial" |
| H-06 | MED | A9 claimed "capability con validez y expiración" sin artefacto | "diseño pendiente (validity_window/revocación en RH-T07)" |
| H-07 | MED | "reformas trazadas" en presente (sólo manual en registry) | "parcial; traza automática = roadmap" |
| H-08 | MED | riesgo no declarado: FN por corpus parcial (fail-closed bloquea citas válidas fuera del slice) | riesgos declarados §NO es |
| H-09 | MED | riesgo no declarado: corpus desactualizado sin señal (vigencia punto-en-el-tiempo) | idem |
| H-10 | LOW | A10 "withhold the claim" citado fuera de contexto (es companion de EndToEndGovernedDelegation) | "(derivación de política §7 a partir de A10)" |
| H-11 | LOW | "merita ADR-0007" leído como existente | "requerirá ADR nuevo (ADR-0007, por crear)" |
| H-12 | LOW | cita §VI/§VII invertida de consenso_pasado_futuro | corregida (VI juicio final, VII dos lenguas) |
| H-13 | LOW | sin métricas ni "qué sigue" | sección métricas por capacidad + puntero plan R1 |
| H-14 | LOW | patrón escrubery no resoluble en repo | glosado en línea |

El revisor verificó además: fidelidad de las filas A6/A5/A4/A7 contra
CAGF-CORE (confirmandas), consistencia con enmienda de promulgación y ADR-0006.

## Veredicto final: **proceed** tras fixes (2026-08-18)

Los 14 fixes son redacción; aplicados en el mismo commit. El documento ahora
distingue hoy/roadmap, corrige el mapa axiomático y declara riesgos.
