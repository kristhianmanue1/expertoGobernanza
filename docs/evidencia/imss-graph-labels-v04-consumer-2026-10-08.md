# Consumo bilateral de rótulos IMSS v0.4 experimental

**Estado:** intercambio técnico probado bajo demanda; rótulos candidatos no
adjudicados. **Observación:** 2026-10-08, México. Productor Skopos
`edd6b391bd677a360d85d14423b15dd8bdd21a19`, observado en `origin/main`.
Consumidor: [`skopos_graph_labels_pilot.py`](../../scripts/skopos_graph_labels_pilot.py).

## Identidad y alcance

La fuente PDF IMSS es `2000-002-001.pdf`, SHA-256
`719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`.
El padre es el manifiesto gráfico v0.3 SHA-256
`5b6db3341f0f6058356de157ea5bab74bbffeceb9d38cfb0892869f25d076884`.
Skopos publicó `expertogobernanza/skopos-graph-labels/v0.4-experimental`,
derivación `54ef4a35842a22896b1f881eb9a1c4c6076ac80e469d83dcbafa81f32e6c7e45`,
manifiesto SHA-256
`07018142b74249edf0bc056f3b10bee5d1d004e43e77f556b3ef745027efaa98`
y configuración privada con hash canónico
`1b21129583a5de8aac2938b00e594df36654452afc6e3c348983387ddd03803b`.
El contrato productor está en
`/Users/krisnova/www/aria/skopos/docs/contratos/pdf-graph-labels-v0.4-experimental.md`.

La proyección cubre los 86 nodos de los organigramas p18–22: 8 rótulos de
lectura visual no ciega, 77 reconstruidos por posición desde texto nativo y
uno con corrección visual explícita de `SALUID` a `SALUD`. Cada registro
conserva página, caja, ítem padre, hash del render, método, texto nativo y
rótulo candidato. Todos tienen `status=candidate_unadjudicated` y el
manifiesto `fidelity_status=unreviewed_partial`. No se modificó v0.3.

## Prueba del consumidor

Se arrancó el Mongo dedicado y el host v0.4 con el procedimiento del
contrato. El cliente propio verificó los pins, la correlación de sobre y
respuesta, `describe_graph_labels`, y `get_graph_labels_page` para las cinco
páginas. Las respuestas coincidieron con el manifiesto íntegro, con conteos
8, 32, 10, 19 y 17. `fetch_graph_label_item` recuperó p18 `n3`, p21 `n5` y
p22 `n10`, incluidos fuente, página, hash del render y estado.

Cuatro controles negativos devolvieron resultado nulo y códigos esperados:
fuente incorrecta `source_mismatch`, manifiesto incorrecto
`labels_identity_mismatch`, página 23 `page_out_of_scope` e ítem inexistente
`evidence_unavailable`. La salida fue `consumer_graph_labels_passed`.
El procedimiento apagó host y Mongo y no dejó socket. El cliente verifica
además los ocho rótulos de p18 contra una transcripción visual previa del
consumidor y la corrección aislada p21 `n5`.

Esta prueba acredita recuperación, procedencia técnica y rechazo de entradas
fuera de contrato en este entorno. Antes de ejecutar el cliente hubo lectura
visual manual de los ocho rótulos de p18 y muestras de p19–22 (p19: `n1`,
`n3`, `n12`, `n20`; p20: `n4`, `n5`, `n6`; p21: `n3`, `n5`, `n9`, `n14`; p22:
`n3`, `n6`, `n10`, `n11`, `n16`). El cliente automatizado fija los ocho textos
de p18 y la corrección de p21 `n5`, pero no repite esa lectura de imágenes.
No existe aún un cotejo visual independiente de los 86 textos. La fidelidad
de las 188 páginas, la vigencia normativa y la interpretación institucional de las relaciones
permanecen fuera de este resultado. La retención vigente termina el
`2026-11-08T00:00:00Z`; no se renovó. El piloto permanece bajo demanda.
