# CTIM RS1 — preflight local de continuidad AN-KLA

Fecha: 2026-10-10. Estado: **BLOQ para activación**; documento de evidencia,
no aceptación del procedimiento ni del contrato operativo.

## Alcance y referencias

El [manifiesto local](ctim-rs1-local-continuity-manifest-2026-10-10.json)
enumera 21 archivos con ruta, tamaño y SHA-256. Se releyeron los 21 y se
verificaron sus hashes; los paquetes de páginas 18 y 21 enlazan con el SHA del
PDF, del derivado, del resultado y de la selección de citas. El manifiesto no
incluye bytes del PDF, pasajes ni conversaciones. Las rutas sólo son recuperables
en este Mac mientras existan los archivos originales. La política Skopos para
el borrador vence `2026-10-11T16:00:00Z`, usa
`verified_external_reference` y no demuestra recuperación tras ese plazo.

## Ensayo de checkpoint en store aislado

Se creó un store sintético separado del consumidor con AN-KLA `0.1.0b28`.
El [recibo saneado](ctim-rs1-ankla-isolated-test-receipt-2026-10-10.json),
SHA-256 `95dc6beb8b178e89623fa08c98d9a4b18d567f48c88b431d0ab5f56d7efde30b`,
conserva estado y autoridades sintéticas, decisiones, consultas de transacción,
salidas de `verify`/`resume` y el rechazo CAS. Identifica el store aislado
observado; ese directorio temporal no es un archivo de respaldo.
Un `working-state-v2` con autoridad `model_derived` obtuvo `decision=write`;
`checkpoint commit` registró la transacción
`bf326403-cd51-461f-9b04-b64ef6be0644`. `verify` y `resume` pasaron; el
resultado de esa transacción fue localizable con `transaction inspect`.
Reintentar el plan con revisión anterior falló con
`checkpoint_plan_base_changed`. `inspect` prueba consulta del journal, no un
timeout real ni recuperación de una respuesta perdida.

**Bloqueo:** un JSON de autoridad preparado por el caller declaró
`channel_confirmed` e `issuer.kind=channel` sin adaptador del host. Aun así,
`checkpoint plan` devolvió `decision=write` y `checkpoint commit` registró la
transacción `3e8f2e94-2353-4885-be44-6a96a5dd3d9b` en ese store aislado.
El control negativo de autoridad falsa falló. No se replicó en el store
canónico; éste permanecía en revisión 29,
`sha256:05b09449af7aafe833fb421596138d5ce2146d7ce5bc8092a2a32472ec6b5cf1`,
al observarlo. El productor AN-KLA debe corregir y verificar la política
central antes de repetir la prueba y considerar un checkpoint CTIM real.

## Límite de activación

El contrato publicado sigue **PROPUESTO**. La decisión del Operador autoriza
un piloto CTIM acotado *cuando pasen* custodia recuperable, autoridad y ensayo;
no convierte este preflight en aceptación bilateral ni coordinación automática.
Un archivo con SHA y acuse no serializa escrituras entre agentes. La activación
debe quedar limitada al plazo de custodia vigente y a una retoma manual en este
Mac, si finalmente se verifican todos los controles.
