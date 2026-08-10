# Confirmación final — EvidenceEdge v0 — 2026-08-10

Después del retry se aplicaron estos fixes adicionales:

1. `trace_url` exige HTTPS y host real; `https://` y HTTP fallan cerrado.
2. `cubre_disposiciones` debe ser lista; no hay membership por substring.
3. `traza_disposiciones` duplicada falla cerrado y el validador la reporta.
4. `traza_disposicion_principal` requiere fecha y URL o identificador DOF.
5. Una fuente raíz no-objeto devuelve `fuente_invalida`, sin excepción.
6. El resolver busca una traza de disposición válida aunque antes haya una
   traza coincidente de alcance instrumento.
7. `traza_disposiciones.f5=true` sólo resuelve con fecha, localizador y
   `revision_vigencia`; el validador exige los mismos campos aun en slices de una
   sola disposición.

Evidencia local final: suite completa `107 tests OK`; py_compile y diff-check verdes.

Confirmar únicamente si queda un bypass activo HIGH/BLOCKER en estos puntos o
en `is_traversable`. Terminar con `DECISION: proceed | fix-and-retry | escalate`.
