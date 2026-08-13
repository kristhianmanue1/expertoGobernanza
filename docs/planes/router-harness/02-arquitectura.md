# 02 — Arquitectura

## Visión general

```
            ┌─────────────┐    files+provider+model
   agente → │   gateway   │ ─────────────────────────┐
            │ route_review│                          │
            └─────┬───────┘                          ▼
                  │ clasifica+confina        CLI externo (claude/codex/…)
                  │ (router.route)           lee SÓLO el bundle sellado (temp)
                  ▼
            ┌─────────────┐   seal (manifiesto+hashes)
            │    seal     │ ─────────────────────────┐
            │  seal.py    │                          │
            └─────┬───────┘                          ▼
                  │ sella bundle             audit_log (jsonl, cadena de hash)
                  ▼                          ← prev_hash encadena entradas
            ┌─────────────┐
            │  audit_log  │   verify_log recorre la cadena → OK | BROKEN
            └─────────────┘
```

Tres módulos nuevos en `review_routing/` + un CLI. Todo stdlib, determinista,
testeable offline.

## Componente 1 — Sello de bundle (`review_routing/seal.py`)

**Responsabilidad:** vincular clasificación ↔ contenido ↔ destino en un objeto
verificable. El sello prueba *“este contenido, con esta clasificación, iba a este
proveedor/modelo”*.

### Formato del sello

```python
seal = {
    "schema": "eg-harness/seal-v1",
    "sealed_at": "2026-08-13T20:00:00Z",       # ISO-8601 UTC
    "provider": "Anthropic",
    "model": "claude-opus-5",
    "config_sha256": "sha256:...",              # hash de config.json (ya en router)
    "bundle_sha256": "sha256:...",              # hash del contenido (ya en router.route)
    "manifest": [
        {"path": "docs/adr/0001-x.md",
         "classification": "publico",
         "bytes": 1234,
         "sha256": "sha256:..."},               # por-archivo
    ],
    "seal_sha256": "sha256:...",                # hash canónico del resto del sello
}
```

`seal_sha256 = sha256(canonical_json(seal sin el campo seal_sha256))`. Canonicalización
= `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False)` (igual que
AN-KLA). **`seal_sha256` se excluye de su propio cómputo.**

### Funciones (contrato)

```python
def build_seal(decision, provider, model, config_sha256) -> dict
    # decision = salida de router.route(); arma manifest + calcula seal_sha256.

def verify_seal(seal, content_getter) -> tuple[bool, str]
    # Re-hashes content via content_getter(path)->bytes, recomputa manifest hashes,
    # recomputa seal_sha256. Devuelve (ok, razón). Cualquier mismatch → (False, ...).
```

**Invariante:** `verify_seal(build_seal(...))` es `(True, ...)`. Un byte cambiado en
cualquier archivo → `verify_seal` falla.

## Componente 2 — Bitácora tamper-evident (`review_routing/audit_log.py`)

**Responsabilidad:** registro append-only donde alterar/reordenar/borrar una entrada
**rompe** una cadena verificable.

### Formato de entrada

```python
entry = {
    "seq": 1,                                   # entero, monótono desde 1
    "ts": "2026-08-13T20:00:01Z",
    "provider": "Anthropic",
    "model": "claude-opus-5",
    "seal_sha256": "sha256:...",                # del sello
    "bundle_sha256": "sha256:...",
    "config_sha256": "sha256:...",
    "response_sha256": "sha256:...",            # hash de la salida del proveedor (o null)
    "prev_hash": "sha256:0000...0000",          # genesis para seq=1 (64 ceros)
    "entry_hash": "sha256:...",                 # sha256(canonical_json(entry sin entry_hash))
}
```

`entry_hash` se excluye de su propio cómputo (igual que `seal_sha256`). `prev_hash`
de la entrada *n* = `entry_hash` de la entrada *n-1*.

### Funciones (contrato)

```python
def append(seal, response_sha256, logpath) -> dict
    # Lee la última entrada (o genesis), construye la nueva con prev_hash, escribe.

def verify_chain(logpath) -> tuple[str, list[str]]
    # Recorre entradas: recomputa cada entry_hash, verifica prev_hash enlaces,
    # verifica seq monótono. Devuelve ("OK"|"BROKEN", [hallazgos]).
```

**Invariante:** alterar cualquier campo, borrar/reordenar una entrada, o saltar seq
→ `verify_chain` devuelve `"BROKEN"` con el hallazgo.

## Componente 3 — Gateway (`review_routing/gateway.py` + CLI `scripts/route_review.py`)

**Responsabilidad:** ser la **ruta sancionada** de invocación al proveedor. Orquesta
router → seal → invoke → log.

### Flujo

1. Parsea `--files --provider --model [--config] [--dry-run]`.
2. `config = load_config()`; `config_sha256 = hash(config)`.
3. `decision = router.route(files, config)`.
4. **Fail-closed:** si `decision["denied"]` y no `--allow-partial` → exit 1 (igual que hoy).
5. Si `decision["bundle"]` vacío → exit 1.
6. `seal = seal.build_seal(decision, provider, model, config_sha256)`.
7. Escribe contenido sellado a un **temp sellado** (contenido del bundle sólo).
8. Si `--dry-run` → imprime el sello, no invoca, no loguea; exit 0.
9. Invoca el CLI externo apuntando al temp sellado (no al repo). Captura stdout.
10. `response_sha256 = sha256(stdout)`.
11. `audit_log.append(seal, response_sha256, logpath)`.
12. Imprime sello + resumen; exit 0.

### CLI (contrato)

```
scripts/route_review.py --files f1 f2 --provider P --model M [--dry-run]
```

`--dry-run` = clasifica + sella + **verifica el sello** + imprime, **sin** invocar al
proveedor ni loguear. Es el modo de prueba determinista (no necesita red ni CLI real).

## Anti-bypass y honestidad

- El gateway es la **ruta fácil**. Un agente que lo usa obtiene sellado + log + chain
  gratis. El que invoca el CLI directo **deja un hueco**: proveedor usado sin entrada
  en `audit_log`. Esa ausencia es la señal de auditoría (no prueba criptográfica).
- El contenido sellado vive en un temp **separado del repo**; el CLI externo no recibe
  acceso al árbol completo, sólo al bundle sellado.
- **No** se declara enforcement OS-level: se documenta como límite (ver ADR del harness).

## Compatibilidad con el router actual

- `router.py` **no se reescribe**: el gateway lo **invoca**. Su `route()` y `write_log()`
  se conservan. `write_log` queda como log simple legacy; el gateway usa `audit_log`
  (cadena). Migrar lectores antiguos es opcional y fuera de este plan.
