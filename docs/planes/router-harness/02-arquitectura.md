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

El sello envuelve un **bundle autocontenido** (manifiesto + contenido). `verify_seal`
re-hashes el **contenido del bundle** (fijo, inmutable), no el repo en vivo → sin
TOCTOU (F2). El bundle sellado es lo que se envía al proveedor; verificarlo verifica
lo que **realmente** se envió.

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
         "classification": "publico",           # de router.classify(), no inferida (F4)
         "bytes": 1234,
         "sha256": "sha256:..."},               # por-archivo, del contenido del bundle
    ],
    "seal_sha256": "sha256:...",                # hash canónico del resto del sello
}
```

`seal_sha256 = sha256(canonical_json(seal sin el campo seal_sha256))`. Canonicalización
= `json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False)` (igual que
AN-KLA). **`seal_sha256` se excluye de su propio cómputo.**

### Funciones (contrato)

```python
def build_seal(decision, config, provider, model, config_sha256) -> dict
    # decision = salida de router.route(). Por cada path en decision["bundle"],
    # re-clasifica con router.classify(path, config) -> manifest.classification
    # (no infiere de la pertenencia al bundle; F4). Lee el contenido del repo
    # UNA vez al sellar y lo guarda en el bundle autocontenido.

def verify_seal(seal, bundle_content) -> tuple[bool, str]
    # bundle_content = {path: bytes} del bundle sellado (inmutable). Re-hashes
    # cada entrada, recomputa manifest hashes + seal_sha256, compara. Opera sobre
    # el contenido sellado, NO sobre el repo vivo (F2: sin TOCTOU).
```

**Invariante:** `verify_seal(build_seal(...), su_bundle)` es `(True, ...)`. Un byte
cambiado en cualquier archivo del bundle → `verify_seal` falla. El repo puede cambiar
después; el sello vincula lo que **se envió**, no el estado actual del repo.

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

def verify_chain(logpath, anchor_hash=None) -> tuple[str, list[str]]
    # Recorre entradas: recomputa cada entry_hash, verifica prev_hash enlaces,
    # verifica seq monótono. Si anchor_hash != None, verifica que el ÚLTIMO
    # entry_hash == anchor_hash (F1: ancla externa contra reemplazo total).
    # Devuelve ("OK"|"BROKEN", [hallazgos]).
```

**Invariante:** alterar cualquier campo, borrar/reordenar una entrada, o saltar seq
→ `verify_chain` devuelve `"BROKEN"`.

**Ancla externa (F1):** la cadena sola no detecta que un atacante **trunce el log y
lo reconstruya** desde genesis (la nueva cadena sería internamente consistente). Por
eso `verify_chain` acepta un `anchor_hash`: el `entry_hash` de la última entrada
conocida-good, **commiteado a git** (sustrato firmado, ADR-0002/0005). El gateway
imprime el último `entry_hash` tras cada `append`; el humano lo registra/commitea como
ancla periódicamente. Un log reconstruido tendría un último hash distinto al ancla →
`BROKEN`. Sin ancla, `verify_chain` sólo certifica consistencia interna (se declara).

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

- El gateway es la **ruta fácil**. Un agente que lo usa obtiene sellado + log + cadena
  gratis.
- **El bypass directo (invocar el CLI sin gateway) NO es detectable de forma fiable**
  (F3, corrección de sobredeclaración previa). No existe mecanismo para saber que un
  proveedor fue invocado fuera del gateway. El control real es **disciplina operativa**
  (el gateway es la única forma documentada) + que el log es el único registro
  sancionado. NO se declara detección del bypass; se declara que la ruta legítima
  deja trazabilidad verificable y que fuera de ella no hay garantías.
- El contenido sellado vive en un bundle autocontenido **separado del repo**; lo que se
  envía al CLI es el bundle, no el árbol completo.
- **Patrón de invocación CLI (F5, abierto):** RH-T05 implementa sólo `--dry-run`
  (determinista, sin CLI real). La invocación real (RH-T07) debe resolver el
  desacople workspace-vs-lista-de-archivos: CLIs como `codex -C /worktree` o `claude`
  consumen un *workspace*, no un temp con archivos sueltos. Esa adaptación es parte de
  RH-T07 y puede requerir un wrapper por CLI; no se pre-diseña aquí.
- **No** se declara enforcement OS-level: se documenta como límite (ver ADR del harness).

## Compatibilidad con el router actual

- `router.py` **no se reescribe**: el gateway lo **invoca**. Su `route()` y `write_log()`
  se conservan. `write_log` queda como log simple legacy; el gateway usa `audit_log`
  (cadena). Migrar lectores antiguos es opcional y fuera de este plan.
