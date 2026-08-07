# Bootstrap del quórum multi-provider — enmienda de gobernanza v1.1

> **Fecha:** 2026-08-06. **Artefacto revisado:** `docs/propuestas/enmienda-gobernanza-v1.1.md`.
> **Autor del artefacto:** opencode (glm-5.2, zai-coding-plan). **Tipo:** ronda adversarial
> multi-provider (bootstrap del Cambio 1 de la enmienda). **Decisión consolidada: `fix-and-retry`.**

## Run summary

| Rol | CLI / proveedor | Modelo (declarado) | Resultado |
|---|---|---|---|
| Autor | opencode | glm-5.2 (zai-coding-plan) | redactó la enmienda |
| Revisor adversarial 1 | claude (Anthropic) | Claude | ✓ revisión completa (36 lín.) |
| Revisor adversarial 2 | kimi (Moonshot) | Kimi | ✓ revisión completa (50 lín.) |
| Revisor adversarial 3 | gemini (Google) | Gemini | ✗ sin auth (esperó browser → timeout) |
| Revisor adversarial 4 | qwen (Alibaba) | Qwen | ✗ OAuth free tier discontinuado |
| (disponible, no usado) | codex (OpenAI) | — | no invocado esta ronda |

**Quórum efectivo:** 3 proveedores distintos (glm-5.2 + Anthropic + Moonshot). 2 de 4
proveedores externos no disponibles por auth/presupuesto — **esto valida empíricamente** el
hallazgo "la reasignación erosiona la decorrelación" (claude MED, kimi MED).

## Hallazgos consolidados (convergentes = señal fuerte)

| # | Hallazgo | Severidad | Quién | Fix prescrito |
|---|---|---|---|---|
| 1 | Título "cierra CAGF-A2" vs DoD "parcialmente cerrada" = incoherente | BLOCKER/HIGH | claude+kimi | renombrar a "mitiga parcialmente"; requerir N≥3 runs **sobre artefactos distintos** antes de redeclarar la brecha |
| 2 | meta-agente reconciliador reintroduce single-provider | BLOCKER/HIGH | claude+kimi | reconciliación humana por defecto; si es agente, proveedor distinto a los 3, sólo agrega, descarte con justificación escrita |
| 3 | "alto impacto vs menores" indefinido + clasificado por el autor | BLOCKER | claude | lista cerrada de disparadores + "ante duda, alto impacto" + auditoría del revisor |
| 4 | compuertas de vigencia/obligatoriedad presuponen corpus inexistente | BLOCKER/HIGH | claude+kimi | gate versionado: v1 = existe + cita coincide + fuente resuelta; vigencia entra con corpus temporal; default `[VIGENCIA-NO-VERIFICABLE]`; prohibir `alto` hasta entonces |
| 5 | gate no determinista extremo-a-extremo (extracción de claims = modelo) | HIGH | claude | salida estructurada (claim→cita→id) + medir recall de extracción vs golden |
| 6 | autoclasificación de datos sin control técnico ex-ante | HIGH | claude+kimi | allowlist machine-readable; router tmux filtra antes de enviar; log hash pre-invocación |
| 7 | vacío de régimen legal (LFPDPPP, retención/entrenamiento, transferencia intl. IMSS) | HIGH | claude | base jurídica + check ToS/retención por proveedor; prohibición dura (no autorizable) de datos personales |
| 8 | prompt idéntico = anclaje compartido; revisores pueden ver veredictos ajenos | HIGH | claude | revisión ciega + lentes por rol (corrección/viabilidad/seguridad-datos) |
| 9 | DoD "bootstrap devuelve proceed" es circular | MED/HIGH | claude+kimi | DoD = run ejecutado con ≥3 proveedores, hallazgos registrados y resueltos/aceptados por escrito, independiente del veredicto; validar sobre artefacto distinto |
| 10 | reasignación erosiona decorrelación | MED | claude+kimi | si <3 proveedores distintos → `PARCIAL (espera-humano)`, nunca `proceed` |
| 11 | sin regla de agregación | MED | kimi+claude | cualquier BLOCKER de cualquier proveedor bloquea; mayoría para MED |
| 12 | proveniencia debe ser por **modelo exacto**, no por CLI | LOW/MED | kimi | opencode/cline son herramientas, pueden correr el mismo modelo |
| 13 | `nivel medio` no acotado (consumidor, fail-closed) | MED | claude | definir quién consume `medio`; prohibir en contextos de decisión; fail-closed a `bajo` |
| 14 | ADR sin ciclo de vida (supersede/rollback) ni clases | MED | claude+kimi | estados `{propuesto, aceptado, supersedido, revertido}`; ADR estratégico (quórum §6) vs táctico (quorum-lite) |
| 15 | roles continuos sin autoridad/plazo; desempate unipersonal del responsable jurídico | MED | claude+kimi | interino = humano-promulgador; fecha límite; prohibir auto-asignación; desempate como ADR-lite con quorum-lite |
| 16 | v1.1 debe **prohibir exponer la plataforma a usuarios finales antes de v1.2** (golden set + runtime) | HIGH residual | claude | añadir prohibición explícita |

**Puntos fuertes (ambos):** la distinción gates-de-código vs gates-de-juicio, y la
auto-declaración honesta de la brecha residual. **Proveniencia por hallazgo** es lo que
vuelve el quórum verificable (kimi: a nivel de modelo, no de CLI).

## Decisión consolidada
**`fix-and-retry`** (unánime). Ningún hallazgo requiere rediseño arquitectónico — son
**precisión de reglas** (kimi). La dirección es correcta; la redacción promete más de lo
que la infraestructura sostiene hoy (claude).

## Próximo paso
1. Aplicar los fixes 1–16 a `enmienda-gobernanza-v1.1.md` (→ v1.1-revisada).
2. **No** re-validar sobre la misma enmienda (circular, hallazgo 9): la próxima validación
   multi-provider será sobre un **artefacto distinto** (p. ej. el verificador de citas del MVP).
3. Tras fixes, el humano reconcilia y decide adoptar (→ fusionar en `politica-agentes.md` v1.1).

---

## Revisión verbatim — claude (Anthropic)

```
Ver `enmienda-v1.1-bootstrap-reviews/claude-anthropic.md` (revisión completa, 36 lín.).
```
> Conflicto de interés declarado por el revisor: "Anthropic es parte del quórum... trátese
> como voto, no como árbitro."

## Revisión verbatim — kimi (Moonshot)

```
Ver `enmienda-v1.1-bootstrap-reviews/kimi-moonshot.md` (revisión completa, 50 lín.).
```
> Conflicto de interés declarado por el revisor: "soy uno de los proveedores del quórum
> propuesto... sesgo probable sobre-valorar la decorrelación."

> Las revisiones verbatim se persisten en el commit (evidencia auditable). El autor
> (opencode/glm-5.2) también es proveedor del quórum → esta síntesis es voto del autor,
> no veredicto árbitro. La reconciliación final es del humano (Cambio 1 corregido).
