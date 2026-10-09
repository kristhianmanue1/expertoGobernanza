# Consulta de fuentes ARIA para expertoGobernanza v0.1 (propuesta)

**Estado:** propuesta de requisitos del consumidor, 8 de octubre de 2026.
No sustituye los contratos vigentes de Skopos o Ágora, no activa AN-KLA y no
admite material al corpus normativo. Se evalúa primero con las siete fuentes
del inventario `docs/evidencia/ctim-source-register-2026-10-08.json`.

## Resultado requerido por consulta

La consulta debe devolver un expediente verificable, no sólo una respuesta:

1. Identidad del original: productor o sitio observado, URL si existe,
   formato real, bytes, SHA-256, revisión y fecha de captura. Una revisión
   nueva conserva la anterior; no sobrescribe la fuente. Clasificación,
   alcance de acceso, base de retención y vencimiento se fijan por fuente;
   una consulta no puede ampliarlos.
2. Derivado: extractor y versión, SHA-256, modalidad (texto nativo, OCR,
   transcripción, tabla, gráfico, HTML), cobertura y fallos por sección.
   Texto literal y normalización/candidato son campos distintos.
3. Localizador: página física y sección/función/actividad en PDF; ancla
   textual y apartado en HTML/TXT; párrafo/tabla en DOCX; turno, hablante
   declarado y marca temporal en conversación si existen. `unknown` es
   válido; no se inventa página o tiempo.
4. Fragmento: texto exacto del derivado con rango y hash; cuando la cita
   dependa de disposición visual, entregar además región de la imagen. La
   integridad del derivado no certifica fidelidad al original.
5. Interpretación: relación candidata entre fuentes con referencias a cada
   fragmento, tipo (`explicit_reference`, `inference`, `conflict` o
   `unresolved_identity`), fechas de las fuentes y estado de revisión.
   Ágora no eleva una inferencia a hecho normativo. Una relación de versión
   `SUPERSEDES` debe apoyar sus extremos en originales distintos y en el
   transitorio literal; las fechas solas no la demuestran.
6. Uso: expertoGobernanza coteja página y fragmento antes de citar, separa
   vigencia comprobada de fecha impresa y registra aprobación humana cuando
   corresponda. AN-KLA recibe sólo un puntero resumido mediante su propio
   contrato y autorización; nunca una ingesta automática de documentos.

## Fronteras por componente

| Componente | Responsabilidad esperada | Evidencia mínima |
| --- | --- | --- |
| Skopos | Custodia y recuperación del original; derivación, cobertura y localizadores por formato admitido | Recibo de admisión, hash de original, manifiesto de derivado, recuperación tras reinicio, error tipado ante identidad/hash erróneo |
| Ágora | Componer candidatos y relaciones entre fuentes sin mezclar localizadores | Hashes y rangos verificados de cada entrada, distinción literal/inferencia, `admitted=false`, cero llamadas a proveedor cuando el contrato sea determinista |
| expertoGobernanza | Inventario de fuentes, pregunta, cotejo visual/textual, análisis y decisión de cita | Fuente y página/apartado precisos, estado temporal, matriz de vínculos y límite de revisión |
| AN-KLA | Continuidad selectiva gobernada, si se autoriza | Puntero a artefacto canónico, revisión y autoridad de escritura; nunca contenido normativo como sustituto del original |

## Secuencia de aceptación por formato

- **PDF:** original PDF en Skopos; extracción nativa completa o cobertura
  explícitamente parcial; OCR/grafo sólo en páginas declaradas; cotejo
  visual de cada cita nueva. El perfil previo de 80 páginas no basta para
  el manual DA de 403 páginas.
- **HTML/TXT:** custodiar bytes originales y un derivado textual separado;
  preservar codificación, estructura y ancla. El DOF de 2021 está en
  ISO-8859-1 y el acuerdo de 2023 en UTF-8; el derivado puede ser UTF-8,
  siempre identificado por otro hash. No convertir HTML en una
  transcripción de reunión para forzar compatibilidad.
- **DOCX:** pendiente un adaptador que preserve párrafos, tablas, notas e
  imágenes con localizadores. El SHA del archivo solo no da trazabilidad
  de fragmentos.
- **Conversaciones:** pendiente contrato explícito para roles, origen,
  turnos, revisiones, redacción de datos personales y completitud de captura.
  Un texto plano sin identidad de turnos no acredita quién dijo qué.

**Prueba bilateral mínima:** desde expertoGobernanza pedir una página o
apartado real a Skopos, convertirla mediante el puente verificado de Ágora,
resolver una relación con dos originales distintos, recuperar después de
reinicio y rechazar una alteración de hash/localizador, una fuente fuera de
política y una operación tras el vencimiento. Apagar sólo procesos
iniciados por la sesión y emitir recibo de estado. Repetir con PDF largo y
HTML; la prueba DOCX/conversaciones se añade cuando existan adaptadores.

**Límite actual:** el inventario de este hito sólo verifica bytes locales.
La versión POBALINES de 2021 se conserva como antecedente histórico: el
acuerdo DOF publicado en 2023 deja sin efectos esa versión y el PDF aprobado
en 2022 aporta el texto posterior. Una consulta debe mostrar qué versión
sustenta cada fragmento y no mezclar sus apartados.
La cobertura multiformato completa y la prueba bilateral con originales
reales deben acreditarse con recibos de Skopos y salidas verificadas de Ágora;
los fixtures de contrato no bastan para ese fin.

## Estado de implementación observado, 9 de octubre de 2026

| Entrada | Skopos | Ágora | Condición antes de citar |
| --- | --- | --- | --- |
| PDF | Custodia v0.3 y derivados parciales de tres fuentes CTIM en PR #5 | Cinco intercambios reales verificados en la prueba bilateral de expertoGobernanza | Cotejar página física y fragmento; cobertura parcial explícita |
| HTML | Dos originales y anclas de bytes con hash en PR #5 | Perfil tipado UTF-8/ISO-8859-1 y rango de bytes; parser sin evaluación CSS | Cotejar fragmento original, contexto y versión |
| TXT/Markdown | Sin perfil de custodia CTIM probado | Perfil tipado para original y derivado UTF-8, sin extractor | Definir y probar productor y localizador |
| DOCX | Sin adaptador probado | Perfil tipado rechaza DOCX | Definir extracción de párrafos, tablas, notas e imágenes |
| Conversaciones | Sin captura de turnos probada | Perfil tipado rechaza turnos | Definir origen, hablante, tiempo, redacción y completitud |

El recibo `docs/evidencia/ctim-bilateral-receipt-2026-10-09.json` prueba sólo
la corrida local de cinco originales contra la rama de Skopos indicada; no
convierte el PR de custodia en contrato fusionado ni escribe AN-KLA.
