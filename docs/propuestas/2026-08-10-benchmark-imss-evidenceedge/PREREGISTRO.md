# Prerregistro — benchmark falsable IMSS sobre EvidenceEdge v0

**ID:** `R1-BENCH-IMSS-EE-01` · **Fecha:** 2026-08-10  
**Estado:** cerrado antes de ejecutar · **Autor:** OpenAI/Codex (sin voto)  
**Alcance:** gate técnico; no es opinión jurídica ni benchmark competitivo

## Hipótesis

El gate aporta valor si distingue afirmaciones textuales con traza suficiente de
afirmaciones no verificadas o interpretativas, sin heredar vigencia entre
instrumento, disposición y relación.

## Muestra fija

| ID | Pregunta | Resultado esperado | EvidenceEdge esperado |
|---|---|---|---|
| Q1 | ¿Qué disposición define al IMSS como organismo público descentralizado? | respondible | `LSS:5|define_naturaleza|IMSS` |
| Q2 | ¿Qué disposición ubica a los organismos descentralizados en la APF paraestatal? | respondible | `LOAPF:1|ubica_clase|administracion_publica_paraestatal` |
| Q3 | ¿Qué disposición atribuye al IMSS organizar y administrar el Seguro Social? | respondible | `RIIMSS:1|define_objeto|Seguro_Social` |
| Q4 | ¿Puede afirmarse automáticamente que LFEP:5 remite específicamente a la LSS? | bloqueada | ninguna; F5 de `LFEP:5` sigue pendiente |
| Q5 | ¿Puede concluirse automáticamente que LSS:5 integra al IMSS al régimen de LFEP:1? | bloqueada | ninguna; es relación interpretativa |

La redacción y los resultados esperados quedan fijados en
`benchmarks/imss_evidence_edge_cases.json`. El catálogo candidato queda fijado
en `benchmarks/fixtures/imss_evidence_edges.json`.

## Protocolo

1. Validar cada candidata con `validate_evidence_edge`.
2. Comprobar que `source_ref` existe, corresponde a la disposición sujeto, que
   la cita está en `texto_verbatim` y que el hash coincide con una fuente del JSON.
3. Considerar elegible sólo una arista para la que `is_traversable` sea `true`.
4. Comparar por igualdad exacta el conjunto elegible con el preregistrado.
5. No generar una respuesta libre ni usar LLM durante la evaluación.

## Métrica y criterio de muerte

- Éxito: **5/5 casos exactos**, cero aristas inválidas, cero fallos de fidelidad,
  cero falsos positivos y al menos dos casos respondibles y dos bloqueados.
- Fracaso: cualquier resultado distinto. Un falso positivo bloquea por sí solo.
- Sólo un éxito autoriza ejecutar el spike AKN. El éxito no autoriza adopción,
  serving ni afirmaciones sobre superioridad frente a productos externos.

## Reproducción prevista

```bash
python3 scripts/benchmark_imss_edges.py
python3 -m unittest tests.test_benchmark_imss_edges -q
```

## Control de mutabilidad

Este prerregistro es evidencia local previa al resultado, no sello de tiempo.
Hasta el commit administrativo puede modificarse; la relatoría deberá publicar
su SHA-256 observado al ejecutar y cualquier desviación invalidará el benchmark.
