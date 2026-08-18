# Visión — ExpertoGobernanza

> **Estado:** adoptado (definición acordada con el humano en sesión, 2026-08-18).
> **Linaje:** instancia domain-specific de CAGF
> (`github.com/kristhianmanue1/constitutional-ai-governance`); política
> `docs/politica-agentes.md` §6/§7; ADR-0001..0006; enmienda promulgación
> institucional (2026-08-18).

## Definición corta (pitch)

**ExpertoGobernanza** — plataforma de trazabilidad y fidelidad normativa:
recolecta evidencia de fuentes oficiales, verifica su vigencia y procedencia,
y permite redactar y auditar documentos normativos — leyes, reglamentos,
manuales, dictámenes — donde **toda afirmación está respaldada por cita
verificable o queda marcada como sin sustento**.

## Las tres capacidades

1. **Gestor de trazabilidad normativa** (evidencia): cadena de custodia del
   corpus — cada disposición con fuente oficial, fecha, hash y estado de
   vigencia; reformas trazadas (qué cambió, desde cuándo, con qué respaldo).
2. **Redacción con base en normatividad vigente** (drafting asistido):
   documentos donde cada afirmación normativa se cita contra el corpus
   verificado; lo no respaldado se declara, nunca se disfraza. Produce
   **borradores técnicos** — la promulgación es potestad institucional
   (enmienda 2026-08-18: nadie del repo promulga).
3. **Verificador/auditor de normas y documentos** (detección): auditoría
   afirmación por afirmación de documentos existentes; detecta citas
   inventadas (alucinaciones), disposiciones derogadas/reformadas,
   contradicciones internas, jerarquía normativa violada y vigencia no
   verificada; emite dictamen técnico con evidencia.

## Lo que NO es (límites que nos distinguen)

No es asesoría legal; no sustituye al DOF ni a las fuentes oficiales; no
promulga. Es la **capa técnica de fidelidad** entre las fuentes oficiales y
quienes deciden — válida para cualquier institución.

## Multi-vertical (IMSS = piloto, no techo)

La maquinaria (ids, hashes, procedencia, verificación, router/harness,
auditoría, metodología de técnica legal) es **dominio-agnóstica**; sólo el
contenido del corpus es por-vertical. Verticales futuros: gubernamental
general, cualquier institución (lineamientos/manuales/criterios), estatal y
municipal. Objetivo generalizado: *cualquier agente que hable de una norma la
cita contra fuente verificada o calla*.

## Consumo (cómo nos usan otros agentes)

- **Hoy (CLI stdlib, offline):** `corpus/lookup.py`, `verify_citations.py`,
  `scripts/audit_document.py`, `scripts/route_review.py`.
- **Futuro (gated, R2):** exposición **MCP** con contrato de consumo
  versionado (patrón escrubery `CONTRATO_API_v0`): tools `lookup_norma`,
  `verificar_cita`, `vigencia`, `auditar_documento` — cada respuesta con su
  bloque de procedencia. Requisitos previos: vigencia DOF nivel 1, recall
  v1.2, congelar contrato v0. Merita ADR-0007.

## Mapa axiomático CAGF (sustento)

Cada práctica del proyecto instancia un axioma de CAGF (ver
`CAGF-CORE.md`/`DEFINITIONS.md`/`MANIFIESTO-DEL-ORIGEN.md` en el repo citado):

| Axioma | Instancia aquí |
|---|---|
| A6 Continuidad de explicación + `causal_integrity` | trazabilidad afirmación→cita→fuente→sha256; sello del harness (`seal.py`), registry con hashes |
| A5 Humildad computacional | nunca se afirma vigencia sin cotejo DOF (banner `VIGENCIA-NO-VERIFICADA`); verificación sintáctica acotada |
| A4 Reflexividad forzada (graduated/adversarial/proof-carrying) | rondas §6 quorum-lite vs multi-provider por impacto; dictámenes con exit codes verificables |
| A2 Decorrelación (+ `epistemic_decorrelation`) | quórum por **modelo subyacente**; decorrelación de contexto declarada como parcial |
| A10 Integridad del sustrato | redactar ≠ promulgar (sin cadena institucional RIIMSS no hay reclamo); "withhold the claim" |
| A7 Transparencia simbiótica | corpus derivado (JSON, agentes) ↔ extractos verbatim (humanos); enlace institucional = auditor declarado |
| A9 Delegación por capacidades | RH-T07/proveedor autorizado = capability con validez y expiración |
| A0/A1 | fail-closed del router/gateway; presupuesto de contexto §3 |
| Manifiesto §I/III | "lo que no se deriva se declara con honestidad" = límites declarados en ADRs, no fingir CI verde |

El análisis de `pasado_y_futuro_de_CAGF` (§VI, "CAGF en dos lenguas") sustenta
la separación visión/principios atemporales vs implementación temporal
(herramientas de nuestro tiempo).
