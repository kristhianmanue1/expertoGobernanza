# 01 — Análisis y alcance

## El estado actual

`review_routing/router.py` (169 líneas, stdlib) hace tres cosas **ex-ante**:

1. **Clasifica** cada path contra `config.json` (allowlist `publico`; default `deny`;
   `interno_institucional` siempre denegado en v1; `personal_confidencial` prohibido).
2. **Confina** rutas al repo (sin `..`/absolutos/symlink-fuera; clasifica ruta pedida
   Y resuelta, aplica la **más restrictiva** → anti-bypass por symlink).
3. **Bitacora** en `logs/review-routing.jsonl` con `bundle_sha256` + `config_sha256`.

Su propio docstring es honesto sobre el límite:

> *este router es un control de advertencia + bitácora de auditoría, NO una frontera
> de egreso criptográficamente enforceada. Un agente determinado podría bypasarlo
> (copiar contenido a una ruta pública, o invocar al CLI externo directamente). El
> egress real (bundle sellado + control de red + log append-only fuera del agente) es
> deuda del harness.*

## El gap (qué falta)

Tres deficiencias concretas:

| # | Deficiencia | Riesgo |
|---|---|---|
| G1 | **No hay sello que vincule lo clasificado con lo enviado.** El agente podría clasificar un set A y enviar un set B. | Envío de contenido no clasificado sin detección |
| G2 | **El CLI externo se invoca directo** (el agente llama `claude`/`codex` con lo que quiera). El router no está en el camino. | Bypass total de la clasificación |
| G3 | **El log lo escribe el router en-proceso** — mismo proceso que el agente. Append simple, sin cadena: alterar/reordenar/borrar entradas es trivial. | Bitácora no confiable ante un agente hostil |

## Qué construye el harness (alcance)

Un **gateway** como ruta sancionada + **bundle sellado** + **log tamper-evident**.
No un sandbox OS. Es la diferencia entre *“advertimos y registramos, pero el agente
puede evadirnos”* y *“la ruta legítima deja cadena de custodia verificable y el
bypass es detectable por ausencia de registro”*.

- **G1 → sellado:** el gateway produce un `seal` (manifiesto + hashes) que vincula
  clasificación ↔ contenido ↔ destino. Verificable offline.
- **G2 → gateway:** un comando `route_review` es la forma fácil de invocar al
  proveedor: clasifica, sella, envía sólo lo sellado, loguea. El agente que lo usa
  obtiene todo gratis; el que no, deja un **hueco de auditoría** (proveedor invocado
  sin entrada de log).
- **G3 → cadena de hash:** cada entrada del log referencia `prev_hash`; alterar una
  rompe la cadena. Un `verify_log` la recorre y reporta integridad.

## Lo que NO resuelve (honestidad de límites, §7.4)

1. **No previene criptográficamente** que un agente hostil copie `docs/fuentes/x` a
   `/tmp/x.md` y llame al CLI externo con ese path. Eso requiere sandbox OS / proxy
   de red — fuera de alcance para alfa monousuario.
2. **No detecta bypass perfecto:** si el agente invoca un CLI sin pasar por el
   gateway, no hay entrada de log. Esa *ausencia* es la señal de auditoría, no una
   prueba criptográfica. Se mitiga con disciplina operativa (el gateway es la única
   forma documentada) y revisión.
3. **No anonimiza** contenido `interno_institucional`: sigue denegado hasta que exista
   un pipeline de anonimización (ticket separado).

Estos límites se **declaran** en el ADR del harness y en el docstring, igual que el
router actual declara los suyos. No se sobredeclara lo que no se cumple.

## Criterio de éxito del plan

Al cerrar el hito, un revisor debe poder:

1. Ejecutar `route_review` y obtener un bundle sellado + entrada de log encadenada.
2. Alterar el log y que `verify_log` lo reporte como `BROKEN`.
3. Verificar que un bundle sellado coincide con su manifiesto re-hasheando el contenido.
4. Confirmar que el bypass directo (sin gateway) **no** produce entrada de log.
