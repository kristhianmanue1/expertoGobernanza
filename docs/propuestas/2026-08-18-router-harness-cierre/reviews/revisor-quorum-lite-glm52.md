# Review adversarial — revisor quorum-lite (ciclo 1 + retry 1 + retry 2)

**Revisor:** subagent glm-5.2 en contexto fresco (no comparte contexto con el
autor). **Limitación declarada:** misma arquitectura subyacente que el autor
(decorrelación de contexto, no multi-provider; política §6 quorum-lite).

## Ciclo 1 (2026-08-18) — veredicto: fix-and-retry

| ID | Sev | Hallazgo | Estado |
|---|---|---|---|
| H-01 | HIGH | `--config` acepta config arbitraria del agente (publico:["**"]) → sella lo que la canónica deniega; contradice "la clasificación la hace la CONFIG" | FIX: pinning de digest en `gateway.run` → `config_no_canonica` |
| M-01 | MED | docstring de `seal.py` sobrestaba autenticidad ("prueba que iba a este proveedor"): hash sin clave es forjable | FIX: docstring integridad-no-autenticidad + límite explícito en ADR-0006 §Límites.4 |
| L-01 | LOW | `verify_chain(anchor)` con última línea JSON no-dict → AttributeError | FIX: `isinstance` guard → `ancla_no_verificable:ultima_entrada_no_objeto` |
| L-02 | LOW | `--files` duplicado → manifest duplicado → rompía verify(build)==True | FIX: `build_seal` rechaza duplicados (`SealError`) |
| L-03 | LOW | NaN/Infinity aceptados (sin allow_nan=False); str en bundle_content → TypeError sin capturar; provider/model sin validar str | FIX: `allow_nan=False`, wrapper TypeError/ValueError → `(False, "tipo_invalido")`, validaciones str/bytes |
| L-04 | LOW | `"seq": true` pasa por igualdad bool/int | FIX: `type(e["seq"]) is not int` → `seq_no_entero` |

Superficie path traversal: **sin hallazgos tras 25 ataques** (.., absolutos,
symlinks in/out, NUL, unicode NFD/NFC, prefijos colisionantes, TOCTOU
symlink-flip detectado por bundle_sha256).

## Retry 1 — veredicto: fix-and-retry (2 LOW de regresión)

Todos los fixes del ciclo 1 VERIFICADOS con PoC originales reproducidos.

| ID | Sev | Hallazgo | Estado |
|---|---|---|---|
| N-01 | LOW | regresión de L-03: `_digest` con NaN lanza ValueError no capturado en `_chain_findings` → verify_chain crashea donde antes reportaba BROKEN | FIX: try/except → finding `entrada_no_serializable:posN` |
| N-02 | LOW | `_bundle_digest` normalizaba clave pero manifest usaba path raw → KeyError fuera del wrapper (backslash vía CLI) | FIX: normalización posix uniforme en `read_bundle`/`build_seal` + KeyError → `(False, "manifest_paths_invalidos")` |

## Retry 2 — veredicto: **proceed**

N-01 y N-02 VERIFICADOS (PoC reproducidos; anti-swallow comprobado: NaN en
pos2 no oculta rotura en pos3; sin falsos OK; colisiones de normalización
fail-closed). 2 hallazgos nuevos LOW estrictamente fail-closed:

| ID | Sev | Hallazgo | Disposición |
|---|---|---|---|
| X-01 | LOW | anidamiento ~60k en una línea JSON → RecursionError en `_parse` (crash, no BROKEN); requiere control del log en disco | **Backlog** (declarado) |
| X-02 | LOW | dup-check de `build_seal` sobre paths raw; 'a/b'+'a\\b' pasaba y rompía verify(build)==True (fail-closed, sin crash) | **FIX aplicado post-proceed** (el mismo que sugirió el revisor: dup-check sobre paths normalizados) + test `test_duplicados_tras_normalizacion_fail_closed` |

INFO: `audit_log.append` con seal NaN del caller → ValueError crudo,
fail-closed efectivo, inalcanzable desde CLI (RH-T07 gated). Backlog.

## Veredicto final: **proceed** (2026-08-18)

Suite: 193/193 OK tras fixes (baseline 180 al inicio de la ronda).
