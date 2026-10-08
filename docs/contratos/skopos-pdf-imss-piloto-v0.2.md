# Contrato bilateral de custodia PDF IMSS — piloto v0.2

**Estado:** aceptado sólo para el piloto local de un usuario y el material indicado.
**Productor:** Skopos `skopos/pdf-custody-host/v0.1`.
**Consumidor:** expertoGobernanza `expertogobernanza/skopos-source` `v0.2`.
**Evidencia:** [corrida bilateral](../evidencia/skopos-pdf-imss-piloto-2026-10-08.md) y [perfil consumidor](../propuestas/2026-10-08-perfil-consumidor-piloto-pdf-imss-skopos.md).

## Objeto y política

El único material admitido es `(expertogobernanza, imss-2000-002-001, 1)`:
PDF `docs/fuentes/imss/2000-002-001.pdf`, SHA-256
`719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`,
1,311,822 bytes; ficha `docs/fuentes/imss/2000-002-001-PROCEDENCIA.md`, SHA-256
`f934b0ec1bfbe97aae347b86bb3aa4e0831af79f704e571c27702f9203b62bff`.
La URL oficial y los límites de su comprobación están en la ficha. El hash
acredita correspondencia de bytes, no vigencia, autenticidad institucional o
idoneidad jurídica.

El host fija fuera de la solicitud `policy_id=expertogobernanza/imss-2000-002-001-reference`,
`policy_version=v0.2-2026-10-08`, `seal_profile_id=expertogobernanza/not-required`,
`classification=consumer_declared_public`, `max_bytes=2000000`, expiración
`2026-11-08T00:00:00Z` y `recovery_requirement=while_reference_available`.
`describe_capabilities` anuncia `policy_sha256` canónico
`a92b9252cc27a5a0a421fa1422b583d61cafdb0026956794a302c09db3c52160`;
el consumidor lo compara con el valor fijado para esta revisión antes de admitir.
La clasificación es una declaración local del consumidor. No habilita egress.
Skopos conserva metadatos de revisión y una referencia verificable; la copia
original permanece en expertoGobernanza. Si ésta falta o cambia, recuperar
debe fallar. La expiración termina el servicio de solicitudes, no borra el
original. Skopos retira sus salidas temporales tras cotejo; expertoGobernanza
administra los sobres y solicitudes que creó bajo su `requests_root` ignorado
por Git, con retiro después de cerrar el piloto y conservar sólo digests y
recibos necesarios para la trazabilidad.

## Intercambio estable dentro del piloto

El consumidor escribe una solicitud JSON bajo `requests_root` y un sobre con
`request_file_ref`, SHA-256 de los bytes de solicitud, `request_id`, `contract_id`
y `contract_version`; envía al socket sólo `envelope_ref`. El host comprueba
versión y digest antes de operar. Política, Mongo, raíces y lista permitida
proceden de configuración del host, nunca de campos de la solicitud.

Secuencia: `describe_capabilities` → `admit_original` → `receipt` →
`fetch_original`. La admisión declara `authorized_reference`, PDF, ficha,
hashes, `single_object`, `verified_external_reference`, sello `not_required`,
recuperación limitada y prohibición de red/OCR. No se acepta `max_pages` en
este perfil binario. `receipt` usa el SHA **de la admisión**, distinto del SHA
de su propia consulta. La respuesta host debe mantener esquema, versiones,
`request_id` y SHA de cada solicitud. El recibo es reducido; no satisface la
respuesta ampliada del pedido general B de 2026-10-05.

El consumidor verifica identidad de política y capacidad, recibo, longitud,
SHA-256 y bytes devueltos frente al original local. El digest anunciado
identifica la política cargada por este host; el aislamiento del host sigue
limitado por el usuario compartido. Un error de versión,
política, material, digest, referencia, formato o disponibilidad detiene el
uso de la respuesta; no hay sustitución por resumen o revisión distinta.
La prueba negativa debe rechazar otro material del mismo proyecto y un
`admission_request_sha256` erróneo sin crear revisión adicional.

## Frontera y cambios

La ejecución local compartió usuario de OS. El socket y la configuración del
host restringen el mensaje de este canal; no demuestran que un agente con el
mismo shell no pueda invocar la CLI directa o acceder a archivos/credenciales.
No se acepta aislamiento entre identidades, backup independiente, `managed_copy`,
ingreso al corpus, extracción de texto, validación jurídica ni uso clínico.

Este contrato cubre sólo la revisión y política fijadas arriba. Cambiar modo
de custodia, recuperación, retención, sello, material, formato o esquema exige
otra versión o revisión bilateral y prueba nueva. La prueba de recuperación
tras reinicio del almacén está documentada en la evidencia; no amplía por sí
sola la garantía `while_reference_available`.
