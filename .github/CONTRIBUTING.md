# Cómo contribuir — ExpertoGobernanza

El trabajo se rige por `docs/politica-agentes.md` (v1.1). Resumen operativo:

## Antes de abrir un PR
1. **Contrato verificable:** cada cambio trae su DoD como checks ejecutables (tests,
   `check_sizes`, archivo existe y < N, norma citada a su fuente). Sin check, no es PR.
2. **Gate de tamaño (§3):** ejecuta `python scripts/check_sizes.py` → exit 0. Líneas
   "Duro": código <800, artefacto <800, doc on-demand <1500, always-on (`AGENTS.md`) <300.
3. **Tests:** `python -m unittest discover -s tests` → verde. Sin nuevas dependencias salvo
   necesidad justificada (y entonces pinéalas en `requirements.txt` con hash).
4. **Fidelidad documental (§7):** toda afirmación normativa cita instrumento + artículo +
   fecha de reforma verificada. Vigencia: si no se verificó contra DOF nivel 1, marca
   `[VIGENCIA-NO-VERIFICADA]`. Redactar ≠ promulgar (el agente propone; un humano aplica).

## Commits y ramas
- **Conventional Commits:** `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`.
- Ramas cortas (`feat/`, `fix/`). PRs < 400 líneas diff idealmente. Nunca `--force` a main.
- El agente **propone** commit/PR; un **admin** (CODEOWNERS) aplica push a `main`.

## Ronda adversarial (§6)
- Hito menor → quorum-lite (1 revisor en contexto fresco).
- Hito de **alto impacto** (cambios a la política, ADR estratégico, compuertas de
  fidelidad, corpus normativo, despliegue) → **≥3 proveedores distintos** por modelo
  subyacente, revisión ciega, lentes por rol; cualquier BLOCKER bloquea.

## Reportar issues
Describe el problema con evidencia (comando + salida, o cita exacta a la fuente). Para
vulnerabilidades, ver `SECURITY.md`.
