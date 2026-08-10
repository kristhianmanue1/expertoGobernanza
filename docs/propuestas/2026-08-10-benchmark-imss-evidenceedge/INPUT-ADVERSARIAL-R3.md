# Entrada adversarial R3 — cierre F5, granularidad y gate

**Hito:** alto impacto · **Autor excluido:** OpenAI/Codex  
**Decisión solicitada:** `proceed`, `fix-and-retry` o `block`

## Objeto de revisión

1. ¿La fuente oficial permite marcar F5 de `LFEP:5` como verdadera sin afirmar
   que “sus leyes específicas” nombra a la LSS?
2. ¿`LOAPF:1:P3` resuelve correctamente la reforma parcial del segundo párrafo
   y evita atribuir una fecha única al artículo agregado?
3. ¿El benchmark conserva su falsabilidad: 3 respondibles, 2 bloqueadas, cinco
   negativos rechazados y 0 FP/FN?
4. ¿El gate local/remoto y el paquete administrativo declaran sus diferencias y
   límites sin aparentar CI verde ni commit/PR inexistente?

## Evidencia mínima

- `PREREGISTRO-R3.md` y `RESULTADOS-R3.md`;
- `corpus/registry.yaml`;
- `corpus/derived/lfep/LFEP-005.json`;
- `corpus/derived/loapf/LOAPF-001.json` y `LOAPF-001-P3.json`;
- casos, fixtures, runner y tests del benchmark;
- `scripts/ci_check.sh`, `.github/workflows/ci.yml`, `docs/ops-github.md`;
- `docs/gobernanza/paquete-admin-2026-08-10-imss-f5-gate.md`.

Todo BLOCKER bloquea. Reportar severidad, evidencia verificable y arreglo
concreto. Las revisiones no promulgan normas ni autorizan merge.

