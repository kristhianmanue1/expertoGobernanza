# Visión — ExpertoGobernanza

> **Estado:** adoptado (definición acordada con el humano en sesión,
> 2026-08-18) · **ronda adversarial quorum-lite** aplicada (2026-08-18:
> capacidades marcadas hoy/roadmap, mapa axiomático corregido; ver
> `docs/propuestas/2026-08-18-vision-plataforma/reviews/`).
> **Linaje:** instancia domain-specific de CAGF
> (`github.com/kristhianmanue1/constitutional-ai-governance`); política
> `docs/politica-agentes.md` §6/§7; ADR-0001..0006; enmienda promulgación
> institucional (2026-08-18).

## Definición corta (pitch)

**ExpertoGobernanza** — plataforma de trazabilidad y fidelidad normativa:
recolecta evidencia de fuentes oficiales, **verifica su procedencia (hoy) y su
vigencia (en construcción — gate v1 la declara no-verificada hasta cotejo
DOF)**, y permitirá redactar y auditar documentos normativos — leyes,
reglamentos, manuales, dictámenes — donde **toda afirmación está respaldada
por cita verificable o queda marcada como sin sustento**.

*Estado del corpus (alfa):* slice piloto (~2 disposiciones: CPEUM:4:P4,
LGS:1, + eje IMSS 5/6); cobertura ≠ ley completa.

## Las tres capacidades (hoy vs roadmap)

1. **Gestor de trazabilidad normativa** (evidencia): cadena de custodia del
   corpus — cada disposición con fuente oficial, fecha, hash y estado de
   vigencia. Reformas trazadas: **parcial** (evidencia manual en
   `corpus/registry.yaml`; traza automática = roadmap).
2. **Redacción con base en normatividad vigente** (drafting asistido) —
   **roadmap, sin iniciar**: documentos donde cada afirmación normativa se
   cita contra el corpus verificado; lo no respaldado se declara, nunca se
   disfraza. Produciría **borradores técnicos** — la promulgación es
   potestad institucional (enmienda 2026-08-18: nadie del repo promulga).
3. **Verificador/auditor de normas y documentos** (detección): auditoría
   afirmación por afirmación. **Hoy (`audit_document.py` v0, claims
   pre-etiquetados):** existencia, match verbatim y recomputo sha256
   (`verify_citations.py`), vigencia declarada no-verificada. **Roadmap:**
   citas inventadas en texto libre, disposiciones derogadas/reformadas,
   contracciones internas, jerarquía normativa violada. Emite dictamen
   técnico con evidencia y exit codes.

## Lo que NO es (límites que nos distinguen)

No es asesoría legal; no sustituye al DOF ni a las fuentes oficiales; no
promulga. Es la **capa técnica de fidelidad** entre las fuentes oficiales y
quienes deciden — válida para cualquier institución.

**Riesgos declarados (ronda 2026-08-18):**
- El auditor es fail-closed sobre un **corpus parcial**: una cita válida
  fuera del slice puede reportarse `bajo` (falso negativo de cobertura);
  cobertura ≠ ley completa. Umbral FP/FN diferido (R1-E0-03).
- **Sin verificación de frescura continua:** la vigencia es
  punto-en-el-tiempo; snapshots (DOF/Wayback) envejecen sin señal al
  consumidor.

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
  versionado (patrón: contrato de API congelado por fases, como el
  `CONTRATO_API_v0.md` de escrubery): tools `lookup_norma`, `verificar_cita`,
  `vigencia`, `auditar_documento` — cada respuesta con su bloque de
  procedencia. Requisitos previos: vigencia DOF nivel 1, recall v1.2,
  congelar contrato v0. **Requerirá ADR nuevo (ADR-0007, por crear).**

## Mapa axiomático CAGF (sustento)

Cada práctica del proyecto instancia un axioma de CAGF (ver
`CAGF-CORE.md`/`DEFINITIONS.md`/`MANIFIESTO-DEL-ORIGEN.md` en el repo citado):

| Axioma | Instancia aquí |
|---|---|
| A6 Continuidad de explicación + `causal_integrity` | trazabilidad afirmación→cita→fuente→sha256; sello del harness (`seal.py`), registry con hashes |
| A5 Humildad computacional | nunca se afirma vigencia sin cotejo DOF (banner `VIGENCIA-NO-VERIFICADA`); verificación sintáctica acotada |
| A4 Reflexividad forzada (graduated/adversarial/proof-carrying) | rondas §6 quorum-lite vs multi-provider por impacto; dictámenes con exit codes verificables |
| A3 Bounded Economy | base del quórum graduado (verificación proporcional al costo); presupuesto de lectura/tarea §4 |
| A2 Decorrelación (+ `epistemic_decorrelation`) | quórum por **modelo subyacente** (decorrelación de **arquitectura**, no de datos de entrenamiento/epistémica — parcial y declarada) |
| A10 Integridad del sustrato | redactar ≠ promulgar — derivación de política §7 a partir de A10 ("withhold the claim" EndToEndGovernedDelegation → sin cadena institucional RIIMSS no hay reclamo) |
| A7 Transparencia simbiótica | corpus derivado (JSON, agentes) ↔ extractos verbatim (humanos); enlace institucional = auditor declarado |
| A9 Delegación por capacidades | **diseño pendiente:** al autorizar proveedor (RH-T07) definir validity_window/revocación de la capability |
| A0/A3 | fail-closed del router/gateway (A0); presupuesto de contexto §4 y economía de verificación (A3) |
| Manifiesto §I/III | "lo que no se deriva se declara con honestidad" = límites declarados en ADRs, no fingir CI verde |

El análisis de `pasado_y_futuro_de_CAGF` (§VI "juicio final" y §VII "CAGF en
dos lenguas") sustenta la separación visión/principios atemporales vs
implementación temporal (herramientas de nuestro tiempo).

## Métricas por capacidad (qué mide cada una)

1. Trazabilidad: cobertura de disposiciones del slice con hash+procedencia
   (hoy 5/6 eje IMSS); frescura declarada por entrada.
2. Redacción (cuando exista): % afirmaciones con cita verificada vs
   marcadas sin sustento en el borrador producido.
3. Auditoría: recall de extracción (v1.2 en curso) y FP/FN del auditor
   (diferido R1-E0-03) sobre el golden set.

**Qué sigue:** plan `docs/plan-r1-90d.md` (cola R1: R1-E8-01, R1-E2, recall
v1.2); humano-gateado: roles §9/DOF nivel 1/proveedor RH-T07.
