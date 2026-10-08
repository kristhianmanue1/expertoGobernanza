# Perfil del consumidor para piloto PDF IMSS con Skopos

**Estado:** perfil consumidor aceptado para el piloto por el Operador el 2026-10-08; instalación de política y admisión sujetas a comprobación separada.
**Objetivo:** permitir que agentes de expertoGobernanza soliciten custodia mecánica y recuperación del original bajo `verified_external_reference`, sin convertir Skopos en autoridad jurídica ni en una segunda copia permanente.

## Decisión y límites

El Operador aceptó iniciar las recomendaciones para el piloto local de un usuario. La opción técnica propuesta es `recovery_requirement=while_reference_available`: si la copia del consumidor falta o cambia, `fetch_original` debe fallar. Esta aceptación no demuestra respaldo independiente, restauración, permisos de servicio, política instalada, ingreso al corpus ni vigencia jurídica.

El consumidor conserva el original y la [ficha de procedencia](../fuentes/imss/2000-002-001-PROCEDENCIA.md). Aporta antecedentes de origen como datos atribuidos y verifica por sí mismo los bytes que Skopos entregue. Un resultado de laboratorio con copias temporales no cambia este perfil.

## Oferta exacta del consumidor para la primera revisión

| Campo | Valor del piloto | Condición |
|---|---|---|
| `project_id` / `material_id` / `source_revision` | `expertogobernanza` / `imss-2000-002-001` / `1` | Identidad única del intercambio; no admite otro material por compartir directorio. |
| Original | `docs/fuentes/imss/2000-002-001.pdf`; SHA-256 `719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`; 1,311,822 bytes | Recalcular antes de solicitar y tras recuperar. No es ruta autorizada hasta que el host la incluya explícitamente. |
| Ficha | `docs/fuentes/imss/2000-002-001-PROCEDENCIA.md`; SHA-256 `f934b0ec1bfbe97aae347b86bb3aa4e0831af79f704e571c27702f9203b62bff` | Aportar como antecedente atribuido para este caso; no elevar su contenido a verificación remota de Skopos. |
| Transporte preferido | `authorized_reference` | `provided_file` queda como alternativa de transporte; no autoriza `managed_copy`. |
| Custodia | `verified_external_reference`; dueño de la copia: expertoGobernanza | Skopos verifica la referencia en cada recuperación. No promete recuperar si la copia del consumidor desaparece. |
| Recuperación | `while_reference_available` | Si el consumidor exige independencia de la copia, rechazar esta política y abrir decisión distinta. |
| Clasificación | `consumer_declared_public` **sólo descriptiva y local** | No autoriza envío a proveedores externos ni adjudica autenticidad, vigencia o licencia. El host debe habilitar expresamente esta clase. |
| Sello | `not_required` para correspondencia mecánica de bytes | Informar `not_applicable`; esta ruta no satisface una consulta que exija sello institucional. |
| Límite binario | 2,000,000 bytes; sin red ni OCR | La custodia no promete número de páginas. `max_pages` pertenece a perfil de extracción con validador propio. |
| Retención de servicio | Piloto hasta `2026-11-08T00:00:00Z` | Fecha aceptada para caducar solicitudes Skopos, **no orden de borrar el original**. Verificarla en la política instalada. |

La carpeta actual del consumidor y sus permisos de lectura observados no son una raíz aprobada para otro proceso. El host deberá fijar el directorio real, identidad del servicio, accesos y lista exacta `(project_id, material_id, source_revision, ruta, SHA del PDF, SHA de ficha)`. La solicitud del agente no puede alterar política, Mongo ni lista de material. Si ambos agentes comparten usuario y shell, una envoltura Python por sí sola no demuestra esa frontera; se debe declarar y probar la limitación.

Skopos, como host que crea `delivery_root`, define y ejecuta el retiro de las salidas temporales. El consumidor verifica los bytes recibidos y no delega en ese retiro el borrado del original. La fecha y este reparto fueron confirmados al agente de Skopos para el piloto; la configuración y la ejecución del retiro requieren evidencia propia.

## Puerta de operación y falsadores

1. Política del host identificada por versión/digest, vigente y compatible con estos valores. Si no existe, `policy_unavailable`; si caducó, `retention_policy_missing`. No fabricar una política desde el JSON del agente.
2. Lectura de PDF y ficha exactos bajo raíz y lista permitidas; recalcular hashes. Probar rechazo de otro archivo dentro de la misma raíz, ruta fuera, enlace y permiso retirado.
3. `describe_capabilities` → `admit_original` → `receipt` → `fetch_original` en entorno bilateral; correlacionar IDs y ambos hashes de solicitud. El consumidor vuelve a leer salida y compara longitud, SHA-256 y bytes.
4. Mutar copia o ficha, perder respuesta, caducar política y hacer salida no escribible con controles positivos de la misma configuración. Ninguna respuesta fallida admite revisión ni ofrece un resumen como sustituto del original.
5. El primer recibo real, versión de contrato/runtime y evidencia de recuperación se revisan antes de llamar a esto admisión técnica. No escribir `corpus/registry.yaml`, EvidenceEdge ni AN-KLA por este intercambio.

**Estado del perfil al redactarlo:** la [evaluación de custodia](2026-10-08-respuesta-custodia-pdf-skopos.md) y el ensayo temporal de Skopos sustentaban preparación, sin prueba bilateral todavía. El estado posterior está en el [contrato v0.2](../contratos/skopos-pdf-imss-piloto-v0.2.md) y su [evidencia](../evidencia/skopos-pdf-imss-piloto-2026-10-08.md). `while_reference_available` sigue sin acreditar restauración independiente.
