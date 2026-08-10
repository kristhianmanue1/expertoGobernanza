# Paquete administrativo — cierre IMSS F5 y gate R3

**Estado:** listo para revisión; espera administrador  
**Fecha/hito:** 2026-08-10 · pasos 1–4  
**Autor material:** OpenAI/Codex · **autoridad Git:** CODEOWNERS/admin

## Decisión solicitada al administrador

Revisar el alcance, ejecutar el gate canónico, seleccionar únicamente los
archivos de este hito y crear commit/PR. El agente no hizo `git add`, commit,
push ni PR: la política del proyecto reserva esas acciones al administrador.

## Alcance del paquete

- Cierre F5 de `LFEP:5` contra el decreto DOF 16-07-2025, sin promover la
  relación genérica hacia la LSS.
- Segmentación `LOAPF:1:P3`; la reforma de 18-03-2025 queda asociada sólo a P2.
- Benchmark R3 y pruebas de regresión.
- Gate local `scripts/ci_check.sh` y paso equivalente en GitHub Actions.
- Prerregistro, resultados, ronda adversarial y relatoría R3.

El worktree contiene también artefactos previos de EvidenceEdge, benchmark y
Akoma Ntoso que forman la cadena de dependencia. No deben incluirse por patrón
ciego; el administrador debe revisar `git status` y el diff antes de seleccionar.

## DoD a reproducir

```bash
./scripts/ci_check.sh
.venv/bin/python -m an_kla --project-root . verify
git diff --check
git status --short
```

Resultado local después de fixes adversariales: 124 pruebas OK; benchmark 5/5,
3 respondibles, 2 bloqueadas, cinco negativos rechazados, 0 FP/FN; tamaño OK.
GitHub Actions sigue suspendido por presupuesto: esto es DoD local, no CI verde.
La ronda R3 cerró 3/3 `proceed` (Moonshot, Zhipu y xAI), sin BLOCKER.

## Propuesta de commits

1. `fix(corpus): cerrar F5 LFEP y segmentar LOAPF`
2. `ci(benchmark): exigir gate IMSS EvidenceEdge`
3. `docs(governance): cerrar ronda R3 del eje IMSS`

Si el administrador prefiere un solo PR, título sugerido:
`fix(imss): cerrar F5 LFEP, granularizar LOAPF y fijar gate R3`.

## Checklist admin

- [ ] Revisar fuentes oficiales, hashes y reserva semántica LFEP→LSS.
- [ ] Confirmar que Q2 usa `LOAPF:1:P3`, nunca el agregado.
- [ ] Confirmar ronda adversarial válida y ausencia de BLOCKER.
- [ ] Ejecutar DoD local y adjuntar salida corta al PR.
- [ ] Seleccionar archivos explícitamente; excluir cambios no relacionados.
- [ ] Tras el staging, ejecutar `git diff --cached --check` para cubrir también
  los archivos que hoy son nuevos/no rastreados.
- [ ] Crear commit/PR sin push directo a `main` ni `--force`.
- [ ] Registrar URL/commit final y, entonces, actualizar estado administrativo.
