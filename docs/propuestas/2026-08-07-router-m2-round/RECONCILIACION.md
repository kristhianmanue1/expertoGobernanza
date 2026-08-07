# Relatoría — Ronda adversarial router §7.4 + rename M2 (2026-08-07)

> **Decisión consolidada: `PROCEED`** (claude + codex, ciclo 3). Reconciliación del autor
> (opencode/glm-5.2) sin voto; la decisión final es del humano.

## Proveniencia (modelo subyacente, no CLI — política §6)
| Rol | Proveedor / modelo | Ciclos |
|---|---|---|
| Autor (excluido de votar) | opencode · glm-5.2 (zai-coding-plan) | — |
| Revisor 1 | **claude** (Anthropic) · Claude Sonnet 5 | 1, 2, 3 |
| Revisor 2 | **codex** (OpenAI) · GPT-5 | 1, 2, 3 |
| No disponibles | cline/qwen (OAuth discontinuado, hub error desde bash) | — |

**Quórum válido:** glm-5.2 + Anthropic + OpenAI = 3 familias distintas. Revisiones **ciegas**
(lente A=corrección/fidelidad a claude; lente B=seguridad-datos/viabilidad a codex). Reviews
verbatim en `reviews/round{1,2,3}-{claude,codex}.md`.

## Ciclo 1 — ambos `fix-and-retry` (BLOCKER convergente)
- **BLOCKER convergente (claude+codex):** `_matches()` con `startswith` + `route()` sin
  confinamiento → bypass por colisión de prefijo (`"docs/adr/**"`→prefix `"docs/adr"`) y
  **path traversal** (`..`, absolutos). Los tests no lo cubrían (falso verde).
- Codex añadió: `--authorize-internal` auto-afirmable; config-swap vía `--config`; bundle
  parcial exit-0; log no inmutable; harness ausente.
- **M2 verificado correcto** por ambos: ordinal `CPEUM:4:P4` (P1=igualdad, P2=hijos,
  P3=alimentación, P4=salud) coincide con `docs/fuentes/cpeum/art-004.txt`.

## Ciclo 2 — claude `proceed`, codex `fix-and-retry`
- Fixes ciclo 1 aplicados: `pattern[:-2]` (conserva `/`), `_confined()` con
  `is_relative_to(repo_root)`, atomicidad fail-closed, `config_sha256` en log.
- Codex halló 2 BLOCKER nuevos: **(B1) symlink in-repo** (ruta pública → archivo
  confidencial del repo; `read_bytes` sigue el enlace); **(B2)** `--authorize-internal-ref`
  aún auto-afirmable + interno enviado sin anonimizar (§7.4).

## Ciclo 3 — ambos `proceed`
- **(F1) anti-symlink:** `route()` clasifica la ruta pedida Y la resuelta (canónica) y
  aplica la clase **más restrictiva** → symlink público→confidencial = `personal_confidencial` → denegado.
- **(F2) interno siempre denegado en v1:** sin pipeline de anonimización, no se enruta;
  se eliminó `--authorize-internal-ref`. Razón: `interno_anonimizacion_pendiente`.
- Limpieza no bloqueante de claude: docstring y código muerto (`_denied_reason`) corregidos.
- Veredicto: claude `proceed`, codex `proceed` ("B1 y B2 cerrados dentro del alcance declarado").

## Deuda declarada (harness, fuera del alcance del módulo router v1)
El router es **control + auditoría**, NO sandbox (declarado en su docstring LIMITES). Deuda
del harness de revisión: bundle sellado, **egress de red** real, **log append-only externo**
al agente, registro criptográfico de autorización humana, pipeline de anonimización para
`interno_institucional`. Estas no se tratan como BLOCKER del módulo (alcance definido y documentado).

## Verificación
- `python -m unittest discover -s tests` → 34/34 OK (incluye regresiones: traversal,
  colisión de prefijo, absoluto, **symlink público→confidencial**, interno siempre denegado, atomicidad).
- `python scripts/check_sizes.py` → exit 0.
