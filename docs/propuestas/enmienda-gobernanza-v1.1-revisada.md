# Enmienda de gobernanza v1.1-revisada (fixes del bootstrap aplicados)

> **Estado:** Propuesta revisada — pendiente de **ronda multi-provider sobre OTRO artefacto**
> (no sobre sí misma, sería circular) + reconciliación humana.
> **Base:** `docs/politica-agentes.md` v1.0. **Fecha:** 2026-08-06. **Autor:** opencode (glm-5.2).
> **Evidencia del bootstrap:** `docs/propuestas/enmienda-v1.1-bootstrap.md` + reviews verbatim
> (claude/Anthropic, kimi/Moonshot). **Relatoría:** `docs/relatorias/2026-08-06-bootstrap-multi-provider.md`.

## Changelog (16 fixes del bootstrap)
1. Título/DoD: "cierra CAGF-A2" → **"mitiga parcialmente"**; redeclarar la brecha exige N≥3 runs **sobre artefactos distintos**. · 2. Reconciliador = **humano por defecto**; si agente, **4º proveedor distinto, sólo agrega** (descarte con justificación escrita). · 3. **"Alto impacto" = lista cerrada** + "ante duda, alto" + audita el revisor. · 4. Gates **versionados** a la existencia del corpus; default `[VIGENCIA-NO-VERIFICABLE]`; prohibir `alto` sin corpus temporal. · 5. Salida **estructurada** (claim→cita→id) + **medir recall** de extracción. · 6. Datos: **allowlist + router ex-ante + log de hash**. · 7. **Base jurídica + ToS/proveedor + prohibición dura de datos personales**. · 8. **Revisión ciega + lentes por rol**. · 9. **DoD no circular** (independiente del veredicto; artefacto distinto). · 10. **<3 proveedores → `PARCIAL`, nunca `proceed`**. · 11. **Regla de agregación** (cualquier BLOCKER bloquea; mayoría para MED). · 12. Proveniencia por **modelo subyacente**, no por CLI. · 13. Nivel `medio` **acotado + fail-closed a `bajo`**. · 14. ADR con **estados + clases estratégico/táctico + rollback**. · 15. Roles: **interino = humano-promulgador, deadline, no auto-asignación**; desempate jurídico = **ADR-lite quorum-lite**. · 16. **Prohibir exponer la plataforma a usuarios finales antes de v1.2.**
> LOW adicionales (anotados, no bloqueantes): inyección de prompt desde PDFs/DOF del corpus; presupuesto/costo por hito; descargo "no constituye asesoría jurídica"; resolver referencias internas (check_sizes, §7.1, ADR-0001).

## Cambio 1 — §6: quórum adversarial multi-provider (MITIGA parcialmente CAGF-A2)

> Sustituye la "Brecha declarada" de §6. No cierra A2: lo **mitiga parcialmente** con evidencia.

- **Decorrelación real de arquitectura:** para hitos de **alto impacto**, quórum de **≥3 proveedores distintos** (autor excluido + adversario + árbitro, cada uno de un proveedor diferente, identificado por **modelo subyacente**, no por CLI — opencode/cline son herramientas y pueden correr el mismo modelo). Hito **menor** = quorum-lite (1 revisor en contexto fresco, proveedor distinto si es factible).
- **"Alto impacto" = lista cerrada de disparadores:** cambios a la política, ADRs estratégicos, compuertas de fidelidad, corpus normativo, despliegue a usuarios. Regla **"ante la duda, alto impacto"**; la clasificación la **audita el revisor** (no la decide en solitario el autor).
- **Reconciliación:** por defecto **humana**. Si es un agente, debe ser de un **proveedor distinto a los 3 del quórum**, sólo puede **agregar** hallazgos; todo **descarte requiere justificación escrita**.
- **Regla de agregación:** **cualquier BLOCKER de cualquier proveedor bloquea** (`fix-and-retry`); para MED, **mayoría** de los revisores.
- **Reasignación:** si un proveedor no tiene presupuesto/tokens y, tras reasignar, quedan **<3 proveedores distintos**, el hito queda **`PARCIAL (espera-humano)`, nunca `proceed`**.
- **Ceguera + lentes:** los revisores **no ven** las salidas ajenas; cada rol recibe un **lente** distinto (corrección / viabilidad / seguridad-de-datos) para evitar anclaje por prompt compartido.
- **Brecha residual (honestidad A8/A10):** la decorrelación es de **arquitectura de modelo**, no de **datos de entrenamiento**; se declara **mitigada parcialmente**. Redeclararla como "mayormente cerrada" exige **≥3 runs con proveniencia archivada sobre artefactos distintos**.
- **Operativa (tmux):** una sesión lanza cada CLI en un pane con prompt+artefacto (filtrado por Cambio 3); cada salida se captura con su proveedor/modelo; se persiste como evidencia auditable.

## Cambio 2 — Compuertas deterministas + niveles de confianza (versionadas)

§7 es binario y sus gates son no-deterministas (§6). Se añaden gates **deterministas en código**, **versionados** a la existencia de su corpus (no aspiracionales):

- **Verificador de citas — por versiones:**
  - **v1 (hoy, sin corpus temporal):** (a) la disposición **existe** en el corpus, (c) el fragmento citado **coincide** con el corpus, (d) la fuente oficial está **resuelta**. Default `[VIGENCIA-NO-VERIFICABLE]`. **Prohibido** emitir nivel `alto`.
  - **v2 (con corpus temporal):** añade (b) estaba **vigente en la fecha jurídica relevante** (reformas/transitorios/DOF). Hasta entonces, (b) se marca, no se afirma.
- **Determinismo extremo-a-extremo reconocido:** la **extracción** de afirmaciones normativas de texto libre es **juicio del modelo** (eslabón no determinista). Se exige **salida estructurada** `claim → cita → id de disposición` y se **mide el recall de extracción** contra el golden set. El gate determinista actúa **sobre la estructura**, no sobre el texto libre.
- **Regla fija block/degrade:** fallo en (a)/(c) → **bloquear**; fallo sólo en (b) → **degradar a `medio`**. El modelo **no elige** entre bloquear y degradar.
- **Compuerta de obligatoriedad:** requiere metadatos SCJN explícitos (época, instancia, contradicción); ante ausencia, **default = no vinculante**.
- **Niveles de confianza:** `alto` (citas verificadas + vigencia confirmada), `medio` (verificación parcial / vigencia no verificada — **prohibido en contextos de decisión**, consumible sólo como borrador), `bajo` (sin respaldo → no se emite como respuesta). Si el verificador falla o no está disponible → **fail-closed a `bajo`**.
- Estos gates son **code**: su corrección se prueba (DoD ejecutable) y ellos mismos pasan ronda adversarial §6 al implementarse.

## Cambio 3 — Manejo de datos en revisión multi-provider (extiende §7.1)

- **Clasificación ex-ante por configuración machine-readable** (no por el agente que envía): **allowlist** de rutas/repos ruteables (`público`: leyes/DOF/Cámara/SCJN, docs de gobernanza); **denylist por defecto** para todo lo demás. El **router tmux filtra antes de invocar** el CLI y **registra un hash** del contenido enviado.
- `público` → enrutamiento permitido. `interno-institucional` (manuales, Normateca, procedimientos IMSS) → **siempre anonimizado o denegado, sin discreción del agente** + requiere **autorización explícita del humano**. `personal/confidencial` → **prohibición dura: no enrutable, no autorizable por el agente**.
- **Régimen legal:** base jurídica (LFPDPPP) + **check de ToS/retención por proveedor**; para contenido no-público se exige **API sin retención / sin entrenamiento**. Se declara transferencia internacional cuando el proveedor esté fuera de México.
- El agente **declara** en el reporte qué contenido envió, a qué proveedor/modelo, con qué hash.

## Cambio 4 — Roles operativos continuos (extiende §5/§7)

- **Interino por defecto = humano-promulgador** (asume los tres roles hasta el nombramiento); **fecha límite** de designación; **prohibido** que el agente se autoasigne o simule estos roles.
- Roles: **Responsable jurídico del corpus** (desempata discrepancias de fuentes —sus desempates son **ADR-lite con quorum-lite**), **Custodio/data steward** (mantenimiento continuo, hashes, procedencia, bitácora), **Product owner** (decide dirección/alcance vía ADRs del Cambio 5).
- Mientras no estén designados, las decisiones que los requieren quedan `PARCIAL (espera-humano)`.

## Cambio 5 — Decisiones estratégicas (ADR)

- Todo ADR en `docs/adr/NNNN-*.md` con `{contexto, decisión, consecuencias, alternativas, estado, ítems abiertos}`.
- **Estados:** `{propuesto, aceptado, supersedido, revertido}`. **Revertir** un ADR = otro ADR de la misma clase. Campo "señal de reversión".
- **Dos clases:** **estratégico** (producto/arquitectura/alcance/política → quórum §6 multi-provider) y **táctico** (renombrar fuente, cambiar hash → quorum-lite) con criterio explícito. Criterio: si toca contrato público, norma publicada o despliegue → estratégico.

## Transversal — DoD y prohibición de despliegue

- **DoD no circular:** la adopción de esta enmienda requiere un run multi-provider con **≥3 proveedores** sobre **un artefacto distinto** (p. ej. el verificador de citas del MVP), con hallazgos **registrados y resueltos/aceptados por escrito**, **independientemente del veredicto**. El `proceed` no es la meta.
- **Prohibición de exposición temprana:** v1.1 **prohíbe exponer la plataforma a usuarios finales** antes de v1.2 (golden set validado + gobernanza de runtime). Mientras tanto, sólo uso interno/borrador con HITL.

## Pendiente para v1.2 (no bloquea v1.1; v1.1 prohíbe exponer antes de tenerlos)
- Gobernanza del **golden set / evaluación jurídica** (validación por especialistas, métricas).
- Capa de **gobernanza de sistema desplegado/runtime** (identificación por respuesta, evidencia por conclusión, aprobación de despliegue).

> Esta enmienda revisada es **propuesta**. Su adopción es un hito de alto impacto: se valida
> con el quórum multi-provider sobre **otro artefacto** (no sobre sí misma) y la reconciliación
> final es del humano (§7.2: redactar/analizar ≠ adoptar).
