# ADR-0001 — Adopción de "Plataforma de inteligencia normativa" + quórum multi-provider

> **Estado:** Aceptado (2026-08-13). La dirección y el MVP se ejecutaron; los
> ítems abiertos materiales se resolvieron (ver §"Resolución 2026-08-13"). Los
> diferenciales (repos OSS seed, equipo jurídico golden set) quedan diferidos.
> **Fecha:** 2026-08-06. **Autor:** agente (síntesis). **Autoridad que adopta:** humano orquestador (§7.2).
> **Insumos:** `docs/propuestas/2026-08-06-dictamen-plataforma-normativa-input.md`,
> `docs/propuestas/analisis-dictamen-2026-08-06.md`.

## Contexto
El orquestador recibió un dictamen que reformula el proyecto: de "RAG legal MX" a una
*Plataforma de inteligencia normativa* (registro normativo temporal + verificador
determinista de citas + análisis de impacto). Dos análisis independientes en contexto
fresco concluyeron **adoptar-con-condiciones** (ver síntesis). La gobernanza actual no
amparaba decidirlo (7/11 requisitos en vacío) NI gobernar el sistema futuro; su punto más
débil era la brecha **single-provider CAGF-A2** (quórum adversarial decorrelacionado).

Hecho nuevo: el entorno dispone de **CLIs de múltiples proveedores** (codex, claude, kimi,
gemini, qwen, opencode, cline) orquestables con **tmux** → la decorrelación de A2 es
alcanzable. Esto cambia el cálculo de gobernanza.

## Decisión (propuesta)
1. **Adoptar la dirección** "registro normativo temporal y verificable", no RAG plano.
   Reservar "Leyes como Código" para una fase posterior (reglas ejecutables + validación formal).
2. **Alcance del corpus** *(interpretación — confirmar)*: base = leyes federales generales
   (CPEUM, LGS, LSS + reglamentos + NOM); **piloto institucional = IMSS** (procedimientos/
   manuales como conjunto operacional a auditar).
3. **Alcance funcional**: lectura + auditoría **+ generación normativa**. Esta última
   **gated**: sólo sobre plantillas institucionales, con compuertas (competencia, marco
   aplicable, referencias vigentes) y HITL obligatorio (§7.2: redactar ≠ promulgar).
4. **MVP honesto primero**, antes que infraestructura amplia: UNA norma en git → lookup
   exacto determinista → verificador de citas determinista → auditor de UN documento piloto
   midiendo falsos positivos. Cada elemento ambicioso (bitemporalidad plena, operadores
   deónticos, jurisprudencia como subsistema) queda *gated by* "cuando el MVP lo justifique".
5. **Quórum adversarial multi-provider (cierra CAGF-A2):** para hitos de alto impacto,
   usar **≥3 proveedores distintos** (p. ej. autor=opencode, adversario=claude/gemini,
   árbitro=kimi/qwen) lanzados vía tmux con el mismo prompt + artefactos; el humano
   reconcilia y reasigna roles si uno no tiene presupuesto/tokens.

## Consecuencias
- **Gobernanza:** antes de ejecutar cualquier fase, extender la política con las 5
  extensiones críticas (ADR/decisiones, roles continuos, compuertas deterministas + niveles
  de confianza, evaluación/golden set jurídico, gobernanza de sistema desplegado). **Bootstrap:**
  la propia extensión de política se revisa con el nuevo quórum multi-provider.
- **Datos / §7.1:** rutear contenido por proveedores externos (OpenAI/Anthropic/Google/
  Alibaba/Moonshot) saca datos de la máquina. Para el dictamen y docs de gobernanza
  (no confidenciales) es aceptable; **cuando entren documentos IMSS internos/confidenciales,
  se requiere autorización explícita + reglas de manejo** (qué se envía, a quién, retención).
- **Riesgo:** "Fase 0 auditor" arrastra ~70 % de la Fase 1 (circularidad); los falsos
  positivos del auditor tienen coste reputacional → definir umbral antes de prometer nada.

## Alternativas consideradas
- **Rechazar y mantener RAG legal:** descartada; el dictamen y el análisis muestran que es
  jurídicamente insuficiente (vigencia≠aplicabilidad, transitorios, citas sin verificar).
- **Adoptar el dictamen tal cual (fases 0–5 completas):** descartada; confunde visión final
  con primer paso y la gobernanza no la ampara hoy.

## Ítems resueltos (2026-08-06)
- **Dominio:** ✓ **federal** (leyes públicas); **IMSS = piloto de prueba**.
- **Norma inicial / corpus:** ver `docs/propuestas/corpus-inicial-analisis-2026-08-06.md`. Target jerárquico CPEUM → LGS → LSS → normativa IMSS; **MVP = rebanada vertical** (traza-desde-el-origen + start-small). Nombres `[VERIFICAR-FUENTE]` (la Cámara da 403 a fetch automatizado).
- **Responsable jurídico del corpus:** **DEUDA** (diferido); interino = humano-promulgador (enmienda v1.1-revisada Cambio 4; rol renombrado **enlace institucional** 2026-08-18, ver ADR-0005 enmienda).

## Ítems aún abiertos (decisión humana)
- **Custodio/data steward** continuo del corpus.
- **Repos OSS** (`ingteranalvarez/lex-mx`, `JoshuaPozos/leyes-mexicanas-markdown`): usar como semilla sí/no (auditar licencia/procedencia).
- **Autorización para rutear contenido por proveedores externos** y proveedores del quórum estable (el bootstrap usó glm-5.2 + claude + kimi).
- **Equipo jurídico** para el golden set (define si Fases 3–4 son alcanzables).
- **Texto oficial** del instrumento raíz del slice (la Cámara bloquea fetch auto → hace falta proveerlo o autorizar un canal de descarga para el componente A).

## Próximas acciones (propuestas)
1. Humano resuelve los ítems abiertos (mínimo: dominio + responsable jurídico + autorización multi-provider).
2. Extender la política (extensiones 1–3) y **revisar la extensión con el quórum multi-provider** (primer uso real del A4+A2).
3. Ejecutar el **MVP honesto** sobre una sola norma como spike, midiendo falsos positivos.
4. Con evidencia, decidir la adopción formal de las fases 0–5 del dictamen.

## Resolución 2026-08-13 (aceptación)

La decisión propuesta se **acepta**: la dirección "registro normativo temporal y
verificable + verificador determinista de citas" es la adoptada. Los ítems
abiertos materiales se resolvieron en R1:

- **Responsable jurídico del corpus** → resuelto (`docs/roles-r1.md`, interino).
- **Custodio/data steward** → resuelto (`docs/roles-r1.md`, interino).
- **Autorización multi-provider** → resuelta (`docs/autorizacion-fuentes-r1.md`).
- **Quórum adversarial multi-provider (≥3)** → ejecutado: política v1.1 §6 +
  router §7.4 estable con ronda multi-provider real (claude + codex + glm-5.2).
- **MVP honesto** → ejecutado: corpus + `lookup.py` + `verify_citations.py` +
  golden set 135 tests + EvidenceEdge gobernado. Eje-salud y eje IMSS F5 cerrados.
- **Dominio** → confirmado: federal (leyes públicas), IMSS = piloto.

**Diferidos (no bloquean la aceptación):**
- Repos OSS (`lex-mx`, `leyes-mexicanas-markdown`) como semilla: auditar
  licencia/procedencia antes de usar.
- Equipo jurídico para el golden set: define si Fases 3–4 son alcanzables.
- Fases 0–5 completas del dictamen: gated by evidencia del MVP (sigue vigente el
  principio "MVP honesto primero").

**Leyes como Código** (reglas ejecutables + validación formal) sigue reservado
para una fase posterior, como decidió la propuesta original.
