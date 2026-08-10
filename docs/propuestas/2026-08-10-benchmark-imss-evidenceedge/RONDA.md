# Ronda adversarial — benchmark IMSS EvidenceEdge — pass 1

**Fecha:** 2026-08-10 · **Autor excluido:** OpenAI/Codex  
**Quórum:** Anthropic + Moonshot + Zhipu/GLM · **Impacto:** alto confirmado

| Proveedor | Decisión | Máxima severidad |
|---|---|---|
| Anthropic | `fix-and-retry` | BLOCKER |
| Moonshot | `fix-and-retry` | HIGH |
| Zhipu/GLM | `proceed` | LOW |

## Agregación

**Resultado: `fix-and-retry`.** Cualquier BLOCKER bloquea. Los hallazgos del voto
`proceed` también se incorporan. No se autoriza el spike AKN.

## Orden de corrección

1. Renombrar el objeto evaluado como gate compuesto `fidelidad + EvidenceEdge`.
2. Añadir trampas de cita, fuente y hash dentro de las mismas cinco preguntas.
3. Exigir cobertura completa del catálogo y contar falsos positivos por arista.
4. Recomputar originales locales y verificar extractos versionados.
5. Corregir citas Q1/Q2, granularidad Q2 y estado interpretativo Q5.
6. Acumular errores estructurales y de fidelidad; fijar fecha de evaluación.
7. Crear prerregistro de retry con nuevos hashes y repetir el quórum.
