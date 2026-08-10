# Operación GitHub — ExpertoGobernanza

**Tipo:** on-demand (infra/ops). **Estado:** vigente 2026-08-10.  
**Audiencia:** admin, agentes, revisores.  
**Fuente de verdad** de este tema; los demás docs solo **apuntan** aquí.

## 1. Qué quedó confirmado (evidencia 2026-08-10)

| Hecho | Evidencia |
|-------|-----------|
| Repo privado `kristhianmanue1/expertoGobernanza` | `gh api …/repos` → `private: true` |
| Cuenta admin con scopes útiles | `gh auth`: `repo`, `workflow`, `gist`, `read:org`; permisos repo `admin` |
| **GitHub Actions no ejecuta jobs** por presupuesto | Annotation en run `31395869334`: *“recent account payments have failed or your spending limit needs to be increased”* / límite de gasto; jobs fallan en ~3–5 s **sin** correr tests |
| Actions **se reactiva con el ciclo de facturación** (p. ej. mensual) o al reponer presupuesto | No hay workaround de código; es billing de la cuenta GitHub |
| **`main` sin branch protection** | `GET …/branches/main/protection` → 404 *Branch not protected* → merge no exige checks verdes |
| Flujo git/admin **sigue disponible** sin Actions | Commits, ramas, PR, merge, tags/releases, issues: vía `git` + `gh` con admin |

Último merge con CI rojo por billing (no por tests): PR #1 → `fa3242a` (DoD **local** verde).

## 2. Qué SÍ se puede usar sin Actions (admin)

Con credenciales admin (`gh` / push):

- Ramas (`feat/`, `fix/`, `chore/`, …)
- Commits (Conventional Commits)
- Pull requests (abrir, revisar, comentar)
- Merges (merge/squash/rebase según settings del repo)
- Tags y **Releases** (`gh release create`, tags semver)
- Issues, CODEOWNERS (revisión social), plantillas
- API GraphQL/REST de GitHub **excepto** minutos de Actions

**No depende de Actions:** el grafo git, el remoto, PRs ni releases.

## 3. Qué NO se puede asumir mientras Actions esté suspendido

- El check **“Tests + gate de tamaño”** en GitHub **no valida** el código (el job no arranca).
- “CI verde en el PR” **no es señal fiable** de calidad en este periodo.
- Re-ejecutar el workflow (`gh run rerun`) **no ayuda** hasta renovar presupuesto.
- No inventar “CI pasó” en reportes §12 si solo falló por billing.

## 4. Gate sustituto (DoD local) — obligatorio

Mientras Actions esté suspendido, el **gate de merge** es el mismo contrato que CI ejecutaría, pero **en la máquina del autor/admin**:

```bash
python -m py_compile corpus/*.py scripts/*.py review_routing/*.py
python -m unittest discover -s tests          # esperado: 34+ OK
python scripts/check_sizes.py                 # exit 0
# si la tarea tocó memoria / contexto de agentes:
.venv/bin/python -m an_kla --project-root . verify
```

En el PR / reporte §12:

- Marcar **DoD local: OK** con comando + resultado (o log corto).
- Marcar **CI remoto: SUSPENDIDO (billing)** y puntero a este doc — **no** fingir verde.
- Estado global razonable: `PARCIAL (ci-billing)` si el resto está OK; no es `BLOQ` de producto.

Cuando Actions vuelva (nuevo mes / presupuesto):

1. Confirmar un run verde en `main` o en un PR de humo.
2. Preferible: reactivar o añadir **branch protection** en `main` exigiendo el check de CI (hoy no hay protection).
3. Dejar de usar el modo sustituto; este doc se actualiza (fact correctivo / nota de cierre).

## 5. Política de agentes (lectura operativa)

- **Calidad no se relaja:** lint/tests/tamaños siguen siendo ley; solo cambia *dónde* se ejecutan (local vs runner).
- **Agente propone; admin aplica** push/merge a `main` (`docs/politica-agentes.md` §5).
- **Nunca** `--force` a `main`; **nunca** secretos en el repo.
- Ronda adversarial (§6) **independiente** de Actions: sigue aplicando según impacto del hito.
- Releases: puede crearlas el admin sin pipeline; el artefacto de release debe citar el commit y el DoD local si CI estaba caído.

## 6. Cómo detectar “fallo por billing” vs fallo de tests

| Señal | Interpretación |
|-------|----------------|
| Job ~3–5 s, annotation de *payments* / *spending limit* | Billing — usar §4 |
| Log con `unittest` / `check_sizes` / traceback | Fallo real de código — **no mergear** |
| `statusCheckRollup` FAILURE + sin log de steps útiles | Tratar como billing hasta probar DoD local |

## 7. Historial breve

| Fecha | Evento |
|-------|--------|
| 2026-08-07 | CI en `main` aún **success** (p. ej. push `264b15b`) |
| 2026-08-10 | Actions suspendido por presupuesto; PR #1 mergeado con DoD local; este doc creado |

## 8. Enlaces

- Workflow: `.github/workflows/ci.yml`
- Contribuir: `.github/CONTRIBUTING.md`
- Política: `docs/politica-agentes.md` §5 (git), §8 (GitHub), §12 (reporte)
- Memoria: fact `github-actions-billing-suspendido-2026-08-10` (si existe en AN-KLA)
