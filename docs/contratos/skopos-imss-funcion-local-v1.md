# Función local Skopos para el manual IMSS 2000-002-001

**Ámbito de aceptación:** consumo por agentes de expertoGobernanza en este
Mac, bajo demanda. Es una función local operativa; el runtime se enciende por
consulta y se apaga al terminar. No es un servicio continuo ni una admisión
jurídica al corpus.

Esta instalación de Mac fija el productor en
`/Users/krisnova/www/aria/skopos` y sus políticas y datos privados bajo
`runs/pdf-document-imss-pilot-v1/` de ese checkout. Es una ruta local histórica
del runtime, aunque la interfaz de consumo sea una función operativa. Mover
el checkout exige repinear configuración, hashes y pruebas bilaterales.

La fuente es el [PDF oficial del IMSS](https://www.imss.gob.mx/sites/all/statics/pdf/manualesynormas/2000-002-001.pdf),
con copia local `docs/fuentes/imss/2000-002-001.pdf` y SHA-256
`719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`.
Su procedencia se documenta en
`docs/fuentes/imss/2000-002-001-PROCEDENCIA.md`. El contrato acepta la
recuperación e identidad técnica acotadas por los manifiestos fijados; cada
cita nueva exige cotejar la página y el fragmento visibles del PDF.

## Invocación del agente

Desde la raíz de expertoGobernanza:

```bash
.venv/bin/python -m scripts.skopos_imss page 188
.venv/bin/python -m scripts.skopos_imss page 1
.venv/bin/python -m scripts.skopos_imss search 'MANUAL DE ORGANIZACIÓN' --limit 5
.venv/bin/python -m scripts.skopos_imss item 188 <item_id>
.venv/bin/python -m scripts.skopos_imss label 21 --node n5
```

`page` devuelve texto, modalidad, página física, caja e ID de cada línea;
p1 usa OCR selectivo y p2–188 texto nativo. `search` hace búsqueda literal
en el manifiesto nativo completo (p1 sin texto nativo) y devuelve candidatos
con localizadores; `--limit` admite 1–20;
`item` recupera una línea exacta por ID. `label` devuelve los nodos p18–22
del contrato Skopos v0.5, con `literal_text` y `normalized_text` separados.
En p21 `n5` lo impreso termina en `SALUID`; `SALUD` sólo es normalización.
La salida informa fuente, URL, identidad, regla de cita y `runtime=stopped`.
Un fallo sale por stderr con código distinto de cero; no devuelve texto
parcial para citar.

El comando verifica hash del PDF, procedencia, política, configuración y
manifiestos antes de consultar. Inicia el Mongo dedicado y el host necesario,
consulta por socket Unix y detiene los procesos propios en `finally`.
Concurrencia sobre el mismo controlador falla cerrado. Tras SIGKILL o corte
de energía debe ejecutarse el preflight de
`/Users/krisnova/www/aria/skopos/scripts/pdf_custody_pilot.py` y revisar el
estado del controlador, sockets y puerto 37034 antes de reintentar; no borrar
sockets ni matar procesos ajenos por nombre. Una parada forzada del hijo se
reporta como fallo de limpieza y exige la misma reconciliación.
La política vigente vence `2026-11-08T00:00:00Z`; este contrato no la renueva.

Identidades fijadas: derivación nativa
`372fdaef7fb1171ec8dce708b79ef1e32b38e43dfb1b079e6b27ae070d8f7587`
y manifiesto `7f81b1616b10549439cd536737e76663cfea7cec3bf7a6ec3fbf10241d8292ed`;
OCR `7f132071b5e1c372e41d0ce9a83df7c966955c7fcb7036f80cdcbcecf5654a46`
y `3ca9d7a5be5e451f63608015585a4eee92d2109046d390de99d793ac2f83651d`.
Etiquetas v0.5: manifiesto `0d79b1e5d10219e844aa54b3d470ccf57a5868611a5a4fe8b5fb1d0fce58e20a`,
derivación `ae1609defbfc0d6441452cae23a36bc6109fadce0ab51b4dfab0fa55dda7b778`
y configuración canónica local `b9333d73a7eabf4ed8bc5e272de20ad81954f9edeaa3eb2c82f708b2e916888f`.

## Alcance de fidelidad

El cotejo visual previo abarcó 86 recuadros de p18–22 y ocho funciones
seleccionadas de p23–188. Fue no ciego. No valida automáticamente los demás
fragmentos, la completitud de flechas del organigrama ni la vigencia
institucional de funciones. El agente debe recuperar el ítem, cotejarlo con
la imagen de la página y citar página física y fuente oficial. La salida
`content_currentness=not_established` recuerda que una consulta técnica no
resuelve vigencia normativa.
