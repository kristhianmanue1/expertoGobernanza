# Checkpoint de sesión — 2026-08-07

**Objetivo:** adoptar la política v1.1 + sprint del backlog (4 pasos) + ronda adversarial real.

## Hecho (verificable)
- **Política v1.1 adoptada** (`2860f55`): fusión de la enmienda multi-provider en `politica-agentes.md` (§6 quórum ≥3 proveedores, §7.3 compuertas, §7.4 datos, §9 roles, §10 ADR). DoD cumplido (run sobre componente F + reconciliación humana).
- **Sprint 4 pasos:** (1) golden set `tests/` — **34 tests** stdlib, congela gate v1 + regresiones B1/B2/B3; (2) router §7.4 `review_routing/`; (3) id ordinal `CPEUM:4:Psalud`→`CPEUM:4:P4` (M2); (4) CI `.github/` + ADR-0002 (firma, propuesto).
- **Ronda adversarial REAL** (`2ca2250`): claude/Anthropic + codex/OpenAI + glm-5.2 (autor excluido) = 3 familias. **3 ciclos → PROCEED unánime**. Cerró: traversal/bypass, **symlink in-repo**, interno siempre denegado v1, atomicidad. Evidence: `docs/propuestas/2026-08-07-router-m2-round/` (reviews verbatim + `RECONCILIACION.md`).
- **Memoria AN-KLA rev 4→6** (6 facts). Fact de estado: `estado-2026-08-07-post-ronda`.
- **Git:** `main` = `82cf761`, **sincronizado con origin** (`kristhianmanue1/expertoGobernanza`).

## Siguiente
1. Reconciliar vigencia con **DOF nivel 1** (quitar `[VIGENCIA-NO-VERIFICADA]`).
2. **Eje estructural IMSS**: ingerir LOAPF + LFEP + Reglamento Interior (modelar la entidad IMSS=OPD).
3. Designar **roles §9** (responsable jurídico del corpus, custodio, product owner — interino = humano).
4. **Recall de extracción** (golden set del eslabón LLM no-determinista) → v1.2.
5. **Harness de revisión** (egress de red real, log append-only externo, bundle sellado, anonimización para interno) — deuda declarada del router.
6. **Ronda adversarial sobre el rename M2** si se quiere promulgar `CPEUM:4:P4` como formalmente estable (los revisores lo verificaron al pasar; no fue foco del ciclo 2/3).

## Bloqueos / deuda
- Responsable jurídico y custodio del corpus **sin designar** (interino = humano-promulgador).
- `cline`/`qwen` no usables desde bash (OAuth discontinuado / hub error); `codex` y `claude` sí → usar esos para el quórum.
- ADR-0002 (firma): requiere que el humano genere clave GPG y active `Require signed commits`.
- `retrieve` AN-KLA es sensible a keywords; el fact stale `alfa-estado-2026-08-06` (rev 0 / Python 3.10) puede aparecer con queries genéricas — **fiarse de AGENTS.md + `an_kla status`**.

## Archivos clave
- Gobernanza: `AGENTS.md`, `docs/politica-agentes.md` (v1.1), `docs/adr/0001-*`, `docs/adr/0002-*`.
- MVP: `corpus/{lookup,verify_citations}.py`, `corpus/derived/cpeum/CPEUM-004-P4-salud.json`, `tests/`, `review_routing/{router.py,config.json}`, `.github/`.
- Evidencia ronda: `docs/propuestas/2026-08-07-router-m2-round/`.

## Reanudar con
Leer `AGENTS.md` (estado actual + próxima tarea) + este checkpoint;
`an_kla --project-root . status` (rev 6) + `retrieve --query "router estable ronda claude codex proceed próximos pasos"`;
`git status` + `git log --oneline -5`.
