# Reconciliación final — benchmark IMSS fidelidad + EvidenceEdge

**Fecha:** 2026-08-10 · **Estado técnico:** `proceed` unánime  
**Autor excluido:** OpenAI/Codex · **Quórum:** Anthropic + Moonshot + Zhipu/GLM

| Proveedor | Pass 1 | Retry final |
|---|---|---|
| Anthropic | `fix-and-retry` (BLOCKER) | `proceed` |
| Moonshot | `fix-and-retry` (HIGH) | `proceed` |
| Zhipu/GLM | `proceed` (LOW) | `proceed` |

## Decisión

El gate técnico R2 queda superado: 5/5 preguntas, 5/5 controles negativos,
cero FP/FN por arista y cuatro originales recomputados. Se autoriza un **spike
AKN local y aislado sobre `LSS:5`**, no adopción, migración ni serving.

## Reservas aceptadas

1. Git sigue `PARCIAL (espera-admin)`: los hashes no son sello de tiempo.
2. La cobertura semántica y la granularidad de párrafo son atestaciones v0.
3. El benchmark mide regresión/consistencia, no ground truth jurídico abierto.
4. `LOAPF:1` conserva metadata agregada inconsistente con una reforma parcial;
   se abre como deuda separada y se excluye del spike.
5. El resultado base conserva `benchmark_id` sin sufijo R2; la cadena documental
   RONDA→PREREGISTRO-RETRY→RESULTADOS-RETRY desambigua la ejecución.

## Agregación

No quedó BLOCKER. Los MED no alcanzaron mayoría sobre un defecto que invalide
R2; se preservan como límites. El HIGH de commit se clasifica como
`PARCIAL (espera-admin)`, consistente con la regla proyecto proponer/aplicar:
impide cierre durable/merge, no el spike local reversible autorizado por el humano.

**Actualización posterior:** la deuda LOAPF y F5 LFEP señalada aquí fue resuelta
en R3; ver `RECONCILIACION-R3.md`. Este documento conserva el cierre histórico R2.
