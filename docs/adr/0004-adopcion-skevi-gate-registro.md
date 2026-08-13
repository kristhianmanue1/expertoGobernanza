# ADR-0004 — Adopción de Skevi: gate de registro + estándar de ingeniería vendorizado

> **Estado:** Propuesto (ronda adversarial pendiente; 2026-08-13).
> **Clase:** Estratégico (gobernanza de agentes y herramienta).
> **Fecha:** 2026-08-13. **Autor:** agente (síntesis). **Autoridad que adopta:** humano orquestador.
> **Relacionados:** ADR-0001 (plataforma normativa), ADR-0003 (frontera AN-KLA),
> `docs/politica-agentes.md` §3, `docs/skevi/estandar-diseno-software.md`,
> `AGENTS.md` (bloque `skevi:registry`).

## Contexto

ExpertoGobernanza (EG) ya tiene una política de agentes madura
(`docs/politica-agentes.md` v1.1): plan→hito→tarea→contrato, ronda adversarial
multi-provider, fidelidad documental, contención de tamaño y un gate de tamaño
ejecutable (`scripts/check_sizes.py`, basado en `git ls-files` con categorías).

Skevi (`kristhianmanue1/Skevi`, repo privado) es un corpus normativo para que
agentes de IA diseñen y mantengan software: un **estándar atemporal** de
ingeniería + una **guía por fases** + un **gate** de estructura/tamaños. Tras
analizarlo se identificaron **gaps reales** que EG no cubre:

1. **Bloque de registro de contexto (§3.5):** `AGENTS.md`/`CLAUDE.md` como
   **punteros** a fuentes únicas, no contenedores. EG referenciaba sus docs en
   prosa, pero sin un mecanismo verificable que evite la duplicación.
2. **Estándar de diseño de software escrito:** EG tiene política de *flujo de
   agentes* pero no un estándar de *diseño de software* (arquitectura,
   estado/concurrencia, errores, seguridad-por-diseño). El código crece
   (router §7.4, corpus, `EvidenceEdge`).
3. **Validación de enlaces:** nada verificaba que los punteros de `AGENTS.md`
   resolvieran a archivos reales.

Skevi mismo prescribe su adopción: *"un proyecto que adopta el método copia el
estándar, fija sus propios límites e instala el gate"*; y §3.5 advierte que un
`AGENTS.md` preexistente **no** se reescribe automáticamente. Su filosofía
anti-duplicado: *"una paráfrasis es una segunda copia que envejece igual de mal"*.

## Decisión

1. **Vendor verbatim del estándar de Skevi** en `docs/skevi/estandar-diseno-software.md`
   con cabecera de **proveniencia** (repo, commit `944e72e`, ruta fuente, fecha).
   El contenido no se edita: para actualizarlo se re-vende desde una revisión
   nueva y se actualiza el commit. Es referencia on-demand para agentes.
2. **Adopción mínima activa = §3.4 (contención) + §3.5 (registro).** Lo demás
   del estándar (§2 diseño, §4 git, §6 automatización) queda como referencia
   consultable; se activa por fases conforme aporte valor (escalar gradual).
3. **Extender el gate existente** (`scripts/check_sizes.py`) con validación del
   bloque `skevi:registry` (§3.5): delimitadores balanceados, sección `[skevi]`,
   al menos una entrada, y que cada ruta resuelva a un archivo real **dentro de
   la raíz**. No se reemplaza el gate ni sus categorías/limits existentes.
4. **Bloque `skevi:registry` al final de `AGENTS.md`** con los punteros a las
   fuentes únicas del proyecto (política, estándar, plantillas, ops-github,
   índice de docs). `CLAUDE.md` sigue siendo puntero a `AGENTS.md` (sin bloque
   propio): el contenido sustantivo vive en un solo lugar.
5. **Precedencia de capas** ante solapamiento: `docs/politica-agentes.md`
   (capa de dominio: fidelidad legal, AN-KLA, multi-provider) **prevalece**
   sobre el estándar vendorizado (capa de ingeniería) en lo que toca al flujo
   y gobernanza de agentes. El estándar prevalece en pura ingeniería de
   software que EG no cubre. Instrucción directa del humano gana sobre ambas.

## Proveniencia

| Campo | Valor |
|---|---|
| Repo fuente | `kristhianmanue1/Skevi` (privado) |
| Ruta fuente | `docs/estandar-diseno-software-github.md` |
| Commit | `944e72e5eae54b0e79f804709f8676c36155d32b` |
| Fecha vendor | 2026-08-13 |
| Destino | `docs/skevi/estandar-diseno-software.md` (verbatim + cabecera) |

## Reconciliación de límites

El estándar vendorizado §3.4 prescribe límites por defecto (AGENTS 200, README
300, otros 800) y un gate con `rglob` + archivos canónicos + markdown suelto.
EG **mantiene su propio gate** (categorías: always-on 300, checkpoint 250,
artefacto 800, doc-ref 1500, código 800; `git ls-files`; exenciones `.an-kla`,
`.venv`, `docs/fuentes`). El §3.4 describe el principio; `scripts/check_sizes.py`
es la implementación autoritativa para EG. La única incorporación de Skevi al
gate es la validación del bloque de registro (§3.5).

## Consecuencias

- **+** `AGENTS.md` es ahora un puntero verificable: el gate falla-cerrado si un
  enlace del registro se rompe o escapa de la raíz.
- **+** Estándar de ingeniería consultable on-demand sin reescribirlo (sin
  divergencia por paráfrasis).
- **+** Fundamento para escalar: activar más secciones del estándar (§2 diseño,
  runbook orquestación codex+opencode) es añadir adopción activa, no re-vendor.
- **−** Mantenimiento de proveniencia: el vendor puede quedar atrás de Skevi;
  se mitiga con el commit registrado en la cabecera y la regla "no editar, re-vender".
- **−** Solapamiento conceptual entre §3.4 (Skevi) y nuestro gate; se mitiga con
  la cláusula de precedencia y este ADR.

## Alternativas consideradas

- **Apuntar `AGENTS.md` al repo externo de Skevi sin vendorizar:** descartada;
  repo privado, agente sin acceso no puede leerlo, dependencia frágil para
  instrucciones centrales.
- **Copiar fragmentos reescritos (paráfrasis):** descartada por la propia filosofía
  de Skevi y de EG (§7 fidelidad): una paráfrasis diverge sin fuente.
- **Reemplazar nuestro gate por el de Skevi:** descartada; nuestro gate es más
  afinado a EG (`git ls-files`, categorías, exención de fuentes legales).
  Extender > reemplazar.
- **No adoptar nada:** descartada tras el análisis; los gaps (registro
  verificable, estándar de ingeniería) son reales.

## Criterio de cumplimiento (DoD)

- [x] Estándar vendorizado verbatim con cabecera de proveniencia
  (`docs/skevi/estandar-diseno-software.md`).
- [x] Gate extendido con validación `skevi:registry` y tests
  (`tests/test_check_sizes.py`, 8 casos nuevos).
- [x] Bloque `skevi:registry` en `AGENTS.md` con rutas que resuelven.
- [x] `scripts/check_sizes.py` en verde (exit 0).
- [x] Suite `test_check_sizes.py` en verde (11 tests).
- [ ] Ronda adversarial con decisión `proceed` (hitos de gobernanza §6).

## Ítems abiertos (no bloquean)

- Activar §2 (diseño de software) y runbook de orquestación como adopción
  activa cuando el código o el uso de multi-agente tmux lo justifiquen.
- Mudar los `checkpoint-*.md` de la raíz a un directorio dedicado (el gate los
  tolera hoy; ideal de Skevi es raíz sin markdown suelto no canónico).
