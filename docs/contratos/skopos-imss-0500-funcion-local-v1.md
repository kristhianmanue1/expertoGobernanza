# Función local Skopos: manual IMSS 0500-002-001

**Ámbito:** consulta bajo demanda en este Mac desde expertoGobernanza. Perfil
separado del manual DPM `2000-002-001`; ambos conservan hash, política,
recibo y derivados independientes. El runtime se inicia por llamada y se
apaga en `finally`. No es admisión al corpus ni verificación de vigencia.

Fuente: [PDF oficial IMSS](https://www.imss.gob.mx/sites/all/statics/pdf/manualesynormas/0500-002-001_3.pdf),
80 páginas, SHA-256
`ce665959759f74331464471c71dc9cff107e061de09b8be5419a7cf1302e48b7`.
La copia y procedencia están en `docs/fuentes/imss/0500-002-001_3*`.

## Invocación

```sh
cd /Users/krisnova/www/expertoGobernanza
.venv/bin/python -m scripts.skopos_imss_0500 page 45
.venv/bin/python -m scripts.skopos_imss_0500 page 1
.venv/bin/python -m scripts.skopos_imss_0500 ocr 37
.venv/bin/python -m scripts.skopos_imss_0500 search 'infraestructura médica' --limit 5
.venv/bin/python -m scripts.skopos_imss_0500 item 45 <item_id>
.venv/bin/python -m scripts.skopos_imss_0500 graph
```

`page` entrega líneas con página física, bbox, `item_id`, modalidad e
identidad del manifiesto; p1 usa OCR selectivo, p2–80 texto nativo. `ocr 37`
expone la capa OCR selectiva del organigrama sin tratarla como rótulos
validados. `search`
es literal y devuelve candidatos, no cobertura semántica. `item` comprueba
que el ítem pertenezca a la página pedida. `graph` devuelve el derivado
visual de p37, actualmente `partial`; sus nodos/aristas son hipótesis del
extractor. La caja DPM visible no está transcrita completa por ese derivado.

El cliente comprueba hash del PDF, procedencia, política, host y manifiestos,
consulta por socket Unix y devuelve `runtime=stopped` sólo tras comprobar
apagado de host y Mongo. En error sale con código distinto de cero y no
entrega un fragmento parcial para citar. El perfil de Skopos vive en
`/Users/krisnova/www/aria/skopos/runs/pdf-imss-0500-pilot-v1/`, con política
que vence `2026-11-08T00:00:00Z`; el retiro o renovación exige revisión
explícita. No borres sockets ni eludas locks si hay un proceso concurrente:
reconcilia controlador, puerto 37034 y recibos antes de reintentar.

La evidencia bilateral con Ágora está en
`docs/evidencia/imss-0500-bilateral-2026-10-08/`. Ágora recibe fragmentos
UTF-8 seleccionados y localizadores, verifica hashes y deja la relación
entre manuales como candidata sin apoyo semántico verificado ni admisión.
Cada cita nueva exige cotejo de página y fragmento en el PDF custodiado.
