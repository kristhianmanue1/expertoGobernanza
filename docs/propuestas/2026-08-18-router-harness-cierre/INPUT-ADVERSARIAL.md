# INPUT adversarial — cierre router harness (RH-T08)

**Fecha:** 2026-08-18 · **Quórum:** quorum-lite (1 revisor en contexto fresco,
política §6; hito de cierre sin cambio de política). **Revisor:** subagent
glm-5.2 (misma arquitectura subyacente que el autor — decorrelación de
**contexto**, no de proveedor; limitación declarada).

## Tu papel

Eres revisor adversarial independiente. NO confías en los docstrings ni en los
tests: **verificas atacando**. Puedes escribir y ejecutar código efímero en
`/var/folders/q1/k3y040sd0rv9cbxcdskwr_zw0000gp/T/opencode/` (usa `.venv/bin/python`
del repo para correr). Reportas hallazgos, no los corriges.

## Superficie bajo ataque (todo en `review_routing/`, stdlib, Python 3.12)

- `seal.py` — sello `eg-harness/seal-v1`: `build_seal`, `verify_seal`,
  `read_bundle`.
- `audit_log.py` — cadena tamper-evident: `append`, `verify_chain`
  (ancla F1).
- `gateway.py` + `scripts/route_review.py` — ruta sancionada dry-run
  (`gateway.run`, CLI exit 0/1).
- `router.py` — clasificación/confinamiento heredado (classify, route,
  _confined, _most_restrictive).
- Tests existentes: `tests/test_seal.py` (21), `tests/test_audit_log.py` (15),
  `tests/test_gateway.py` (9), `tests/test_router.py` (~30).

## Superficies de ataque exigidas por el plan (03-tareas.md RH-T08)

1. **Sellado:** ¿se puede forjar un sello que verifique sin poseer el
   contenido? ¿colisiones por canonicalización (unicode, floats, NaN)?
   ¿bytes vs str? ¿manifest duplicado/extra/faltante? ¿bundle_sha256
   inconsistente con el contenido?
2. **Cadena de log:** ¿alterar/borrar/reordenar/saltos de seq sin detección?
   ¿reconstrucción desde genesis vs ancla? ¿append sobre log malicioso?
   ¿linea final sin \n, CRLF, BOM, entradas anidadas?
3. **Fail-closed del gateway:** ¿algún camino que devuelva ok con denegados?
   ¿--allow-partial filtra contenido prohibido al sello? ¿bundle vacío con
   exit 0? ¿errores de lectura convertidos en ok silencioso?
4. **Path traversal heredado del router:** .., absolutos, symlinks (in-repo y
   out-of-repo), backslashes en POSIX, mayúsculas/normalización unicode,
   prefijos colisionantes (`review_routing_evil/`), rutas resueltas vs
   pedidas.

## Formato de salida (obligatorio)

Para cada hallazgo: `ID | severidad (BLOCKER/HIGH/MED/LOW) | archivo:línea |
descripción | PoC (comando o código mínimo que lo demuestra)`.

Veredicto final exactamente uno: `proceed` (sin BLOCKER/HIGH abierto) |
`fix-and-retry` (hay BLOCKER/HIGH reparable) | `escalate`.

Además: lista de checks ejecutados (comando + resultado una línea). Sé
adversarial de verdad: un `proceed` sin ataques intentados no vale.
