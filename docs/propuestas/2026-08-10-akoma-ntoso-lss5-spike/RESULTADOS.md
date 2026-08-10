# Resultados — spike Akoma Ntoso sobre LSS:5

**Spike:** `R1-AKN-LSS5-01` · **Fecha:** 2026-08-10  
**Estado:** resultado R1 supersedido por el retry adversarial; no usar como cierre

## Integridad

| Artefacto | SHA-256 |
|---|---|
| Prerregistro antes de ejecutar | `6070ad39c25970b4d85dcd581bfc2467186c937c182b36da6c37e43e52c32367` |
| JSON fuente `LSS-005.json` | `78b63f6c736f5dcf993eba65e453b020a2542d30777683f40b053c93e46c33ec` |
| XSD oficial temporal | `6f61fe84cbb6f8cb0e8418cd67b74a63da9990e6573b5a3491f623184f45c4fd` |
| XML producido | `a03bba61ed46d836a1c23394b07dc45f6da5c42e48e2481000652bc94e159078` |
| Script final | `dd00b9d28ccc66a8572e891996320740b671901a4f23a6d344e73979b5d18129` |
| Tests | `43af0ecda809f0e24bd45ccf34351baed30f8aab6ab13cf7ff64bdf97c221331` |

## Ejecución

El primer intento falló en el generador por colisión del argumento `name` con
el atributo `FRBRalias@name`; el XML estático sí validó. Se renombró el argumento
a `element_name` y se repitió toda la ejecución.

| Check final | Resultado |
|---|---|
| XSD OASIS `akomantoso30.xsd` | válido |
| Instrumento/disposición/artículo/texto | 4/4 exactos |
| SHA-256 texto roundtrip | idéntico (`448bc2e6…657d9`) |
| Determinismo | 10 ejecuciones → una salida |
| Unit tests | 5 OK |
| Tamaño script | 183 líneas (<250) |
| Dependencias nuevas | ninguna |
| Mutación de corpus/registry | ninguna por el spike |

## Matriz de pérdida

| Capacidad/campo | Resultado AKN core | Evaluación |
|---|---|---|
| Texto exacto | conservado | sin pérdida |
| Artículo y fragmento | `article`, `eId`, `GUID` | conservado |
| ID interno `LSS:5` | `FRBRalias` + `GUID` | conservado con convención local |
| Work/Expression/Manifestation | explícitos | ganancia |
| Idioma | `FRBRlanguage=spa` | ganancia |
| Referencias interoperables | IRI + `includedIn` | ganancia potencial |
| Publicación/reforma | `FRBRdate` | parcial; no prueba vigencia |
| Hash del original | sin mapeo core usado | pérdida |
| F5 y cobertura de disposición | sin mapeo core | pérdida crítica |
| Revisor/razón/estado EvidenceEdge | sin mapeo core | pérdida crítica |
| Clases de afirmación y gate | sin mapeo core | pérdida crítica |
| Relaciones interpretativas | omitidas intencionalmente | evita promoción |
| Lineage parser/extracción | sin mapeo core usado | pérdida |

La conversión no transporta suficiente información para sustituir el JSON
interno. Un consumidor del XML no puede reconstruir por sí solo si la vigencia,
cobertura o relación fueron verificadas.
