# Prerregistro R3 — F5 LFEP:5 y granularidad LOAPF:1

**ID:** `R1-BENCH-IMSS-EE-01-R3` · **Fecha fija:** 2026-08-10  
**Estado:** cerrado antes de modificar corpus/fixtures · **Autor:** OpenAI/Codex

## Hipótesis

Cerrar F5 de `LFEP:5` no convierte en textual la identificación de la Ley del
Seguro Social: el artículo nombra al IMSS y remite genéricamente a “sus leyes
específicas”, pero no nombra la LSS. Q4 debe seguir bloqueada.

La respuesta Q2 sólo depende del tercer párrafo de `LOAPF:1`. Se sustituirá la
fuente agregada `LOAPF:1` por `LOAPF:1:P3`; la reforma de 18-03-2025 cubre el
segundo párrafo y no debe heredarse ni ocultarse.

## Cambios esperados

1. `LFEP:5`: F5 true con decreto DOF 16-07-2025, que reforma el primer párrafo.
2. La relación `LFEP:5 → LSS` permanece no recorrible por falta de identificación
   textual del objeto y de la relación específica.
3. `LOAPF:1:P3` conserva la cita sobre APF paraestatal y traza de publicación
   original; `LOAPF:1` agregado deja de presentarse como una sola fecha vigente.
4. Q1–Q5 conservan resultados: tres respondibles y dos bloqueadas.
5. Los cinco controles negativos continúan rechazados, sin FP/FN.

## Criterio de muerte

R3 falla si Q4 recorre por el solo hecho de cerrar F5; si Q2 usa la metadata
agregada de todo `LOAPF:1`; si cualquier cita/hash/fuente deja de validar; o si
el conjunto global deja de coincidir exactamente con las tres aristas positivas.

## Ejecución

```bash
./scripts/ci_check.sh
python3 scripts/benchmark_imss_edges.py
```

Git/PR siguen reservados al administrador. Este prerregistro local no es sello
de tiempo independiente y sólo será durable cuando el admin lo integre.
