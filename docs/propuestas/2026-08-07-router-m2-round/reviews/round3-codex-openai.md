> **Estado general:** OK  
> **Modelo subyacente:** OpenAI GPT-5 · **Conflicto:** ninguno  
> **Revisión:** ciega; no se consultaron dictámenes ajenos  
> **Fecha:** 2026-08-07 · **Hito:** router §7.4, ciclo 3

B1 y B2 quedaron cerrados dentro del alcance declarado del router.

## Hallazgos

- [MED] `--allow-partial` está descrito como diagnóstico, pero puede devolver éxito y escribir log fuera de `--dry-run`; un harness automatizado podría aceptar una ronda incompleta — [router.py:157](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:157), [router.py:167](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:167), [test_router.py:153](/Users/krisnova/www/expertoGobernanza/tests/test_router.py:153) — exigir `--dry-run` cuando se use `--allow-partial`, o eliminarlo del wrapper de producción. No permite enviar el archivo denegado y no reabre B1/B2.

- [LOW] El docstring aún afirma que el contenido interno puede pasar con autorización humana y el helper muerto conserva `sin_autorizacion_humana`, contradiciendo v1 — [router.py:5](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:5), [router.py:56](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:56), frente a [router.py:88](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:88) — actualizar el docstring y eliminar `_denied_reason`.

## Verificación de los BLOCKER anteriores

- **B1 cerrado:** `_confined()` resuelve el enlace y verifica confinamiento; luego se clasifican la ruta solicitada y la canónica, aplicando la clase más restrictiva antes de `read_bytes()` — [router.py:64](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:64), [router.py:98](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:98), [router.py:108](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:108). La regresión está en [test_router.py:130](/Users/krisnova/www/expertoGobernanza/tests/test_router.py:130).

- **B2 cerrado:** `interno_institucional` siempre toma `interno_anonimizacion_pendiente`; no existe argumento de autorización en el CLI — [router.py:109](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:109), [router.py:150](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:150). Incluso `--allow-partial` no convierte un bundle compuesto sólo por contenido interno en éxito.

- **Fail-closed:** ruta desconocida → `default_deny`; faltante → `archivo_no_encontrado`; cualquier denegado produce salida 1 salvo la excepción diagnóstica explícita — [router.py:108](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:108), [router.py:115](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:115), [router.py:170](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:170).

- **Auditoría:** se registran hashes deterministas del bundle y de la configuración, junto con proveedor/modelo y decisiones — [router.py:121](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:121), [router.py:131](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:131). El log local sigue siendo manipulable y no prueba que esos bytes exactos fueran enviados; son precisamente límites del harness excluidos por el encargo.

Checks ejecutados: 10 pruebas sin escritura pasaron; checks adversariales in-memory para B1/B2, faltante, desconocido, hash y exit code pasaron; AST, `git diff --check`, tamaños y AN-KLA `verify` pasaron. El suite completo no pudo crear `TemporaryDirectory` por el sandbox de solo lectura; no hubo fallos de aserción.

Para cada ronda real, el harness debe fijar la configuración/hash aprobado, prohibir `--allow-partial` salvo dry-run y materializar exactamente los bytes hasheados. La inmutabilidad externa del log, bundle sellado y control de red permanecen como deuda fuera de alcance.

**Decisión: proceed**
