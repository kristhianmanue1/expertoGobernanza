# Entrada ciega — EvidenceEdge v0 — 2026-08-10

## Objetivo

Revisar un contrato JSON/YAML plano para afirmaciones jurídicas trazables. Una
arista sólo debe ser recorrible cuando su afirmación completa está verificada;
se prohíbe heredar estados instrumento→disposición→relación.

## Artefactos bajo revisión

- `corpus/evidence_edge.py`
- `tests/test_evidence_edge.py`
- `corpus/registry_rules.py` (regla previa por disposición)
- `docs/propuestas/2026-08-10-arquitectura-mercado-round/RECONCILIACION.md`

## Invariantes esperados

1. Taxonomías y versiones cerradas; valores desconocidos fallan cerrado.
2. `verification.status` pertenece a la relación, nunca a sus nodos.
3. `verified` exige cobertura explícita de sujeto, objeto y relación.
4. `verified` exige revisión y traza nivel 1 de la disposición fuente exacta.
5. Sólo `is_traversable` autoriza recorrido; inválido o no verificado = `False`.
6. Sin base de grafos, Akoma Ntoso, LLM ni dependencia externa en R1.

## Preguntas adversariales

- ¿Existe alguna entrada malformada que lance excepción o resulte recorrible?
- ¿Se puede promover una inferencia usando vigencia o cobertura de un nodo?
- ¿El modelo temporal confunde reforma del cuerpo con la disposición concreta?
- ¿Alguna clase/estado permite convertir interpretación en hecho sin revisión?
- ¿El contrato es desproporcionado, ambiguo o imposible de migrar desde el corpus?

## Salida requerida

Hallazgos `BLOCKER | HIGH | MED | LOW`, cada uno con archivo/función, evidencia y
fix prescrito. Terminar con `DECISION: proceed | fix-and-retry | escalate`.
