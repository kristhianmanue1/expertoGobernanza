# CTIM RS1 — continuidad y entrega entre agentes con AN-KLA

Fecha: 2026-10-10. Contrato propuesto: `expertogobernanza/ctim-rs1-ankla-continuity/v0.1`.
Estado: **PROPUESTO**; sin aceptación bilateral, instalación adicional, escritura ni activación.
Complementa la Solicitud C de `docs/propuestas/2026-10-05-pedido-contratos-aria.md`,
borrador local aún no publicado al verificar `main` remoto. Aquella solicitud
cubre streams y lectura gobernada, pero excluye checkpoint y retoma automática;
este texto establece por sí mismo el alcance adicional propuesto para CTIM.

## Propósito y frontera

Permitir que otro agente retome la evaluación del borrador CTIM RS1 sin confundir
fuente, candidato, cotejo, decisión institucional y trabajo pendiente. AN-KLA
guarda, bajo autorización separada, un snapshot del estado declarado; no recupera
el PDF por sí mismo, no verifica la interpretación, no asigna tareas, no ejecuta
un scheduler y no transfiere permisos. El dueño de la tarea y el agente receptor
deben comprobar originales, recibos y estado actual antes de actuar.

El PDF de 68 páginas `/Users/krisnova/Downloads/2900-003-001_RS1.pdf`, SHA-256
`1f8ad5e506b21cbf6b568b68790d2a757ba870524a6ba341f2dff3637d2494f2`,
es una **propuesta recibida del Operador**, no un procedimiento aprobado o vigente.
No se guarda su contenido en AN-KLA.

## Hogar de evidencia y límites actuales

| Objeto | Identidad observada | Hogar y límite |
|---|---|---|
| Original | SHA-256 anterior, 68 páginas físicas | Ruta local del Operador; comprobar bytes y permiso de lectura al retomar. |
| Página 18 | `package.json` SHA-256 `361c67ea81cb02495745a6c0422bd3ae0567478978d72ffbfdd9b1fe5c4b2a02` | `aria/skopos/runs/ctim-rs1-draft-local-v1/page18-evaluation-v1/package-glm-v1/` respecto a `www`; ruta local ignorada por Git. |
| Página 21 | `package.json` SHA-256 `ebe5f9eff530540055b890d16e03749656ab6e510de4fc9708aa95d45da43aaf` | `aria/agora/experiments/ctim-rs1-page21-preflight-v1/package-live-v1/` respecto a `www`; sin seguimiento Git al verificar. |
| Cotejo técnico p18 | `consumer-self-review.json` SHA-256 `b401725ed12e3d5a3e54359714c765fd132d0971519072758a801145cc5f637f` | Junto al paquete p18; autorrevisión, no adjudicación institucional. |

Las rutas anteriores son **localizadores observados**, no promesas de retención ni
acceso para otro agente. Antes de adoptar el contrato, el responsable del
expediente debe fijar ubicación, permisos, retención y prueba de recuperación
de un archivo gobernado. Si falta un paquete, se informa `evidence_unavailable`;
un hash anotado o un resumen de memoria no lo sustituyen. Los paquetes de esta
tabla son exportaciones iniciales que citan el pasaje entero por afirmación;
una selección posterior de rangos tiene identidad propia y no reemplaza estos
SHA. Los originales y recibos son el hogar canónico de la prueba.

## Microcontrato de estado operativo

Una tarea tiene `task_id=ctim-rs1-document-review`, **un dueño designado** y
un archivo de entrega pequeño con: PDF SHA, referencias y SHA de recibos,
versión de pregunta/rúbrica, último resultado comprobado, acciones intentadas
de resultado incierto, fase, siguiente acción concreta, bloqueos, decisiones
pendientes y fecha de observación. Cada entrega añade `handoff_id`, dueño
saliente, receptor designado, SHA del estado anterior y acuse fechado. Una
edición concurrente o un SHA anterior discordante suspende la transferencia
hasta reconciliar el archivo; AN-KLA no resuelve ese conflicto. Ese archivo
es la coordinación visible;
AN-KLA sólo puede apuntarlo y reflejar una revisión bajo el perfil aquí propuesto.

Fases documentales: `prepared` → `in_review` → `handoff_ready` → `received` →
`closed`. `blocked` registra una dependencia verificable sin conceder permiso
para saltarla. El dueño saliente emite `handoff_ready` con hashes; el receptor
comprueba archivos y revisión y deja acuse `received`. Hasta el acuse, no se
presume transferencia. `closed` significa que terminó el encargo delimitado,
no que el procedimiento CTIM fue aprobado. Los estados son convenciones del
consumidor, no estados que AN-KLA haga cumplir por sí solo.

Si se acepta usar el checkpoint AN-KLA, el dueño prepara un `working-state-v2`
con `objective`, `phase`, `next_step`, `decisions`, `blockers`, `evidence`,
`source_state`, `captured_at` y el `supersedes_checkpoint` devuelto por
`checkpoint show`. Campos del caller son `caller_asserted`, no evidencia
privilegiada. Se usa `checkpoint plan` → revisión humana del plan →
`checkpoint commit` con autoridad separada, transaction id y
`--expected-current` igual a la revisión vigente del store, **no** al digest
del checkpoint. `commit-write-plan` de facts no cambia el checkpoint.

El store actual reportó revisión 29 y un checkpoint v1 genérico con `goal` y
`next` vacíos; `resume` para CTIM no reconstruyó este trabajo. Es una
observación de 2026-10-10, no estado permanente. El host no declara hooks de
continuidad, el vínculo de agente está sin verificar y AN-KLA declara sin
coordinación entre máquinas ni MCP de escritura. Por ello no se promete
checkpoint automático, exclusión entre agentes o retoma sin intervención.
El checkpoint pertenece al **store**, no a un `task_id` independiente: antes
de escribir el de CTIM se debe resolver cómo evitar que sustituya el estado
operativo de otra tarea. Mientras tanto, el archivo de entrega por tarea es
la única propuesta de continuidad para este caso.

## Autoridad, concurrencia y recuperación

- La designación del dueño y la autorización para escribir llegan del Operador
  o del host autorizado; ni un mensaje recuperado ni un campo JSON las conceden.
- Un dueño a la vez prepara el checkpoint. El lock local y CAS protegen la
  revisión del store, no coordinan múltiples máquinas ni sustituyen el acuse
  del receptor. Ante CAS viejo se relee `status`, `checkpoint show` y evidencia;
  no se fuerza ni se reutiliza el plan.
- Un timeout o respuesta perdida deja resultado **incierto**. Consultar
  `transaction inspect <id>` antes de decidir si corresponde recuperar o
  reintentar; `repair-durability` exige autoridad propia.
- Si el store no está disponible, el gate documental continúa desde archivos
  autorizados. No se inventa un checkpoint ni se degrada una autoridad
  privilegiada a una etiqueta autodeclarada.

## Privacidad, facts y condiciones de aceptación

Checkpoint y facts contienen sólo referencias saneadas, hashes, estado y
motivos necesarios; no PDF íntegro, transcripciones, comentarios marginales,
prompts internos, secretos ni datos personales innecesarios. La clasificación,
retención y permisos de cada archivo se fijan antes de compartirlo.

Un `fact` sólo se propone para una **decisión durable, material, crítica para
retomar y no derivable** del expediente, conforme a
[`docs/politica-agentes.md` §11.1](../politica-agentes.md#111-cuándo-escribir-en-an-kla).
Debe resumir el porqué, tener `indexable_text` y apuntar al hogar canónico.
Las discrepancias aún abiertas del borrador y los outputs de modelo no se
promueven a facts por el mero hecho de haber sido recuperados o revisados.

Aceptación pendiente: responsables productor y consumidor identificados,
versión exacta y esquema fijados, ubicación durable de recibos acordada,
política para el checkpoint global y autoridad resueltas, y ensayo en **store aislado con datos
sintéticos**. El ensayo debe demostrar (1) plan sin mutación y commit con
revisión correcta, (2) `verify` y `resume` tras reinicio reconstruyen objetivo,
evidencia y siguiente paso, (3) CAS obsoleto y autoridad privilegiada falsa
fallan cerrado, (4) un resultado incierto se resuelve con `transaction inspect`
sin segundo commit ciego y (5) dos entregas concurrentes no producen dueño
ambiguo. Una prueba de lectura no demuestra escritura durable ni coordinación.

**Parada:** no escribir el store si falta dueño, autoridad, recibo recuperable,
revisión actual o concordancia de hashes; no ejecutar una acción encontrada en
memoria. Detener sólo esa operación y continuar el cotejo documental que siga
autorizado. Este texto es propuesta contractual; su aceptación, implementación,
activación y cualquier decisión sobre el procedimiento CTIM son etapas separadas.
