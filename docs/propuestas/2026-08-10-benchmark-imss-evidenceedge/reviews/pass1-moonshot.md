# Pass 1 — Moonshot / Kimi

**Proveedor/modelo:** Moonshot / Kimi K3 256K · **Lente:** falsabilidad  
**Decisión:** `fix-and-retry`

## Hallazgos

- **HIGH H1:** `LOAPF:1` se declara a granularidad artículo con traza 1976,
  aunque el propio artículo contiene un párrafo reformado en 2025. La cita de
  Q2 pertenece a otro párrafo no marcado como reformado, pero la traza no cubre
  todo el artículo como se declara. Fix: granularidad párrafo y reserva explícita.
- **HIGH H2:** una arista recorrible extra, fuera de `candidate_edge_ids`, queda
  invisible. Fix: igualdad entre todo el catálogo recorrible y la unión esperada.
- **MED:** muestra coautorada mide regresión/consistencia, no verdad externa;
  fidelidad declarada no recomputa originales; prerregistro aún no comprometido
  en Git.
- **LOW:** métrica de falso positivo subreporta extras en casos respondibles;
  `claim_class` es autoatestiguada; una sola persona atestigua las tres aristas.

El revisor reprodujo 5/5 y 4 tests, comprobó las citas en extractos y recomputó
los cuatro PDF locales correctamente. La clasificación de alto impacto se confirmó.
