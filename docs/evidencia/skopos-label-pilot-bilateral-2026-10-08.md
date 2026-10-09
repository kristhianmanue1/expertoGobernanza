# Recibo bilateral: candidatos de rótulo PDF v0.2 experimental

**Estado:** `consumer_label_smoke_passed` bajo demanda; fidelidad
`unreviewed`, grafo `partial`. **Fecha local:** 2026-10-08 (México).
**Productor:** Skopos `main@46e32e6bba55d4e4f9f91c48a8010ba834118b8c`.
**Consumidor:** `scripts/skopos_label_pilot.py` de este repositorio.

## Identidad y alcance

El [contrato productor](https://github.com/kristhianmanue1/skopos/blob/46e32e6bba55d4e4f9f91c48a8010ba834118b8c/docs/contratos/pdf-label-candidates-v0.2-experimental.md)
declara `expertogobernanza/skopos-label-candidates/v0.2-experimental`.
La sesión fijó original PDF SHA-256
`719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`,
manifiesto gráfico SHA-256
`8a1880b84b0e52f934f09759f3a83efb5a3a752afda914d6c5cce9c7803aaaee`,
política de rótulos SHA-256
`21540db84c1b6b10cdbd433392caa6ed66b26d9820814c227d2d08dec948be1d`
y política documental padre
`4d09e940ea340ea686c77b4fab84dcf8bb05a371c2119434e60d8744227b3c6b`.
El host v0.2 sirve sólo p18–22, una página por solicitud. P1 permanece
en el derivado OCR v0.1 sin nodos de grafo.

## Ejecución del consumidor

Desde la raíz de Skopos, la sesión comprobó `pdf_custody_pilot.py preflight`,
inició su Mongo dedicado y `skopos.pdf_label_host serve` con la configuración
privada del piloto. Después ejecutó el cliente de expertoGobernanza con
`--socket`, `--requests-root`, `--manifest` y `--derived-root` fijados al
piloto. Una trampa de salida detuvo host y Mongo; la salida devolvió
`stopped`. Se comprobó después socket ausente y puerto 37034 cerrado.

El cliente leyó el PDF local y el manifiesto exacto por SHA, confirmó
identidad/capacidades/retención, y para cada página cotejó respuesta con
manifiesto: nodos y aristas, estado de capas, hash de los bytes PNG,
`parent_item_id`, cajas, y **todas** las líneas nativas/OCR esperadas por
centro de caja en orden, `item_id`, texto y región. Comprobó
`fidelity_status=unreviewed` y `topology_completeness=unreviewed_partial`.
Comprobó el rechazo de tres solicitudes inválidas sin candidatos:
p23→`page_out_of_scope`, SHA falso→`manifest_mismatch` y política falsa→
`label_policy_mismatch`. No se probaron aquí mutaciones reales del PDF.
Una solicitud positiva de p20 quedó con
`request_id=eg-label-consumer-7dcfa65de5e3ec4b5462` y SHA-256 de bytes
`be93c2f734f9e62fdcb6d18f6dbd16c837b60b029e4182f58bb34140862c24de`
en expertoGobernanza,
`runs/pdf-custody-imss-pilot-v1/requests/bb62415c598f03d7ddef56d8.request.json`
(archivo local ignorado
por Git, sujeto a retiro). El cliente verificó que la respuesta repitiera
ambos valores; el resumen de salida no conserva el cuerpo completo.

| Página | Nodos | Aristas | Conectores no resueltos | Sin nativo | Sin OCR |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 18 | 8 | 7 | 0 | 8 | 0 |
| 19 | 32 | 19 | 3 | 0 | 9 |
| 20 | 10 | 9 | 0 | 0 | 2 |
| 21 | 19 | 5 | 4 | 0 | 4 |
| 22 | 17 | 5 | 4 | 0 | 3 |

Todas las filas devolvieron `graph_status=partial`. El consumidor confirmó
`request_persistence=existing_requests_root` y
`response_persistence=none_by_label_host`. Sobres y solicitudes quedan bajo
la retención local ya declarada; no se afirmó que todo el intercambio sea
efímero. La sesión no alteró manifiesto ni original.

## Alcance de la conclusión

Este resultado prueba el intercambio técnico en la máquina y política
indicadas, no que los rótulos sean correctos ni que el grafo sea completo.
El [cotejo visual](skopos-imss-problem-pages-visual-review-2026-10-08.md)
encuentra OCR deformado y conectores inferiores omitidos, especialmente en
p19, p21 y p22. No se admite contenido al corpus ni se automatizan citas.
El siguiente gate es una referencia visual independiente de cajas,
rótulos y conexiones para p18–22, con métricas por página y revisión de
cada evidencia antes de uso normativo.
