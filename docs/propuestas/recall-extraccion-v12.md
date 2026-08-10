# Diseño — Golden set de extracción de citas (v1.2 / R1-E4-01)

**Estado:** diseño · **Fecha:** 2026-08-10 · **Depende:** auditor v0 (E3)  
**No ejecuta LLM en este doc.** Router §7.4: solo texto **público**.

## Objetivo

Medir el eslabón **no determinista**: dado un documento, el extractor (LLM u otro)
devuelve claims `{disposicion_id?, cita_texto}` y se evalúa contra un **gold**.

El gate `verify_claim` / `audit_document` queda como **juez determinista** post-extracción.

## Formato gold (por documento)

```json
{
  "doc_id": "synth-salud-01",
  "texto": "…documento sintético público…",
  "gold_claims": [
    {
      "claim_id": "g1",
      "disposicion_id": "CPEUM:4:P4",
      "cita_texto": "…verbatim o casi…",
      "must_find": true
    }
  ],
  "traps": [
    {"claim_id": "t1", "cita_texto": "afirmación falsa…", "must_find": false}
  ]
}
```

- `must_find: true` → si el extractor no produce una cita **alineable** al gold → **FN**.  
- Cita inventada que el extractor devuelve y no está en gold ni en corpus → **FP**
  (tras `verify_claim` = bajo o match falso).

## Alineación extractor ↔ gold

Una predicción `p` matchea gold `g` si:

1. mismo `disposicion_id` (si el extractor lo emite; si no, solo por texto), y  
2. `normalize(p.cita)` es subcadena de `normalize(g.cita)` o overlap ≥ umbral
   documentado (v1.2 default: subcadena o igualdad normalizada).

## Métricas

| Métrica | Definición |
|---------|------------|
| Recall | TP / (TP+FN) sobre gold `must_find` |
| Precision | TP / (TP+FP) sobre predicciones |
| Gate-bajo rate | fracción de predicciones con `verify_claim` = bajo |

## Proveedores / datos

- Solo docs **sintéticos o públicos** del corpus (auth `autorizacion-fuentes-r1.md`).  
- Allowlist CLI igual que auth.  
- **CI:** extractor **fake** determinista (sin red).  
- Run manual: plugin real opcional, sin commitear secretos ni logs de texto interno.

## Semilla reproducible

- Fixtures bajo `tests/fixtures/extraction_gold/`.  
- Fake extractor: devuelve subset fijo de gold + 0–1 trampa configurable.  
- Seed numérico en config si el plugin real usa sampling.

## Fuera de alcance v1.2

- Jurisprudencia, IMSS interno, ranking BM25 de AN-KLA, bitemporalidad.

## DoD del diseño (este ticket)

- [x] Formato gold + métricas + fake/CI + §7.4  
- [ ] E4-02 fixtures ≥3  
- [ ] E4-03 `eval_extraction.py` + tests fake  
