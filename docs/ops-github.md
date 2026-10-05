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

### 1.1 Estado al 2026-10-05

El hecho de agosto permanece. No describe los runs de octubre: esos jobs sí ejecutaron la suite.

| Run | SHA | Resultado |
|---|---|---|
| `37339265192` | merge PR #40 | 193 tests, 1 error: `FileNotFoundError: xmllint` en `tests/test_akn_spike.py` |
| `37348191223` | `8410075` (merge PR #43) | la misma causa |

Actions arranca. Esos dos rojos son el binario ausente en el runner.

Run verde de la instalación de `libxml2-utils`: [`37353194656`](https://github.com/kristhianmanue1/expertoGobernanza/actions/runs/37353194656), SHA `b56d8f873c577823572c9cbc3c7fae6428662159` (PR #45). 193 tests OK, incluido el paso `xmllint` y `test_akn_spike`.

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

Esta sección es el periodo de billing de agosto 2026. No es el diagnóstico de los runs de octubre, que sí ejecutaron unittest (§1.1).

- El check **“Tests + gate de tamaño”** en GitHub **no valida** el código (el job no arranca).
- “CI verde en el PR” **no es señal fiable** de calidad en este periodo.
- Re-ejecutar el workflow (`gh run rerun`) **no ayuda** hasta renovar presupuesto.
- No inventar “CI pasó” en reportes §12 si solo falló por billing.

## 4. Gate sustituto (DoD local) — obligatorio

Mientras Actions esté suspendido, el **gate de merge** es el mismo contrato que CI ejecutaría, pero **en la máquina del autor/admin**:

```bash
./scripts/ci_check.sh                         # gate canónico; PDF originales requeridos
# si la tarea tocó memoria / contexto de agentes:
.venv/bin/python -m an_kla --project-root . verify
```

El workflow remoto ejecuta el mismo benchmark con `--allow-missing-originals`
porque los PDF del corpus no se versionan. Por ello, el rehash de originales es
una garantía adicional exclusiva del gate local y debe constar en el PR.

En el PR / reporte §12:

- Marcar **DoD local: OK** con comando + resultado (o log corto).
- Marcar **CI remoto: SUSPENDIDO (billing)** y puntero a este doc — **no** fingir verde.
- Estado global razonable: `PARCIAL (ci-billing)` si el resto está OK; no es `BLOQ` de producto.

## 5. Checklist — cuando vuelva Actions (mes / presupuesto)

**No activar branch protection antes de tener al menos un run verde real.**
Si se exige el check y el runner sigue caído, **nadie puede mergear**.

### 5.1 Detectar que el runner ya arranca

```bash
# Billing / runs recientes (admin)
gh run list --limit 5
# Abrir el último fallido: si ya hay log de unittest/check_sizes, no es billing
gh run view <RUN_ID> --log-failed 2>&1 | head -40
```

Criterio de “Actions vivo”:

- [ ] Un job del workflow `CI` dura **más de ~15 s** (no muere en 3–5 s).
- [ ] El log muestra pasos `Compilación` / `Golden set` / `Gate de tamaño`.
- [ ] **No** aparece annotation de *payments* / *spending limit*.

### 5.2 Humo de verificación (obligatorio antes de protection)

```bash
# Opción A — re-ejecutar un workflow en main (si el evento lo permite)
gh workflow run CI --ref main   # si el workflow tiene workflow_dispatch; si no, B

# Opción B — PR de humo vacío/docs (recomendado)
git checkout -b chore/ci-smoke-$(date +%Y%m%d)
# cambio mínimo (p. ej. una línea en este doc: "smoke <fecha>")
git push -u origin HEAD
gh pr create --title "chore(ci): humo post-billing" --body "DoD: validar runner Actions."
gh pr checks   # esperar "Tests + gate de tamaño" = pass
```

- [ ] Check **“Tests + gate de tamaño”** = **success** en el PR de humo (o en push a `main`).
- [ ] DoD local sigue verde en paralelo (regresión de entorno).

### 5.3 Branch protection en `main` (admin, solo tras 5.2 verde)

Objetivo mínimo (alfa): PRs obligatorios + check de CI requerido + sin force-push.

```bash
# Nombre exacto del check = name del job en .github/workflows/ci.yml
# hoy: "Tests + gate de tamaño"
REPO=kristhianmanue1/expertoGobernanza

gh api -X PUT "repos/${REPO}/branches/main/protection" \
  --input - <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Tests + gate de tamaño"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON

# Verificar
gh api "repos/${REPO}/branches/main/protection" --jq '{
  checks: .required_status_checks.contexts,
  strict: .required_status_checks.strict,
  allow_force: .allow_force_pushes.enabled
}'
```

Notas:

- `enforce_admins: false` deja escape de emergencia al admin; subir a `true` cuando el
  equipo confíe en el runner estable.
- Si el plan GitHub no permite protection rules en privados, documentar la limitación
  aquí y mantener DoD local + CODEOWNERS como control social.
- **No** exigir checks que no existan en el workflow (rompe todos los PR).

- [ ] Protection aplicada y `gh api …/protection` devuelve el contexto esperado.
- [ ] Un PR de prueba no mergea sin el check verde (o el UI lo bloquea).

### 5.4 Cierre del modo “DoD local sustituye CI”

1. Actualizar **este doc**:
   - Cabecera: `Estado: Actions operativo desde <fecha>` (o añadir fila en §8 historial).
   - §3–4: marcar como régimen **histórico / de contingencia**, no default.
2. Memoria AN-KLA: `supersede` del fact
   `github-actions-billing-suspendido-2026-08-10` por uno
   `github-actions-operativo-<fecha>` (puntero a este doc + run verde).
3. Reportes §12: volver a exigir **CI remoto verde** (o `PARCIAL` solo por otras causas).
4. Opcional: borrar ramas `chore/ci-smoke-*` remotas tras merge.

- [ ] Doc + fact actualizados; agentes ya no asumen billing eterno.

### 5.5 Si el presupuesto se agota otra vez

1. Revertir a §3–4 (DoD local) **sin** drama de producto.
2. **Quitar o relajar** branch protection que exija el check de CI (si no, merges
   bloqueados). Comando de emergencia (admin):

```bash
gh api -X DELETE "repos/${REPO}/branches/main/protection"
```

3. Nueva fila en historial (§8) + fact correctivo / supersede.

## 6. Política de agentes (lectura operativa)

- **Calidad no se relaja:** lint/tests/tamaños siguen siendo ley; solo cambia *dónde* se ejecutan (local vs runner).
- **Agente propone; admin aplica** push/merge a `main` (`docs/politica-agentes.md` §5).
- **Nunca** `--force` a `main`; **nunca** secretos en el repo.
- Ronda adversarial (§6) **independiente** de Actions: sigue aplicando según impacto del hito.
- Releases: puede crearlas el admin sin pipeline; el artefacto de release debe citar el commit y el DoD local si CI estaba caído.

## 7. Cómo detectar “fallo por billing” vs fallo de tests

| Señal | Interpretación |
|-------|----------------|
| Job ~3–5 s, annotation de *payments* / *spending limit* | Billing — usar §4 |
| Log con `unittest` / `check_sizes` / traceback | Fallo real de código — **no mergear** |
| `statusCheckRollup` FAILURE + sin log de steps útiles | Tratar como billing hasta probar DoD local |

## 8. Historial breve

| Fecha | Evento |
|-------|--------|
| 2026-08-07 | CI en `main` aún **success** (p. ej. push `264b15b`) |
| 2026-08-10 | Actions suspendido por presupuesto; gate local incorpora benchmark IMSS y rehash de PDF |
| *(pendiente)* | Actions vivo + humo verde + (opcional) branch protection — marcar §5.4 |

## 9. Enlaces

- Workflow: `.github/workflows/ci.yml` (job name = contexto de protection)
- Contribuir: `.github/CONTRIBUTING.md`
- Política: `docs/politica-agentes.md` §5 (git), §8 (GitHub), §12 (reporte)
- Memoria: fact `github-actions-billing-suspendido-2026-08-10`
