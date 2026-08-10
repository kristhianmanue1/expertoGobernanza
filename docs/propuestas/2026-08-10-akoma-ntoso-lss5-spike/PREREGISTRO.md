# Prerregistro — spike Akoma Ntoso sobre LSS:5

**ID:** `R1-AKN-LSS5-01` · **Fecha:** 2026-08-10  
**Estado:** cerrado antes de ejecutar · **Autor:** OpenAI/Codex (sin voto)  
**Unidad única:** `corpus/derived/lss/LSS-005.json`

## Pregunta

¿Un adaptador de borde a Akoma Ntoso 1.0 conserva identidad, estructura y texto
de `LSS:5` con costo pequeño, sin sustituir JSON/YAML interno ni fingir que AKN
resuelve vigencia, procedencia o interpretación?

## Fuentes técnicas oficiales

- OASIS Standard, Akoma Ntoso 1.0 Part 1 (2018):
  `https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html`
- OASIS Standard, Part 2 y XSD normativo:
  `https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part2-specs.html`
- Naming Convention 1.0 (2019):
  `https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/akn-nc-v1.0.html`

El estándar define `portion` para una parte independiente de otro documento,
separa Work/Expression/Manifestation y usa `eId` para fragmentos. Este spike
probará esas capacidades; no copiará ni modificará los documentos OASIS.

## Mapeo fijado antes de ejecutar

| Campo interno | AKN propuesto | Expectativa |
|---|---|---|
| `instrumento.id=LSS` | Work IRI + `FRBRname` | exacto |
| `disposicion_id=LSS:5` | `FRBRalias` + `article@GUID` | exacto |
| artículo `5.` | `article@eId=art_5` + `num` | exacto |
| `texto_verbatim` | `article/content/p` | exacto |
| idioma | `FRBRlanguage=spa` | nuevo dato explícito |
| publicación/revisión | FRBR dates mínimas | parcial, no bitemporal |
| hash/procedencia/F5 | sin equivalente core suficiente | pérdida declarada |
| EvidenceEdge/gate | fuera del XML | pérdida declarada |
| relaciones interpretativas | no exportar | exclusión intencional |

La Manifestation se marcará `FRBRauthoritative=false`: el XML es una conversión
de trabajo, no publicación oficial.

## Criterios de salida

**`adaptador`** sólo si todos se cumplen:

1. XML válido contra `akomantoso30.xsd` oficial OASIS 1.0;
2. roundtrip exacto de instrumento, disposición, número y texto;
3. SHA-256 del texto antes/después idéntico;
4. salida determinista y script <250 líneas, stdlib, sin dependencia nueva;
5. ninguna modificación a `registry.yaml` ni a los JSON normativos;
6. matriz de pérdida identifica todo campo no representado.

**`diferir`** si el XML valida pero requiere extensiones propietarias para los
cuatro campos core o supera el costo. **`no adoptar`** si no valida, cambia texto
o identidad, o induce a tratar la Manifestation como fuente oficial.

## Ejecución prevista

```bash
python3 scripts/akn_spike.py --check interop/akn/lss-005.akn.xml
xmllint --noout --schema /private/tmp/eg-akn-schema-20260810/akomantoso30.xsd \
  interop/akn/lss-005.akn.xml
python3 -m unittest tests.test_akn_spike -q
```

Los XSD viven en `/private/tmp`; no se vendorizan. Aun si resulta `adaptador`,
la decisión no autoriza migración, dependencia runtime ni adopción institucional.
