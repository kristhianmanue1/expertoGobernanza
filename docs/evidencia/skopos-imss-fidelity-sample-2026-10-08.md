# Muestreo diagnóstico de fidelidad: PDF IMSS 2000-002-001

**Estado:** cotejo exploratorio del consumidor, no compuerta de fidelidad ni
admisión al corpus. **Fecha local:** 2026-10-08. **Páginas examinadas
visualmente:** portada física 1 y organigrama físico 20 de 188. La selección
se hizo después de observar las salidas; no sustenta métricas de precisión
ni estimaciones para otras páginas.

## Fuentes y método

- Original conservado por expertoGobernanza:
  `docs/fuentes/imss/2000-002-001.pdf`, SHA-256
  `719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`.
  La [ficha de procedencia](../fuentes/imss/2000-002-001-PROCEDENCIA.md)
  documenta el cotejo puntual previo con la URL del IMSS. Su frase histórica
  «No se invocó Skopos» describe el momento de creación de la ficha; este
  expediente registra una ejecución posterior e **INFORMS** el análisis,
  sin modificar la ficha fijada por SHA ni afirmar vigencia jurídica.
- Política local de derivados SHA-256 canónico
  `4d09e940ea340ea686c77b4fab84dcf8bb05a371c2119434e60d8744227b3c6b`.
  Manifiesto OCR SHA-256
  `3ca9d7a5be5e451f63608015585a4eee92d2109046d390de99d793ac2f83651d`;
  manifiesto visual SHA-256
  `8a1880b84b0e52f934f09759f3a83efb5a3a752afda914d6c5cce9c7803aaaee`.
  Se recomputaron ambos SHA sobre los bytes locales del almacén. Los
  derivados declaran `fidelity_status=unreviewed`.
- Se renderizaron p1 a 1400 px y p20 a 1800 px con `pdftoppm`, y se
  compararon visualmente rótulos seleccionados con las líneas nativas,
  OCR y nodos del manifiesto. Es autorrevisión del consumidor, sin anotador
  independiente ni muestra ciega. No se alteró el PDF, el almacén o la
  política.
- Se activó el host bajo demanda y se consultó `search_document` con
  `EDUCACIÓN EN SALUD` sobre el derivado visual. Devolvió un candidato nativo
  en p20; `fetch_evidence` recuperó el mismo texto, caja e `item_id`
  `4b46fd1a085070d21b6de3e6c8a061b94e134902402039ea63a1a972368d451c`,
  unido al padre exacto. La sesión devolvió `stopped`; después no existía el
  socket del host y el puerto Mongo 37034 rechazó conexión. Es una consulta
  positiva acotada, no una medición de búsqueda. Recibo de esa repetición a
  continuación.

### Recibo mínimo de consulta bajo demanda

Observación local terminada el `2026-10-09T00:30:00Z` (fecha UTC; 2026-10-08
en México). Se ejecutó una secuencia temporal: `pdf_custody_pilot.py
preflight`, `start`, `document-host serve`, cliente
`scripts/skopos_document_pilot.py` mediante `exchange` para
`search_document` y `fetch_evidence`, y `pdf_custody_pilot.py stop` bajo
`trap EXIT`. La salida capturada localmente tuvo SHA-256
`6db9ea4eff748e3f4c4ddcf286ecd4a7e0fc32c8670f4352a1a81f33c1da88f9`:

```text
{"status": "ready_to_start"} → {"status": "ready"}
{'status': 'bounded_evidence_retrieved', 'query': 'EDUCACIÓN EN SALUD',
 'page': 20, 'item_id': '4b46fd1a085070d21b6de3e6c8a061b94e134902402039ea63a1a972368d451c',
 'text': 'EDUCACIÓN EN SALUD',
 'bbox': [0.3851149374151757, 0.4359718255026873, 0.48113664483754953, 0.4429363727932074],
 'fidelity': 'unreviewed'}
{"status": "stopped"}
```

El extracto omite `policy_sha256` y `startup_seconds` presentes en la salida
completa; el SHA identifica esa salida local, no el extracto. Tras el comando,
`test ! -S` sobre `runs/pdf-document-imss-pilot-v1/document.sock` devolvió
0 y `nc -z 127.0.0.1 37034` devolvió 1. El recibo documenta una ejecución,
sin acreditar disponibilidad continua ni precisión de recuperación.

## Observaciones acotadas

| Página/región | Lectura visual del original | Derivado observado | Resultado |
| --- | --- | --- | --- |
| p1, título | Manual de organización de la Dirección de Prestaciones Médicas | OCR recupera ambas líneas del título | Coincide en esas líneas; portada sin texto nativo. |
| p1, línea de cargo | Titular de la Dirección de Prestaciones Médicas | OCR escribe `Dirécción` | Error de acento; no citar automáticamente. |
| p1, párrafo inferior | Texto pequeño sobre conducta | OCR contiene `realzará`, `Confictos`, `Pudicas` y otras deformaciones | No se cotejó frase completa; el OCR no es transcripción fiel de esa región. |
| p20, caja izquierda `n3` | Coordinación de Educación en Salud | Nodo visual con `label=""`, `label_status=unknown` y ninguna línea OCR asociada; texto nativo dentro de la caja: `COORDINACIÓN DE` + `EDUCACIÓN EN SALUD` | El rótulo puede recuperarse del texto nativo y cotejarse con la imagen; el `label` del nodo no basta. |
| p20, caja derecha `n4` | Coordinación de Investigación en Salud | Nodo OCR `COBRARON BE`; texto nativo en la caja: `COORDINACIÓN DE` + `INVESTIGACIÓN EN` + `SALUD` | OCR incorrecto; nativo y región coinciden con la lectura visual. |
| p20, estructura | Unidad conectada visualmente a ambas coordinaciones | Grafo `n2–n3` y `n2–n4`, 10 nodos y 9 relaciones topológicas; dirección `unknown` | Conexiones visibles en esta página; no hay flechas que prueben dirección. |

Las cajas n3 y n4 del grafo están aproximadamente en
`[0.377,0.414,0.489,0.459]` y `[0.653,0.414,0.764,0.460]` del render,
respectivamente. Las líneas nativas indicadas tienen cajas interiores y
`item_id` trazables en el manifiesto; las etiquetas OCR no sustituyen ese
cotejo. La posición vertical sugiere jerarquía, pero la dirección de cada
arista permanece hipótesis.

## Decisión de uso para este caso

Para la pregunta «¿qué coordinaciones aparecen en el organigrama de la
Unidad de Educación e Investigación?», el **original visual p20**, junto con
las líneas nativas localizadas, respalda mencionar las coordinaciones de
Educación en Salud e Investigación en Salud **como elementos representados
en esta copia del manual**. No se usa el rótulo OCR de los nodos como cita.
No se infiere vigencia institucional, autoridad normativa ni dirección
formal de dependencia a partir del grafo. Toda cita futura debe recuperar
el PDF exacto y verificar la región pertinente en ese momento.

## Pendiente

Este muestreo no cubre p18, p19, p21, p22, todas las divisiones de p20,
ni búsqueda cuantitativa. Antes de aceptar fidelidad o automatizar citas:
fijar anotaciones ciegas por región, cotejar cada modalidad y medir falsos
positivos/omisiones. Una versión posterior de Skopos podría exponer
`label_candidates` por nodo con modalidad, `item_id` y caja; sería otro
contrato y requeriría pruebas nuevas. No se cambió v0.1 por esta propuesta.
