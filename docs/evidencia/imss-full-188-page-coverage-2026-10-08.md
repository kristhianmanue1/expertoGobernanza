# Cobertura del manual IMSS 2000-002-001 completo — 188 páginas

**Estado:** inventario técnico completo bajo demanda; fidelidad visual y
semántica no aceptada. **Última observación:** 2026-10-09T02:22Z
(2026-10-08 en México). Consumidor: expertoGobernanza; productor de
derivados: Skopos.

## Fuente y partición física

El original `docs/fuentes/imss/2000-002-001.pdf` tiene 188 páginas y SHA-256
`719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`.
La [ficha de procedencia](../fuentes/imss/2000-002-001-PROCEDENCIA.md)
registra el cotejo puntual de esos bytes con la URL oficial del IMSS el
2026-10-08; la URL no se volvió a consultar en esta ronda.

El índice y los encabezados del PDF ubican las secciones 1–5 en p5–17,
**6. Organigramas en p18–22** y **7. Funciones Sustantivas desde p23 hasta
p188**. P22 contiene `6.1.4`; p23 abre `7. Funciones Sustantivas`.
Se renderizaron a 500 px las 166 páginas p23–188 y se inspeccionaron cuatro
hojas de contacto temporales: todas muestran formato de texto numerado,
sin un organigrama evidente. En los XObjects de imagen directos consultados,
las páginas p23–188 tienen cada una un único payload raster compartido (el
logo); este inventario no recorre imágenes anidadas o inline ni descarta
trazos vectoriales. La observación visual fue de miniaturas, no una lectura
detallada de cada página.

## Derivados de Skopos vinculados al mismo original

| Derivado v0.1 | Identidad observada | Cobertura |
| --- | --- | --- |
| Nativo completo | derivación `372fdaef7fb1171ec8dce708b79ef1e32b38e43dfb1b079e6b27ae070d8f7587`; manifiesto SHA-256 `7f81b1616b10549439cd536737e76663cfea7cec3bf7a6ec3fbf10241d8292ed` | 188 páginas inventariadas; p2–188 `extracted`, p1 `no_text` |
| OCR selectivo | derivación `7f132071b5e1c372e41d0ce9a83df7c966955c7fcb7036f80cdcbcecf5654a46`; manifiesto SHA-256 `3ca9d7a5be5e451f63608015585a4eee92d2109046d390de99d793ac2f83651d` | p1 y p18–22; 20 líneas OCR en p1 |
| Gráfico visual | derivación `1ef12d5a480075214369e9d19dcb6949370119e212b84007ce1b1a5ef1b7b8cf`; manifiesto SHA-256 `8a1880b84b0e52f934f09759f3a83efb5a3a752afda914d6c5cce9c7803aaaee` | p18–22, todos `partial` |

La política documental común SHA-256
`4d09e940ea340ea686c77b4fab84dcf8bb05a371c2119434e60d8744227b3c6b`
vence el `2026-11-08T00:00:00Z`; no se renovó ni se cambió retención.

## Auditoría independiente de cobertura

El [verificador](../../scripts/audit_imss_full_pdf.py) recomputó los cuatro
hashes, validó `item_id` y páginas de los tres manifiestos, el pie
`Página N de 188` en p2–188, y comparó dos extractores locales sobre todas
las páginas: `pypdf` desde el original y texto nativo de Skopos/PDFKit.
La dependencia reproducible `pypdf==6.15.0` está fijada en
`requirements.txt`. El gate local se ejecuta con los tres manifiestos en
`/Users/krisnova/www/aria/skopos/runs/pdf-document-imss-pilot-v1/derived/`
y `.venv/bin/python -m scripts.audit_imss_full_pdf --native-manifest ...
--ocr-manifest ... --graph-manifest ...`; los SHA-256 fijos impiden
sustituirlos por otros. `./scripts/ci_check.sh` comprueba el import de
`pypdf`, además del resto de gates del repositorio.
La comparación usa multiconjuntos de palabras Unicode con NFKC/minúsculas;
ignora orden y puntuación. El resultado fue:

- `full_page_inventory_passed`; **187/187 páginas con texto nativo esperado**,
  más p1 sin texto nativo y con OCR selectivo.
- `pypdf`: 55 158 palabras; Skopos: 55 079; intersección multiconjunto:
  **54 997**. Mínimo de recuperación por página contra `pypdf`: **0,979**
  en p61; ninguna p2–188 cayó por debajo del umbral diagnóstico 0,95.
- 17 páginas tuvieron comparación inferior a 0,99. En p8, p61, p65,
  p111 y p167 se revisaron las diferencias de tokens: los ejemplos observados
  son palabras fragmentadas o unidas de forma distinta entre extractores.
  No se adjudicaron visualmente todas las diferencias de las 17 páginas.
- Mutaciones controladas: quitar una página produjo
  `native_page_inventory`; vaciar el texto de p61 produjo
  `page_61_missing_text`. El control positivo completo pasó.

Esto acredita **cobertura y concordancia técnica entre dos lecturas de la
capa de texto del PDF**, no fidelidad frente a la imagen ni exactitud de
cada función institucional. La portada y los organigramas conservan los
límites de los expedientes [p1](imss-p1-visual-ocr-gate-2026-10-08.md) y
[p18–22](skopos-imss-problem-pages-visual-review-2026-10-08.md).

## Recuperación bilateral y siguiente gate

Una sesión con Mongo y host documental bajo demanda devolvió
`consumer_smoke_passed` para el derivado nativo de **188 páginas**.
Otra sesión recuperó por `fetch_evidence` líneas exactas de p2, p18,
p22, p23, p61 y **p188**, rechazó un `item_id` inexistente, y cerró host
y Mongo. Después el socket estaba ausente y el puerto 37034 cerrado.
Las solicitudes/sobres persisten bajo la retención ya aceptada del piloto.

El siguiente gate de uso es una muestra visual independiente y estratificada
de funciones en p23–188, más anotación de cajas, rótulos y conexiones de
p18–22. Para aceptar una cita concreta se recuperará siempre la página y
el fragmento exactos; no se promueve todo el manual por el conteo anterior.
La continuidad después del vencimiento de política requiere decisión y
renovación separadas. Sin vectores, admisión al corpus ni operación continua.
