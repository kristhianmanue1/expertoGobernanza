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
Esa comprobación inicial corroboró dos ejemplos concretos. El recibo del
productor cubre todos los pares pero es autorrevisión, no adjudicación
independiente.

### Ampliación visual acotada de p22

En una segunda lectura del render a 2200 px, tracé las 16 conexiones de p22
de caja a caja antes de comparar el conjunto con el manifiesto. Agrupadas por
origen, fueron: `n1→n2`; `n2→n3,n5,n4,n6`; `n3→n8,n12,n17`;
`n5→n9,n13`; `n4→n7,n14`; `n6→n10,n11`; `n10→n15`; `n11→n16`.
La comparación de conjuntos devolvió 16 pares esperados y 16 emitidos,
sin faltantes ni extras; todas esas aristas siguen con estado
`visual_candidate_unadjudicated`. Esta es una revisión visual del consumidor
separada del productor, pero de una sola instancia agéntica y sólo de p22.
Esta lectura de p22 no corrige los errores OCR de otros nodos ni evalúa las
65 aristas de p18–21, examinadas en la sección siguiente.

### Ampliación visual de p18–21

Rendericé p18–21 a 2200 px desde el mismo PDF fijado y seguí cada trazo
visible entre cajas. Identifiqué los nodos por posición y caja en el
manifiesto v0.3; la notación `n1→n2,n3` significa dos pares distintos.
La lista visual, preparada antes de comparar conjuntos, fue:

- **p18 (7):** `n1→n3,n4,n2,n5,n6,n7`; `n7→n8`.
- **p19 (31):** `n1→n2`; `n2→n3,n4,n5,n6,n7,n8,n9`;
  `n3→n10,n12,n20`; `n10→n11,n19`; `n4→n13,n21,n27,n31`;
  `n5→n14,n22,n28,n32`; `n6→n15,n23,n29`; `n7→n16,n24`;
  `n8→n17,n25`; `n9→n18,n26,n30`.
- **p20 (9):** `n1→n2`; `n2→n3,n4`; `n3→n5,n7,n9`;
  `n4→n6,n8,n10`.
- **p21 (18):** `n1→n2`; `n2→n3,n5,n6,n4`;
  `n3→n7,n11,n15,n18`; `n5→n8,n12`; `n6→n9,n13,n17`;
  `n4→n10,n14,n16,n19`.

La comparación de conjuntos devolvió 7/7, 31/31, 9/9 y 18/18,
respectivamente, sin faltantes ni extras frente al manifiesto; todas las
65 aristas conservan `visual_candidate_unadjudicated`. Las 81 relaciones
de p18–22 cuentan ahora con un cotejo visual del consumidor, separado de
la autorrevisión del productor, pero realizado por una sola instancia
agéntica y sin adjudicación institucional. En p19 los trazos compartidos
entre columnas merecen especial atención en una revisión posterior.

La capa de texto nativa del PDF contiene etiquetas de p19–22, mientras que
p18 tiene poca información nativa en el área gráfica. El grafo v0.3 aún
conserva numerosos rótulos OCR incompletos; el cotejo de aristas no corrige
esos rótulos ni demuestra fidelidad textual de las 188 páginas.

**Límite de uso:** el servicio v0.3 permite consultar candidatos con
trazabilidad y recuperar el PDF completo por el contrato documental v0.1.
No demuestra fidelidad de las 188 páginas ni autoriza citas automáticas de
relaciones orgánicas. La lectura visual de esta instancia no sustituye la
adjudicación del Operador de los elementos que se usarán. La
política de retención vence el `2026-11-08T00:00:00Z`; no se renovó.
