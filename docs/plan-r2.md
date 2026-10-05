# Plan R2: evaluación sin gold y diagnóstico de evidencia del gate v1

**Contexto:** R1 incorporó gobernanza, registry y trazas; conserva pendientes. La frase «el extractor copia el gold» describe el árbol anterior a T1; en `main` el stub no lee el gold. **Fecha:** 2026-10-05. **Estado:** precisiones de contrato incorporadas por instrucción del Operador; expediente en `docs/propuestas/2026-10-05-plan-r2/RECOMENDACIONES-RETRY.md`. Quórum de cierre de H1/H2 **PARCIAL**. No es `proceed` ni sustituye a `docs/plan-r1-90d.md` como cola vigente. **Arranque:** T0 cerrado en `aa7f06a`. El Operador ordenó el merge el 2026-10-05: T1 PR #47, T1b PR #48, T3 PR #49 y T4 PR #50 quedaron en `main` `5f94d38`. La punta con este registro es `d5aea67`. Ese merge no es `proceed` de §6. Integrar el código y un CI verde dejan H1/H2 en **PARCIAL** hasta revisiones elegibles y reconciliación. T2 sigue en ejecución manual. T5 nombra un panel; nombrarlo no lo autoriza.
**Roadmap:** R2. **Fuente:** verificación local del repo el 2026-10-05; el borrador externo del mismo día no se ejecuta tal cual.

## Objetivo y criterio de cierre

- Objetivo técnico: preparar una evaluación sin acceso del extractor al gold y reportar por separado substring, recomputo de fuente y resultado del resolver. Se conserva `GATE_VERSION = "v1"`, `version_valid_for_date = "N/A_v1"` y `alto` inalcanzable conforme a política §7.3. Una futura v2 temporal requiere otro contrato y decisión del Operador.
- Cierre de infraestructura: T0, T1, T1b, T3 y T4 verificados, con evidencia remota para T0 y rondas exigidas para H1/H2. No demuestra calidad de un extractor real.
- Cierre experimental: T2 ejecutado por humano con protocolo previo y resultados recalculables. Mientras esté pendiente, no se declara cumplido el objetivo de medir extracción real. T5 es una dependencia humana de disponibilidad de quórum, no un permiso implícito.
- Ningún ticket modifica `corpus/evidence_edge.py`, `corpus/registry_rules.py`, `review_routing/router.py`, `review_routing/seal.py` ni `review_routing/audit_log.py`.

## Estado vigente: tres papeles distintos

Instrucción del Operador posterior al merge `d5aea67`. Implementación, experimento y adjudicación se leen por separado.

- **Implementación.** T0, T1, T1b, T3 y T4 están en `main`. El código de T1–T4 queda en `5f94d38`. La punta de docs es `d5aea67`. CI del código: run [`37356297144`](https://github.com/kristhianmanue1/expertoGobernanza/actions/runs/37356297144), 216 tests OK. CI de la punta: run [`37356407958`](https://github.com/kristhianmanue1/expertoGobernanza/actions/runs/37356407958), success. El stub de `corpus/extractor.py` devuelve una cita plantada solo si esa frase está en el texto. El gate sigue en `v1`, con `alto` inalcanzable. Esto no cierra H1 ni H2.
- **Experimento (T2).** Corrida de extracción con un modelo. El protocolo se fija antes de observar resultados. Las predicciones se conservan y las métricas se recalculan con `--predictions-file`, sin volver a invocar al modelo. Modo vigente: la ejecuta el Operador, a mano. Delegarla a un agente exige una instrucción posterior que nombre la revisión de este plan, el ticket `R2-H1-02` y un CLI que ya esté en `docs/autorizacion-fuentes-r1.md` §2. Sin esa frase, el agente se detiene.
- **Adjudicación (T5 y §6).** H1 y H2 permanecen **PARCIAL** hasta que existan revisiones elegibles del SHA final y un humano reconcilie los hallazgos. El código integrado y el CI en verde no sustituyen esa ronda. La autorrevisión no cuenta. Ver la matriz de T5.

## Baseline observado (histórico)

Fotografía del árbol al abrir este plan, antes de T1–T4. No describe `main` `d5aea67`. El estado vigente es la sección anterior.

Verificados entonces en el árbol, no en el borrador externo:

- `scripts/eval_extraction.py` llamaba `fake_extract`, que copiaba `gold_claims` con `must_find`. R1-E4-03 lo declaró hecho; el plugin real quedó explícitamente a futuro (`docs/plan-r1-90d.md`). En `main` ese símbolo ya no está.
- `corpus/verify_citations.py` ya era gate `v1`. Si el PDF existía, recomputaba sha256. Si no existía, marcaba `resolved: true` con nota. `alto` era, y sigue, inalcanzable porque `version_valid_for_date` es `N/A_v1`. En aquel árbol el gate no consultaba el registry; en `main`, T4 sí lo consulta y mantiene el tope `medio`.
- `corpus/registry_rules.py` valida dicts. No parsea YAML. El regex del banner vivía en `scripts/audit_document.py`. En `main` el banner lee el dict de `corpus/registry_loader.py`. `tests/test_registry_vigencia.py` conserva su regex de prueba.
- `corpus/registry.yaml` ya trae trazas y `revision_vigencia` de CPEUM, LGS, LOAPF, LFEP, LSS y RIIMSS. No hace falta un corpus DOF nuevo para preguntar vigencia. El agente no edita esas trazas ni afirma derecho.
- `scripts/ci_check.sh` ejecuta el benchmark sin `--allow-missing-originals`. `.github/workflows/ci.yml` sí lo pasa. Los PDF están en `corpus/originals/` y en `.gitignore`. Hay 11 extractos versionados en `docs/fuentes/`.
- El run `37339265192` (2026-10-05, merge PR #40) sí ejecutó tests: 193, 1 error. `tests/test_akn_spike.py` falla porque el runner no tiene `xmllint`. El run `37348191223` (merge PR #43, `8410075`) repite esa causa. La nota de billing en `docs/ops-github.md` (2026-08-10) no describe esos rojos.
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

- H0 — CI dice la causa real. [hecho: PR #45, run `37353348315`, SHA `f198847`]
- H1 — El extractor recibe solo texto; el evaluador sí recibe gold y produce métricas resistentes a duplicados. [en `main` `5f94d38` por instrucción del Operador; cierre §6 PARCIAL]
- H2 — Evidencia desglosada, errores explícitos y tope `medio`; fecha jurídica sin evaluar. [en `main` `5f94d38` por instrucción del Operador; cierre §6 PARCIAL]
- Experimento T2 — medición real, separado del cierre de infraestructura. [espera-humano]

H0 es bajo impacto (toolchain). H1 y H2 tocan la compuerta de fidelidad: al ejecutarlos, la ronda de cierre es de alto impacto (`docs/politica-agentes.md` §6). Este doc, al crearse, también se ronda antes de tratarlo como cola vigente.

## Tareas

- [x] T0 — `R2-H0-01`: `xmllint` en CI y nota de ops. → Contrato T0. Run [`37353348315`](https://github.com/kristhianmanue1/expertoGobernanza/actions/runs/37353348315), SHA `f198847`.
- [x] T1 — `R2-H1-01`: extractor recibe sólo texto; juez conserva acceso al gold. → Contrato T1. PR #47.
- [x] T1b — `R2-H1-03`: juez corregido e importación offline de predicciones. → Contrato T1b. PR #48.
- [ ] T2 — `R2-H1-02`: corrida allowlisted. Protocolo y métricas en `docs/propuestas/2026-10-05-plan-r2/t2/`. La casilla de autorización en el PR sigue abierta. → Contrato T2.
- [x] T3 — `R2-H2-01`: cargar `registry.yaml` con PyYAML y banner sobre el dict. → Contrato T3. PR #49.
- [x] T4 — `R2-H2-02`: diagnóstico de evidencia compatible con gate v1. → Contrato T4. PR #50.
- [ ] T5 — `R2-H4-01`: fila de allowlist. **HUMANO. No la cierra un agente.** → Contrato T5.

Orden: T0–T1–T1b–T3–T4 están en `main` `5f94d38` (punta `d5aea67`). El merge lo ordenó el Operador y no sustituye el `proceed` de §6. H1 y H2 siguen **PARCIAL** aunque el CI pase: faltan revisiones elegibles del SHA final y la reconciliación de sus hallazgos. La autorrevisión no cuenta. T2 sigue en ejecución manual del Operador. La allowlist actual no autoriza el panel nombrado en T5; tener los CLI instalados no demuestra diversidad ni autorización. R1 sigue siendo la cola vigente fuera de los tickets adoptados. Reconciliar sus tickets hechos/pendientes mediante referencias, sin declarar R1 cerrado.

## Contrato T0 — R2-H0-01: CI con xmllint

**Presupuesto:** cabe holgado.
**Entradas:** `.github/workflows/ci.yml`, `scripts/akn_spike.py` (`validate_xsd`), `tests/test_akn_spike.py`, `docs/ops-github.md` §1 y §4.
**Salidas:** workflow y un párrafo fechado en ops. No se toca el generador AKN ni el XSD.

### Definition of Done

- [x] El job instala `libxml2-utils` (o el paquete que provee `xmllint`) antes de `unittest`.
- [x] Run remoto del SHA del ticket ejecuta la validación XSD y termina verde; registrar URL y SHA. Si no puede ejecutarse, T0 queda parcial con causa observada, aunque el local pase. Evidencia: [`37353194656`](https://github.com/kristhianmanue1/expertoGobernanza/actions/runs/37353194656) en `b56d8f8` y [`37353348315`](https://github.com/kristhianmanue1/expertoGobernanza/actions/runs/37353348315) en `f198847`; 193 tests OK.
- [x] `python -m unittest tests.test_akn_spike` pasa en local si `xmllint` existe. Si no existe, el mensaje nombra el binario; no se omite el test con `skip` silencioso en CI. Local: 7 tests OK.
- [x] `docs/ops-github.md` conserva el hecho de billing del 2026-08-10 y añade que el run `37339265192` ejecutó la suite y falló por `xmllint` ausente. No dice que Actions siga suspendido. También queda `37348191223`.
- [x] `python scripts/check_sizes.py` limpio. Diff < 400 líneas.
- [x] `interop/akn/` y `scripts/akn_spike.py` quedan byte-idénticos salvo que el único cambio sea el mensaje de binario ausente, y ese cambio mide < 30 líneas.

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
- `evaluate(doc, preds)` sigue siendo el juez, pero sus métricas no se aceptan hasta T1b. Sigue usando `verify_claim` para el conteo `gate_bajo`.
- Se borra `fake_extract`. `rg -n "fake_extract" scripts tests corpus` queda vacío.
- En T1 el único modo es `--extractor stub`; sin modo sale 2 y no imprime métricas. T1b añade exclusivamente importación offline de predicciones, sin otro backend.
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

## Contrato T1b — R2-H1-03: juez y predicciones offline

**Depende:** T1. **Salidas:** evaluador y tests, PR propio <400 líneas. Sin red ni SDK.

- Emparejamiento uno-a-uno de máxima cardinalidad entre predicciones y gold; desempate estable. Congelar el criterio textual antes de T2. El recall usa gold distintos recuperados / total gold; no TP repetidos.
- Antes del matching, agrupar predicciones equivalentes por `(normalize(cita_texto), disposicion_id)`. `normalize` es la de `corpus/verify_citations.py`: NFKD, sin marcas, minúsculas y espacios colapsados. IDs son exactos, nulo incluido, sin normalización que fusione identificadores. Cada clase aporta como máximo un TP; copias adicionales son FP. Gold exige claim IDs únicos. La unidad medida es cita identificable, no repetición de ocurrencias textuales.
- Repetir la misma clase —mismo texto ya normalizado y mismo ID exacto, nulo incluido— no aumenta TP ni recall; las copias suman FP y pueden bajar la precisión. Reordenar no cambia las métricas. IDs no nulos distintos son clases distintas y pueden recuperar gold distintos si el alineamiento coincide. Un ID nulo no recupera el gold restante de esa misma cita cuando otra clase con ID ya cubre uno de esos gold.
- Cada predicción duplicada no emparejada cuenta FP. Duplicar o reordenar predicciones no aumenta recall ni cambia el número de aciertos; probar también coincidencias ambiguas y permutaciones del gold.
- Conservar `precision`/`recall` como métricas de extracción: ID opcional; cuando ambos IDs existen deben coincidir, conforme al diseño v1.2. Reportar diagnóstico de IDs ausentes/incorrectos, TP/FP/FN y denominadores. Denominador cero → valor null con razón. Un TP sin ID puede tener gate bajo; no es una contradicción.
- Conservar `gate_bajo` como conteo y añadir `gate_bajo_rate` con denominador `n_pred`; no tratarlo como precision ni mezclarlo con calidad de extracción.
- CLI: modos excluyentes `--extractor stub` o `--predictions-file PATH`. El segundo consume `{doc_id: [predicciones]}` validado; no ejecuta proveedor. Rechaza IDs de documentos desconocidos/faltantes, claves JSON duplicadas y predicciones mal tipadas. Lista vacía explícita es válida. Sin modo, exit 2 sin métricas.
- Tests: dos gold y diez copias de una cita de la misma clase → TP=1, FP=9, FN=1, recall=0.5; control positivo con ambas citas → recall=1. Dos copias con ID `A:1` → TP=1, FP=1, FN=1, recall=0.5. Dos copias con ID nulo → el mismo resultado. `A:1` y `B:1` sobre el mismo texto → recall=1. `A:1` y nulo frente a gold `A:1` y `B:1` del mismo texto → recall=0.5. Una variante de mayúsculas, espacios o acentos de la misma clase no suma otro TP. Incluir ID incorrecto, no coincidencia, gold vacío y entrada malformada. Cita sin ID puede ser TP textual con gate bajo.
- Versionar el alineador: conservar normalización y mínimo de 20 caracteres; exigir predicción contenida en gold, no la inclusión inversa que acepta una predicción sobredimensionada. Test negativo con texto completo que contiene la cita. No comparar métricas entre versiones como equivalentes.
- `python -m unittest tests.test_eval_extraction tests.test_extractor` y `python scripts/check_sizes.py` verdes. Registrar versión del evaluador y del gate en la salida.
- La firma de un argumento demuestra separación de interfaz, no aislamiento del proceso: inspeccionar extractor sin accesos al gold. La corrida T2 usa contexto fresco y sólo el payload autorizado.

## Contrato T2 — R2-H1-02: corrida real (humano)

**Presupuesto:** no lo ejecuta un agente de este repo, salvo la delegación expresa de abajo.
**Entradas:** T1 y T1b mergeados; `docs/autorizacion-fuentes-r1.md` §2.
**Salidas:** un JSON de métricas en `docs/propuestas/` sin cadenas del modelo, sin texto de fixture y sin secretos. Lo archiva el humano.

### Modo de ejecución

Quedó precisado el 2026-10-05, después de `d5aea67`: T2 es el experimento, distinto de la implementación ya integrada y de la adjudicación de T5.

- El 2026-10-05 el Operador escribió «t2 te lo delego a ti, continua». No nombró CLI. Grok no recibió el texto. Claude respondió 403 en un preflight sin fixture. La corrida usó `codex` (OpenAI, modelo reportado `gpt-6.1-sol`) bajo el protocolo `692bdd9`.
- Otra corrida, u otro CLI, pide otro protocolo fechado antes de medir. Esta delegación no se extiende.
- En ambos modos el protocolo se escribe antes de observar el número. Las predicciones se conservan. El recálculo usa `--predictions-file` y no vuelve a llamar al modelo.

### Reglas

- Proveedor de la corrida: `claude` o `codex`, ya listados. Cualquier otro CLI, incluido Grok y OpenCode, no recibe el texto mientras no exista la enmienda humana de la allowlist. Nombrarlos en T5 no los habilita para T2.
- El proceso ve únicamente el campo `texto` de fixtures sintéticos o públicos. No ve `gold_claims` ni `traps`.
- No hay umbral 0.8 que cumplir tuneando el prompt. El número se registra. Fijar un mínimo es otra decisión humana.
- Antes de la corrida, no después de ver el número, el humano escribe el protocolo: métricas (`precision`, `recall`, `gate_bajo`), ids de fixtures, ceguera al gold y qué contaría como regresión. Si hay umbral numérico, va en ese protocolo. Elegirlo después de medir no cuenta. El método es el de Skevi `docs/ai-agent-guide/06-componentes-con-llm.md` §2–§3 en `https://github.com/kristhianmanue1/skevi.git@d7a80b26962cd66a806943ff46f779de14c16708` (corpus `v4`). Ese archivo no existe en el commit vendorizado `944e72e`. La guía no se copia a este repo.
- Si el CLI no está en la máquina, el ticket sigue abierto. No se simula la corrida.
- Congelar prompt, configuración, intentos y regla de agregación antes de medir; registrar fallos y retries, sin seleccionar sólo el mejor resultado. Los fixtures actuales son conocidos: es piloto exploratorio, no evidencia de generalización ni holdout ciego.
- Conservar predicciones estructuradas y protocolo en una ubicación autorizada por el humano, con hashes y referencias desde el resultado. No guardar razonamiento interno ni secretos. Un hash sin artefacto recuperable no hace recalculables las métricas.

### Definition of Done

- [x] Existe un protocolo fechado antes del JSON de resultados, con métricas, fixtures, ceguera al gold y criterio de regresión. Commit `692bdd9`, archivo `docs/propuestas/2026-10-05-plan-r2/t2/PROTOCOLO.md`.
- [x] JSON con proveedor, modelo solicitado/reportado (unknown si falta evidencia), fixture IDs y hashes de texto/gold, SHA del evaluador, versión del gate y métricas/denominadores T1b. Prompt/configuración, protocolo y predicciones se incluyen sólo como referencias y hashes a artefactos recuperables autorizados; no cadenas del modelo en el JSON publicado. Archivo `docs/propuestas/2026-10-05-plan-r2/t2/RESULTADOS.json`.
- [x] Recalcular las métricas desde las predicciones conservadas mediante `--predictions-file`, sin volver a invocar al modelo. Registrar resultado y ubicación autorizada de evidencia. Segunda ejecución idéntica a la primera.
- [ ] Un humano de roles §9 anota en el PR que autorizó esa corrida. La frase de delegación está citada en el PR; la casilla queda abierta hasta esa anotación.
- [ ] `git diff` no contiene `API_KEY`, tokens ni transcript.

### Git

- Rama: la abre el humano. Un agente que encuentre este ticket se detiene y lo reporta `espera-humano`, salvo la delegación expresa del modo de ejecución.

## Contrato T3 — R2-H2-01: loader del registry

**Presupuesto:** cabe holgado. Leer `corpus/registry_rules.py` (firma de `resolve_disposicion_vigencia` y `validate_registry`) y el banner en `scripts/audit_document.py`. No leer el registry entero: localizar con `grep` la forma de `fuentes:`.
**Salidas:** `corpus/registry_loader.py` (< 150 líneas), `requirements.txt` con un pin de PyYAML, cambio del banner, tests. `registry_rules.py` no se edita.

### Contrato de código

- `load_registry(path) -> dict` usa un loader basado en `yaml.SafeLoader`, sin constructores de objetos, que rechaza claves duplicadas antes de colapsarlas. Exige mapping con lista `fuentes`, entradas mapping e IDs no vacíos únicos. Ejecuta `validate_registry`; errores estructurales levantan excepción identificable. No captura esa excepción para “seguir”.
- `fuente_por_instrumento(doc, instrumento_id) -> dict | None`.
- `corpus_vigencia_banner` deja de leer texto crudo. Recorre las fuentes ya parseadas y devuelve `CORPUS_VIGENCIA_PARCIAL_O_OK` solo si algún `vigencia_verificada is True` (booleano). Un comentario o un string `"true"` no cuenta.
- El banner no es el gate por disposición, no autoriza `alto` y no afirma vigencia jurídica. Puede quedar en `PARCIAL_O_OK` con las seis fuentes ya en `true` aunque `resolve_disposicion_vigencia` sea `false` para una disposición (ejemplo ya en el registry: `LSS:1` con `f5: false`).
- El agente instala el pin en el venv (`pip install -r requirements.txt`) antes de declarar un check verde. `.github/workflows/ci.yml` hace el mismo `pip install` antes de `unittest`. `scripts/ci_check.sh` no instala por la red; si falta `yaml`, el loader falla nombrando `PyYAML` y el ticket no se cierra.

### Definition of Done

- [ ] Test: YAML con `vigencia_verificada: true` dentro de un comentario y el único valor real `false` → banner `CORPUS_VIGENCIA_NO_VERIFICADA`.
- [ ] Tests: claves YAML duplicadas, IDs repetidos, fuente no mapping y error de validación se rechazan. String `"true"` no cuenta como booleano; si invalida el registry, produce error explícito.
- [ ] Test: el mismo archivo vía `safe_load` round-trip conserva `traza_disposiciones` como lista de dicts en un fixture mínimo, no en el registry de producción.
- [ ] Test: el banner no llama a `verify_claim`. Un registry de fixture con el instrumento en `true` y una disposición en `f5: false` sigue en `PARCIAL_O_OK`.
- [ ] `.venv/bin/python -c "import yaml"` sale 0 después del `pip install` del ticket, y `ci.yml` contiene ese install antes de unittest.
- [ ] `python -m unittest tests.test_registry_loader tests.test_audit_document` verde.
- [ ] `registry_rules.py` sin diff. `python scripts/check_sizes.py` limpio. Diff < 400.

### Git

- Rama: `feat/R2-H2-01`
- Commit: `feat(registry): cargar YAML con PyYAML para el banner`

## Contrato T4 — R2-H2-02: diagnóstico compatible con gate v1

**Presupuesto:** cabe holgado. Depende de T3 mergeado. Leer `corpus/verify_citations.py` y `tests/test_verify_citations.py` completos.
**Salidas:** diagnósticos del gate v1, integración con auditor y tests. No se editan JSON derivados ni `registry.yaml`.

### Reglas de estado

`GATE_VERSION` permanece en `v1`. Añadir `evidence_schema_version: "v1"` para el diagnóstico aditivo. Conservar campos públicos y exit codes; v2 temporal queda fuera de alcance.

- `source_declared_ok`: hay sha256 de 64 hex en `fuentes_oficiales`.
- `source_recomputed_ok`: true sólo con lectura y hash coincidente. `source_check`: `missing`, `match`, `mismatch`, `error` o `invalid_declaration`. Conservar `source_resolved` legacy v1: declarado válido con PDF ausente puede ser true; documentar que no equivale a recomputo.
- `registry_check`: `verified`, `unverified`, `missing_evidence` o `error`, con razón del resolver. Seleccionar fuente por `modelo["instrumento"]["id"]` y llamar `resolve_disposicion_vigencia`. Fuente ausente en registry válido → `missing_evidence`; instrumento malformado, loader fallido o excepción del resolver → `error`. No usar `vigencia.verificada_contra_dof_nivel1` del derivado como atajo.
- Precedencia: disposición/cita inválida, hash inválido/distinto, error de lectura, loader o resolver → `bajo` con razón; ninguna degradación puede ocultarlos.
- Substring y declaración válidos, `source_check` en `missing|match` y registry sin error operativo → `medio`. Ese “sin error” incluye `verified`, `unverified` y `missing_evidence`. Resolver negativo es evidencia insuficiente. `alto` sigue inalcanzable, aun con todos los diagnósticos positivos.
- Si la disposición existe en el modelo derivado, la cita cumple el substring y la declaración de hash es válida, con `source_check` en `missing|match`, la ausencia de la fuente en un registry cargado y válido produce `response_status=medio` y `registry_check=missing_evidence`. La ausencia de la disposición en el modelo derivado produce `bajo`. Hash distinto, declaración inválida, PDF ilegible, loader fallido o excepción del resolver conservan precedencia hacia `bajo` y no quedan ocultos por `missing_evidence`.
- `version_valid_for_date` conserva `N/A_v1`. Nota fija: «Fecha jurídica no evaluada; evidencia mecánica y atestación del registry no autorizan decisión, aplicabilidad ni promulgación».
- El campo `relaciones_normativas` no entra al resultado. Un test con dos modelos idénticos salvo esa lista produce el mismo status.
- Test sin disco: flag derivado true y hash coincidente; resolver false → `registry_check=unverified`, resolver true → `verified`. Afirmar argumentos y razón; ambos son `medio`. Comprobar sólo ausencia de `alto` sería vacuo.

Los golden conservan `v1` y `medio`, añadiendo diagnósticos. Matriz hermética: PDF ausente/coincidente/distinto/ilegible, registry ausente/malformado, fuente no encontrada y resolver positivo/negativo/error. El auditor deriva `gate_version` de la constante compartida y conserva diagnósticos por claim; probar coherencia y exit codes. Ninguna combinación produce `alto`.

Límite: match contra JSON y hash del PDF no prueban por sí solos fidelidad de extracción JSON→PDF. Se conserva la procedencia declarada; no elevar los checks a prueba semántica o temporal.

El agente ejecuta el resolver y pega en el PR la tabla `disposicion_id → verificada → razon` del slice, rotulada «salida del resolver, no declaración de vigencia». No la redacta a mano. No “corrige” un `false`. CPEUM y LGS no tienen `traza_disposiciones`: el fallback a `trazas_publicacion` es el que ya está en `registry_rules.py`; no se añade otro.

### Definition of Done

- [ ] `python -m unittest tests.test_verify_citations tests.test_audit_document` verde.
- [ ] Tests de campos legacy, diagnóstico aditivo, argumentos del resolver y coherencia con auditor. `GATE_VERSION=v1`, `version_valid_for_date=N/A_v1`, `alto` inalcanzable.
- [ ] Disposición ausente del modelo derivado → `bajo`. Modelo válido, fuente ausente en registry válido, PDF ausente o coincidente → `medio` y `missing_evidence`. Fuente ausente y hash distinto → `bajo`. Fuente ausente y PDF ilegible → `bajo`.
- [ ] `rg -n "relaciones_normativas" corpus/verify_citations.py` vacío.
- [ ] `./scripts/ci_check.sh` verde en local (unittest + benchmark + tamaños). Si faltan PDF, decirlo y no usar `--allow-missing-originals` para fingir el gate local.
- [ ] Diff < 400. `registry.yaml` y `corpus/derived/` sin diff.

### Git

- Rama: `feat/R2-H2-02`
- Commit: `feat(citas): diagnosticos de evidencia compatibles con gate v1`
- Admin: H2 es compuerta de fidelidad. Merge solo con ronda de alto impacto y `proceed`. Un solo proveedor no alcanza.

## Contrato T5 — R2-H4-01: allowlist (humano)

**Presupuesto:** no aplicable a un agente.
**Entradas:** `docs/autorizacion-fuentes-r1.md` §2, `docs/roles-r1.md`.
**Salidas:** configuración autorizada de ≥3 proveedores revisores elegibles, autor excluido, permisos de datos y reconciliador conforme a §6. Puede requerir varias filas. La tabla de abajo es la intención del Operador. No es la enmienda de `docs/autorizacion-fuentes-r1.md` y no autoriza envío de corpus ni de fixtures.

### Panel previsto y matriz del SHA final

Disponibilidad de un CLI no demuestra diversidad ni autorización. La diversidad se cuenta por el modelo que la corrida archivada reporte. La autorización es una fila fechada y firmada en la allowlist. Hoy esa allowlist sigue en `claude` (Anthropic) y `codex` (OpenAI).

SHA de código a adjudicar: `5f94d38`. Punta de `main` que lo contiene: `d5aea67`. Quien produjo T1 (`7645a7e`), T1b (`1d3ae70`), T3 (`2cb3c55`) y T4 (`5c0c0de`) fue el agente Grok (xAI); el git author de esos commits es `devcdmx`. Los merge commits son del admin.

| Papel sobre `5f94d38` | CLI | Modelo efectivo | ¿Cuenta para el quórum? |
|---|---|---|---|
| Produjo el código | Grok | xAI, sesión que escribió T1–T4 | No. Es el autor. La autorrevisión no entra. |
| Revisor previsto | Codex | OpenAI. El binario ya está en la allowlist. El modelo se anota en la corrida. | Sí, cuando exista una revisión de ese SHA, en contexto fresco, sin ver las otras. La revisión previa del borrador del plan no es esta fila. |
| Revisor previsto | OpenCode | Config local del 2026-10-05: `zai-coding-plan/glm-5.3-flash` (Z.AI). Si el CLI apunta a otro modelo, la familia cambia. | Solo si la corrida usa una familia distinta de la del autor y de Codex, y la allowlist ya tiene la fila. Hoy no la tiene. |
| Nombrado en el panel, no elegible sobre este SHA | Grok | xAI | No ocupa asiento de revisor del código que produjo. |

Con esa matriz, los revisores elegibles todavía no son tres: Codex puede serlo cuando revise el SHA; OpenCode falta autorización y la corrida; Grok queda fuera por autor. H1/H2 siguen **PARCIAL**. Un humano de roles §9 reconcilia los hallazgos cuando esas revisiones existan. `gateway.py` sigue rechazando `dry_run=False`.

### Definition of Done

- [ ] Filas necesarias con fecha y rol autorizante; matriz de asignación y exclusión del autor por proveedor. Más CLIs del mismo proveedor no completan quórum. La matriz de arriba es intención: las filas de Grok y OpenCode siguen sin firmar.
- [ ] Hasta entonces `gateway.py` sigue rechazando `dry_run=False`.
- [ ] Un agente no abre PR de este ticket.

## Riesgos

- PyYAML nuevo en CI. Pin en `requirements.txt` y paso `pip install` en el workflow. Si no está instalado, `ci_check.sh` falla nombrando el paquete; instalado, el gate local no requiere red.
- Tests dependientes del disco: matriz hermética de diagnósticos y estados `medio`/`bajo`, con `alto` inalcanzable.
- T4 debe probar argumentos y resultado del resolver: la mera ausencia de `alto` no detecta un bypass del diagnóstico.
- Tres roles en una persona. Cualquier edición de trazas queda fuera. Si el resolver devuelve `false`, se reporta; no se “arregla” el YAML en el mismo PR.
- Actions puede fallar por billing otro mes. El síntoma de octubre 2026 es `xmllint`. No reutilizar la frase de agosto sin mirar el run.

## Instrucciones al agente que tome un ticket

1. Leer `AGENTS.md`, este plan y solo el contrato del ticket. Presupuesto ≤ 30k tokens.
2. Un ticket, un PR, diff < 400. Rama `feat/` o `fix/` con el id.
3. Parar en T2 y T5. T2 solo se opera si el Operador delegó por escrito ese ticket, con revisión y CLI allowlisted. T5 no lo abre un agente.
4. No citar artículos de ley que no estén ya en el registry o en el derivado que el ticket lee. No promulgar.
5. DoD local: los checks del contrato. `an_kla verify` solo si se tocó memoria. Este plan no pide writes AN-KLA.
6. Al cerrar H1 o H2 hace falta ronda de alto impacto (≥3 proveedores por modelo, autor excluido). Sin `proceed` no hay merge. H0 admite quórum-lite.
7. No declarar CI verde. Pegar el resultado local y, si se consulta GitHub, el id del run.

Las autorizaciones históricas de los puntos 8 y 9 se aplican a un ticket de este plan solo después de una adopción que identifique la revisión y el alcance. La instrucción del Operador del 2026-10-05 adoptó T0 sobre el texto publicado en `aa7f06a`. Una instrucción posterior del mismo día adopta, sobre esa revisión, la implementación en rama de T1, T1b y T3, sin merge de H1/H2 y sin T4, T2 ni T5. Un ticket fuera de ese alcance no queda habilitado. Una excepción posterior tiene que nombrar la revisión y el ticket. Editar este borrador, o aceptar un análisis, no adopta el ticket.

8. **Commit y push autorizados** (instrucción humana del 2026-10-05, posterior a la ronda; no cambia el quórum). Sujeto al párrafo de adopción anterior. Cuando hay avance relevante, el agente no vuelve a pedir permiso para `git commit` ni para `git push` de la rama del ticket. Avance relevante quiere decir: el DoD de ese ticket está verde en local, o hay un corte coherente ya verificado (tests del contrato en verde, diff < 400, sin secretos ni transcripts).
9. Sujeto al mismo párrafo. El merge a `main` de H0 entra en esa autorización. El merge a `main` de H1 o H2 sigue exigiendo `proceed` de alto impacto. T2 y T5 no los commitea un agente. Nada de `--force`, nada de datos que el contrato no nombre.

Instrucción del Operador posterior a `d5aea67`: separar implementación, experimento y adjudicación. T2 permanece como corrida manual con protocolo previo y predicciones conservadas; la operación por un agente requiere delegación expresa. T5 registra el panel Grok / Codex / OpenCode y la matriz de autoría de `5f94d38`. Ese registro no enmienda la allowlist ni cierra H1/H2. El apartado «Baseline observado» es histórico.

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
