# Adversarial — Plan R2 borrador — 2026-10-05

**Artefacto:** `docs/plan-r2.md` antes de los parches de esta página.
**Quórum:** 2 revisores en contexto fresco, lentes distintos, **un solo proveedor** (Grok). Autor excluido de la revisión. No hay segundo ni tercer modelo. Por `docs/politica-agentes.md` §6 el resultado es **PARCIAL (espera-humano)**. No es `proceed`.

## Hallazgos que se incorporaron

- [HIGH] T1 dejaba vivo `fake_extract` y no ataba el argumento de `extract`. Fix: borrar `fake_extract`, un solo `--extractor stub`, y un test de que el argumento es `doc["texto"]`.
- [HIGH] Los golden de CPEUM y LGS fijan `v1`, `source_resolved` y `medio`. En esta máquina, con PDF y resolver verdadero, T4 los pasa a `alto`. Fix: reescribir esas aserciones; mock sin disco para las cuatro ramas.
- [HIGH] No hay PyYAML ni `pip install` en CI. `ci_check.sh` fallaría al importar el loader. Fix: pin, install en el venv y el mismo paso en `ci.yml` antes de unittest. Sin el import, T3 no cierra.
- [HIGH] El flag `verificada_contra_dof_nivel1` de CPEUM y LGS coincide con el resolver, así que un test de `relaciones_normativas` no prueba que el gate use el resolver. Fix: mock con ese flag en `true`, hash ok y resolver en `false` → no `alto`.
- [HIGH] `alto` y el retiro de `N/A_v1` se leen como vigencia jurídica. El código vigente llama a `alto` «apto para decisión». Fix: tres chequeos mecánicos; `version_valid_for_date` queda en `no_evalua_fecha_juridica`; la tabla del PR se rotula como salida del resolver.
- [HIGH] El banner por cualquier `vigencia_verificada: true` no distingue `LSS:1` (`f5: false`). Fix: el banner no es el gate por disposición, no autoriza `alto` y puede seguir en `PARCIAL_O_OK`.
- [MED] La frase «alto si y solo si recomputo y resolver» omitía el substring. Fix: las tres condiciones; sin substring, `bajo`.

No se descartó ningún HIGH.

## Decisión

- [ ] proceed
- [x] fix-and-retry — los HIGH quedaron escritos en `docs/plan-r2.md` por el autor, que es el mismo proveedor. No hubo re-ronda fresca después del parche.
- [ ] escalate

Un humano puede leer el plan afinado. Merge de H1 o H2 sigue exigiendo ≥3 proveedores por modelo y `proceed`. H0, cuando se ejecute, admite quórum-lite.
