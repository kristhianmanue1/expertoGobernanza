# Spike Argos Epistemic 0.2.0rc2 × ExpertoGobernanza

**Fecha:** 2026-08-10  
**Rama:** `spike/argos-0.2.0rc2-eg` (no merge a `main` como dependencia de producto)  
**Issue de feedback (Argos):** https://github.com/kristhianmanue1/argos-epistemic/issues/18  
**Wheel:** `v0.2.0rc2` verificado con `SHA256SUMS` (artefactos locales bajo `.spikes/`, gitignored).

## Decisión

| Opción | Veredicto |
|--------|-----------|
| Argos en camino crítico legal / F5 / DOF | **No** |
| Argos como dependencia de `main` EG | **No** (por ahora) |
| Argos como auditor lateral de *software gates* | **Sí, experimento acotado** con verificadores |
| Feedback al equipo Argos | **Issue de consumidor** (métricas saneadas) |

Argos es un motor **epistémico de software** (L0–L5, claims, `supports`/`refutes`, presupuesto). EG es **inteligencia normativa MX**. Son complementarios en gobernanza de agentes (junto a AN-KLA), no intercambiables en dominio legal.

## Protocolo del spike

1. Venv aislado en `.spikes/argos-0.2.0rc2/` (no contaminar `.venv` de EG).
2. Staging sin corpus oficial: `review_routing/`, `corpus/*.py` + `registry.yaml`, `scripts/`, `tests/`.
3. `analyze_path` estático (`run_dynamic/history/logs/coverage/profile=False`).
4. Goal con 7 aspectos de gates de software (no DOF).
5. Solo métricas agregadas en este doc / issue; `report-full.json` queda local.

## Resultados (agregados)

| Métrica | Valor |
|---------|--------|
| `files_discovered` / `eligible` | 22 / 17 |
| `bytes_discovered` / `read` | ~79.5 KB / ~60.1 KB |
| `read_truncations` | 2 (`registry.yaml`, `test_router.py`) |
| `levels_covered` | 1–5 |
| `evidence_kinds` | behavior, callgraph, code, config, test, topology |
| `retrieval_coverage` | 0.4286 |
| Retrieval por aspecto | `review_routing`, `registry_vigencia`, `audit_document_pipeline` = 1.0; resto 0.0 |
| `evidential_coverage` / `structural` / `coverage` | 0.0 |
| `coverage_capability` | `unavailable` |
| Claims | 5 × `mentions` (“X mentioned”), no `supports`/`refutes` |
| `termination_reason` | `no_eligible_actions` |
| `residual_risk` | 1.0 |
| Tokens observados | ~15.5k de 200k |

`completion.reason_codes`: `threshold_not_met`, `insufficient_sources`, `missing_production_evidence`, `coverage_capability_unavailable`, `content_truncated`, `no_eligible_actions`.

`next_actions` (no ejecutadas; `authorization_required: true`):

1. `increase_read_limit` — diagnóstico; no convierte retrieval en evidencia.
2. `enable_probative_verifier` — camino real a valor probatorio.

## Lectura para EG

- **Instalación y contratos machine-first:** aptos para un agente colaborador.
- **Valor hoy sin verifiers:** inventario + ranking/retrieval; útil para explorar un monorepo, insuficiente para DoD de gates.
- **Valor potencial:** verificadores deterministas sobre invariantes de `review_routing`, `verify_citations`, registry — *después* de que existan ejemplos/verifiers reutilizables o se escriban en un segundo spike.
- **Riesgo a evitar:** confundir un bundle Argos con “prueba de vigencia” o con ronda adversarial §6.

## No hacer

- Merge de dependencia Argos a `main`.
- Citar reportes Argos como fuente normativa.
- Subir `report-full.json` o wheels al remoto de EG.

## Reproducir (local)

```bash
# desde la raíz de EG, con gh autenticado
mkdir -p .spikes/argos-0.2.0rc2 && cd .spikes/argos-0.2.0rc2
gh release download v0.2.0rc2 --repo kristhianmanue1/argos-epistemic \
  --pattern 'argos_epistemic-0.2.0rc2-py3-none-any.whl' --pattern SHA256SUMS
grep 'argos_epistemic-0.2.0rc2-py3-none-any.whl' SHA256SUMS | shasum -a 256 -c -
python3.12 -m venv .venv
.venv/bin/python -m pip install ./argos_epistemic-0.2.0rc2-py3-none-any.whl
# staging + run_spike.py viven solo en la máquina del spike
```

## Próximo paso opcional (segundo spike)

Registrar un único verificador sobre un invariante medible de EG y re-medir `coverage_capability`. Solo si el issue de Argos confirma interés en ese patrón de consumidor.
