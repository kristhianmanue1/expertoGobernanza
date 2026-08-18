# Paquete administrativo — router harness H0+H1 (sello + bitácora)

**Estado:** listo para revisión; espera administrador
**Fecha/hito:** 2026-08-18 · plan `docs/planes/router-harness/` hitos H0–H1
**Autor material:** Zhipu/glm-5.2 (opencode) · **autoridad Git:** CODEOWNERS/admin

## Decisión solicitada al administrador

Merge de **PR #28 y luego PR #29** (apilado: #29 tiene base `feat/rh-t01`;
al mergear #28, GitHub re-apunta #29 a `main` automáticamente — verificar
antes de approvar). Sin merges, el agente NO continúa con RH-T05/T06
(decisión de pausa: no apilar un 3er piso sobre PRs sin fusionar).

## Alcance

- **PR #28** (`feat/rh-t01` → `main`, 313 líneas): RH-T01
  `review_routing/seal.py` (sello `eg-harness/seal-v1`: `build_seal` /
  `verify_seal` / `read_bundle`; F2 sin TOCTOU, F4 re-clasificación con
  `router.classify`) + RH-T02 `tests/test_seal.py` (21 tests). Commits
  `ee0d881`, `18d527a`.
- **PR #29** (`feat/rh-t03` → `feat/rh-t01`, 307 líneas): RH-T03
  `review_routing/audit_log.py` (`append` + `verify_chain`; cadena de hash
  con genesis 64 ceros, ancla externa F1, fail-closed sobre log roto) +
  RH-T04 `tests/test_audit_log.py` (15 tests). Commit `a1df24b`.

Ambos son archivos NUEVOS; no tocan código existente (`router.py` intacto).

## Sobre el check rojo de CI en PR #28

`Tests + gate de tamaño` aparece FAIL, pero el job **nunca arrancó**:
anotación de GitHub = *"recent account payments have failed or your spending
limit needs to be increased"* (run 32184192982, 2s, sin pasos ejecutados).
Sigue siendo la suspensión por billing documentada en `docs/ops-github.md`;
la X es artefacto del estado de cuenta, NO una falla de código. Se declara
como DoD local, sin fingir CI verde.

## DoD a reproducir (local, con la rama correspondiente checked out)

```bash
.venv/bin/python -m unittest discover -s tests   # 171/171 OK
.venv/bin/python scripts/check_sizes.py          # 146 archivos OK
git log --show-signature -3 --format="%h %G? %s" # ee0d881/18d527a/a1df24b = G
```

Contado sobre `feat/rh-t03` (incluye ambos PRs): 171 tests; sobre `feat/rh-t01`
solo: 156. Límites: `seal.py` 143<200, `audit_log.py` 121<200.

## Checklist admin

- [ ] Verificar firma G de los 3 commits (ED25519 devcdmx).
- [ ] Reproducir DoD local y adjuntar salida corta al merge.
- [ ] Merge #28 a `main` (squash o merge normal según criterio; el historial
      firmado se conserva mejor sin squash).
- [ ] Confirmar que #29 re-apuntó a `main` y merge #29.
- [ ] (Opcional, cuando se renueve el billing) re-run de CI en `main` post-merge.
- [ ] Reportar merge al agente para retomar RH-T05 (gateway dry-run) sobre
      `main` limpio.

## Límites declarados (no reclamar más de esto)

El sello + bitácora certifican integridad/procedencia del bundle por la ruta
sancionada. NO previenen bypass (invocar al proveedor fuera del gateway no es
detectable — F3); sin `anchor_hash` la bitácora sólo certifica consistencia
interna (F1). Ronda adversarial de cierre del harness = RH-T08 (ADR-0006
pendiente).
