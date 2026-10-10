# CTIM RS1 — AN-KLA beta.29 en el consumidor

Observado el 2026-10-10, hasta 19:17 UTC. Estado: **BLOQ para activar el
checkpoint CTIM canónico**. Este recibo no aprueba el procedimiento RS1 ni
amplía su custodia.

## Versión y actualización

La `.venv` de expertoGobernanza instaló `an-kla-memory` `0.1.0b29` desde la
etiqueta remota exacta `v0.1.0-beta.29`; `direct_url.json` registra el commit
`366c0d22c393ca1619612ed6d9fef5308fc73b7e`. El tag anotado remoto resuelve
a ese commit. Se ejecutó `upgrade inspect` → `upgrade apply` → `upgrade verify`
y `rebuild-index`. La plantilla gestionada de `AGENTS.md` permanece en beta.26.
La inspección detectó cambio fuera del bloque gestionado; el archivo actual
coincidía con `origin/main`, y `apply --confirm-target-drift` absorbió esa
línea base sin cambiar `AGENTS.md` ni `AN-KLA.md`. `upgrade verify` devolvió
`ok=true`, identidad `complete` y store rev. 29,
`sha256:05b09449af7aafe833fb421596138d5ce2146d7ce5bc8092a2a32472ec6b5cf1`.
El checkpoint canónico seguía en v1, con `goal` y `next` vacíos. No se escribió
en él.

## Repetición aislada

Store sintético nuevo: `/tmp/ctim-ankla-b29-isolated-78uggxmd` (efímero, no
respaldo). Con el mismo estado sintético del
[recibo beta.28](ctim-rs1-ankla-isolated-test-receipt-2026-10-10.json):

| Control | Resultado observado |
| --- | --- |
| JSON de caller que declara `channel_confirmed`/`issuer.kind=channel` | `checkpoint plan` salió 1 con `channel_confirmed_requires_adapter`; revisión inicial intacta. |
| Autoridad `model_derived` sintética | `plan` decidió `write`; `commit` registró tx `877fa8d3-daa5-4027-b5ae-cc2f0672ff4b`. |
| Verificación y recuperación | `verify.ok=true`, rev. 1; `resume` recuperó el objetivo sintético; `transaction inspect` encontró el commit. |
| CAS obsoleto | Reutilizar plan y revisión inicial salió 1 con `checkpoint_plan_base_changed`. |

`transaction inspect` demuestra consulta del resultado registrado; no se
simuló un timeout real. Se releyeron las 21 referencias del
[manifiesto local](ctim-rs1-local-continuity-manifest-2026-10-10.json): todas
seguían presentes y coincidían en tamaño y SHA-256. Su política sólo permite
recuperación mientras existan esos archivos y hasta `2026-10-11T16:00:00Z`;
la comprobación actual no asegura disponibilidad posterior.

## Gate restante

El CLI y la API de checkpoint de beta.29 reciben una autoridad JSON del caller.
El ensayo anterior comprobó el rechazo de `channel_confirmed`; la política
instalada también codifica el rechazo de `tool_observed` sin adaptador del host,
pero aquí no se ejecutó ese control. `emit-authority-template` ofrece
`model_derived`, que no acredita la decisión humana del Operador. El mecanismo
`attest` de observación local
tampoco acredita por sí mismo un mensaje humano. Para un checkpoint con
autoridad humana hace falta un adaptador confiable que vincule una confirmación
del canal a la propuesta, revisión, alcance y emisor, y verifique ese vínculo
en plan y commit. No se degradó la autorización a `model_derived`.

El [contrato CTIM propuesto](../propuestas/ctim-rs1-ankla-continuity-v0.1.md)
también deja pendientes dueño y acuse de relevo, serialización del archivo
compartido, ubicación recuperable de recibos y aceptación bilateral. La
lectura y retoma manual desde los archivos locales está disponible dentro
de la ventana de custodia comprobada; **el contrato de continuidad CTIM no
está activo**.
