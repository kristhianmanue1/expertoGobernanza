# Revisión ciega — Google — lente gobernanza/datos/arquitectura

Lee exclusivamente estos archivos del repositorio:

- `docs/propuestas/2026-08-10-arquitectura-mercado-round/INPUT.md`
- `corpus/registry.yaml`
- `corpus/derived/lfep/LFEP-005.json`
- `docs/propuestas/gate-confianza-multieje-v1.md`

Eres revisor externo y árbitro, no autor. No leas salidas de otros revisores ni
modifiques archivos. Revisa corrección y requisitos, no estilo. Tu lente es
gobernanza, datos y arquitectura: límites de autoridad, granularidad temporal,
provenance, campos mínimos de `EvidenceEdge`, interoperabilidad AKN, seguridad
del serving para agentes y criterios de salida del spike. Señala cualquier forma
en que una arista o estado agregado pueda promover una inferencia no verificada.

Empieza declarando proveedor, modelo subyacente exacto y conflicto de interés.
Después usa sólo:

`[BLOCKER|HIGH|MED|LOW] problema — evidencia — fix prescrito`

Termina con `Decisión: proceed | fix-and-retry | escalate` y una justificación de
máximo tres líneas. Cualquier BLOCKER debe ser requisito real, no preferencia.
