# Relatoría — Primer ejercicio del quórum multi-provider (2026-08-06)

> **Propósito:** registro persistente y **prueba/auditoría** del primer ejercicio de ronda
> adversarial multi-provider del proyecto ExpertoGobernanza. Documenta qué pasó, qué se dijo,
> qué se **aplicó** y qué se **criticó** de CAGF, los 16 hallazgos y la decisión.
> **Autor de la relatoría:** opencode (glm-5.2). **Reconciliación final:** humano.

## Proveniencia de modelos en este ejercicio
| Rol | Proveedor / modelo | Alcance |
|---|---|---|
| Autor + relator | opencode · **glm-5.2** (zai-coding-plan) | redactó plan, ADR, enmienda, síntesis |
| Revisor adversarial (H1/H2/H3, dictamen) | subagentes opencode (single-provider) | rondas previas |
| Revisor adversarial 1 (enmienda) | **claude** (Anthropic) | bootstrap, fix-and-retry |
| Revisor adversarial 2 (enmienda) | **kimi** (Moonshot) | bootstrap, fix-and-retry |
| No disponibles | gemini (Google, sin auth), qwen (Alibaba, OAuth discontinuado) | cayeron |

## §1. Cronología (qué pasó y qué se dijo)

**F0 — Diagnóstico/entorno.** "Analiza" → venv roto (3.9/3.10, AN-KLA no ejecutable). "Hay
3.12" → reparo venv a 3.12, reinstalo `an_kla@v0.1.0-beta.6`. Reconcilio: memoria en rev 1
(no 0); `proposal/authority.json` obsoletos.

**F1 — Plan R0 + git.** Redacto `plan-r0.md`. T1 (sync AGENTS.md). Indicas repo
`kristhianmanue1/expertoGobernanza` + fuentes = leyes MX (CPEUM/LGS) + pides mejores
prácticas. "Adelante" → con tus credenciales `gh`: `git init`, `.gitignore`, commit
`87e69db`, push a `main`. "Avanza hasta T6" → T2 (fact correctivo, rev 1→2) + T6
(`check_sizes.py`); adversarial single-provider `fix-and-retry`→fixes→`proceed` (H1/H2/H3).

**F2 — Dictamen.** Traes Dictamen+análisis → "Plataforma de inteligencia normativa". 2
subagentes: veredicto **adoptar-con-condiciones**; gobernanza **0/11 cubiertos, 7 vacíos**;
CAGF-A2 = punto más débil. Síntesis + ADR-0001.

**F3 — Decisiones + enmienda.** Respondes: federal+IMSS piloto; lectura+auditoría+generación;
y que tienes CLIs multi-provider (codex/claude/kimi/opencode/cline) vía tmux. Verifico 7
proveedores → **CAGF-A2 cerrable**. Redacto **enmienda v1.1** (multi-provider + compuertas +
datos + roles + ADR).

**F4 — Bootstrap multi-provider.** Ronda sobre la enmienda con 3 proveedores (glm-5.2 autor +
claude + kimi). gemini/qwen cayeron (auth/presupuesto). Ambos revisores: **`fix-and-retry`
unánime**, 16 hallazgos, conflicto de interés declarado. Commit `3bb5ce2`.

## §2. CAGF — qué se APLICÓ y qué se CRITICÓ

### Aplicado (instancias reales en este ejercicio)
- **CAGF-A4 (Reflexividad Forzada):** el quórum adversarial se ejecutó de verdad sobre la
  enmienda (≥3 revisores con ≥1 adversario). Los hallazgos BLOCKER convergentes entre dos
  proveedores demostraron que no fue decorativo.
- **CAGF-A5 (Humildad Computacional):** la enmienda la revisaron proveedores **externos al
  autor** (no introspección); y el "verificador de citas determinista" se declaró como
  verificación por **código**, no por prompt.
- **CAGF-A2 (Decorrelación Eterna) — parcialmente:** se logró decorrelación **real de
  arquitectura** (glm-5.2 + Anthropic + Moonshot, tres familias de modelo distintas). Es el
  primer cumplimiento parcial de A2 del proyecto.
- **CAGF-A10 (Integridad del Sustrato):** ADR-0001 y la enmienda declaran que **adoptar**
  corresponde al humano (redactar/analizar ≠ promulgar/adoptar); la reconciliación es humana.
- **CAGF-A6 (Trazabilidad):** cadena completa versionada (commits, AN-KLA rev 2, ADR,
  enmienda, reviews verbatim con proveedor/modelo).
- **Honestidad radical (precedente A8/A10):** el ejercicio **no fingió** cumplimiento pleno
  de A2; declaró la brecha y la rebajó a "mitigada parcialmente" tras evidencia.

### Criticado / donde CAGF no llegó (hallazgos del propio quórum)
- **A2 NO cerrado plenamente:** la decorrelación fue de *arquitectura de modelo*, **no de
  datos de entrenamiento**; 2/4 proveedores cayeron (auth/presupuesto) → la reasignación
  erosiona la decorrelación; el reconciliador reintroduce single-provider; mismo prompt =
  anclaje compartido; opencode/cline son herramientas que pueden correr el **mismo modelo**
  subyacente. → A2 = mitigada, no resuelta.
- **A4 debilitado sin reglas:** sin definición de "alto impacto" ni regla de agregación, el
  quórum podía volverse decorativo; clasificar el impacto el propio autor = incentivo a
  degradarlo.
- **A5 — gates wishful:** las compuertas deterministas resultaron dependientes de un corpus
  temporal inexistente (el gate depende del sistema que gobierna) → no eran testeables hoy.
- **Circularidad auto-referencial (kimi):** "esta misma ronda *es* el run que valida el
  proceso" → el proceso se validaba a sí mismo en su primer ejercicio.

**Lectura CAGF:** el ejercicio **elevó** la postura del proyecto (A2 pasó de "declarada, no
resuelta" a "mitigada parcialmente con evidencia") y **mostró el límite honesto**: el
multi-provider decorrelaciona arquitectura, no entrenamiento; y requiere reglas de
agregación/proveniencia para no ser decorativo. Eso es exactamente lo que CAGF pide: declarar
el alcance del cumplimiento, no afirmarlo falsamente.

## §3. Los 16 hallazgos/fixes (del bootstrap)
*(detalle completo en `docs/propuestas/enmienda-v1.1-bootstrap.md`; aquí resumen)*

| # | Severidad | Hallazgo | Fix |
|---|---|---|---|
| 1 | BLOCKER | título "cierra A2" vs DoD "parcial" | "mitiga parcialmente"; N≥3 runs sobre artefactos distintos |
| 2 | BLOCKER | reconciliador single-provider | humano por defecto; agente = 4º proveedor, sólo agrega |
| 3 | BLOCKER | "alto impacto" indefinido/autor | lista cerrada + "ante duda, alto" + audita revisor |
| 4 | BLOCKER | gates sin corpus | gate versionado; v1 testeable; `[VIGENCIA-NO-VERIFICABLE]` |
| 5 | HIGH | gate no determinista e2e | salida estructurada + medir recall |
| 6 | HIGH | autoclasificación de datos | allowlist + router ex-ante + log hash |
| 7 | HIGH | vacío régimen legal (LFPDPPP) | base jurídica + ToS/proveedor + prohibición datos personales |
| 8 | HIGH | prompt idéntico/anclaje | revisión ciega + lentes por rol |
| 9 | HIGH/MED | DoD circular | DoD independiente del veredicto; artefacto distinto |
| 10 | MED | reasignación erosiona | <3 proveedores → `PARCIAL`, nunca `proceed` |
| 11 | MED | sin regla agregación | cualquier BLOCKER bloquea; mayoría MED |
| 12 | LOW/MED | proveniencia por CLI no modelo | registrar modelo subyacente |
| 13 | MED | nivel `medio` sin acotar | quién consume; fail-closed a `bajo` |
| 14 | MED | ADR sin ciclo de vida | estados + estratégico/táctico + rollback |
| 15 | MED | roles sin autoridad/plazo | interino=humano; deadline; no auto-asignación |
| 16 | HIGH res. | diferir v1.2 desprotege daño | prohibir exponer a usuarios antes de v1.2 |

**LOW adicionales (no en los 16):** inyección de prompt desde PDFs/DOF del corpus;
presupuesto/costo por hito; descargo "no es asesoría jurídica"; resolver referencias internas.

## §4. Decisión y estado
**Decisión consolidada del quórum: `fix-and-retry` (unánime).** Ningún hallazgo requiere
rediseño arquitectónico — son precisión de reglas. Estado: relatoría persistida (este doc) →
aplicar 16 fixes (→ `enmienda-gobernanza-v1.1-revisada.md`) → **no re-validar sobre la misma
enmienda** (circular) → próxima validación multi-provider sobre **otro artefacto**
(verificador de citas del MVP) → reconciliación/adopción por el humano.
