# Contrato bilateral propuesto: derivados documentales Skopos v0.1

**Estado:** intercambio técnico bajo demanda probado e integrado en
expertoGobernanza; propuesta de contrato pendiente de aceptación formal. La
fidelidad del contenido derivado no está aceptada. El diagnóstico exploratorio
de [p1 y p20](../evidencia/skopos-imss-fidelity-sample-2026-10-08.md) y la
[revisión del cálculo de rótulos p20](../evidencia/skopos-label-eval-consumer-review-2026-10-08.md)
no amplían esa aceptación.
**Identificador propuesto:** `expertogobernanza/skopos-document-derivatives/v0.1`.
**Caso inicial:** `expertogobernanza / imss-2000-002-001 / revisión 1`.
**Base:** [custodia v0.2](skopos-pdf-imss-piloto-v0.2.md). Conserva su original,
ficha, SHA-256, recibo y política; ninguna extracción cambia esa revisión.

## Propósito y frontera

Skopos entrega derivados localizables del PDF y candidatos de búsqueda.
expertoGobernanza comprueba cada evidencia y decide si puede usarla en un
análisis. La salida de Skopos no certifica autenticidad institucional,
vigencia jurídica, relaciones normativas ni admisión al corpus.

La ejecución sigue siendo local, de un usuario y bajo demanda. Una política
nueva y separada del host debe fijar derivadores, versiones, páginas, tamaño,
presupuesto, lectores, retención de derivados y salidas, y prohibición de
egress. Una petición del agente no puede ampliar esos valores. La fecha
de la política v0.2 no se extiende por este documento.
La búsqueda vectorial y los embeddings quedan fuera de este incremento.
El perfil macOS puede usar PDFKit/Vision local si prueba su comportamiento;
otras plataformas anuncian esa modalidad `unavailable` hasta tener otro
derivador comprobado. Una puntuación de confianza OCR no adjudica texto.

**Parámetros técnicos acordados para la prueba:** política separada
`expertogobernanza/imss-2000-002-001-derivatives@v0.1-2026-10-08`, vigencia
máxima `2026-11-08T00:00:00Z`; `native_text` en páginas físicas 1–188;
`selective_ocr` sólo en 1 y 18–22 (máximo seis páginas); `visual_graph` sólo
en 18–22 y anunciado disponible únicamente tras sus gates. Render hasta
2400 píxeles de lado mayor, 120 segundos y 10 MB de salida por trabajo,
`allow_network=false`. `derived_root` y salidas son privados/locales en
Skopos, sin backup independiente acreditado. El vencimiento bloquea uso,
no ordena borrado automático; el retiro de derivados exige acto acotado.

## Intercambio técnico observado en v0.1

1. `describe_document_capabilities`: capacidades parciales, motor declarado,
   política y límites con digest. La declaración no prueba fidelidad.
2. `derive_document`: identidad y SHA del original, recibo v0.2 y digest de su
   política, alcance de
   páginas, modalidades `native_text`, `selective_ocr`, `visual_graph`, límite
   de recursos y solicitud idempotente. Los límites de la petición sólo pueden
   reducir los del host. Responde un `manifest_ref`/SHA y resumen acotado;
   páginas completas se consultan por partes. No sobrescribe el PDF ni infiere
   éxito para páginas no examinadas.
3. `derivation_receipt`: identidad y SHA de la solicitud original; reconcilia
   una respuesta perdida sin repetir OCR ni publicar otro manifiesto.
4. `fetch_derivative`: identidad, revisión y SHA del derivado; devuelve bytes
   exactos y su relación con el original. Revalida PDF y ficha exactos bajo
   `while_reference_available`; un derivado ausente o un original perdido
   falla cerrado, sin servir una copia derivada como sustituto.
5. `search_document`: búsqueda literal acotada; devuelve candidatos, no
   respuestas finales. Cada candidato identifica original, derivado, página
   física, región, fragmento y método; la respuesta incluye cobertura por
   página y exclusiones. No promete recuperación semántica.
6. `fetch_evidence`: recupera el registro exacto de línea o nodo y su
   localizador; revalida fuente y ficha. El consumidor coteja `item_id`,
   contenido, caja, página, padre, manifiesto y render cuando existe antes
   de considerar una cita. V0.1 no declara un slice UTF-8 del PDF.

## Datos publicados por el manifiesto v0.1

- Identidad: `parent` con material, revisión, SHA y recibo/política de custodia;
  `derivation_id`, política de derivados con SHA, `engine_schema`, límites,
  `page_count`, páginas, `artifacts` y `fidelity_status=unreviewed`. El SHA
  del manifiesto está en el recibo y en `manifest.sha256` del almacén.
- Página física 1-based: `page_number`, ancho/alto en puntos, rotación,
  `native_text`, `ocr_text`, `render` y `visual_graph`. Las capas de texto
  contienen `status` y `lines`; `not_run`, `no_text` y `extracted` se
  distinguen en el caso probado. OCR y texto nativo permanecen separados.
  V0.1 no publica un campo universal `render_ok`, etiqueta impresa, cobertura
  por región ni errores por página. La cobertura de búsqueda se declara en
  la respuesta de `search_document`.
- Cada línea lleva texto, `bbox` normalizada 0..1, origen arriba a la
  izquierda, e `item_id`; OCR añade confianza del motor, sin que ésta valide
  fidelidad. Un render PNG lleva archivo, bytes, SHA, dimensiones,
  renderizador y escala. Su hash identifica bytes PNG, no el PDF.
- `visual_graph` contiene `nodes`, `connectors`, `edges`, `unknown` y
  `status`; cuando se ejecuta añade `diagram_type` y regla de dirección.
  Los nodos incluyen caja,
  rótulo no revisado, `item_id` y referencias OCR. Cada arista referencia
  nodos y conector; dirección `observed` exige punta visible, mientras que
  sin ella queda `unknown`/hipótesis topológica. El productor no se declara
  revisor humano del resultado.
- El recibo de derivación permite reconciliar una respuesta perdida. La
  identidad fija fuente, política y hashes de motores; cambiar código o
  política crea otro derivado. `no_match`, error de presupuesto y bytes
  indisponibles no se convierten en una respuesta afirmativa.

## Comprobación técnica y aceptación del contenido

El *smoke test* bilateral v0.1 comprobó: inventario nativo de 188 páginas
(187 con líneas, p1 `no_text`); OCR con líneas en p1 y p18–22; grafo parcial
en p18–22; recibo, manifiesto/render por SHA, búsqueda literal positiva y
negativa, evidencia de línea y nodo, rechazo de SHA falso y topología de p20
sin cruce de ramas ni dirección afirmada sin flecha. El productor probó un
fixture sintético con flecha invertida; la guía repitió los tres modos tras
arranque nuevo y verificó la parada. Son pruebas de intercambio e integridad
acotadas; el estado resultante es `consumer_smoke_passed`.

**Pendiente para aceptar fidelidad o automatizar citas:** transcripción humana
y cotejo de rótulos/zonas OCR; anotación visual previa e independiente de
p18–22 con nodos, conectores, dirección y `unknown`; medición de recall,
precisión, presupuesto y latencia sobre consultas fijadas; y controles
negativos adicionales de localizador, revisión y relación alterados. Esos
criterios no se satisfacen por las tres corridas de humo ni por CI verde.
Una eventual compuerta de fidelidad o admisión al corpus requiere su propia
revisión y autoridad. No se promete recuperar paráfrasis sin palabras comunes.

## Condiciones de parada y continuidad

Si faltan dependencias, política, presupuesto, permiso u original,
la operación afectada falla con causa tipada; continúan las partes independientes.
La iteración sigue con corrección y nueva prueba del artefacto final hasta
cumplir el piloto acotado o documentar un bloqueo material comprobado.

## Evidencia del piloto bajo demanda (2026-10-08)

El cliente de consumidor `scripts/skopos_document_pilot.py` ejecutó el canal
local bajo demanda contra `skopos/pdf-document-host/v0.1`, política canónica
`4d09e940ea340ea686c77b4fab84dcf8bb05a371c2119434e60d8744227b3c6b`.
El productor publicó `main@7f01eed9aa699d38de7c4587e5ea19e3cba428de`
y el remoto `origin/main` reportó el mismo SHA al cotejarlo. Su suite local
reportó 502/502 pruebas verdes; el consumidor ejecutó sus tres recorridos
contra el mismo digest. Esto no acredita despliegue continuo.
La derivación nativa de 188 páginas produjo manifiesto SHA-256
`7f81b1616b10549439cd536737e76663cfea7cec3bf7a6ec3fbf10241d8292ed`:
187 páginas con líneas y p1 `no_text`. La derivación OCR de p1 y p18–22
produjo manifiesto SHA-256
`3ca9d7a5be5e451f63608015585a4eee92d2109046d390de99d793ac2f83651d`:
las seis páginas reportaron líneas y se recuperó el PNG de p20 por SHA.
La derivación visual de p18–22 produjo manifiesto SHA-256
`8a1880b84b0e52f934f09759f3a83efb5a3a752afda914d6c5cce9c7803aaaee`.
El cliente comprobó en p20 diez nodos y nueve relaciones topológicas sin
cruce de ramas; la dirección permanece `unknown` porque no hay flechas.
P19, p21 y p22 conservan relaciones `unknown` y cobertura parcial.
Se cotejaron recibos recuperados, candidato literal con `fetch_evidence`,
`no_match` y rechazo de SHA falso. Esto prueba el circuito para ese host y
política; no prueba fidelidad OCR ni validez semántica integral del grafo.
En p19–21 el OCR deformó
rótulos pequeños (`PRESIACONAS`, `RESTACIONES MÉDICAS`,
`PRESPACIONEO MEDICAS`). El estado de fidelidad sigue `unreviewed`.
`visual_graph` se anuncia `partial`; el cliente aún no habilita uso
automático de citas ni admisión al corpus.
La guía de encendido, verificación y apagado quedó publicada en Skopos
`main@3aa162d3a2b9e9d352307bfc125c4ed1ebeae0b3`, archivo
`docs/evidencia/pdf-document-pilot-operations-2026-10-08.md`. El bloque
publicado se ejecutó completo y dejó el host y Mongo del piloto apagados.
