# Respuesta de custodia a Skopos — manual IMSS 2000-002-001

**Estado:** evaluación documental del consumidor; no es política aprobada, admisión operativa ni aceptación del contrato bilateral.
**Observado:** 2026-10-08 19:05 UTC.
**Ámbito:** copia local de `docs/fuentes/imss/2000-002-001.pdf` y ficha `2000-002-001-PROCEDENCIA.md` en expertoGobernanza. La respuesta sirve para que el agente de Skopos evalúe precondiciones; no le concede acceso ni instala configuración.

**Actualización posterior:** el Operador aceptó iniciar un piloto por referencia con `while_reference_available`; ver el [perfil del consumidor](2026-10-08-perfil-consumidor-piloto-pdf-imss-skopos.md). Para ese modo no se afirma recuperación independiente tras perder la copia y no se presenta una restauración no demostrada como requisito ya satisfecho. Este diagnóstico conserva la evidencia observada antes de esa decisión; la instalación de la frontera del host y la prueba bilateral siguen pendientes.

**Estado posterior:** la admisión y recuperación bilateral del piloto quedaron registradas en [contrato v0.2](../contratos/skopos-pdf-imss-piloto-v0.2.md) y [evidencia](../evidencia/skopos-pdf-imss-piloto-2026-10-08.md). Las frases de este diagnóstico sobre trabajo pendiente o archivos sin seguimiento describen sólo el corte de las 19:05 UTC; no son el estado actual.

## Contrato de esta revisión

Producir una respuesta pequeña y trazable sobre custodia y preparación del consumidor. Comprobaciones: ambos archivos existen y conservan los hashes indicados abajo; cada conclusión remite a una fuente inspeccionada; `python3 scripts/check_sizes.py` pasa; ningún archivo distinto de esta respuesta se modifica. La ronda siguiente puede refutar la respuesta con una política o una prueba de restauración específica de estos bytes.

## Evidencia observada y alcance

| Campo para el intercambio | Resultado del consumidor | Evidencia y límite |
|---|---|---|
| Material | PDF local de 1,311,822 bytes; SHA-256 `719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323` | `shasum -a 256` y `stat` sobre la copia local. Identifica estos bytes, no disponibilidad futura. |
| Procedencia | Ficha local de 3,165 bytes; SHA-256 `f934b0ec1bfbe97aae347b86bb3aa4e0831af79f704e571c27702f9203b62bff` | `shasum -a 256` y `stat`. La ficha, líneas 11–16, atribuye origen inmediato al archivo aportado por el Operador y documenta un cotejo puntual con la URL IMSS el 2026-10-08. Skopos no repitió la descarga remota. |
| Ubicación actual | `docs/fuentes/imss/2000-002-001.pdf`; PDF y ficha legibles por el proceso local observado | Ruta de trabajo, no raíz persistente preautorizada para Skopos. Permisos actuales `644`; no prueban ACL de un host futuro. |
| Estado Git | PDF y ficha sin seguimiento en `feat/R2-H1-02@97f3c33239070e2e0487ae55043dd805a918f088` al observar | `git status --short --branch`. No prueba por sí solo ausencia de respaldo, pero tampoco conservación gobernada. |
| Clasificación | **No acreditada como política bilateral.** La URL IMSS y `consumer_declared_public` son antecedentes descriptivos | `docs/autorizacion-fuentes-r1.md` §§1–2 autoriza canales y determinados textos públicos para análisis/proveedores; no clasifica este PDF para custodia en Skopos ni acredita vigencia jurídica. |
| Retención y retiro | **Sin política aprobada localizada para esta copia en los archivos inspeccionados** | La ficha, líneas 30–44, difiere ubicación, retención y admisión al corpus. La Solicitud B, `docs/propuestas/2026-10-05-pedido-contratos-aria.md` líneas 76–95, exige acordar retención y límites reales de borrado antes de admitir; es propuesta, no política instalada. |
| Respaldo y restauración | **No se localizó una prueba de restauración de este PDF y su ficha** | El ensayo temporal de Skopos, `docs/evidencia/pdf-custody-readiness-2026-10-08.md` líneas 30–60, recuperó bytes desde una copia temporal y destruyó el entorno. No restaura la copia del consumidor. |
| Recuperación requerida | `while_reference_available` es **candidato para un piloto**, si una política vigente acepta expresamente ese límite | La Solicitud B exige recuperar bytes identificables; no fija recuperación independiente tras pérdida de la copia. Si se exige esa propiedad, `verified_external_reference` no basta. |

## Respuesta al productor

**Resultado al observar: `not_ready_for_operational_admission`.** No ofrecer `verified_external_reference` como capacidad operativa para este material hasta que el host tenga una política bilateral vigente, raíz autorizada y accesible, alcance limitado al material permitido, plazo/retiro y límite de recuperación aceptado. Respaldo y restauración son requisitos adicionales sólo si la política promete recuperar la copia tras su pérdida; no se infieren en `while_reference_available`. La causa contractual propuesta es `policy_unavailable` o `retention_policy_missing`, según el control que falle primero. No se pide al Operador elegir una ruta o un plazo en cada solicitud; los agentes aplican la política instalada y rechazan si falta.

El expediente de Skopos `docs/evidencia/pdf-custody-readiness-2026-10-08.md` reporta admisión y recuperación mecánicas en una base Mongo aislada usando una copia del PDF y una ficha con los hashes anteriores. Ese resultado es un control positivo de laboratorio; no establece una segunda custodia, política del consumidor, disponibilidad posterior ni conformidad de los dos agentes instalados. La CLI de laboratorio permite al invocador elegir política y base de datos (`docs/propuestas/2026-10-08-incremento-custodia-pdf.md` de Skopos, líneas 124–134); antes del intercambio debe existir una frontera del host que fije esos valores fuera de la solicitud del agente.

## Continuación entre agentes

1. El consumidor entrega este resultado y, cuando exista, la referencia a la **política aprobada** y a una restauración comprobada de estos bytes. No inventa esos recibos.
2. El host de Skopos fija política, raíces y Mongo; demuestra que la solicitud del agente no puede cambiarlos ni abrir otro material dentro de la raíz. Para ello aísla la raíz a objetos permitidos o fija una lista por proyecto, material, revisión, ruta y hash. El host consumidor permite sólo la lectura autorizada de su copia.
3. Ambos agentes ejecutan `describe_capabilities` → `admit_original` → recibo → `fetch_original` → cotejo del consumidor, con controles positivos y negativos sobre pérdida, modificación, permisos, salida y respuesta incierta. Registran versión efectiva del contrato y discrepancias con el perfil PDF propuesto, incluido `max_pages`.
4. La aceptación técnica del intercambio no incorpora el manual al `corpus/registry.yaml`, no valida citas ni adjudica autenticidad o vigencia jurídica.

**Falsación de este diagnóstico:** una política vigente que cubra explícitamente esta copia, sus raíces, retención y límite de recuperación, más una prueba bilateral con el host configurado, cambiarían el estado. Si la política promete recuperar tras pérdida, se requiere además evidencia de respaldo/restauración de los bytes exactos. Hasta entonces, el agente consumidor debe devolver incertidumbre y no presentar el ensayo como admisión operativa.
