# Entrada ciega — gate del benchmark IMSS EvidenceEdge

**Autor excluido:** OpenAI/Codex. **Clasificación propuesta:** alto impacto,
porque prueba una compuerta de fidelidad y usa corpus normativo.

## Artefactos a revisar

- `docs/propuestas/2026-08-10-benchmark-imss-evidenceedge/PREREGISTRO.md`
- `docs/propuestas/2026-08-10-benchmark-imss-evidenceedge/RESULTADOS.md`
- `benchmarks/imss_evidence_edge_cases.json`
- `benchmarks/fixtures/imss_evidence_edges.json`
- `scripts/benchmark_imss_edges.py`
- `tests/test_benchmark_imss_edges.py`
- `corpus/evidence_edge.py`
- JSON fuente bajo `corpus/derived/{lss,loapf,lfep,riimss}/`

## Pregunta de gate

¿El benchmark es realmente falsable, reproduce sólo recorridos autorizados por
EvidenceEdge y justifica pasar a un spike AKN aislado sin convertir el resultado
en una afirmación jurídica o comercial más amplia?

## Contrato del revisor

Marcar únicamente defectos de corrección, fidelidad, seguridad de datos o
requisitos. Formato: `[BLOCKER|HIGH|MED|LOW] problema — evidencia — fix`.
Terminar con `DECISION: proceed | fix-and-retry | escalate`.

Reglas: un falso positivo es BLOCKER; cualquier cita inexistente es BLOCKER;
la clasificación de alto impacto debe auditarse; no proponer AKN todavía.
