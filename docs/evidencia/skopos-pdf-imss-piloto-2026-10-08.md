# Evidencia de admisión bilateral PDF IMSS — 2026-10-08

**Estado:** admisión técnica y recuperación tras reinicio observadas y
cotejadas por ambos agentes. No es aprobación jurídica o ingreso al
corpus. Cliente: `scripts/skopos_pdf_pilot.py`; host Skopos dedicado al piloto.
El productor publicó su [acta bilateral](https://github.com/kristhianmanue1/skopos/blob/e3cce1873cc73048ec18740e07166784df67b7bd/docs/evidencia/pdf-custody-imss-pilot-2026-10-08.md)
en Skopos `e3cce1873cc73048ec18740e07166784df67b7bd`. Esta referencia
identifica el código y acta publicados, no un servicio encendido permanente.

## Entorno y ejecución

El consumidor leyó los bytes locales y comprobó SHA-256/longitud del PDF y SHA
de la ficha antes de llamar al host. `requests_root` vive bajo
`runs/pdf-custody-imss-pilot-v1/requests` ignorado por Git. Skopos configuró
socket, política y Mongo replica set dedicado en sus `runs/`; la conexión usa
loopback/socket local y la misma identidad de OS. El primer intento quedó
bloqueado por el sandbox de la tarea (`PermissionError: Operation not permitted`)
antes de conectar. Un reintento con permiso específico para el socket terminó
con código cero. Ese permiso no cambia la política de Skopos.

El cliente exigió `describe_capabilities` compatible y ejecutó admisión,
consulta de recibo y recuperación. Su salida de resultado fue:

| Dato | Valor observado |
| --- | --- |
| Contrato / host | `expertogobernanza/skopos-source@v0.2` / `skopos/pdf-custody-host/v0.1` |
| Política | `expertogobernanza/imss-2000-002-001-reference@v0.2-2026-10-08` |
| Admisión | `admitted`; solicitud `imss-2000-002-001-r1-admit-v1` |
| SHA-256 de solicitud admitida | `4fbed2bd3d2633aafc2646e8369e0227610d37672cee2f048b7a9b1b3dde870a` |
| Recibo | `expertogobernanza:imss-2000-002-001:1:4fbed2bd3d2633aa` |
| PDF recuperado | 1,311,822 bytes; SHA-256 `719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`; comparación byte por byte positiva |
| Ficha local | SHA-256 `f934b0ec1bfbe97aae347b86bb3aa4e0831af79f704e571c27702f9203b62bff` |

La consulta de recibo con SHA de admisión falso obtuvo
`invalid_input/revision_conflict`. Una solicitud de admisión de
`other-in-same-project` con la misma revisión y hash recibió
`invalid_input/material_not_allowed`; digest de esta solicitud negativa
`065f5824a9b54ab8ddc4852b8e822d4c07a25a14e2d7deccab9368541d7171ec`.
Estos resultados no prueban aislamiento frente a un proceso que comparte
usuario, shell y posibles credenciales.

Skopos informó un cotejo separado del consumidor en su Mongo: una revisión y una cabeza,
recibo idéntico, `record_sha256=0cc590c6e4f278c4350665526d8ee63732494afb977d4a97472e328b6b6f3ffb`,
salida byte por byte idéntica; retiró únicamente el archivo temporal
`imss-pdf-61bbac923fa772861dc1b6d4.pdf` tras el cotejo y confirmó ausencia.
El [acta publicada del productor](https://github.com/kristhianmanue1/skopos/blob/e3cce1873cc73048ec18740e07166784df67b7bd/docs/evidencia/pdf-custody-imss-pilot-2026-10-08.md)
registra ese cotejo; sigue siendo autorrevisión de Skopos. PDF/ficha originales
y revisión permanecen según el productor.

Skopos reinició el Mongo dedicado y el host con el mismo `dbpath` y política.
La segunda corrida del mismo cliente devolvió `admission_status=duplicate`,
el mismo SHA de solicitud admitida y el mismo `receipt_id`. Recuperó una nueva
salida `imss-pdf-c72218d58bc6fa7015082cfd.pdf`: 1,311,822 bytes, SHA-256
igual al original y comparación byte por byte positiva. El consumidor volvió
a observar rechazo del digest de recibo erróneo. Skopos cotejó revisión,
recibo y bytes; informó una revisión y una cabeza, y retiró sólo esta salida.
El PDF y ficha originales permanecen según el productor. El SHA-256 canónico
de la política guardado en la revisión es
`a92b9252cc27a5a0a421fa1422b583d61cafdb0026956794a302c09db3c52160`;
el SHA-256 de los bytes de `policy.json` es
`eba99bfb8132824c4d533c2a58410d61bc5a2d35f7716698937a130e8ac4f18b`.
Son representaciones distintas y no deben intercambiarse.

Tras la revisión adversarial, Skopos añadió `policy_sha256` canónico a
`describe_capabilities` sin cambiar las versiones. El consumidor fijó ese
digest y repitió el intercambio completo con el cliente actualizado: código
cero, `duplicate`, mismo digest de admisión y recibo, rechazo de recibo con
digest falso y de otro material, y nueva salida
`imss-pdf-8424161c0931bf32e9a2e6df.pdf` de 1,311,822 bytes idénticos al
original. Skopos informó una revisión y una cabeza tras esta corrida, cotejó
recibo/digest/bytes y retiró únicamente esa salida, como registra su acta.
El consumidor comprobó después que su ruta de salida ya no existe.

## Límites y continuación

La política de host vive fuera de Git; su identidad y ambos digests se
conservan aquí y en el expediente publicado del productor. Mongo
persistente local no equivale a backup independiente. El productor reportó
10 pruebas focales y 497 de suite completa sin omisiones sobre su código
final; su árbol y referencia local `origin/main` coinciden en `e3cce187`.
Tras el ensayo, comprobé ausencia del socket y de la última salida. La base,
política y configuración permanecen locales para reanudar el piloto; el host
está detenido. El contrato
acepta sólo este material y esta política, con salida temporal y recuperación
dependiente de la copia original de expertoGobernanza.

La frase «No se invocó Skopos» en la ficha de procedencia describe el momento
en que se redactó esa ficha, antes de esta admisión. Este expediente registra
la invocación posterior. La ficha se conserva sin edición porque su SHA-256
está fijado en la política y en la revisión admitida; cualquier cambio de sus
bytes requeriría otra revisión y comprobación bilateral.

## Arranque bajo demanda posterior

Skopos añadió un [procedimiento de arranque y parada](https://github.com/kristhianmanue1/skopos/blob/55d4716ef4ea054300fa1a1224daf16a6375db8a/docs/evidencia/pdf-custody-pilot-operations-2026-10-08.md)
para la política y revisión ya admitidas. Su acta informa un ciclo inicial y
tres ciclos después de los ajustes de parada, limpieza y sonda: mismo recibo,
PDF idéntico byte por byte, una revisión/una cabeza y salida temporal retirada.
Los arranques observados fueron 0.972, 0.939, 1.041 y 0.957 segundos; no
constituyen un SLA. Al final se comprobaron sockets ausentes, carpeta de
entrega vacía y Mongo detenido.
`smoke` no vuelve a admitir el PDF. Este expediente registra el resultado del
productor; la disponibilidad futura exige ejecutar el preflight y arrancar
manualmente. Para repetir `smoke` se requieren los tres sobres existentes en
`requests_root` o sobres equivalentes preparados por el consumidor. La fecha
límite de política sigue siendo
`2026-11-08T00:00:00Z`.
