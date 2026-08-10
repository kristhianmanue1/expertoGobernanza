# R3 pass 1 — Zhipu / GLM-5.2

**Resultado:** `block` · **Fecha:** 2026-08-10 · **Autor excluido:** sí

GLM reprodujo 123 tests y el benchmark, pero `ci_check.sh` terminó con código 2
porque `git diff --check` encontró espacios finales en el checklist F5. Clasificó
la afirmación de DoD verde como BLOCKER mientras el wrapper fallaba.

También señaló:

- MED: el runner aceptaba mínimos `answered >= 2` / `blocked >= 2`, no la cuota
  exacta prerregistrada 3/2;
- LOW: Q5 dependía sólo de `status: disputed`, aunque la cita no cubría objeto ni
  relación.

Se aceptó el bloqueo. Los fixes fueron: limpiar whitespace, exigir exactamente
3/2/5, negar `covers_object` y `covers_relation` en Q5, agregar test de mutación
y alinear `ultima_reforma_cuerpo.cubre_disposicion: false`.

