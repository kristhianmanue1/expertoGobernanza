# Plan R2: extractor sin gold y gate de citas v2

**Contexto:** R1 cerró gobernanza, registry y trazas. El extractor de citas sigue siendo un oráculo del gold. **Fecha:** 2026-10-05. **Estado:** afinado tras ronda del mismo día. Decisión de la ronda: `fix-and-retry` aplicada en este texto. Quórum **PARCIAL** (un solo proveedor, Grok). No es `proceed` y no sustituye a `docs/plan-r1-90d.md` como cola vigente.
**Roadmap:** R2. **Fuente:** verificación local del repo el 2026-10-05; el borrador externo del mismo día no se ejecuta tal cual.

## Objetivo y criterio de cierre

- Objetivo: medir extracción real sin filtrar el gold, y hacer que `alto` signifique solo tres chequeos mecánicos: la cita es subcadena del texto derivado, el sha256 del PDF local fue recomputado y coincide, y `resolve_disposicion_vigencia(...).verificada is True`. Ese `alto` no promulga, no declara aplicabilidad, no resuelve vacatio y no es «vigente en la fecha jurídica». `version_valid_for_date` no pasa a `true`.
- Cierre: T0, T1, T3 y T4 en verde local; T2 y T5 siguen `espera-humano`. Ningún ticket de este plan modifica `corpus/evidence_edge.py`, `corpus/registry_rules.py`, `review_routing/router.py`, `review_routing/seal.py` ni `review_routing/audit_log.py`.

## Hechos que el agente debe tomar como dados

Verificados en el árbol, no en el borrador externo:

- `scripts/eval_extraction.py` llama `fake_extract`, que copia `gold_claims` con `must_find`. R1-E4-03 lo declaró hecho; el plugin real quedó explícitamente a futuro (`docs/plan-r1-90d.md`).
- `corpus/verify_citations.py` es gate `v1`. Si el PDF existe, recomputa sha256. Si no existe, hoy marca `resolved: true` con nota. `alto` es inalcanzable porque `version_valid_for_date` es `N/A_v1`. No consulta el registry.
- `corpus/registry_rules.py` valida dicts. No parsea YAML. El regex vive en `scripts/audit_document.py` (`corpus_vigencia_banner`) y en `tests/test_registry_vigencia.py`.
- `corpus/registry.yaml` ya trae trazas y `revision_vigencia` de CPEUM, LGS, LOAPF, LFEP, LSS y RIIMSS. No hace falta un corpus DOF nuevo para preguntar vigencia. El agente no edita esas trazas ni afirma derecho.
- `scripts/ci_check.sh` ejecuta el benchmark sin `--allow-missing-originals`. `.github/workflows/ci.yml` sí lo pasa. Los PDF están en `corpus/originals/` y en `.gitignore`. Hay 11 extractos versionados en `docs/fuentes/`.
- El run `37339265192` (2026-10-05, merge PR #40) sí ejecutó tests: 193, 1 error. `tests/test_akn_spike.py` falla porque el runner no tiene `xmllint`. La nota de billing en `docs/ops-github.md` (2026-08-10) no describe ese rojo.
- `review_routing/gateway.py` con `dry_run=False` devuelve `invocacion_real_no_disponible_rh_t07`. Allowlist vigente: `claude` y `codex` (`docs/autorizacion-fuentes-r1.md`). Grok no está.
- Ningún módulo lee `relaciones_normativas`. Hay entradas `verificada: true` y `false`. No son un gate.
- `interop/akn/` es el spike de `LSS:5`. No se extiende.
- El estándar Skevi vendorizado es el blob de `944e72e` (commit del 2026-08-12, hora `-0600`; fecha de vendor en este repo: 2026-08-13). No es el corpus `v4`. El pin `.skevi/corpus-pin.json` solo nombra esa diferencia. No es un registro `skevi/corpus-install/v1` y no se le pasa a `check_templates.py`. La guía, los ADR y el gate de Skevi no se copian. Los homónimos de este repo (`docs/adr/`, `scripts/check_sizes.py`) no se borran ni se sustituyen.

## Fuera de este plan

- RH-T07, invocación real del gateway, control de red y ancla git.
- Enmienda de la allowlist. La firma es humana (roles §9). Un agente no la suple.
- Aria, Ancla, Scopus, memoria L1/L2/L3.
- Nuevo árbol `corpus/derived/dof/`.
- Cambiar `vigencia_verificada` o reescribir trazas.
- Crecer Akoma Ntoso o añadir disposiciones al spike.
- Enviar texto del corpus, fixtures legales o este plan con citas verbatim a un CLI fuera de la allowlist.

## Hitos

- H0 — CI dice la causa real. [pendiente]
- H1 — El eval no puede ver el gold. La corrida con modelo queda en espera humana. [pendiente]
- H2 — `alto` solo con hash recomputado y `resolve_disposicion_vigencia(...).verificada is True`. [pendiente]

H0 es bajo impacto (toolchain). H1 y H2 tocan la compuerta de fidelidad: al ejecutarlos, la ronda de cierre es de alto impacto (`docs/politica-agentes.md` §6). Este doc, al crearse, también se ronda antes de tratarlo como cola vigente.

## Tareas

- [ ] T0 — `R2-H0-01`: `xmllint` en CI y nota de ops. → Contrato T0.
- [ ] T1 — `R2-H1-01`: contrato de extractor y eval ciego al gold. → Contrato T1.
- [ ] T2 — `R2-H1-02`: corrida allowlisted. **HUMANO. No la abre un agente.** → Contrato T2.
- [ ] T3 — `R2-H2-01`: cargar `registry.yaml` con PyYAML y banner sobre el dict. → Contrato T3.
- [ ] T4 — `R2-H2-02`: gate v2. → Contrato T4.
- [ ] T5 — `R2-H4-01`: fila de allowlist. **HUMANO. No la cierra un agente.** → Contrato T5.

Orden: T0 ∥ T1. T3 antes de T4. T2 solo después de T1 y de un humano con CLI `claude` o `codex`. T5 no desbloquea código de este plan.

## Contrato T0 — R2-H0-01: CI con xmllint

**Presupuesto:** cabe holgado.
**Entradas:** `.github/workflows/ci.yml`, `scripts/akn_spike.py` (`validate_xsd`), `tests/test_akn_spike.py`, `docs/ops-github.md` §1 y §4.
**Salidas:** workflow y un párrafo fechado en ops. No se toca el generador AKN ni el XSD.

### Definition of Done

- [ ] El job instala `libxml2-utils` (o el paquete que provee `xmllint`) antes de `unittest`.
- [ ] `python -m unittest tests.test_akn_spike` pasa en local si `xmllint` existe. Si no existe, el mensaje nombra el binario; no se omite el test con `skip` silencioso en CI.
- [ ] `docs/ops-github.md` conserva el hecho de billing del 2026-08-10 y añade que el run `37339265192` ejecutó la suite y falló por `xmllint` ausente. No dice que Actions siga suspendido.
- [ ] `python scripts/check_sizes.py` limpio. Diff < 400 líneas.
- [ ] `interop/akn/` y `scripts/akn_spike.py` quedan byte-idénticos salvo que el único cambio sea el mensaje de binario ausente, y ese cambio mide < 30 líneas.

### Git

- Rama: `fix/R2-H0-01`
- Commit: `fix(ci): instalar xmllint para el spike AKN`
- Admin: no marcar el check de GitHub como señal de fidelidad normativa. Sigue sin branch protection.

## Contrato T1 — R2-H1-01: extractor ciego

**Presupuesto:** cabe holgado. Leer `scripts/eval_extraction.py`, `tests/test_eval_extraction.py`, `docs/propuestas/recall-extraccion-v12.md`, `corpus/verify_citations.py` (solo `verify_claim` y `_normalize`).
**Salidas:** `corpus/extractor.py` (< 200 líneas), `scripts/eval_extraction.py` reescrito, tests. No se añade SDK ni clave.

### Contrato de código

```text
extract(texto: str) -> list[{"disposicion_id": str | None, "cita_texto": str}]
```

- La firma acepta un solo `str`. No acepta el documento gold, `gold_claims`, `traps` ni `must_find`.
- `evaluate(doc, preds)` se queda como juez. Sigue usando `verify_claim` para el conteo `gate_bajo`.
- Se borra `fake_extract`. `rg -n "fake_extract" scripts tests corpus` queda vacío.
- El CLI tiene un solo valor de extractor dentro del repo: `--extractor stub`. Sin ese flag sale 2 y no imprime métricas. No hay otro flag ni otro backend.
- Con `--extractor stub`, `main` llama `extract(doc["texto"])` y nada más. Un test sustituye `extract` y afirma que el único argumento es exactamente el string `doc["texto"]`, no el dict gold.
- El stub de prueba busca una cita plantada en ese string. No abre el JSON gold.
- Prohibido: red, subprocess a un CLI, leer `tests/fixtures/extraction_gold/` desde `corpus/extractor.py`.

### Definition of Done

- [ ] `python -m unittest tests.test_eval_extraction tests.test_extractor` verde.
- [ ] Un test falla si `extract` tiene otro parámetro que no sea `texto`.
- [ ] Un test del CLI afirma que el argumento de `extract` es `doc["texto"]` (tipo `str`).
- [ ] Un test arma un texto que contiene la cita y otro que no, y el stub solo devuelve la que está en el texto. Recall y precision salen de `evaluate`, no de copiar `must_find`.
- [ ] `rg -n "fake_extract" scripts tests corpus` vacío.
- [ ] `python scripts/eval_extraction.py`; el exit code es 2.
- [ ] `python -m py_compile corpus/*.py scripts/*.py review_routing/*.py`
- [ ] `python scripts/check_sizes.py` limpio. Diff < 400 líneas.

### Git

- Rama: `feat/R2-H1-01`
- Commit: `feat(extractor): contrato ciego al gold`
- Admin: este PR no reporta recall de un modelo.

## Contrato T2 — R2-H1-02: corrida real (humano)

**Presupuesto:** no lo ejecuta un agente de este repo.
**Entradas:** T1 ya mergeado; `docs/autorizacion-fuentes-r1.md` §2.
**Salidas:** un JSON de métricas en `docs/propuestas/` sin cadenas del modelo, sin texto de fixture y sin secretos. Lo archiva el humano.

### Reglas

- Proveedor: `claude` o `codex`, ya listados. Cualquier otro CLI, incluido Grok, no recibe el texto.
- El proceso ve únicamente el campo `texto` de fixtures sintéticos o públicos. No ve `gold_claims` ni `traps`.
- No hay umbral 0.8 que cumplir tuneando el prompt. El número se registra. Fijar un mínimo es otra decisión humana.
- Antes de la corrida, no después de ver el número, el humano escribe el protocolo: métricas (`precision`, `recall`, `gate_bajo`), ids de fixtures, ceguera al gold y qué contaría como regresión. Si hay umbral numérico, va en ese protocolo. Elegirlo después de medir no cuenta. El método es el de Skevi `docs/ai-agent-guide/06-componentes-con-llm.md` §2–§3 en `https://github.com/kristhianmanue1/skevi.git@d7a80b26962cd66a806943ff46f779de14c16708` (corpus `v4`). Ese archivo no existe en el commit vendorizado `944e72e`. La guía no se copia a este repo.
- Si el CLI no está en la máquina, el ticket sigue abierto. No se simula la corrida.

### Definition of Done

- [ ] Existe un protocolo fechado antes del JSON de resultados, con métricas, fixtures, ceguera al gold y criterio de regresión.
- [ ] El JSON trae `provider`, `model`, `fixture_ids`, `precision`, `recall`, `gate_bajo`, `texto_sha256`.
- [ ] Un humano de roles §9 anota en el PR que autorizó esa corrida.
- [ ] `git diff` no contiene `API_KEY`, tokens ni transcript.

### Git

- Rama: la abre el humano. Un agente que encuentre este ticket se detiene y lo reporta `espera-humano`.

## Contrato T3 — R2-H2-01: loader del registry

**Presupuesto:** cabe holgado. Leer `corpus/registry_rules.py` (firma de `resolve_disposicion_vigencia` y `validate_registry`) y el banner en `scripts/audit_document.py`. No leer el registry entero: localizar con `grep` la forma de `fuentes:`.
**Salidas:** `corpus/registry_loader.py` (< 150 líneas), `requirements.txt` con un pin de PyYAML, cambio del banner, tests. `registry_rules.py` no se edita.

### Contrato de código

- `load_registry(path) -> dict` usa `yaml.safe_load`. Si el archivo no es un mapping con lista `fuentes`, lanza error. No captura esa excepción para “seguir”.
- `fuente_por_instrumento(doc, instrumento_id) -> dict | None`.
- `corpus_vigencia_banner` deja de leer texto crudo. Recorre las fuentes ya parseadas y devuelve `CORPUS_VIGENCIA_PARCIAL_O_OK` solo si algún `vigencia_verificada is True` (booleano). Un comentario o un string `"true"` no cuenta.
- El banner no es el gate por disposición, no autoriza `alto` y no afirma vigencia jurídica. Puede quedar en `PARCIAL_O_OK` con las seis fuentes ya en `true` aunque `resolve_disposicion_vigencia` sea `false` para una disposición (ejemplo ya en el registry: `LSS:1` con `f5: false`).
- El agente instala el pin en el venv (`pip install -r requirements.txt`) antes de declarar un check verde. `.github/workflows/ci.yml` hace el mismo `pip install` antes de `unittest`. `scripts/ci_check.sh` no instala por la red; si falta `yaml`, el loader falla nombrando `PyYAML` y el ticket no se cierra.

### Definition of Done

- [ ] Test: YAML con `vigencia_verificada: true` dentro de un comentario y el único valor real `false` → banner `CORPUS_VIGENCIA_NO_VERIFICADA`.
- [ ] Test: el mismo archivo vía `safe_load` round-trip conserva `traza_disposiciones` como lista de dicts en un fixture mínimo, no en el registry de producción.
- [ ] Test: el banner no llama a `verify_claim`. Un registry de fixture con el instrumento en `true` y una disposición en `f5: false` sigue en `PARCIAL_O_OK`.
- [ ] `.venv/bin/python -c "import yaml"` sale 0 después del `pip install` del ticket, y `ci.yml` contiene ese install antes de unittest.
- [ ] `python -m unittest tests.test_registry_loader tests.test_audit_document` verde.
- [ ] `registry_rules.py` sin diff. `python scripts/check_sizes.py` limpio. Diff < 400.

### Git

- Rama: `feat/R2-H2-01`
- Commit: `feat(registry): cargar YAML con PyYAML para el banner`

## Contrato T4 — R2-H2-02: gate v2

**Presupuesto:** cabe holgado. Depende de T3 mergeado. Leer `corpus/verify_citations.py` y `tests/test_verify_citations.py` completos.
**Salidas:** gate v2 y tests. No se editan JSON derivados ni `registry.yaml`.

### Reglas de estado

`GATE_VERSION` pasa a `v2`.

- `source_declared_ok`: hay sha256 de 64 hex en `fuentes_oficiales`.
- `source_recomputed_ok`: el archivo existe, se leyó, y el sha256 coincide. Si no existe, es `false` (deja de contarse como resuelto).
- `vigencia_ok`: `resolve_disposicion_vigencia(fuente, disposicion_id)["verificada"] is True`, con la fuente sacada del loader por `modelo["instrumento"]["id"]`. Si falta el id de instrumento o el loader falla, `vigencia_ok` es `false`. No se lee `vigencia.verificada_contra_dof_nivel1` del JSON derivado. En CPEUM y LGS ese flag ya es `true` y coincide con el resolver: no sirve para demostrar que el gate usa el resolver.
- `alto`: substring ok y `source_recomputed_ok` y `vigencia_ok`. Las tres. Sin substring el estado es `bajo`, aunque hash y resolver cuadren.
- `medio`: substring ok y `source_declared_ok`, y falta recomputo o falta vigencia.
- `bajo`: el resto (cita corta, disposición ausente, hash declarado inválido, hash recomputado distinto).
- `version_valid_for_date` queda en el string `no_evalua_fecha_juridica`. No es booleano ni `true`.
- `alto` no es promulgación, aplicabilidad, vacatio ni vigencia en una fecha jurídica. La nota del resultado lo dice en una línea fija.
- El campo `relaciones_normativas` no entra al resultado. Un test con dos modelos idénticos salvo esa lista produce el mismo status.
- Otro test, independiente del disco: `verificada_contra_dof_nivel1: true`, hash recomputado igual al declarado, y `resolve_disposicion_vigencia` parcheado a `verificada: false`. El status no es `alto`.

Los tests golden de CPEUM y LGS se reescriben. Hoy fijan `gate_version == v1`, `source_resolved is True` y `response_status == medio` (`tests/test_verify_citations.py`). Eso deja de valer. La aserción nueva: sin PDF, `medio` y recomputo ausente; con PDF y resolver verdadero, `alto`. Un test mockeado, sin disco, cubre `alto`, `medio` por PDF ausente, `medio` por resolver falso y `bajo` por hash distinto.

El agente ejecuta el resolver y pega en el PR la tabla `disposicion_id → verificada → razon` del slice, rotulada «salida del resolver, no declaración de vigencia». No la redacta a mano. No “corrige” un `false`. CPEUM y LGS no tienen `traza_disposiciones`: el fallback a `trazas_publicacion` es el que ya está en `registry_rules.py`; no se añade otro.

### Definition of Done

- [ ] `python -m unittest tests.test_verify_citations tests.test_audit_document` verde.
- [ ] `rg -n "N/A_v1|verificada_contra_dof_nivel1" corpus/verify_citations.py` vacío. `GATE_VERSION` es `v2`. `version_valid_for_date` solo toma `no_evalua_fecha_juridica`.
- [ ] `rg -n "relaciones_normativas" corpus/verify_citations.py` vacío.
- [ ] `python scripts/ci_check.sh` verde en local (unittest + benchmark + tamaños). Si faltan PDF, decirlo y no usar `--allow-missing-originals` para fingir el gate local.
- [ ] Diff < 400. `registry.yaml` y `corpus/derived/` sin diff.

### Git

- Rama: `feat/R2-H2-02`
- Commit: `feat(citas): gate v2 con hash recomputado y vigencia del registry`
- Admin: H2 es compuerta de fidelidad. Merge solo con ronda de alto impacto y `proceed`. Un solo proveedor no alcanza.

## Contrato T5 — R2-H4-01: allowlist (humano)

**Presupuesto:** no aplicable a un agente.
**Entradas:** `docs/autorizacion-fuentes-r1.md` §2, `docs/roles-r1.md`.
**Salidas:** una fila nueva solo si un humano de §9 la escribe y la fecha. Grok no se añade desde este plan.

### Definition of Done

- [ ] La fila existe en la tabla, con fecha y nombre del rol que autoriza.
- [ ] Hasta entonces `gateway.py` sigue rechazando `dry_run=False`.
- [ ] Un agente no abre PR de este ticket.

## Riesgos

- PyYAML nuevo en CI. Pin en `requirements.txt` y paso `pip install` en el workflow. Sin red, `ci_check.sh` falla nombrando el paquete.
- Tests de citas dependientes del disco. Las ramas `alto`/`medio`/`bajo` se cubren con mock; los golden solo comprueban la implicación.
- Un agente puede leer `verificada_contra_dof_nivel1` del JSON derivado y saltarse el resolver. T4 lo corta con un mock: ese flag en `true`, hash recomputado ok y resolver en `false` no puede dar `alto`.
- Tres roles en una persona. Cualquier edición de trazas queda fuera. Si el resolver devuelve `false`, se reporta; no se “arregla” el YAML en el mismo PR.
- Actions puede fallar por billing otro mes. El síntoma de octubre 2026 es `xmllint`. No reutilizar la frase de agosto sin mirar el run.

## Instrucciones al agente que tome un ticket

1. Leer `AGENTS.md`, este plan y solo el contrato del ticket. Presupuesto ≤ 30k tokens.
2. Un ticket, un PR, diff < 400. Rama `feat/` o `fix/` con el id.
3. Parar en T2 y T5.
4. No citar artículos de ley que no estén ya en el registry o en el derivado que el ticket lee. No promulgar.
5. DoD local: los checks del contrato. `an_kla verify` solo si se tocó memoria. Este plan no pide writes AN-KLA.
6. Al cerrar H1 o H2 hace falta ronda de alto impacto (≥3 proveedores por modelo, autor excluido). Sin `proceed` no hay merge. H0 admite quórum-lite.
7. No declarar CI verde. Pegar el resultado local y, si se consulta GitHub, el id del run.
8. **Commit y push autorizados** (instrucción humana del 2026-10-05, posterior a la ronda; no cambia el quórum). Cuando hay avance relevante, el agente no vuelve a pedir permiso para `git commit` ni para `git push` de la rama del ticket. Avance relevante quiere decir: el DoD de ese ticket está verde en local, o hay un corte coherente ya verificado (tests del contrato en verde, diff < 400, sin secretos ni transcripts).
9. El merge a `main` de H0 entra en esa misma autorización. El merge a `main` de H1 o H2 sigue exigiendo `proceed` de alto impacto. T2 y T5 no los commitea un agente. Nada de `--force`, nada de datos que el contrato no nombre.

## Enlaces

- R1: `docs/plan-r1-90d.md`
- Política: `docs/politica-agentes.md` §6 y §7
- Allowlist: `docs/autorizacion-fuentes-r1.md`
- Plantilla: `docs/plantillas-agente.md`
- Ops: `docs/ops-github.md`
- Diseño del gold: `docs/propuestas/recall-extraccion-v12.md`
- Ronda de este borrador: `docs/propuestas/2026-10-05-plan-r2/ADVERSARIAL.md`
- Pin Skevi (no es el canon): `.skevi/corpus-pin.json`
- Ronda de ese pin: `docs/propuestas/2026-10-05-plan-r2/ADVERSARIAL-PIN.md`
