# Revisión adversarial — kimi (Moonshot)

> Bootstrap enmienda v1.1 · 2026-08-06 · proveedor: Moonshot · CLI: \`kimi -p\` · rol: adversario · conflicto de interés declarado por el revisor.

---

• ## Hallazgos

  **Cambio 1 — quórum multi-provider**

  - [HIGH] El cierre de CAGF-A2 es parcial pero la enmienda lo declara con honestidad; el problema es que el DoD lo contradice — "[BLOCKER-ish incoherencia] `La brecha CAGF-A2 se declara como "parcialmente cerrada vía multi-provider" (no "no resuelta")`" obliga a rebajar la brecha *antes* de que exista evidencia de que el quórum funcionó (el run bootstrap es un solo ejercicio). — Fix: requerir N≥3 runs con logs de proveniencia archivados antes de redeclarar la brecha.
  - [HIGH] El quórum es verificable solo en intención: "el humano (o un meta-agente) reconcilia hallazgos" — un meta-agente reconciliador reintroduce un punto único de fallo *single-provider* (¿qué proveedor es el meta-agente? ¿quién revisa al reconciliador?). — Fix: especificar que la reconciliación de hitos de alto impacto es humana o, si es meta-agente, con proveedor distinto a los 3 del quórum y decisión registrada.
  - [MED] La reasignación por presupuesto erosiona la decorrelación silenciosamente: "Si un proveedor no tiene presupuesto/tokens, se reasigna el rol a otro disponible" — en la práctica todos los roles pueden colapsar a 1-2 proveedores disponibles y el reporte igual "pasó quórum". — Fix: si tras reasignar no hay ≥3 proveedores distintos, el hito queda `PARCIAL (espera-humano)`, no `proceed`.
  - [MED] No hay criterio de desempate ni umbral de acuerdo: ¿2 de 3 `proceed` con 1 `escalate` qué decide? El quórum sin regla de agregación es decorativo. — Fix: definir regla (p. ej. cualquier BLOCKER de cualquier proveedor bloquea; mayoría para MED).
  - [LOW] La salvedad "decorrelación de arquitectura ≠ datos de entrenamiento compartidos" es honesta y correcta; incluso podría ser más fuerte: varios de los CLIs listados (opencode, cline) son *herramientas*, no proveedores de modelo — pueden estar corriendo el mismo modelo subyacente, rompiendo la decorrelación. — Fix: exigir registrar modelo exacto (no CLI) en la proveniencia.

  **Cambio 2 — compuertas deterministas**

  - [HIGH] El verificador de citas es una *wish*: "(b) estaba vigente en la fecha jurídica relevante" presupone un corpus con historia de vigencias (reformas/abrogaciones DOF) que la propia plataforma aún no construye — la compuerta depende del sistema que gobierna. Es sound como especificación pero in-testeable como DoD hoy. — Fix: versionar el gate: v1 solo (a)+(c)+(d); (b) entra cuando exista timeline de vigencias, con `VIGENCIA-NO-VERIFICADA` como default obligatorio.
  - [MED] "bloquear o degradar" es ambiguo como gate determinista: ¿quién elige entre bloquear y degradar? Si elige el modelo, el gate no es determinista. — Fix: regla fija (p. ej. fallo en (a)/(c) → bloquear; fallo solo en (b) → degradar a `medio`).
  - [MED] La compuerta de obligatoriedad ("tesis aislada vs jurisprudencia") no es determinista en la práctica: clasificar obligatoriedad exige resolver metadatos SCJN (época, instancia, contradicción de tesis) que no se mencionan como insumo del corpus. — Fix: explicitar qué metadatos del corpus alimentan el gate y qué hace ante ausencia (default: no-vinculante).
  - [LOW] Los niveles alto/medio/bajo son operativos en definición, pero falta quién *consume* `response_status`: sin gate downstream que impida mostrar `medio` como definitivo, es etiqueta decorativa. — Fix: ligar niveles a la regla de "Fallo → bloquear o degradar".

  **Cambio 3 — manejo de datos**

  - [HIGH] Agujero de enforcement: todo el cambio es auto-declaración del agente ("El agente **declara** en el reporte qué contenido envió") — el mismo agente que clasifica es el que reporta, sin verificación. La clasificación `público/interno/personal` no tiene gate técnico (el Cambio 2 muestra que saben hacer gates en código; aquí no lo aplican). — Fix: lista de rutas/patrones permitidos (`público`) en config machine-readable; el router tmux filtra antes de enviar, no después.
  - [MED] "si aplica, anonimización/selección" deja al agente decidir cuándo aplica anonimizar datos internos IMSS — exactamente el juicio que la clasificación debía quitar. — Fix: `interno-institucional` → siempre anonimizado o denegado; sin discreción.
  - [LOW] No cubre retención/entrenamiento por parte del proveedor externo (los datos `públicos` están bien, pero los términos de API de cada CLI difieren). — Fix: declarar requisito de API sin-retención/no-training para cualquier contenido no público.

  **Cambio 4 — roles continuos**

  - [MED] Son cargos sin autoridad operativa, pero la enmienda lo maneja bien con `PARCIAL (espera-humano)`; el riesgo real es el inverso: que el "Responsable jurídico del corpus" pueda "desempatar discrepancias de fuentes" sin quórum §6 — una decisión jurídica unipersonal contradice el espíritu adversarial. — Fix: los desempates del responsable jurídico se registran como ADR-lite y pasan quorum-lite mínimo.
  - [LOW] No define quórum ni suplencia entre los tres roles; PO decide ADRs "vía Cambio 5" pero Cambio 5 exige quórum multi-provider para adoptarlos — circularidad menor: ¿quién redacta el ADR antes del quórum?

  **Cambio 5 — ADR**

  - [MED] Todo ADR como "hito de alto impacto" con quórum ≥3 proveedores no escala: decisiones tácticas menores (renombrar una fuente, cambiar un hash) pagarían quórum completo → presión para no registrarlas. — Fix: dos clases de ADR (estratégico → quórum §6; táctico → quorum-lite) con criterio explícito.
  - [MED] Sin proceso de rollback/supersede: el schema tiene `estado` pero no dice qué valores ni cómo se revierte una decisión adoptada que resultó errónea. — Fix: estados `{propuesto, aceptado, supersedido, revertido}` + regla de que revertir un ADR es otro ADR de la misma clase.

  **Faltante transversal**

  - [HIGH] El DoD "Un run debootstrap del quórum multi-provider sobre esta enmienda devuelve `proceed`" es circular: esta misma ronda adversarial *es* ese run; si la enmienda se adopta tras ella, el check se auto-cumple sin evidencia de operativa real. — Fix: exigir run sobre un artefacto *distinto* (p. ej. el verificador de citas) antes de declarar CAGF-A2 parcialmente cerrada.
  - [MED] v1.2 difiere "gobernanza de runtime" y "golden set", pero el verificador de citas (Cambio 2) ya depende de ambos; el ordenamiento de dependencias es frágil. — Fix: declarar explícitamente que los gates de Cambio 2 se activan progresivamente.

  ## Punto fuerte

  La auto-declaración honesta de la brecha residual ("se declara como mejora parcial, no cumplimiento pleno") y el principio "Estos gates son **code**, no prompts" son exactamente la postura correcta: la enmienda no se engaña sobre lo que cierra y exige DoD ejecutable.

  ## Decisión

  - [ ] proceed  |  [x] fix-and-retry  |  [ ] escalate

  ## Nota residual

  Conflicto de interés declarado: soy uno de los proveedores del quórum propuesto. La dirección es correcta y adoptable en espíritu, pero hay 3 HIGH operativos (DoD circular, reconciliador single-point, datos por auto-declaración) que convierten piezas clave en decorativas si se fusionan tal cual. Ninguno requiere rediseño — son precisión de reglas, no de arquitectura. Mi sesgo probable: sobre-valorar la decorrelación de proveedores por ser parte del mecanismo; compensado al exigir proveniencia a nivel de modelo, no de CLI.

