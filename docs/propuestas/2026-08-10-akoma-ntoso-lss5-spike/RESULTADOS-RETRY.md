# Resultados R2 — spike Akoma Ntoso LSS:5

**Estado:** éxito técnico · **Decisión final:** `adaptador` experimental

## Checks

| Check | Resultado |
|---|---|
| XML vs XSD OASIS pinneado | válido; hash XSD coincide |
| Inversa XML→subconjunto JSON | exacta |
| Texto y SHA-256 | idénticos |
| Versiones | cuerpo 2026-01-15; porción 2001-12-20 |
| Determinismo | una salida |
| Tests | 7 OK |
| Script | 248 líneas, stdlib |
| Corpus/registry | no modificados por spike |

XML R2: `afad20a0eaff575a6704f2196cdd34a1d3fe1a7b11a71e3058bb551b10a23826`.

## Matriz exhaustiva por grupos del JSON fuente

| Campo/grupo | Mapeo | Pérdida/reserva |
|---|---|---|
| `disposicion_id` | `FRBRalias` | exacto |
| `instrumento.id` | alias interno; `FRBRname=lss` | exacto por inversa |
| `instrumento.nombre_oficial` | `original@showAs` | parcial; no vuelve en inversa |
| `jerarquia_documental.articulo` | `article/eId/num` | exacto tras inversa `Artículo 5.`→`5.` |
| `jerarquia_documental.elemento` | ninguno | pérdida total |
| `texto_verbatim` | `article/content/p` | exacto |
| `vigencia.estado` | ninguno | pérdida; XML no afirma vigencia |
| `vigencia.ultima_reforma_dof_declarada` | fecha de reforma de porción | parcial |
| `vigencia.verificada_contra_dof_nivel1` | ninguno | pérdida crítica |
| `vigencia.marcador/traza/registry_ref` | ninguno | pérdida crítica |
| `vigencia.nota_cuerpo` | sólo fecha de versión de Expression | parcial; resto perdido |
| `fuentes_oficiales.tipo/nivel/archivo/fecha_consulta` | ninguno | pérdida |
| `fuentes_oficiales.sha256/extracto_verbatim_en` | ninguno | pérdida crítica |
| `relaciones_normativas` | no se exportan | exclusión intencional |
| `lineage` completo | ninguno | pérdida |

La Expression 2026-01-15 representa el consolidado del cuerpo usado como fuente;
`last-amendment-of-portion=2001-12-20` sólo describe `LSS:5`. Ninguna fecha AKN
prueba vigencia. El sidecar de procedencia/EvidenceEdge es obligatorio para todo
uso distinto de visualización estructural.

## Desviación del prerregistro

AKN 1.0 core no permite `FRBRauthoritative` en Manifestation. R2 lo declara en
Expression para señalar que la edición XML no es oficial, sin negar autoridad al
Work legislativo. Ningún consumidor LegalDocML real fue probado; sólo XSD OASIS.

La validación XSD usa la copia oficial pinneada en `interop/akn/schema/` junto
con su dependencia `xml.xsd`; ambos hashes se comprueban antes de `xmllint`.
`includedIn=#lss` resuelve el `eId` de `original`, que apunta al Work contenedor;
la Expression identifica la versión consolidada exportada.
