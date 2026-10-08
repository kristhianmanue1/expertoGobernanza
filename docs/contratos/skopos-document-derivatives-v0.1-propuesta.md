# Contrato bilateral propuesto: derivados documentales Skopos v0.1

**Estado:** piloto bilateral bajo demanda probado; propuesta de contrato
pendiente de aceptación formal y merge del consumidor.
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

## Intercambio solicitado (nombres y versión por acordar)

1. `describe_document_capabilities`: formatos, métodos realmente instalados,
   versión/configuración, política y límites con digest.
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
5. `search_document`: búsqueda textual acotada; devuelve candidatos, no
   respuestas finales. Cada candidato identifica original, derivado, página
   física, región, fragmento, método, límites y exclusiones. Esta operación
   puede apoyarse en la búsqueda léxica existente sólo si cumple el contrato.
6. `fetch_evidence`: recupera el fragmento exacto y su localizador; revalida
   fuente y ficha. El consumidor valida hash, slice UTF-8 cuando exista,
   página y región antes de citar.

## Datos mínimos del manifiesto

- Por página física 1-based: `render_ok`, modalidad, método, errores,
  cobertura y exclusiones. `run_status` distingue `unavailable`, `not_run`,
  `no_text`, `partial`, `extracted` y `failed`; `fidelity_status` permanece `unreviewed`
  hasta cotejo externo y nunca se infiere del éxito del proceso.
  Numeración impresa queda como etiqueta observada separada.
- Por derivado: padre `(material_id, source_revision, original_sha256)`,
  `derivation_id`, bytes/hash, herramienta y versión/configuración, página,
  coordenadas normalizadas 0..1 con origen arriba a la izquierda y rotación,
  `render_sha256` de una representación con resolución/codec fijados, modalidad
  y límites. El hash de render no es el hash del PDF. OCR y texto
  nativo divergentes permanecen separados.
- Para diagramas: nodos con rótulo/caja, conectores y aristas dirigidas con
  regiones de origen; una lista `unknown` conserva relaciones no resueltas.
  El productor distingue `observed` de `hypothesis`; proximidad de texto no
  crea una arista. La revisión humana se registra en el consumidor, nunca como
  autocalificación del extractor.
- `no_match`, `budget_exceeded`, índice ausente y bytes indisponibles son
  resultados distintos. Una coincidencia textual no significa verdad.
- Un recibo de derivación ya publicado es inmutable. Reintentar la misma
  solicitud reconcilia la identidad; cambiar motor, versión, configuración o
  contenido crea otro derivado, sin sustituir el anterior silenciosamente.
  `complete` sólo se declara para la modalidad y páginas efectivamente
  comprobadas, nunca por el mero retorno del proceso.

## Pruebas de aceptación del piloto

1. Inventario de las 188 páginas del PDF y manifestación explícita de páginas
   sin texto o con cobertura parcial. Control: `pypdf` observa texto nativo en
   187 páginas y ninguno en la portada física 1; esto no mide fidelidad.
2. OCR local de la portada y de un fixture de página imagen; comparar rótulos
   seleccionados con transcripción humana y conservar caja y render. Un OCR
   vacío exige control positivo del motor antes de atribuir ausencia al PDF.
3. Organigramas reales en páginas físicas 18–22 y un diagrama de flujo
   sintético con flecha invertida como negativo. Evaluar nodos, conectores,
   dirección y localización por separado contra anotación visual fijada antes
   de ajustar el extractor; relaciones inciertas deben abstenerse. En la
   página 20, comprobar conectores entre Dirección de Prestaciones Médicas,
   Unidad de Educación e Investigación y ambas coordinaciones de Educación e
   Investigación en Salud; rechazar una conexión cruzada entre ramas. La
   orientación jerárquica sin flecha se declara hipótesis, no dirección
   observada. En el fixture de flujo, una punta de flecha visible permite
   probar dirección observada y su inversión como error.
4. Búsqueda textual sobre fragmentos derivados con preguntas fijadas por el
   consumidor y consultas sin respuesta. Medir recall, precisión de candidatos,
   cobertura, presupuesto y latencia; cada acierto debe pasar `fetch_evidence`.
   No se promete recuperar paráfrasis sin palabras en común.
5. Corrida completa consumidor→Skopos→consumidor: admisión v0.2 permanece en
   una revisión/cabeza; se recuperan original, manifiesto, derivado y cita;
   alterar hash, localizador, revisión, política o relación de diagrama se
   rechaza. Repetir tras `stop/start` con las mismas identidades.
6. Gates del productor y consumidor, revisión adversarial del artefacto final
   y actas separadas. Reportar páginas y relaciones `unknown` sin promoverlas
   a éxito ni a corpus. No se declara capacidad general fuera del caso probado.

## Condiciones de parada y continuidad

Si faltan dependencias, política, presupuesto, permiso, índice o original,
la operación afectada falla con causa tipada; continúan las partes independientes.
La iteración sigue con corrección y nueva prueba del artefacto final hasta
cumplir el piloto acotado o documentar un bloqueo material comprobado.

## Evidencia provisional del intercambio (2026-10-08)

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
