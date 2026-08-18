# ADR-0006 — Router harness de egress verificable (sello, bitácora, gateway)

> **Estado:** Aceptado (2026-08-18, ronda adversarial RH-T08 `proceed` — ver
> `docs/propuestas/2026-08-18-router-harness-cierre/RONDA.md`).
> **Clase:** Arquitectura (egress, auditoría, §7.4).
> **Fecha:** 2026-08-18. **Autor:** agente (síntesis). **Autoridad que adopta:** humano orquestador.
> **Relacionados:** ADR-0002 (proveniencia/firma de agentes), ADR-0005 (firma
> legal, dos capas), `docs/politica-agentes.md` §7.4, `docs/planes/router-harness/`
> (plan técnico), `review_routing/router.py` (deuda declarada en su docstring).

## Contexto

El router §7.4 clasifica contenido contra una allowlist ANTES de enrutarlo a un
proveedor externo, pero corre **en-proceso con el agente**: es control de
advertencia + bitácora, **no** una frontera de egreso enforceada. La ronda
adversarial del 2026-08-13 (sobre el diseño, pre-ejecución) produjo F1–F5,
incorporados al plan antes de implementar. RH-T01..T06 están mergeados
(seal, audit_log, gateway dry-run; 180 tests).

## Decisión

**Adoptar el harness de egress verificable como capa de trazabilidad del
router §7.4**, compuesto por tres módulos stdlib (`review_routing/`):

1. **Sello de bundle** (`seal.py`, formato `eg-harness/seal-v1`): `build_seal`
   congela contenido + clasificación + destino en un bundle autocontenido con
   `seal_sha256` canónico (excluido de su propio cómputo). La clasificación del
   manifiesto se **re-obtiene** de `router.classify` (F4), nunca se infiere de
   la pertenencia al bundle. `verify_seal` re-hashea el **contenido sellado**
   (inmutable), no el repo vivo → sin TOCTOU (F2).
2. **Bitácora tamper-evident** (`audit_log.py`): JSONL append-only con cadena
   `prev_hash`→`entry_hash` (genesis = 64 ceros; hash canónico excluido de sí
   mismo). `verify_chain(log, anchor_hash)` detecta alterar/borrar/reordenar;
   con `anchor_hash` (último entry_hash conocido-good commiteado a git =
   sustrato firmado ADR-0002) detecta además **truncado+reconstrucción** (F1).
   `append` es fail-closed: no extiende una bitácora rota.
3. **Gateway ruta sancionada** (`gateway.py` + `scripts/route_review.py`):
   orquesta router → fail-closed (`denegado_fail_closed` / `bundle_vacio`) →
   sello → verificación propia. `--dry-run` determinista (sin red ni CLI
   externo). La invocación real (RH-T07) queda **gated** por proveedor
   autorizado y debe resolver el wrapper workspace-vs-archivos por CLI.

**Canonicalización única** para sello y bitácora:
`json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False)` —
misma familia que AN-KLA (canonical-json/v1).

## Límites declarados (no reclamar más)

1. **No es sandbox OS-level.** No hay confinamiento de red ni de procesos; un
   agente determinado puede copiar contenido o invocar CLIs directamente.
2. **El bypass NO es detectable criptográficamente** (F3). No existe mecanismo
   para saber que un proveedor fue invocado fuera del gateway. El control real
   es **disciplina operativa** (el gateway es la única ruta documentada) +
   `audit_log` como único registro sancionado. La ausencia de entrada en el log
   es un **hueco de trazabilidad**, no una prueba de bypass.
3. **Sin `anchor_hash`, `verify_chain` sólo certifica consistencia interna**
   (F1): un log truncado y reconstruido desde genesis sería internamente
   válido. El ancla git periódica es obligación operativa del humano/admin.
4. **El sello es SHA-256 determinista, no firma legal ni autenticación de
   origen** (M-01, ronda RH-T08): al ser hash sin clave, cualquiera puede
   forjar un sello internamente válido. El sello certifica **integridad**
   (contenido ↔ hashes ↔ clasificación ligados), no que el sello lo emitiera
   este proyecto. La autenticidad vive en el sustrato git firmado
   (ADR-0002) + la bitácora anclada. La firma con efectos externos es la
   e.firma (ADR-0005).
5. **Pinning de config (H-01, ronda RH-T08):** el gateway sólo sella bajo la
   config canónica `review_routing/config.json` (comparación de digest,
   fail-closed `config_no_canonica`). La clasificación ex-ante NO queda en
   manos de una `--config` inyectada por el agente supervisado. El CLI
   `router.py` conserva `--config` como herramienta de diagnóstico del admin.
6. `router.py` **no se reescribe**: el gateway lo invoca; `write_log` queda
   como log legacy simple.

## Alternativas consideradas

- **Sandbox OS / proxy de red**: rechazado para alfa (overkill, single-usuario;
  se agenda si hay multi-usuario).
- **No hacer nada** (router como está): deja egress sin cadena de custodia.
- **Firmar el bundle con e.firma**: mezcla capas de ADR-0005; el sello SHA-256
  basta para integridad de código.

## Consecuencias

- Toda revisión externa que pase por el gateway obtiene sellado + bitácora
  verificables gratis (la ruta fácil).
- El admin debe anclar `entry_hash` a git periódicamente (operación humana).
- RH-T07 (invoke real) abre el diseño de wrappers por CLI; el harness cerrado
  no lo bloquea.
