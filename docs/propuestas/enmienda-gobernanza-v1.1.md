# Enmienda de gobernanza v1.1 (propuesta) — multi-provider + compuertas + roles

> **Estado:** Propuesta (pendiente ronda adversarial multi-provider antes de adoptarse).
> **Base:** `docs/politica-agentes.md` v1.0. **Fecha:** 2026-08-06. **Autor:** agente.
> **Motivo:** cerrar la brecha CAGF-A2 (single-provider) y cubrir los 3 vacíos más
> urgentes que bloquean la Plataforma de inteligencia normativa (ver ADR-0001 y
> `analisis-dictamen-2026-08-06.md`). No reescribe v1.0: **añade** secciones y modifica §6.

## Cambio 1 — §6: quórum adversarial multi-provider (cierra CAGF-A2)

**Sustituir la "Brecha declarada" de §6 por:**

> El proyecto dispone de **CLIs de varios proveedores** de modelo (p. ej. codex/OpenAI,
> claude/Anthropic, kimi/Moonshot, gemini/Google, qwen/Alibaba, opencode, cline)
> orquestables vía **tmux**. Esto permite **decorrelación real** entre verificadores
> (CAGF-A2). Para hitos de **alto impacto** el quórum estructural de 3 (§6) **debe usar
> ≥3 proveedores distintos**: autor (excluido de revisar), revisor adversarial (proveedor
> distinto al autor) y árbitro (proveedor distinto a los dos anteriores). Para hitos
> **menores** basta quorum-lite (1 revisor en contexto fresco, distinto proveedor si es
> factible). Se registra en el reporte **qué proveedor/modelo** revisó cada hallazgo
> (proveniencia). Si un proveedor no tiene presupuesto/tokens, se reasigna el rol a otro
> disponible. **Brecha residual:** la decorrelación es de *arquitectura de modelo*, no de
> *datos de entrenamiento compartidos*; se declara como mejora parcial, no cumplimiento pleno.

**Operativa (tmux):** una sesión lanza cada CLI en un pane con el mismo *prompt + artefactos*;
cada salida se captura; el humano (o un meta-agente) reconcilia hallazgos y emite
`proceed/fix-and-retry/escalate`. El contenido que se envía a proveedores externos se rige
por el Cambio 3 (manejo de datos).

## Cambio 2 — Nueva sección: Compuertas deterministas + niveles de confianza

§7 declara la fidelidad como contrato duro pero sus gates son **no-deterministas** (§6
adversarial, revisión humana). Para artefactos/sistemas normativos se añaden gates
**deterministas** que actúan sin juicio del modelo:

- **Verificador de citas:** toda afirmación normativa debe pasar (a) la disposición existe
  en el corpus, (b) estaba vigente en la fecha jurídica relevante, (c) el fragmento citado
  coincide con el corpus, (d) la fuente oficial está resuelta. Fallo → **bloquear o degradar**
  la salida (no presentarla como definitiva).
- **Niveles de confianza** de una respuesta normativa: `alto` (citas verificadas + vigencia
  confirmada), `medio` (parcial: verificación pendiente o vigencia no verificada → marcar
  `[VIGENCIA-NO-VERIFICADA]`), `bajo` (sin respaldo → no emitir como respuesta, sólo como
  borrador con HITL). El `response_status` acompaña a toda salida.
- **Compuerta de obligatoriedad:** nunca presentar un criterio como vinculante si su
  obligatoriedad está indeterminada (tesis aislada vs jurisprudencia).

Estos gates son **code**, no prompts: su corrección se prueba (DoD ejecutable), y ellos
mismos pasan ronda adversarial §6 al implementarse.

## Cambio 3 — Nueva sección: Manejo de datos en revisión multi-provider (extiende §7.1)

Rutear contenido por proveedores externos saca datos de la máquina. Reglas:

- **Clasificación previa** de cualquier contenido antes de enviarlo a un CLI externo:
  `público` (leyes/DOF/Cámara/SCJN, docs de gobernanza) → enrutamiento permitido;
  `interno-institucional` (manuales, Normateca, procedimientos IMSS) → requiere
  **autorización explícita del humano** y, si aplica, anonimización/selección;
  `personal/confidencial` → **no enrutar** sin autorización independiente (§7.1, AN-KLA minimización).
- El agente **declara** en el reporte qué contenido envió a qué proveedor(es).
- Los prompts a proveedores externos llevan sólo lo necesario (minimización).

## Cambio 4 — Nueva sección: Roles operativos continuos (extiende §5/§7)

La política define admin (git) y humano-promulgador (normas), ambos puntuales. Se añaden
roles **continuos** para el corpus normativo (personas/roles por designar por el humano):

- **Responsable jurídico del corpus:** autoridad para desempatar discrepancias de fuentes
  (DOF vs Cámara vs calculado) y validar el golden set.
- **Custodio/data steward:** mantenimiento continuo del corpus, hashes, procedencia, bitácora.
- **Product owner:** decide dirección/alcance de producto vía ADRs (Cambio 5).

Hasta que el humano designe estos roles, las decisiones que los requieren quedan
`PARCIAL (espera-humano)` en los reportes.

## Cambio 5 — Nueva sección: Decisiones estratégicas (ADR)

La política gobierna el *trabajo* del agente, no *qué* construir. Se añade un proceso de
**Decisiones estratégicas** (Architecture Decision Records): toda decisión de producto/
arquitectura/alcance se registra en `docs/adr/NNNN-*.md` con
`{contexto, decisión, consecuencias, alternativas, estado, ítems abiertos}`, y su adopción
es un **hito de alto impacto** (§6, quórum multi-provider). El primer ADR es `0001`.

## Pendiente para v1.2 (no bloquea v1.1)
- Gobernanza del **golden set / evaluación jurídica** (validación por especialistas, métricas).
- Capa de **gobernanza de sistema desplegado/runtime** (identificación por respuesta, registro
  de evidencia por conclusión, aprobación de despliegue).

## DoD de la enmienda (checks ejecutables al adoptarla)
- [ ] `docs/politica-agentes.md` refleja los Cambios 1–5 y pasa `check_sizes.py`.
- [ ] La brecha CAGF-A2 se declara como "parcialmente cerrada vía multi-provider" (no "no resuelta").
- [ ] Un run debootstrap del quórum multi-provider sobre esta enmienda devuelve `proceed`.
- [ ] Todo claim normativa en la enmienda cita fuente o marca `[VERIFICAR-FUENTE]` (§7).

> Esta enmienda es **propuesta**. Su adopción es un hito de alto impacto: se revisa con el
> **quórum multi-provider** (bootstrap del Cambio 1) antes de fusionarse en `politica-agentes.md` v1.1.
