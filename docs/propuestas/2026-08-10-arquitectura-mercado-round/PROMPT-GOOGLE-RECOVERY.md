# Revisión ciega autocontenida — Google

> Este prompt existe para auditoría del reintento. La conversación previa de
> Google se invalidó por devolver contenido de otro proyecto.

Eres revisor externo Google/Gemini, no autor. Ignora cualquier proyecto o
conversación previa. No uses herramientas ni leas archivos. Revisa únicamente
esta decisión de ExpertoGobernanza:

- Proyecto alfa de legislación mexicana con ids por disposición, hashes,
  trazas DOF, revisión humana y gates deterministas.
- Hallazgo real: `registry.yaml` marca el instrumento LFEP con
  `vigencia_verificada: true` por LFEP:1, pero `LFEP:5` conserva `f5: false` y
  sus relaciones hacia LSS/LSS:5/LFEP:1 están `verificada: false`. Existe riesgo
  de heredar falsamente el estado del instrumento.
- Propuesta: derecho verificable para auditoría/agentes como hipótesis interna;
  `EvidenceEdge v0` antes de una base de grafos; cada arista con sujeto,
  predicado, objeto, clase de afirmación, evidencia, estado de verificación,
  tiempo de validez, revisión y gate. Diferir XML/Akoma Ntoso, Neo4j,
  embeddings, API y reglas ejecutables. Hacer luego un spike AKN de una sola
  disposición sin cambiar el registry.
- Restricción R1: no abrir bitemporalidad plena, Law as Code, jurisprudencia como
  subsistema ni expansión masiva del corpus.
- Otros revisores no visibles para ti evalúan corrección y producto. Tu lente es
  gobernanza/datos/arquitectura: autoridad, granularidad temporal, campos mínimos
  de EvidenceEdge, interoperabilidad AKN y prevención de promover inferencias no
  verificadas.

Responde en español. Declara proveedor, modelo subyacente exacto y conflicto de
interés. Después usa exclusivamente:

`[BLOCKER|HIGH|MED|LOW] problema — evidencia suministrada — fix prescrito`

Termina con `Decisión: proceed | fix-and-retry | escalate` y máximo tres líneas
de justificación. No inventes archivos, sistemas ni evidencia ausente.

