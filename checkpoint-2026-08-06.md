# Checkpoint de sesión — 2026-08-06

**Objetivo:** Arranque gobernado (R0) + MVP honesto del slice eje-salud + enmienda multi-provider.

## Hecho (verificable)
- **Entorno:** venv reparado a Python 3.12; AN-KLA rev 3 (3 facts, 3 events, verify ok).
- **R0 (T1–T6) ✓** + H1/H2/H3 cerrados con ronda adversarial.
- **Git:** repo privado `kristhianmanue1/expertoGobernanza`, `main` = `586822c`, sincronizado.
- **Dictamen** analizado (crítico/adversarial/gobernanza); **ADR-0001** propuesto (adoptar-con-condiciones).
- **Enmienda v1.1-revisada** (multi-provider + compuertas + roles + ADR); **bootstrap** con claude+Anthropic y kimi+Moonshot → `fix-and-retry` → 16 fixes aplicados.
- **MVP slice eje-salud:** componentes A (registro fuentes) + B (extractos) + D (`corpus/lookup.py`) + F (`corpus/verify_citations.py`, gate v1 con fixes). Cadena **CPEUM:4:Psalud → LGS:1** verificada (verbatim + sha256 recomputado: CPEUM `ca63a23a`, LGS `a2d3f947`).
- **§7:** "Ley Federal de Salud" no existe → **Ley General de Salud**; IMSS = OPD (descentralizado, no desconcentrado) `[verificar en LSS]`; Cámara es nivel 2 ("informativo", aviso verbatim); DOF nivel 1 pendiente.

## Siguiente
1. Tests/golden set (B4 del bootstrap) + granularidad por-párrafo (M2).
2. Reconciliar vigencia con **DOF nivel 1** (sigue `[VIGENCIA-NO-VERIFICADA]`).
3. **Eje estructural IMSS**: ingerir Reglamento Interior + LOAPF/LFEP (modelo de la entidad).
4. **Adopción humana de la enmienda v1.1-revisada** → fusionar en `politica-agentes.md` v1.1.
5. Activar `check_sizes` como pre-commit/CI (T7, diferible).

## Bloqueos / deuda
- **Responsable jurídico del corpus** = deuda (interino = humano-promulgador).
- Quórum multi-provider efectivo: glm-5.2 + Anthropic + Moonshot (gemini/qwen sin auth).
- DOF nivel 1 no consultado automáticamente → vigencia no verificada.
- `check_sizes` no es pre-commit hook aún (es script).

## Archivos clave
- Gobernanza: `AGENTS.md`, `docs/politica-agentes.md`, `docs/adr/0001-*`, `docs/propuestas/enmienda-gobernanza-v1.1-revisada.md`.
- MVP: `corpus/registry.yaml`, `corpus/lookup.py`, `corpus/verify_citations.py`, `corpus/derived/cpeum/CPEUM-004-salud.json`, `corpus/derived/lgs/LGS-001.json`, `docs/fuentes/{cpeum,lgs}/`.
- Evidencia: `docs/propuestas/componente-F-bootstrap-reviews/`, `docs/relatorias/2026-08-06-bootstrap-multi-provider.md`.

## Reanudar con
Leer `AGENTS.md` + este checkpoint + `retrieve --query "MVP slice eje salud CPEUM LGS" --budget 6000`;
luego `status` + `verify` de AN-KLA y `git status`.
