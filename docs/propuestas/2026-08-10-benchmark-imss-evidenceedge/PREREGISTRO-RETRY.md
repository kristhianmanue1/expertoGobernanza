# Prerregistro de retry — benchmark IMSS sobre fidelidad + EvidenceEdge

**ID:** `R1-BENCH-IMSS-EE-01-R2` · **Fecha de evaluación fija:** 2026-08-10  
**Estado:** cerrado antes del retry · **Autor:** OpenAI/Codex (sin voto)  
**Antecedente:** pass 1 `fix-and-retry`; AKN sigue no autorizado

## Cambio de hipótesis

Este retry no atribuye fidelidad a `is_traversable` aislado. Evalúa el gate
compuesto que exige, en este orden:

1. validez estructural de EvidenceEdge;
2. fuente local segura y existente;
3. sujeto coincidente;
4. cita presente en JSON derivado y extracto versionado;
5. hash declarado coincidente y, si el original local es obligatorio,
   recomputado contra el PDF;
6. autorización de `is_traversable` con fecha inyectada.

## Cinco preguntas; muestra adversarial ampliada

Las preguntas Q1–Q5 no cambian. Cada una conserva su resultado esperado, pero
Q1–Q3 incorporan distractores estructuralmente válidos:

| Pregunta | Positivo esperado | Control negativo añadido |
|---|---|---|
| Q1 | LSS:5 textual | cita fabricada |
| Q2 | LOAPF:1, párrafo no reformado citado | `source_ref` inexistente |
| Q3 | RIIMSS:1 textual | hash divergente |
| Q4 | ninguno | promoción LFEP:5 sin F5, atestiguada `not_verified` |
| Q5 | ninguno | relación interpretativa en estado `disputed` |

Q2 se limita al párrafo que afirma que los organismos descentralizados componen
la APF paraestatal. No afirma que la traza de 1976 cubra todos los párrafos del
artículo 1, uno de los cuales fue reformado posteriormente.

## Criterio de muerte R2

Éxito sólo si, simultáneamente:

- 5/5 preguntas coinciden exactamente;
- las tres aristas positivas pasan estructura, fidelidad y recorrido;
- los cinco controles negativos quedan fuera del conjunto recorrible;
- cero falsos positivos y negativos contados por arista;
- todo edge del catálogo pertenece a alguna pregunta;
- conjunto recorrible global = unión positiva preregistrada;
- fecha de evaluación = `2026-08-10`;
- en la corrida probatoria, los cuatro originales locales existen y sus hashes
  se recomputan correctamente.

Cualquier desviación bloquea. El resultado seguirá siendo un benchmark de
regresión/consistencia sobre muestra fija, no ground truth jurídico abierto.

## Ejecución prevista

```bash
python3 scripts/benchmark_imss_edges.py
python3 -m unittest tests.test_benchmark_imss_edges tests.test_evidence_edge -q
```

Sólo `proceed` de tres proveedores distintos después del retry puede autorizar
el spike AKN aislado. El commit administrativo sigue siendo el dispositivo de
compromiso durable; estos hashes locales no son sello de tiempo.
