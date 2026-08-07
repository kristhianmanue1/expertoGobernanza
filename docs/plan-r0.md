# Plan: R0 — Arranque gobernado de ExpertoGobernanza

**Contexto:** tras reparar el venv (Python 3.12.12 + `an_kla` 0.1.0b6), AN-KLA corre
y `verify` está verde, pero la memoria está en **revisión 1** (1 fact, 1 event) y
`AGENTS.md`/`proposal.json` quedaron desincronizados. Falta git, remoto,
`check_sizes.py` y el primer documento oficial fuente. **Fecha:** 2026-08-06.
**Estado:** borrador. **Roadmap:** R0. **Fuente:** iniciativa humana + hallazgos de
reparación del entorno.

## Objetivo y criterio de cierre
- Objetivo: dejar el proyecto con entorno saneado, memoria y docs sincronizados,
  git+remoto privados activos, gate de tamaño (§3) automatizado, y el primer
  documento oficial fuente identificado y referenciado (no promulgado).
- Cierre (verificable global): `verify` verde · `check_sizes.py` exit 0 · `git
  status` limpio sobre rama `main` con remoto privado · al menos 1 fact de mapeo
  norma↔fuente recuperable por `retrieve`.

## Hitos (cada uno dispara ronda adversarial, §6)
- **H1 — Entorno y docs sincronizados con memoria** [tareas-hechas, falta adversarial]:
  AGENTS.md refleja revisión 2; fact correctivo del venv (3.12) commiteado; JSON obsoletos
  retirados a `.archive/`. *Hito menor → quorum-lite (1 revisor en contexto fresco).*
- **H2 — Git + remoto privados** [tareas-hechas, falta adversarial]: repo local sobre
  `main`, `.gitignore` correcto, remoto privado enlazado, commit base aplicado y pusheado.
  *Hito menor → quorum-lite.*
- **H3 — Gate de tamaño automatizado** [tareas-hechas, falta adversarial]:
  `scripts/check_sizes.py` implementa la tabla Duro de §3 y pasa sobre el árbol.
  *Hito menor → quorum-lite.*
- **H4 — Primer documento oficial fuente referenciado** [pendiente]: doc identificado
  por el humano + fact de mapeo norma↔fuente en AN-KLA (puntero, sin copia verbatim).
  *Toca fidelidad documental (riesgo #1): quorum-lite pero el revisor verifica
  cita↔fuente (§7) antes de `proceed`.*

## Tareas (1 tarea = 1 contrato + 1 salida pequeña)
- [ ] **T1 — sync-agents**: actualizar en `AGENTS.md` el bloque "Estado actual de la
  memoria" y "PRÓXIMA TAREA" a revisión 1 / 1 fact, con fact-id puntero. → ver Contrato T1.
- [x] **T2 — fact-correctivo-venv** ✓: fact `fact-expertogobernanza-venv-reparado-312-2026-08-06`
  commiteado (revisión 1→2) con autoridad `glm-5.2` (model_derived→summary); `verify` ok y
  `retrieve` lo encuentra.
- [ ] **T3 — cleanup-json**: mover `proposal.json`/`authority.json` obsoletos
  (base_revision rev 0) a `.archive/` o regenerarlos para el siguiente write.
- [x] **T4 — git-init** ✓: `git init` rama `main`; `.gitignore` (ignora `.venv*`,
  `.an-kla/`, `__pycache__/`, `.DS_Store`, `/proposal.json`, `/authority.json`);
  commit base `87e69db` sobre `e44c3b1` (fast-forward, autorizado por el admin).
- [x] **T5 — git-remote** ✓: repo `kristhianmanue1/expertoGobernanza` (privado, ya
  existía con solo `LICENSE` Apache); `origin` enlazado y `git push -u origin main`
  exitoso con credenciales `gh` del admin (cuenta `kristhianmanue1`).
- [x] **T6 — check-sizes** ✓: `scripts/check_sizes.py` (140 líneas) implementa la tabla
  Duro §3; exit 0 sobre el árbol; detecta violación de prueba (850 > 800); exenciones
  correctas (`.venv*`, `.an-kla/`, lock, data, docs fuente).
- [ ] **T7 — github-skeleton** *(diferible a R1)*: `.github/` con CI (lint+sizes),
  `CODEOWNERS`, `SECURITY.md`, `CONTRIBUTING.md`, PR template.
- [ ] **T10 — metodología fuentes legales MX**: redactar `docs/fuentes-legal-mx.md`
  (on-demand, <800) con mejores prácticas **informáticas** (hash SHA-256 de integridad,
  identificador persistente URL DOF/diputados + fecha última reforma + fecha de consulta,
  versionado por reforma, proveniencia por afirmación, no-copia-verbatim por artículo) y
  **legales** (jerarquía normativa con citas a verificar, vigencia vía DOF, lex
  superior/posterior/specialis, distinción ley/reglamento/NOM). Toda afirmación normativa
  en el doc cita su fuente (§7).
- [ ] **T8 — fuente-1** *(espera-humano)*: corpus = **leyes mexicanas** (CPEUM + leyes
  federales que de ella emanan, p. ej. Ley General de Salud, más sus reglamentos y NOM).
  Se deposita/referencia bajo `docs/fuentes/`; cargado/verificación sigue T10.
- [ ] **T9 — mapeo norma↔fuente-1**: fact AN-KLA con resumen + `indexable_text` (términos
  clave del doc) + puntero al doc; **sin copia verbatim** (§9.1).

## Riesgos / supuestos
- **Escritura en memoria sin git:** la beta no permite `supersede`; T2 es un fact
  correctivo "al lado" del stale. Mitigación: `indexable_text` con ambas afirmaciones
  (3.10 y 3.12) para que cualquiera sea grep-eable (§9.1).
- **Brecha single-provider (CAGF-A2):** el adversarial de cada hito es quorum-lite por
  diseño; declarado, no resuelto (§6).
- **T5/T8 bloqueados por el humano:** el plan avanza en T1→T4→T6 sin esperarlos.
- **Redacción ≠ autoridad (§7.2):** T9 sólo registra el mapeo; no redacta ni promulga
  norma alguna todavía.
- **Riesgo #1 elevado (corpus legal MX):** las fuentes son leyes en vigor, reformables;
  cada afirmación normativa debe citar instrumento+artículo+fecha de reforma verificada en
  DOF. Mitigación: T10 define el pipeline de integridad (hash + proveniencia) antes de T8/T9.

## Enlaces
- Memoria: `retrieve --query "estado alfa ExpertoGobernanza" --budget 6000`
- Política: `docs/politica-agentes.md` (§3 tamaños, §5 git, §6 adversarial, §7 fidelidad)
- Plantillas: `docs/plantillas-agente.md`
- Fact vigente: `fact-expertogobernanza-alfa-estado-2026-08-06` (revisión 1)
