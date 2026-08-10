# Insumo — arquitectura y posicionamiento tras análisis externo

> **Estado:** propuesta bajo revisión adversarial; no es decisión adoptada.
> **Fecha:** 2026-08-10. **Clasificación §7.4:** público.
> **Autor:** OpenAI/Codex — excluido de votar en esta ronda.

## Pregunta de decisión

¿Qué partes del análisis externo sobre mercado, Akoma Ntoso, Law as Code y un
“Legal Provenance Graph” deben incorporarse al roadmap de ExpertoGobernanza sin
romper el alcance R1 ni convertir hipótesis comerciales o interpretaciones
jurídicas en hechos?

## Tesis del análisis externo

1. Lexis+ Protégé, vLex Vincent AI y Harvey construyen asistentes/agentes
   jurídicos con investigación y citas; ExpertoGobernanza podría diferenciarse
   como infraestructura jurídica verificable para cualquier agente.
2. OpenLaws es el comparable arquitectónico más próximo: corpus estructurado,
   jerarquía, citas, vigencia/cambios y API para LegalTech/IA.
3. Akoma Ntoso/LegalDocML podría evitar reinventar estructura e identificadores;
   se propone compatibilidad desde el inicio, aun conservando JSON/YAML interno.
4. La prioridad correcta sería `machine-verifiable` antes de
   `machine-executable`; Rulemapping/Law as Code quedaría para otra fase.
5. Un “Legal Provenance Graph” permitiría responder preguntas mediante cadenas
   de evidencia entre disposiciones, reformas, fuentes y conceptos.
6. La oportunidad comercial sugerida es “Legal Infrastructure for AI — México”,
   aunque no existe evidencia suficiente para afirmar ausencia de competidores.

## Evidencia primaria contrastada

- Lexis+ Protégé declara citas enlazadas, Shepard's e integración de fuentes
  internas: https://www.lexisnexis.com/en-us/products/lexis-plus-protege/legal-research.page
- Vincent AI declara memos con citas y fuentes inspeccionables:
  https://knowledge.vlex.com/en/features/vincent/ask-a-research-question
- Harvey declara agentes que planean, investigan y entregan resultados citados:
  https://www.harvey.ai/agents
- OpenLaws se posiciona como infraestructura de datos jurídicos estructurados
  para LegalTech/IA: https://openlaws.us/api/
- OASIS LegalDocML/Akoma Ntoso 1.0 cubre estructura, FRBR, identificadores,
  referencias, modificaciones, `temporalData` y metadata propietaria:
  https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html
- Rulemapping ofrece RUML y modelos ejecutables:
  https://rulemapping.org/

Las páginas comerciales prueban funciones declaradas por los proveedores, no
su exactitud real ni cobertura mexicana; eso requeriría un benchmark empírico.

## Estado real del proyecto que condiciona la decisión

- R1 prohíbe abrir bitemporalidad plena, operadores deónticos, jurisprudencia
  como subsistema, “leyes como código” o expansión masiva del corpus.
- El corpus usa YAML/JSON pequeño, ids como `CPEUM:4:P4`, hashes, trazas DOF,
  revisión humana y gates deterministas.
- `LFEP:5` tiene F5 pendiente y sus relaciones derivadas hacia LSS/LSS:5/LFEP:1
  están marcadas `verificada: false`.
- En `registry.yaml`, el instrumento LFEP tiene `vigencia_verificada: true`
  porque LFEP:1 fue revisado, mientras la traza de LFEP:5 conserva `f5: false`.
  Un consumidor podría heredar incorrectamente el estado del instrumento.
- H1 y H5 todavía requieren cierre adversarial multi-provider formal.

## Decisión propuesta por el autor (objeto de la ronda)

### Adoptar ahora como hipótesis interna

- Posicionamiento: “infraestructura verificable de legislación mexicana para
  auditoría y agentes de IA”. No usar aún “único”, “sistema operativo jurídico”
  ni “no existe competidor”.
- Prioridad: machine-readable/addressable/traceable/verifiable antes de
  interpretable/executable.
- Unidad autoritativa: afirmación/disposición, no un booleano heredado del
  instrumento.

### Adaptar

- Formalizar un contrato `EvidenceEdge v0` antes de una base de grafos. Cada
  relación debe tener sujeto, predicado, objeto, clase de afirmación, evidencia,
  estado de verificación, tiempo de validez, revisión y versión del gate.
- Tratar “Git jurídico” sólo como metáfora de trazabilidad; Git no modela por sí
  mismo vigencia, eficacia, aplicabilidad ni autoridad.

### Diferir

- No migrar el modelo interno a XML ni adoptar Akoma Ntoso como dependencia en
  R1. Hacer después un spike de compatibilidad sobre una disposición, sin
  cambiar el registry, con matriz explícita de pérdida/duplicación.
- No introducir Neo4j, embeddings, Agent API ni reglas ejecutables hasta que un
  caso de usuario y métricas demuestren necesidad.

### Orden propuesto

1. Cerrar deuda actual: rondas H1/H5 y F5 de LFEP:5.
2. Spike AKN aislado: mapear Work/Expression/Manifestation, `eId`, referencias,
   modificación, texto, hash y revisión; no cambiar el núcleo.
3. `EvidenceEdge v0`: la consulta “¿por qué el IMSS es OPD?” sólo recorre aristas
   verificadas por defecto y expone las pendientes sin promoverlas.
4. Mapa competitivo basado en evidencia: cobertura México, unidad de
   direccionamiento, temporalidad, actualización, procedencia, validación,
   revisión humana, API/exportación, licencia, seguridad, precio y SLA.

## Preguntas obligatorias a los revisores

1. ¿Hay un BLOCKER jurídico, técnico o estratégico en la decisión propuesta?
2. ¿Compatibilidad-en-el-borde con Akoma Ntoso conserva demasiado poco o es la
   opción proporcional al estado alfa/R1?
3. ¿`EvidenceEdge v0` evita realmente convertir interpretación en hecho? ¿Qué
   campo mínimo falta?
4. ¿La diferenciación propuesta es falsable y defendible frente a OpenLaws y
   suites jurídicas, o sigue siendo sólo narrativa?
5. ¿Qué debe cambiar antes de `proceed` y qué puede diferirse sin riesgo?

