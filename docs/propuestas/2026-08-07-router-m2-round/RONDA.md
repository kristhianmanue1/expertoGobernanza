# Ronda adversarial — router §7.4 + rename M2 (2026-08-07)

> **Artefactos:** router `review_routing/` + id ordinal `CPEUM:4:P4`. **Bundle sha256:**
> `66ec4a5b56735ffcc6197ec1ba752ed835ede4151637ac71c1516802a91b1d49` (6 archivos).
> **Autor:** opencode/glm-5.2 (zai-coding-plan) — EXCLUIDO de votar; no revisa su propia obra.
> **Revisores:** claude (Anthropic) + cline/**qwen-max** (Alibaba).
> **Quórum:** glm-5.2 + Anthropic + Alibaba = **3 familias distintas → VÁLIDO** (§6 satisfecho; A2 mitigada parcialmente como siempre).
> **Decisión consolidada:** la hace el humano; el autor (opencode) sólo sintetiza, sin voto.
> **gemini (Google):** árbitro opcional, no requerido (auth inestable en ejercicios previos).

## Cómo usar este archivo (orquestador = humano, en tmux)
1. Abre 2 panes. En cada, pega el **BRIEF COMÚN** + **sólo su lente** (A para claude, B para cline).
2. Cada revisor trabaja **ciego** (no ve el otro pane) y declara modelo subyacente + conflicto de interés.
3. Vuelve con las dos salidas verbatim; opencode reconcilia (agrega, no descarta sin justificación).
4. **Validez del quórum:** ✓ **VÁLIDO** — glm-5.2 (autor) + Anthropic (claude) + Alibaba (qwen-max) = 3 familias distintas por modelo subyacente. Si uno de los dos revisores no puede correr, cae a `PARCIAL` (requeriría un 3.º externo, p. ej. gemini).

---

## BRIEF COMÚN (pegar en ambos panes)

```
RONDA ADVERSARIAL MULTI-PROVIDER — 2026-08-07 — ExpertoGobernanza
Artefactos bajo revisión (bundle sha256 66ec4a5b…, 6 archivos, todos 'público'):
  - review_routing/router.py + review_routing/config.json   (implementa política §7.4)
  - corpus/derived/cpeum/CPEUM-004-P4-salud.json + corpus/derived/lgs/LGS-001.json  (rename id ordinal, M2)
  - tests/test_router.py + tests/test_verify_citations.py
Autor: opencode/glm-5.2 (EXCLUIDO de votar). Tú eres revisor EXTERNO.

Marco (docs/politica-agentes.md v1.1):
  §6   quórum ≥3 proveedores por MODELO SUBYACENTE (no CLI); revisión ciega + lentes; cualquier BLOCKER bloquea.
  §7.3 compuertas deterministas; gate v1: (a) disposición existe, (c) cita aparece verbatim ≥40 chars normalizados,
       (d) fuente resuelta (sha256 64-hex, recomputado si el original está accesible); 'alto' PROHIBIDO en v1 (tope 'medio').
  §7.4 clasificación ex-ante MACHINE-READABLE (no el agente que envía): router filtra ANTES de invocar;
       'público' permitido; 'interno_institucional' sólo anonimizado + autorización humana;
       'personal_confidencial' PROHIBICIÓN DURA; log de hash de lo enviado.

Alcance: CORRECCIÓN y REQUISITOS (no estilo). Para el rename M2, verifica el ordinal
(4º párrafo del Art. 4) contra la fuente docs/fuentes/cpeum/art-004.txt.

Reglas:
  - REVISIÓN CIEGA: no busques ni leas la salida de otros revisores.
  - Proveniencia: declara tu MODELO SUBYACENTE exacto (no tu CLI).
  - Conflicto de interés: decláralo si tu proveedor es parte del quórum.

Salida (plantilla obligatoria):
  [BLOCKER|HIGH|MED|LOW] problema — evidencia (file:line o cita a fuente) — fix prescrito
  ...
  Decisión: proceed | fix-and-retry | escalate
```

## LENTE A — para el pane de **claude** (Anthropic)
```
TU LENTE: CORRECCIÓN / FIDELIDAD del gate y del router.
Enfócate en:
  - ¿El router implementa §7.4 correctamente? allowlist, default deny, matches() con '**', hash determinista.
  - ¿Hay BYPASS? (p. ej. path con '..', mayúsculas/minúsculas, '\' vs '/', allowlist que deja fuera algo crítico).
  - ¿El rename CPEUM:4:P4 respetó la fuente? ¿el ordinal 4º es correcto? ¿se afirmó algo no verificable?
  - ¿El gate v1 sigue correcto tras el rename? ¿algún test da falso verde?
Cita file:line. Si afirmas algo del CPEUM, verifica contra docs/fuentes/cpeum/art-004.txt.
```

## LENTE B — para el pane de **cline**
```
TU LENTE: SEGURIDAD DE DATOS / VIABILIDAD operativa.
Enfócate en:
  - ¿El router PREVIENE fuga real? ¿personal_confidencial es realmente imparnable por el agente?
  - ¿El log de hash (logs/review-routing.jsonl) es auditable y no manipulable por el agente?
  - ¿Es fail-closed? (path no clasificado -> deny; archivo faltante -> denied).
  - ¿Viabilidad del harness tmux? ¿qué falta para usarlo en cada ronda real?
Declara tu MODELO SUBYACENTE exacto (requerido para la validez del quórum).
```

## Al volver con las salidas
- Pega ambas reviews verbatim (el humano las persiste bajo este directorio como evidencia).
- El autor (opencode) reconcilia **sólo agregando**; cualquier descarte lleva justificación escrita (§6).
- Decisión agregada: cualquier BLOCKER de cualquier revisor → `fix-and-retry`; sin `proceed` no se promulga como estable.
