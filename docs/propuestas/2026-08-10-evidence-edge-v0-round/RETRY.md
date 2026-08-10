# Retry — EvidenceEdge v0 — 2026-08-10

## Resultado de ronda 1

Anthropic, Moonshot y Zhipu/GLM: `fix-and-retry`; cero blockers.

## Correcciones aplicadas

1. `verified` exige evidencia nivel 1/2 y granularidad `articulo|parrafo`.
2. `covers_object` debe ser `true`; `not_applicable` no habilita recorrido.
3. `trace_date <= reviewed_at <= hoy`; snapshot explícito a la revisión.
4. `verified` exige `subject.kind=disposicion` y el mismo id fuente.
5. Sólo `{textual, remision_normativa, vigencia}` es recorrible en v0; las clases
   interpretativas pueden registrarse, pero `is_traversable` devuelve `false`.
6. IDs usan un léxico sin espacios ni `|`; se elimina la colisión de tripletas.
7. El scope conserva granularidad; la traza acepta identificador DOF o URL.
8. El resolver del registry ya no acepta alcance `instrumento` como evidencia de
   una disposición; `vigencia_verificada` exige booleano real.

## Fronteras aceptadas, no ocultas

- El validador comprueba la estructura de una atestación. No abre archivos ni
  recomputa hashes; esa integración corresponde al gate de citas. El docstring
  ya prohíbe presentarlo como verificación de bytes.
- `inheritance: prohibited` y `gate_version` se mantienen porque la
  reconciliación multi-provider previa los exige como invariante y procedencia.
- No se habilita serving externo: la política v1.1 lo prohíbe antes de v1.2.

## Evidencia local

- `python3 -m unittest tests.test_evidence_edge tests.test_registry_vigencia`
  → 50 pruebas verdes.

## Pregunta de retry

¿Queda algún bypass que permita que `is_traversable` devuelva `true` heredando
estado, usando evidencia nivel 3/4, alcance instrumento, objeto no cubierto,
fecha incoherente, sujeto no-disposición o clase interpretativa?

Salida: hallazgos con severidad y fix; terminar con `DECISION: proceed |
fix-and-retry | escalate`.
