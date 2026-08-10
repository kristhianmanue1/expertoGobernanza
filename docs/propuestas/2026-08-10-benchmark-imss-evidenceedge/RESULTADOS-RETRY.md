# Resultados R2 — benchmark IMSS fidelidad + EvidenceEdge

**Benchmark:** `R1-BENCH-IMSS-EE-01-R2` · **Fecha:** 2026-08-10  
**Estado:** éxito técnico; quórum final en [`RECONCILIACION.md`](RECONCILIACION.md)

## Hashes observados antes de ejecutar

| Archivo | SHA-256 |
|---|---|
| `PREREGISTRO-RETRY.md` | `a865d57b674c0086147c3ecdb76b2f4a16888b126cee02ae336b712ab44331a0` |
| `imss_evidence_edge_cases.json` | `4be0b8f0a48c3374ede8a02538ec8c5906179f3e9df12477c606ea06ced0b570` |
| `imss_evidence_edges.json` | `aca2826a52c98e3a1a96e78b480ee2399edade93ff080bf4e7e236a69eda1993` |
| `benchmark_imss_edges.py` | `bad9d4afb8b9731ba514761156e1b6ec4d96bcfbadcf7b15e94eb3efdbbaac96` |
| `evidence_edge.py` | `9f37d3d464446a06f1269fa0fa9dc9dd910d4314e006bdb3419622c2e0c3a9da` |

## Resultado R2

| Métrica | Observado |
|---|---|
| Preguntas exactas | 5/5 |
| Positivas | 3 |
| Bloqueadas | 2 |
| Controles negativos rechazados | 5/5 |
| Falsos positivos/negativos por arista | 0/0 |
| Aristas fuera de casos | 0 |
| Divergencia conjunto global | 0 |
| Errores inesperados en positivas | 0 |

Los cuatro PDF locales requeridos existieron y sus SHA-256 fueron recomputados
durante la ejecución. La fecha jurídica del gate fue inyectada como
`2026-08-10`; el resultado no dependió del reloj de pared.

```text
python3 scripts/benchmark_imss_edges.py → passed=true
python3 -m unittest tests.test_benchmark_imss_edges tests.test_evidence_edge -q
→ 36 tests OK
```

## Alcance de la conclusión

R2 es un gate de regresión/consistencia sobre muestra fija. Prueba que, para
estas ocho candidatas, el compuesto de fidelidad y EvidenceEdge conserva tres
textuales y rechaza cinco controles. No demuestra ground truth jurídico abierto,
recall de recuperación, calidad generativa ni ventaja comercial.
