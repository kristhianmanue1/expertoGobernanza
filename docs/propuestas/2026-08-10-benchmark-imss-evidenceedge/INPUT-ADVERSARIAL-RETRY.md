# Entrada ciega — retry final benchmark IMSS

**Autor excluido:** OpenAI/Codex · **Impacto:** alto  
**Objeto:** confirmar cierre de pass 1; no diseñar AKN

## Revisar

- `PREREGISTRO-RETRY.md` y `RESULTADOS-RETRY.md`
- `benchmarks/imss_evidence_edge_cases.json`
- `benchmarks/fixtures/imss_evidence_edges.json`
- `scripts/benchmark_imss_edges.py`
- `corpus/evidence_edge.py`
- `tests/test_benchmark_imss_edges.py`
- `tests/test_evidence_edge.py`
- `reviews/pass1-*.md` y `RONDA.md`

## Confirmaciones requeridas

1. gate compuesto declarado, sin atribuir fidelidad al validador aislado;
2. citas Q1/Q2 cubren objeto y relación;
3. fuente inexistente, cita falsa y hash divergente se rechazan;
4. cinco controles negativos y cobertura global completa;
5. falsos positivos contados por arista;
6. PDF local recomputado y extracto versionado comprobado;
7. fecha inyectada; Q2 a granularidad párrafo; Q5 `disputed`;
8. límites epistemológicos declarados.

Devuelve sólo defectos de corrección/requisitos con severidad y
`DECISION: proceed | fix-and-retry | escalate`. Sólo lectura.
