# Consumo bilateral del grafo IMSS v0.3 experimental

**Estado:** intercambio técnico probado bajo demanda; relaciones y rótulos
visuales no adjudicados. **Última observación:** 2026-10-08 en México.
Productor: Skopos `8791d90cfa006c621e9e6ee3c007db73c381e11c`, verificado en
`origin/main`. Consumidor: expertoGobernanza, cliente
[`skopos_graph_review_pilot.py`](../../scripts/skopos_graph_review_pilot.py).

## Identidades y alcance

Fuente IMSS `2000-002-001.pdf` SHA-256
`719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`.
El grafo padre v0.1 tiene manifiesto SHA-256
`8a1880b84b0e52f934f09759f3a83efb5a3a752afda914d6c5cce9c7803aaaee`.
El contrato nuevo es `expertogobernanza/skopos-graph-review`, versión
`v0.3-experimental`, con derivación
`3cd64933f11b0e64733565b4c7acf99423bca129fc7ee5526daf35962cd8504c`
y manifiesto SHA-256
`5b6db3341f0f6058356de157ea5bab74bbffeceb9d38cfb0892869f25d076884`.
La configuración local quedó fijada por hash canónico
`8ee6ec7b550dfcee2eb244425d39f8af8a15301fc89a074214eebfb695c02515`.
Estas identidades se comprobaron de los archivos publicados en Skopos;
su contrato está en
`/Users/krisnova/www/aria/skopos/docs/contratos/pdf-graph-review-v0.3-experimental.md`.

La proyección cubre sólo los organigramas p18–22: 86 nodos y 81 aristas
candidatas, 36 añadidas desde la autorrevisión visual no ciega del productor.
El estado de las páginas es `partial` y el de cada arista
`visual_candidate_unadjudicated`. Sólo cinco nodos tienen un rótulo visual
corregido como candidato; los demás mantienen el OCR bruto sin revisar.
La dirección `layout_parent_to_child_candidate` describe el dibujo y no
acredita jerarquía jurídica por sí misma.
El cliente comprueba estos estados en los 86 nodos y las 81 aristas del
manifiesto fijado, incluidas las 36 de origen `nonblind_visual_review`.

## Prueba desde expertoGobernanza

Se arrancó el Mongo dedicado y el host v0.3 bajo demanda con el procedimiento
del contrato; el cliente propio envió solicitudes con sobre correlacionado
al `requests_root` ya autorizado y comprobó:

- `describe_graph_review`: identidad, fuente y `unreviewed_partial`.
- `get_graph_review_page`: bytes lógicos exactos del manifiesto para cada
  página 18, 19, 20, 21 y 22; conteos `8/7`, `32/31`, `10/9`, `19/18`,
  `17/16` (nodos/aristas).
- `fetch_graph_review_item`: un nodo corregido de p22 (`n10`) y la arista
  añadida `n3→n8`, con `item_id`, modalidad, página, fuente, hash de render,
  derivación, manifiesto y estado coincidentes.
- Rechazos sin resultado parcial: fuente errónea `source_mismatch`, hash de
  manifiesto erróneo `graph_identity_mismatch`, p23 fuera del contrato
  `page_out_of_scope` e ítem inexistente `evidence_unavailable`.

La salida fue `consumer_graph_review_passed`; el procedimiento detuvo host
y Mongo. `./scripts/ci_check.sh` pasó 219 pruebas y el gate de tamaños
sobre el cliente preparado. La sesión crea solicitudes y sobres persistidos
bajo la retención del piloto, sin cambiar política ni admitir el PDF al corpus.

Como control visual propio, se renderizó p22 a 2200 px. La caja `n10` visible
dice «COORDINACIÓN TÉCNICA DE INFRAESTRUCTURA MÉDICA» y el trazo de la caja
`n3` (gestión de calidad) llega a `n8` (división de gestión de calidad).
Esto corrobora esos dos ejemplos concretos; no revisa las otras 80 aristas
ni los cuatro rótulos corregidos restantes. El recibo del productor cubre
todos los pares pero es autorrevisión, no adjudicación independiente.

**Límite de uso:** el servicio v0.3 permite consultar candidatos con
trazabilidad y recuperar el PDF completo por el contrato documental v0.1.
No demuestra fidelidad de las 188 páginas ni autoriza citas automáticas de
relaciones orgánicas. Para promover rótulos o aristas hace falta cotejo visual
independiente de los elementos que se usarán y decisión de autoridad. La
política de retención vence el `2026-11-08T00:00:00Z`; no se renovó.
