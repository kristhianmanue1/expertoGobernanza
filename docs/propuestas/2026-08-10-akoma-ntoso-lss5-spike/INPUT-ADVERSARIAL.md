# Entrada ciega — gate del spike Akoma Ntoso LSS:5

**Autor excluido:** OpenAI/Codex · **Impacto:** alto por decisión estratégica  
**Objeto:** auditar `adaptador | diferir | no adoptar`

## Archivos

- `PREREGISTRO.md`, `RESULTADOS.md`, `DECISION.md`
- `scripts/akn_spike.py`
- `interop/akn/lss-005.akn.xml`
- `tests/test_akn_spike.py`
- `corpus/derived/lss/LSS-005.json`
- XSD temporal oficial:
  `/private/tmp/eg-akn-schema-20260810/akomantoso30.xsd`

## Preguntas

1. ¿El XML es AKN 1.0 válido y el uso de `portion`, FRBR, IRI y `eId` es correcto?
2. ¿El roundtrip y la matriz de pérdida están completos y reproducibles?
3. ¿`adaptador` es proporcional o el resultado exige `diferir/no adoptar`?
4. ¿Existe alguna afirmación normativa o de interoperabilidad exagerada?
5. ¿Se preserva la frontera: AKN no equivale a vigencia/EvidenceEdge?

Sólo defectos de corrección/requisitos. Formato con severidad, fix y
`DECISION: proceed | fix-and-retry | escalate`. No modificar archivos ni
proponer una plataforma AKN más amplia.
