# Resultados — benchmark IMSS sobre EvidenceEdge v0

**Benchmark:** `R1-BENCH-IMSS-EE-01` · **Fecha:** 2026-08-10  
**Estado:** resultado provisional invalidado por el pass adversarial 1

## Integridad de entrada observada antes de ejecutar

| Archivo | SHA-256 |
|---|---|
| `PREREGISTRO.md` | `0ffa2f9ce7454ba8f90df879ac5f6e822023e5010866bf876a4b6852835e61e7` |
| `benchmarks/imss_evidence_edge_cases.json` | `6456bf4407c1c93981e5be6b4b6a9b580db84351404214a1a0171c68c985c9e6` |
| `benchmarks/fixtures/imss_evidence_edges.json` | `823d04b34becd7d564af1d9cf246f67507b38cee6e0bc059fed905ecca2288db` |

Los hashes son evidencia del orden operativo dentro del worktree, no sello de
tiempo independiente. El commit administrativo sigue pendiente.

## Resultado

| Métrica preregistrada | Observado |
|---|---|
| Casos exactos | 5/5 |
| Respondibles | 3 |
| Bloqueados | 2 |
| Falsos positivos | 0 |
| Falsos negativos | 0 |
| Aristas inválidas/fidelidad fallida | 0 |

Detalle:

- Q1 → `LSS:5|define_naturaleza|IMSS`.
- Q2 → `LOAPF:1|ubica_clase|administracion_publica_paraestatal`.
- Q3 → `RIIMSS:1|define_objeto|Seguro_Social`.
- Q4 → bloqueada: `LFEP:5` no tiene F5 y la relación específica no está cubierta.
- Q5 → bloqueada: `jerarquia_interpretativa` no es recorrible en v0.

## Checks ejecutados

```text
python3 scripts/benchmark_imss_edges.py                    → passed=true, 5/5
python3 -m unittest tests.test_benchmark_imss_edges -q     → 4 tests OK
python3 -m py_compile scripts/benchmark_imss_edges.py ...  → OK
```

## Interpretación limitada

El resultado inicial sugería que esta muestra fija distinguía aristas textuales
recorribles de dos clases de promoción indebida. No mide recall abierto,
paráfrasis, recuperación de candidatas, calidad de una respuesta generativa ni
comparación con terceros. Por tanto sólo habilita evaluar el costo/beneficio de
un adaptador AKN aislado; la ronda adversarial encontró que aún no bastaba para
autorizarlo. No prueba diferenciación comercial ni adopción.
