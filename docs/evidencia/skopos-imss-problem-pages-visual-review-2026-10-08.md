# Cotejo visual del consumidor: páginas problemáticas del PDF IMSS

**Estado:** diagnóstico manual de p1 y p18–22; no referencia ciega de
fidelidad ni admisión al corpus. **Observación:** 2026-10-08 (México).

## Material y método

- Original conservado en `docs/fuentes/imss/2000-002-001.pdf`, 188 páginas,
  SHA-256 `719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`.
  La [ficha de procedencia](../fuentes/imss/2000-002-001-PROCEDENCIA.md)
  contiene la URL oficial y el alcance de su cotejo anterior.
- Recalculé los SHA-256 de los manifiestos Skopos: OCR
  `3ca9d7a5be5e451f63608015585a4eee92d2109046d390de99d793ac2f83651d`
  y visual
  `8a1880b84b0e52f934f09759f3a83efb5a3a752afda914d6c5cce9c7803aaaee`.
  Sus `derivation_id` son, respectivamente,
  `7f132071b5e1c372e41d0ce9a83df7c966955c7fcb7036f80cdcbcecf5654a46`
  y `1ef12d5a480075214369e9d19dcb6949370119e212b84007ce1b1a5ef1b7b8cf`;
  los manifiestos están bajo `runs/pdf-document-imss-pilot-v1/derived/`
  en Skopos.
  Ambos derivan del original identificado, con `fidelity_status=unreviewed`.
- Rendericé de nuevo el PDF original con `pdftoppm -scale-to 2200 -png`
  para p1 y p18–22 y leí directamente las imágenes. Comparé regiones
  seleccionadas con `native_text`, `ocr_text` y `visual_graph` del manifiesto.
  Las imágenes temporales no son un artefacto custodiado; el PDF y el comando
  permiten repetir la inspección. El cotejo es autorrevisión visual, posterior
  a ver las salidas de Skopos, no anotación independiente ni muestra ciega.

## Comparación por página física

| Página | Original visible | Manifiesto Skopos | Hallazgo del consumidor |
| --- | --- | --- | --- |
| 1, portada | Título, autorización, cargo, sello y párrafo inferior escaneados | `native_text=no_text`; OCR 20 líneas | Título y sello principal legibles en OCR. El cargo dice visualmente «Dirección» y el OCR `Dirécción`. En el párrafo, OCR `realzará`, `Confictos`, `Pudicas` donde se leen «realizará», «Conflictos», «Públicas». Esas líneas tienen `confidence=1.0`: la confianza del motor no es fidelidad. No se transcribió el párrafo completo. |
| 18, organigrama general | 8 cajas conectadas; entre ellas Unidad de Atención Médica, Unidad de Planeación e Innovación en Salud y Unidad de Infraestructura, Servicios Médicos Indirectos e Integración Sectorial | 8 nodos, 7 aristas; 7 líneas nativas fuera de las cajas; OCR de las cajas | La topología registrada coincide preliminarmente con las conexiones visibles. OCR n2 `PLANEACION E NOVACIÓN EN SALU`, n3 `lIDAD ENCIÓN MÉD` y n5 `LININA DE INFRA...` pierden partes materiales del rótulo. El texto nativo no ofrece candidato dentro de ninguna caja. |
| 19, Unidad de Atención Médica | Organigrama denso con 32 cajas contadas visualmente, incluida «Coordinación de Unidades de Primer Nivel» | 32 nodos, 19 aristas; OCR n4 vacío y nativo `COORDINACIÓN DE UNIDADES DE PRIM ER NIVEL` | Faltan en el grafo las conexiones visibles de la Unidad hacia sus coordinaciones n3–n9; no debe tratarse como árbol completo. Muchos rótulos OCR son fragmentos, p. ej. n1 `PRESIACONAS`, n6 `SPECAALIDA` y n18 `ADULTOS`. El nativo conserva más texto, con espacios internos erróneos. |
| 20, Unidad de Educación e Investigación | 10 cajas y 9 conexiones visibles sin flechas de dirección | 10 nodos, 9 aristas; OCR n3 vacío y n4 `COBRARON BE` | El texto nativo localizado en las mismas cajas recupera «Coordinación de Educación en Salud» y «Coordinación de Investigación en Salud». El [cálculo acotado](skopos-label-eval-consumer-review-2026-10-08.md) reproduce 7/10 rótulos nativos exactos y 1/10 OCR; no mide el resto del PDF. |
| 21, Unidad de Planeación e Innovación en Salud | 19 cajas contadas visualmente, con conectores hacia divisiones | 19 nodos, sólo 5 aristas (raíz, Unidad y cuatro coordinaciones); OCR n10 vacío | El grafo omite las ramas inferiores visibles. La caja n10 dice «División de Medicamentos y Reactivos»; el nativo la aproxima como `DIVISIÓN DE M EDICAM ENTOS Y REACTIVOS`, mientras el OCR no da línea. |
| 22, Unidad de Infraestructura… | 17 cajas contadas visualmente, incluidas dos coordinaciones técnicas y sus divisiones | 17 nodos, sólo 5 aristas superiores; OCR n10 y n11 vacíos | Faltan conexiones inferiores. La caja n10 dice «Coordinación Técnica de Infraestructura Médica» y n11 «Coordinación Técnica de Equipamiento Médico»; existen líneas nativas con espacios internos, pero no rótulos OCR. |

En p19, p21 y p22, un árbol visible conectado y sin ciclos tendría
respectivamente 31, 18 y 16 relaciones entre esas cajas; el manifiesto
contiene 19, 5 y 5. Este es un **conteo visual preliminar**, no un conjunto
de aristas anotadas y adjudicadas una por una. No asigné dirección formal:
los trazos no muestran puntas de flecha y el manifiesto marca `unknown`.

## Consecuencia para el contrato

La detección de cajas y la lectura de sus nombres deben evaluarse por
separado de la cobertura de conectores. Para p19, p21 y p22, una consulta
que pida relaciones completas debe devolver `partial` y enumerar lo no
resuelto; no debe inferir que la ausencia de arista significa ausencia de
dependencia. `label_candidates` puede mejorar la revisión de nombres al
conservar nativo y OCR con página, caja e `item_id`, pero no repara por sí
solo las conexiones omitidas. El siguiente gate exige anotación visual
independiente de cajas, rótulos y conectores para p18–22 y métricas por
página; la portada requiere evaluación OCR de regiones, no de grafo.
