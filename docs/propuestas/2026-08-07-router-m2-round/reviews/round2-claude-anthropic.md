**Modelo subyacente: Claude Sonnet 5 (Anthropic).**

Revisión ciega, lente A (corrección/fidelidad del gate y router), ciclo 2 — verificación de fixes sobre `review_routing/router.py`, `tests/test_router.py`, `review_routing/config.json`.

**Verificación de los 6 fixes declarados:**

1. **Colisión de prefijo (`_matches`)** — `prefix = pattern[:-2]` conserva la `/` final (`router.py:34-35`), verificado: `"docs/adresses/secreto.md"` ya no matchea `"docs/adr/**"`. Confirmado por test y por `python3 -m pytest` (21/21 pass) y por `review_routing/config.json` real (`review_routing_evil/x.py` → deny, `router.py:151` cubre esto en `TestRealConfig`). **Cerrado.**
2. **Confinamiento de ruta** — `_confined()` (`router.py:63-71`) resuelve `root/rel` y exige `is_relative_to(root)`; `route()` además rechaza explícitamente absolutos y segmentos `".."` (`router.py:88`). Cubre traversal (`docs/adr/../../../etc/passwd`), rutas absolutas (`/etc/passwd`), y symlinks fuera de repo (por `resolve()` + `is_relative_to`). **Cerrado**, con una redundancia inocua: el chequeo explícito de `..`/absoluto en `route()` (`router.py:88`) es superfluo dado que `_confined` ya lo captura vía `is_relative_to`, pero no introduce falso verde.
3. **`--authorize-internal-ref`** — reemplaza el booleano por un string de referencia externa (`router.py:157-158`), y queda registrado en el log (`internal_authorization_ref`, `router.py:110`). Nota de fidelidad: el valor sigue siendo un string arbitrario que el propio agente puede fabricar en el CLI (`--authorize-internal-ref "cualquier-cosa"`) — no hay verificación criptográfica contra un registro real de autorización. Esto es consistente con lo que el docstring ya declara como límite ("bitácora de auditoría, NO... enforceada"), así que no lo elevo a BLOCKER, pero **no es una barrera técnica real**, solo trazabilidad para auditoría posterior humana. [LOW, ya declarado como límite]
4. **Atomicidad fail-closed** — `main()` retorna 1 si hay `denied` y no se pasó `--allow-partial` (`router.py:187-188`). Verificado con `test_main_atomico_parcial_no_cero` y `test_main_allow_partial_escapa`. **Cerrado.**
5. **`config_sha256` en salida y log** — presente en `decision["config_sha256"]` (`router.py:171`) y en el log (`router.py:104`). **Cerrado.**
6. **Tests adversariales** — `TestAdversarial` y `TestRealConfig` cubren traversal, colisión de prefijo, absolutos, interno sin ref, atomicidad, y prefijo real del propio repo. Todos pasan (21/21).

**Hallazgo no bloqueante (LOW):** `write_log` solo se invoca `if not args.dry_run and decision["bundle"]` (`router.py:184`) — si **todo** el input es denegado (bundle vacío) en modo no-dry-run, no se escribe nada en el log, perdiendo la traza de los intentos denegados en ese caso particular. Dado que el docstring promete "bitácora... (c) bitácora con hash de bundle Y de config", esto es una laguna de auditoría menor, no un bypass de seguridad.

**Rename `CPEUM:4:P4`:** fuera del diff entregado en este ciclo (solo se incluyó código de `review_routing/`). No puedo evaluarlo como parte de "código corregido" de esta ronda; inspección rápida de `corpus/derived/cpeum/CPEUM-004-P4-salud.json` muestra que el propio artefacto se autodeclara "Pendiente de confirmación contra DOF nivel 1" — no emito veredicto sobre su corrección, está fuera del alcance de este ciclo de verificación del router.

**No se detectan bypasses nuevos** (case-sensitivity no es explotable como bypass — solo produce falsos-deny, dirección segura; backslashes se normalizan en `_matches` y `_confined`; rutas tipo `C:\...` no escapan el confinamiento en POSIX).

**Decisión: proceed**
