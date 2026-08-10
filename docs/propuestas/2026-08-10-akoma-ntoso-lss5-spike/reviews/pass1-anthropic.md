# Pass 1 — Anthropic / Claude

**Decisión:** `fix-and-retry` · **Máxima severidad:** HIGH

- Expression usaba 2001-12-20, fecha de reforma de `LSS:5`, como versión de
  todo el documento; debía usar 2026-01-15 y conservar 2001 como metadata de la porción.
- `FRBRauthoritative=false` en Work podía negar autoridad a la ley; el XSD no
  permite el flag en Manifestation. Debía quedar sólo en la Expression editorial.
- Faltaba `FRBRportion`; `<original>` no era la referencia adecuada al contenedor.
- `GUID=LSS:5` duplicaba el alias interno.
- XSD y transformación inversa real no formaban parte del arnés.
- Fechas/roles necesitaban fuente declarada y la interoperabilidad no debía
  afirmarse sin consumidor probado.

El revisor confirmó validez XSD, hashes, cinco tests y proporcionalidad del
adaptador; bloqueó el cierre por fidelidad de identidad/autoridad.
