# Recibo bilateral local: Skopos → expertoGobernanza → Ágora

**Observación:** 2026-10-08, Mac local. **Estado:** comportamiento técnico
comprobado bajo demanda; relación semántica y vigencia institucional pendientes
de revisión. Los PDF originales y su procedencia están en
`docs/fuentes/imss/0500-002-001_3*` y `2000-002-001*`.

## Ejecución y resultado

1. Desde expertoGobernanza, `.venv/bin/python -m scripts.skopos_imss_0500`
   recuperó `page 45`, `page 1`, `ocr 37`, `graph`, `search 'infraestructura médica'`
   e `item 45 1f34c691088742641564c57fca9722efc76e42213d58c199b9674cfef786768e`.
   Se conservaron `skopos-0500-page1.json`, `skopos-0500-ocr37.json`,
   `skopos-0500-graph37.json`,
   `skopos-0500-search.json` y `skopos-0500-item45.json`, además de la
   respuesta p45. Cada salida informó `runtime=stopped`. p45: 37 líneas nativas con
   `item_id`, bbox y manifiesto fijado; p1: 23 líneas OCR, con errores visibles
   como `FECHA_ 2 6 DIC. 2022`; p37: 52 nodos, 39 aristas, estado `partial`.
   La búsqueda literal devolvió una línea de p46. El control negativo pidió
   ese ítem de p45 en p44: salida 1, `item_page_mismatch`, sin contenido para
   citar (`skopos-0500-wrong-page.err`). El control negativo no guardó la
   salida de proceso como artefacto estructurado; el código 1 consta en el
   registro de ejecución de esta tarea. Una observación posterior de sockets
   ausentes y puerto 37034 cerrado está en `runtime-stop-check.json`; es una
   instantánea local, no prueba histórica de cada ciclo de apagado.
2. El consumidor antiguo `.venv/bin/python -m scripts.skopos_imss page 172`
   recuperó 39 líneas nativas del otro manual, también con `runtime=stopped`.
   Se conservaron las respuestas operativas en `skopos-0500-page45.json` y
   `skopos-2000-page172.json` (SHA-256 respectivamente
   `6de4ebe19dd800c29478e0b72dd4308c0064cb3b26d09fc2497691ea7791f010`
   y `aaee5352ae552f001b22afce334a0a433ae697943c8a7dc1d0de3fb68a54ef21`).
3. `agora.skopos_page_bridge` cotejó ambas respuestas con sus manifiestos
   Skopos fijados, seleccionó p45 `item_id=1f34…6768e` y p172
   `item_id=e40f…4beb` y produjo los dos pares `agora-*-derived.txt` y
   `agora-*-exchange.json`. `agora.source_evidence_exchange validate`
   comprobó cada original con `original_integrity=sha256_verified`.
   Un cambio de texto en una copia de la respuesta p45 fue rechazado con
   `skopos_page_content_mismatch` y salida 2.
4. `resolve-bundle` con `agora-relation-candidate.json` produjo
   `agora-relation-result.json`: dos SHA de originales diferentes, localizadores
   p45 y p172, `status=candidate_unreviewed`, `semantic_support=not_verified`,
   `admitted=false`, `provider_calls=0`. La reproducción desde los archivos
   conservados produjo bytes idénticos (`cmp`).

## Reproducción sin iniciar Skopos

```sh
cd /Users/krisnova/www/expertoGobernanza
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/krisnova/www/aria/agora/src \
  /Users/krisnova/www/aria/agora/.venv/bin/python -m agora.source_evidence_exchange resolve-bundle \
  --derived docs/evidencia/imss-0500-bilateral-2026-10-08/agora-0500-derived.txt \
  --manifest docs/evidencia/imss-0500-bilateral-2026-10-08/agora-0500-exchange.json \
  --original docs/fuentes/imss/0500-002-001_3.pdf \
  --derived docs/evidencia/imss-0500-bilateral-2026-10-08/agora-2000-derived.txt \
  --manifest docs/evidencia/imss-0500-bilateral-2026-10-08/agora-2000-exchange.json \
  --original docs/fuentes/imss/2000-002-001.pdf \
  --candidate docs/evidencia/imss-0500-bilateral-2026-10-08/agora-relation-candidate.json
```

Estos archivos acreditan el intercambio local observado, no la autenticidad
institucional del PDF, fidelidad visual del OCR/organigrama, equivalencia
jurídica de funciones ni vigencia. El gráfico p37 omite el rótulo completo de
DPM y su arista hacia Dirección General; esa caja se cotejó visualmente por
separado. El contrato de Ágora se fusionó en su `main` mediante el PR #1;
su checkout local debe estar disponible para repetir el comando.
