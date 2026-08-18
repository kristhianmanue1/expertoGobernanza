# RONDA adversarial — cierre router harness (RH-T08)

**Fecha:** 2026-08-18 · **Quórum:** quorum-lite (1 revisor en contexto fresco,
política §6) — hito de cierre de plan técnico sin cambio de política.
**Decorrelación declarada:** revisor = subagent glm-5.2, misma arquitectura
subyacente que el autor (contexto fresco sí; multi-provider no). Para el
próximo cambio de política/compuerta se exige quórum completo ≥3 proveedores.

## Objeto atacado

`review_routing/{seal,audit_log,gateway}.py` + `scripts/route_review.py`
(H0+H1+H2 mergeados), superficies exigidas por `docs/planes/router-harness/
03-tareas.md` RH-T08: sellado, cadena de log, fail-closed del gateway,
path traversal heredado. Baseline: 180 tests.

## Ciclos

| Ciclo | Veredicto | Hallazgos | Acción |
|---|---|---|---|
| 1 | fix-and-retry | H-01 HIGH, M-01 MED, L-01..L-04 LOW | fixes + 9 tests (189) |
| retry 1 | fix-and-retry | N-01, N-02 LOW (regresiones de fixes) | fixes + 4 tests (192) |
| retry 2 | **proceed** | X-01, X-02 LOW (fail-closed) | X-02 fix aplicado (sugerido por el revisor) + 1 test (193); X-01 backlog |

Detalle: `reviews/revisor-quorum-lite-glm52.md`. Input: `INPUT-ADVERSARIAL.md`.

## Resultado

**proceed** → ADR-0006 pasa a **Aceptado**; hito marcado CERRADO en
`docs/planes/router-harness/00-INDICE.md`. Suite final 193/193 OK.

## Backlog derivado (abierto, declarado)

- X-01: RecursionError en `audit_log._parse` ante anidamiento profundo
  (crash fail-closed, no falsos OK) — endurecer parser en RH-T07.
- INFO: `append` con seal NaN del caller → ValueError crudo (fail-closed
  efectivo) — validar tipos al entrar a RH-T07.
