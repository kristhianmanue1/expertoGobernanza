**Resumen (lente A — corrección/fidelidad):**

- **B1 (symlink público→confidencial): CERRADO.** `_confined()` resuelve symlinks vía `.resolve()` y `route()` (router.py:105-112) clasifica tanto `rel` como `rel_resolved` tomando la clase más restrictiva (`_most_restrictive`, router.py:63-69) → un symlink hacia un archivo `personal_confidencial` queda denegado con `prohibicion_dura`, exactamente como cubre `test_symlink_publico_a_confidencial_denegado`.
- **B2 (auto-afirmación de autorización interna): CERRADO.** No existe `--authorize-internal-ref` en `main()`; `interno_institucional` siempre deniega con `interno_anonimizacion_pendiente` (router.py:111), sin ningún camino de escape para el agente.
- `_matches`/`classify` mantienen precedencia correcta (`personal_confidencial` > `interno_institucional` > `publico` > `deny`) y el fix de prefijo con `/` evita el bypass tipo `docs/adr/**` vs `docs/adresses/`.
- Verifiqué el rename `CPEUM:4:Psalud → CPEUM:4:P4` contra `docs/fuentes/cpeum/art-004.txt`: el 4º párrafo del Art. 4 es efectivamente "protección de la salud" (P1=igualdad, P2=decidir hijos, P3=alimentación/maíz, P4=salud). Correcto.

Encontré dos issues menores de fidelidad (no BLOCKER, reportados arriba): el docstring del módulo (línea 5) sigue describiendo una vía de autorización humana para `interno_institucional` que F2 eliminó, y `_denied_reason()` quedó como código muerto con un valor de razón obsoleto que contradice el dict inline real usado en `route()`.

**Decisión: proceed** (con limpieza sugerida de docstring/código muerto, no bloqueante).
