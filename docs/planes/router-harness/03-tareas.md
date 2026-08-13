# 03 — Tareas

> **Convención:** cada tarea = 1 PR = 1 contrato. DoD con checks ejecutables.
> Ramas `feat/rh-TNN`. Commits firmados (`-S`). Gate `check_sizes.py` en verde
> + `unittest` en verde antes de declarar hecho. Stdlib sólo.

---

## Hito H0 — Sello de bundle

### RH-T01 · `review_routing/seal.py` — build_seal + verify_seal

**Implementa el sello v1** (formato `eg-harness/seal-v1` del §2).

- Archivos: `review_routing/seal.py` (nuevo), `review_routing/__init__.py` (si hace
  falta export).
- **Entradas:** `decision` (salida de `router.route`), `provider`, `model`,
  `config_sha256`. Construye `manifest` (path, classification inferida de la
  ausencia en denied → "publico", bytes, sha256 por archivo), `bundle_sha256`
  (ya viene en decision), `seal_sha256` (canonical).
- `verify_seal(seal, content_getter)` re-hashes vía `content_getter(path)->bytes`,
  recomputa manifest + `seal_sha256`, compara.
- **Dep:** ninguna.

**DoD:**
- [ ] `python -m py_compile review_routing/seal.py` limpio.
- [ ] `build_seal` produce un dict con los 8 campos del §2 y `seal_sha256` = 64 hex.
- [ ] `verify_seal(build_seal(d,p,m,c), getter)` → `(True, "ok")`.
- [ ] Mutar 1 byte del contenido → `verify_seal` → `(False, ...)`.
- [ ] `check_sizes.py` en verde; `seal.py` < 200 líneas.

### RH-T02 · Tests del sello (`tests/test_seal.py`)

- Casos: round-trip ok; tamper contenido → fail; tamper manifest → fail; tamper
  `seal_sha256` → fail; bundle vacío; seal sin schema rechazado.
- **Dep:** RH-T01.

**DoD:**
- [ ] `python -m unittest tests.test_seal -v` todo PASSED.
- [ ] Al menos 1 caso negativo por cada campo crítico (contenido, manifest,
      `seal_sha256`).
- [ ] Suite completa `unittest discover -s tests` en verde (sin regresiones).

---

## Hito H1 — Bitácora tamper-evident

### RH-T03 · `review_routing/audit_log.py` — append + verify_chain

- `append(seal, response_sha256, logpath)`: lee última entrada (o genesis
  `sha256:` + 64 ceros para seq=1), construye entry con `seq`+1, `prev_hash`,
  `entry_hash` (canonical), escribe 1 línea JSON.
- `verify_chain(logpath)`: recorre, recomputa cada `entry_hash`, verifica
  `prev_hash` enlaces + `seq` monótono. Devuelve `("OK"|"BROKEN", [hallazgos])`.
- **Dep:** RH-T01 (usa `seal_sha256`).

**DoD:**
- [ ] `py_compile` limpio; `audit_log.py` < 200 líneas.
- [ ] `append` 3 veces → `verify_chain` → `("OK", [])`.
- [ ] Alterar 1 campo de una entrada intermedia → `("BROKEN", [...])`.
- [ ] Borrar entrada del medio → `("BROKEN", [...])`.
- [ ] Reordenar dos entradas → `("BROKEN", [...])`.
- [ ] `seq` no monótono → `("BROKEN", [...])`.

### RH-T04 · Tests de la cadena (`tests/test_audit_log.py`)

- Casos del DoD de RH-T03 + genesis (log vacío → seq=1, prev=64 ceros) + log
  inexistente (append lo crea).
- **Dep:** RH-T03.

**DoD:**
- [ ] `python -m unittest tests.test_audit_log -v` todo PASSED.
- [ ] Suite completa en verde.

---

## Hito H2 — Gateway + CLI (ruta sancionada)

### RH-T05 · `review_routing/gateway.py` + `scripts/route_review.py` (dry-run)

- `gateway.run(files, provider, model, config, dry_run)`: orquesta router → fail-closed
  → `build_seal` → (si dry_run) `verify_seal` propio + retorna sello sin invocar/loguear.
- CLI `scripts/route_review.py` con `--files --provider --model --config --dry-run
  --allow-partial`. Exit codes: 0 ok; 1 denied/vacío/error.
- **El modo `--dry-run` es determinista y no necesita red ni CLI externo.**
- **Dep:** RH-T01, RH-T03.

**DoD:**
- [ ] `python scripts/route_review.py --files docs/adr/0001-*.md --provider Test
      --model m1 --dry-run` imprime un sello válido y exit 0.
- [ ] Mismo comando con un path no-público (p. ej. `nomina/x.md` si estuviera) →
      exit 1 y lista el denegado.
- [ ] `--dry-run` **no** escribe en `logs/`.
- [ ] `gateway.py` < 250 líneas; `route_review.py` < 100.

### RH-T06 · Integration test gateway (`tests/test_gateway.py`)

- End-to-end en dry-run con un repo temporal: crea config + archivos públicos y
  uno denegado; verifica que el gateway sella sólo los públicos, fail-closed con
  el denegado (sin `--allow-partial`), y `verify_seal` ok.
- **Dep:** RH-T05.

**DoD:**
- [ ] `python -m unittest tests.test_gateway -v` todo PASSED.
- [ ] Suite completa en verde; `check_sizes.py` en verde.

---

## Hito H3 — Cierre (invoke real + ADR + adversarial)

### RH-T07 · Invoke path real + append al log (opcional, gated)

- Extiende el gateway: tras sellar, escribe bundle sellado a temp, invoca el CLI
  externo (subprocess) apuntando al temp, captura stdout, `response_sha256`,
  `audit_log.append`.
- **Gated:** este task requiere un proveedor real disponible y autorizado
  (`docs/autorizacion-fuentes-r1.md`). No bloquea H0–H2. Puede quedar como diseño
  listo hasta que se ejecute una revisión multi-provider real.
- **Dep:** RH-T05, RH-T06, + proveedor autorizado.

**DoD:**
- [ ] Una invocación real (p. ej. claude) vía gateway deja entrada en `audit_log`.
- [ ] `verify_chain` sobre esa entrada → `OK`.
- [ ] El CLI externo recibe el temp sellado, NO el repo completo.

### RH-T08 · ADR + ronda adversarial (cierre de hito)

- `docs/adr/0006-router-harness-egress-verificable.md`: decisión, formato seal/log,
  **límites declarados** (no sandbox OS; bypass detectable por hueco de log, no
  prevención criptográfica). Referencia este plan.
- Ronda adversarial (quorum-lite mínimo; multi-provider si hay cambio de política):
  atacar sellado, cadena de log, fail-closed, path traversal heredado del router.
- **Dep:** RH-T01..T06.

**DoD:**
- [ ] ADR-0006 escrito, estado Aceptado tras la ronda.
- [ ] Ronda adversarial con decisión `proceed` (o `escalate` con hallazgos abiertos
      declarados).
- [ ] `00-INDICE.md` de este plan marca el hito **CERRADO**.

---

## Orden sugerido y dependencias

```
RH-T01 (seal) ──┬─→ RH-T02 (tests seal)
                │
                └─→ RH-T03 (audit_log) ──→ RH-T04 (tests log)
                            │
RH-T05 (gateway) ←──────────┘  (dep T01+T03)
        │
        └─→ RH-T06 (tests gateway) ──→ RH-T07 (invoke real, gated) ──→ RH-T08 (ADR+adversarial)
```

**Paralelizable:** T02, T04 y T06 son tests que pueden escribirse junto a su módulo
(mismo PR o PR inmediatamente siguiente). T01 y T03 pueden ir en paralelo (T03 sólo
necesita el formato `seal_sha256` de T01).

## Definición de “hecho” del plan (cierre global)

- [ ] RH-T01..T06 mergeados (seal + log + gateway + tests, todo verde).
- [ ] `route_review --dry-run` funciona determinista offline.
- [ ] ADR-0006 aceptado con límites declarados.
- [ ] Ronda adversarial del hito: `proceed`.
- [ ] RH-T07 puede quedar gated (no bloquea el cierre del harness verificable).
