# Plan R1 — 90 días: verdad jurídica + auditor usable

**Contexto:** análisis crítico 2026-08-10: gobernanza fuerte, cadena DOF abierta,
sin auditor de documento, roles §9 vacíos. **Fecha:** 2026-08-10.  
**Estado:** borrador (listo para ejecución por agentes). **Roadmap:** R1.  
**Fuente:** análisis de sesión + ADR-0001 + `docs/ops-github.md` + memoria AN-KLA.  
**Ejecutores:** agentes de IA + admin humano (CODEOWNERS). **No es** promulgación
normativa ni asesoría legal.

## Objetivo y criterio de cierre global

**Objetivo:** en ~90 días, (1) al menos una disposición del slice salud con
**vigencia DOF nivel 1**, (2) roles §9 designados (aunque interinos con fecha),
(3) un **auditor de documento** medible (citas + `verify_claim` + matriz FP/FN),
(4) higiene de planes/ADR, (5) camino claro a IMSS **público** sin romper §7.4,
(6) reanudación de Actions cuando haya presupuesto.

**Cierre global (verificable):**

| KPI | Meta R1 |
|-----|---------|
| `vigencia_verificada: true` en registry (slice) | ≥1 disposición, ideal 2 (CPEUM:4:P4 + LGS:1) |
| Roles §9 en doc firmado por humano | 3/3 (jurídico, custodio, PO) con fecha |
| CLI auditor + 1 doc piloto + matriz FP/FN | existe, tests, doc < límites §3 |
| ADR-0001 | aceptado / superado / rechazado (no “propuesta” eterna) |
| `plan-r0.md` | marcado cerrado u obsoleto |
| CI remoto | humo verde **o** régimen DoD local vigente documentado |
| Golden recall LLM (v1.2) | al menos diseño + 1 fixture; ideal suite mínima |

Sin roles + sin DOF, el resto se etiqueta `PARCIAL (espera-humano)` y **no** se
promete “auditoría confiable” al exterior.

---

## Reglas de ejecución para agentes de IA (OBLIGATORIO)

1. **Leer antes de actuar:** `AGENTS.md` → este plan → contrato del ticket →
   `docs/politica-agentes.md` (solo secciones citadas). Presupuesto lectura ≤ ~30k
   tokens; preferir `grep` + `offset`.
2. **1 ticket = 1 PR = 1 contrato.** Diff ideal < 400 líneas. Rama corta
   `feat|fix|docs|chore|test/<ticket-id>`.
3. **DoD = checks ejecutables.** Si no hay check, el ticket no se abre.
4. **Git:** agente propone; **admin** mergea. Nunca `--force` a `main`. Mientras
   Actions esté en billing: DoD **local** + declarar `CI remoto: SUSPENDIDO
   (billing)` (`docs/ops-github.md`). No fingir CI verde.
5. **Fidelidad §7:** toda afirmación normativa cita fuente; si no hay DOF,
   `[VIGENCIA-NO-VERIFICADA]`. Redactar ≠ promulgar.
6. **Datos §7.4:** no enviar internos/confidenciales a proveedores. Router
   deniega interno en v1. Contenido IMSS interno = **bloqueado** hasta tickets
   de autorización.
7. **AN-KLA:** solo facts con valor no derivable + `indexable_text`; puntero a
   doc, no copia verbatim. Preferir `supersede` si hay id estable (beta.11).
8. **Adversarial:** al cerrar cada **hito** (no cada ticket). Menor = quorum-lite;
   alto impacto = ≥3 proveedores (política §6). Sin `proceed` no merge del hito.
9. **Checkpoint** si se agota contexto: `checkpoint-<ticket-id>.md` + parar.
10. **No implementar tickets `HUMAN`** ni los bloqueados por dependencia abierta.
11. **Anti-roadmap R1 (no abrir tickets):** bitemporalidad plena, operadores
    deónticos, jurisprudencia como subsistema, “leyes como código”, ampliar
    corpus a decenas de leyes nivel 2, rondas adversarial de infra sin dominio.

### Convención de IDs

- Formato: `R1-E{epic}-{nn}` (ej. `R1-E1-02`).
- Prioridad: `P0` (bloquea valor) · `P1` · `P2` · `P3`.
- Actor: `AGENT` · `ADMIN` · `HUMAN` · `AGENT+ADMIN`.
- Tamaño: `S` (1 sesión) · `M` (1–2) · `L` (dividir si >L).

### Comandos DoD base (casi todo PR)

```bash
python -m py_compile corpus/*.py scripts/*.py review_routing/*.py 2>/dev/null || true
python -m unittest discover -s tests -q
python scripts/check_sizes.py
# si tocó memoria/contexto:
.venv/bin/python -m an_kla --project-root . verify
```

---

## Hitos (cada uno → ronda adversarial)

| Hito | Criterio de cierre | Impacto adversarial | Depende |
|------|--------------------|---------------------|---------|
| **H0** | Roles §9 designados + decisiones humanas mínimas registradas | menor (doc humano) | — |
| **H1** | ≥1 disposición slice con vigencia DOF verificada en registry + tests | **alto** (§7/corpus) | H0 parcial OK si humano autoriza DOF |
| **H2** | Higiene: plan-r0 cerrado, ADR-0001 decisión, estado AGENTS coherente | menor | — |
| **H3** | Auditor CLI + doc piloto + matriz FP/FN (citas pre-etiquetadas) | menor→alto si promete métricas externas | H1 recomendado |
| **H4** | Recall extracción v1.2: diseño + fixtures + tests de contrato | alto (eval/compuerta) | H3 |
| **H5** | Eje IMSS **público**: LOAPF/LFEP/RI ingeridos nivel fuente + lookup smoke | alto (corpus) | H0, H1; auth datos |
| **H6** | Actions vivo + humo CI + (opcional) branch protection | menor | billing |
| **H7** | Router harness (egress/log/bundle) — solo si H5 interno se acerca | alto (§7.4) | H5 path |

Orden de olas recomendado: **H0 ∥ H2 → H1 → H3 → H4**; **H6** cuando billing;
**H5** tras H1; **H7** solo si hace falta.

```text
H0 (roles) ──┬──► H1 (DOF) ──► H3 (auditor) ──► H4 (recall LLM)
H2 (higiene)─┘         │
                       └──► H5 (IMSS público) ──► H7 (harness) [opcional]
H6 (Actions) ── independiente cuando haya presupuesto
```

---

## Epic E0 — Decisiones humanas y roles (§9) · H0

> Sin esto el agente no puede “cerrar” confianza. Tickets HUMAN no se automatizan.

### R1-E0-01 · Designar roles §9 · P0 · HUMAN · S

**Salida:** párrafo en `docs/politica-agentes.md` §9 o `docs/roles-r1.md` (<150 L)
con: nombre/handle, rol (jurídico | custodio | PO), vigencia desde/hasta, interino
sí/no.  
**DoD:**

- [ ] Archivo existe y lista 3 roles (aunque sea la misma persona interina)
- [ ] Fecha límite de designación formal si son interinos
- [ ] Commit humano o PR firmado/merge admin
- [ ] Fact AN-KLA puntero (AGENT tras merge): `roles-r1-designados-<fecha>`

**Git:** `docs/roles-r1.md` o enmienda §9. **Adv:** quorum-lite al merge.

### R1-E0-02 · Autorizar canal DOF + multi-provider público · P0 · HUMAN · S

**Salida:** nota en `docs/ops-github.md` o `docs/fuentes-legal-mx.md` (si se crea):
autorización para (a) descargar/consultar DOF nivel 1 del slice, (b) rutear **solo
textos públicos** a proveedores del quórum.  
**DoD:**

- [ ] Autorización explícita (quién, qué, hasta cuándo)
- [ ] Lista de proveedores permitidos / prohibidos
- [ ] Interno IMSS: **no autorizado** por defecto

**Bloquea:** R1-E1-*, partes de H5.

### R1-E0-03 · Umbral FP del auditor (exploratorio) · P1 · HUMAN · S

**Salida:** 3–5 líneas en plan o `docs/adr/` lite: umbral FP aceptable para piloto
interno (ej. “exploratorio, no publicar al exterior hasta FP&lt;X en N citas”).  
**DoD:** [ ] Número o regla cualitativa firmada por PO/jurídico.  
**Bloquea:** promesas externas en H3/H4.

### R1-E0-04 · Decisión OSS leyes MX · P2 · HUMAN · S

**Salida:** sí/no a semillas `lex-mx` / similares + razón licencia/procedencia.  
**DoD:** [ ] ADR-lite o sección en corpus-inicial. Default si empty: **no usar** OSS.

---

## Epic E1 — Vigencia DOF nivel 1 (slice salud) · H1

### R1-E1-01 · Procedimiento de procedencia DOF (doc) · P0 · AGENT · S · Dep: E0-02

**Entradas:** `corpus/registry.yaml`, política §7.  
**Salida:** `docs/fuentes-legal-mx.md` (<800 L artefacto o <1500 doc_ref si no
`plan-`/`contrato`) con: niveles 1–4, cómo registrar permalink DOF, hash, fecha
reforma, fecha consulta, regla no-copia-verbatim.  
**DoD:**

- [ ] Archivo existe; cada regla normativa cita fuente o se marca metodología
- [ ] `check_sizes` OK
- [ ] No afirma vigencia de un artículo concreto sin evidencia

**Git:** `docs/fuentes-legal-mx.md`. **Adv:** con H1.

### R1-E1-02 · Ingerir evidencia DOF CPEUM Art.4 slice · P0 · AGENT+ADMIN · M · Dep: E0-02, E1-01

**Salida:** actualización `corpus/registry.yaml` (CPEUM): `url_dof_nivel1`,
`vigencia_verificada: true` **solo si** evidencia real; notas de reforma; hash
recomputable si hay PDF/nivel1 local. Posible `docs/fuentes/cpeum/` nota de
consulta (sin copiar ley entera si no hace falta).  
**DoD:**

- [ ] `vigencia_verificada: true` **únicamente** con URL/identificador DOF y fecha
- [ ] Si duda: dejar `false` + `[VIGENCIA-NO-VERIFICADA]` — **no inventar**
- [ ] sha256 de archivo local coincide si `originals/` presente
- [ ] Test o check script: registry parseable; flag documentado
- [ ] DoD base tests verdes

**Git:** `fix(corpus): vigencia DOF CPEUM slice` / `docs(corpus): …`.  
**Nota agente:** si no hay acceso DOF en entorno, **PARCIAL** + checklist para admin
(descarga manual path). No marcar true.

### R1-E1-03 · Ingerir evidencia DOF LGS Art.1 · P0 · AGENT+ADMIN · M · Dep: E1-02 patrón

Igual que E1-02 para LGS.  
**DoD:** análogo LGS. Preferir mismo PR solo si diff &lt;400; si no, PR separado.

### R1-E1-04 · Tests de no-regresión de vigencia · P0 · AGENT · S · Dep: E1-02

**Salida:** `tests/test_registry_vigencia.py` (&lt;80 L).  
**DoD:**

- [ ] Falla si `vigencia_verificada` true sin `url_dof_nivel1` (o campo canónico doc)
- [ ] Pasa con registry actual
- [ ] `unittest discover` verde; tamaños OK

### R1-E1-05 · Gate v1.1 — ¿habilitar `alto`? (diseño) · P1 · AGENT · S · Dep: E1-02, E0-01

**Salida:** propuesta corta `docs/propuestas/gate-v1.1-alto-diseno.md` (&lt;150 L):
criterios legales+técnicos para `alto`; **default recomendado:** no habilitar hasta
jurídico firme.  
**DoD:** [ ] Doc existe; no cambia código sin ticket de implementación.  
**Implementación código** = ticket futuro tras HUMAN accept.

### R1-E1-06 · Ronda adversarial H1 · P0 · AGENT (multi) · M · Dep: E1-02..04

**Salida:** `docs/propuestas/r1-h1-dof-round/` (RONDA + reviews).  
**DoD:** [ ] ≥3 proveedores si se tocó corpus/vigencia; `proceed` antes de merge final
del hito; BLOCKER = no merge.

---

## Epic E2 — Higiene de verdad operativa · H2

### R1-E2-01 · Cerrar plan-r0 · P1 · AGENT · S

**Salida:** encabezado `plan-r0.md`: **Estado: cerrado/histórico**; checklist T*
actualizado; puntero a este plan R1.  
**DoD:** [ ] No contradice `main` actual; tamaños OK; sin borrar historia.

### R1-E2-02 · Decisión formal ADR-0001 · P0 · HUMAN+AGENT · S

**HUMAN** elige: aceptar / aceptar-con-condiciones / rechazar.  
**AGENT** actualiza estado del ADR + enlace a evidencia.  
**DoD:** [ ] Campo `Estado:` ≠ solo “Propuesta” sin fecha de revisión; commit en main.

### R1-E2-03 · ADR-0002 firma agentes — siguiente paso · P2 · AGENT · S · Dep: HUMAN GPG

**Salida:** checklist en ADR-0002 (clave GPG humana, require signed commits).  
**DoD:** [ ] No activar require-signed si humano no tiene clave; doc listo.

### R1-E2-04 · Sincronizar AGENTS estado · P1 · AGENT · S · Dep: merges recientes

**Salida:** bloque “Estado actual” / PRÓXIMA TAREA alineado a `main` + AN-KLA
`status` + este plan.  
**DoD:** [ ] `context status` OK; always-on &lt;300; sin editar bloque managed a mano.

### R1-E2-05 · Índice de docs vigentes · P2 · AGENT · S

**Salida:** sección corta en `docs/plantillas-agente.md` o `docs/README.md` (&lt;80 L):
qué es vigente (política, ops-github, plan-r1) vs archivo (`propuestas/`).  
**DoD:** [ ] Un agente nuevo encuentra el plan R1 en &lt;1 min de lectura de AGENTS.

### R1-E2-06 · Adversarial H2 · P1 · AGENT · S · quorum-lite

**DoD:** [ ] proceed sobre docs de higiene.

---

## Epic E3 — Auditor de documento (MVP honesto) · H3

### R1-E3-01 · Contrato de interfaz del auditor · P0 · AGENT · S

**Salida:** `docs/propuestas/auditor-v0-contrato.md` (&lt;120 L): CLI,
entrada/salida JSON schema (campos), niveles gate, no-LLM en v0.  
**DoD:** [ ] Schema de salida con `disposicion_id`, `cita`, `nivel`, `reasons`;
límites tamaño.

### R1-E3-02 · Fixture documento piloto (citas pre-etiquetadas) · P0 · AGENT · S · Dep: E3-01

**Salida:** `tests/fixtures/piloto-salud-citas.json` + opcional
`docs/fuentes/.../piloto.md` sintético **no normativo** o extractos ya en corpus
con citas alineadas a `CPEUM:4:P4` / `LGS` id real.  
**DoD:**

- [ ] Fixture solo usa ids que existen en lookup
- [ ] Sin afirmar derecho vigente sin marca de verificación
- [ ] &lt;200 L total fixtures

### R1-E3-03 · Implementar `scripts/audit_document.py` (v0 sin LLM) · P0 · AGENT · M · Dep: E3-01, E3-02

**Comportamiento:** lee claims JSON → llama `verify_claim` → imprime reporte JSON
+ exit code según peor nivel (o política documentada).  
**DoD:**

- [ ] Archivo &lt;200 L (si crece, partir módulo)
- [ ] `python scripts/audit_document.py tests/fixtures/...` produce JSON válido
- [ ] Tests `tests/test_audit_document.py` ≥5 casos (medio/bajo/missing id)
- [ ] DoD base + sizes OK
- [ ] No usa red ni LLM

**Git:** `feat(audit): auditor v0 citas preetiquetadas`.

### R1-E3-04 · Matriz FP/FN humana (plantilla + primera pasada) · P1 · AGENT+HUMAN · M · Dep: E3-03

**Salida:** `docs/propuestas/auditor-v0-matriz-fpfn.md` plantilla; humano rellena
primera fila de veredictos.  
**DoD:** [ ] Plantilla con columnas cita / nivel sistema / nivel humano / FP|FN|TP|TN;
al menos N=1 pasada humana **o** ticket PARCIAL espera-humano.

### R1-E3-05 · Adversarial H3 · P0 · AGENT · S–M

Quorum-lite si solo CLI interno; **alto** si el PR publicita métricas al exterior.  
**DoD:** [ ] proceed.

---

## Epic E4 — Recall extracción LLM (v1.2) · H4

### R1-E4-01 · Diseño golden set extracción · P0 · AGENT · S · Dep: E3-03

**Salida:** `docs/propuestas/recall-extraccion-v12.md` (&lt;150 L): formato gold
(spans/citas), métricas (recall/precision a nivel cita), proveedores, **router
§7.4** (solo público), semilla reproducible.  
**DoD:** [ ] No ejecuta LLM aún; contrato de datos claro.

### R1-E4-02 · Fixtures gold (mínimo 3 docs sintéticos públicos) · P0 · AGENT · M · Dep: E4-01

**Salida:** `tests/fixtures/extraction_gold/*.json`.  
**DoD:** [ ] ≥3 fixtures; ids corpus válidos; tests de schema cargan OK.

### R1-E4-03 · Harness eval offline (sin red en CI) · P1 · AGENT · M · Dep: E4-02

**Salida:** `scripts/eval_extraction.py` + tests con **extractor fake** determinista
(para CI) + interfaz para extractor real (plugin).  
**DoD:**

- [ ] CI/local sin API keys: fake extractor → métricas deterministas
- [ ] Documentado cómo correr con CLI real **offline manual**
- [ ] No subir secretos; no loguear textos internos

### R1-E4-04 · Adversarial H4 · P0 · AGENT · multi · Dep: E4-01..03

**DoD:** [ ] proceed; ≥3 proveedores (cambia compuerta de evaluación).

---

## Epic E5 — Eje IMSS público (estructura OPD) · H5

### R1-E5-01 · Alcance público vs interno (matriz) · P0 · AGENT · S · Dep: E0-01, E0-02

**Salida:** `docs/propuestas/imss-alcance-publico.md` (&lt;100 L): LOAPF, LFEP,
Reglamento Interior IMSS = ¿público? rutas; **manuales internos = fuera**.  
**DoD:** [ ] Cada instrumento con clasificación y fuente URL pública o “no ingerir”.

### R1-E5-02 · Registry + descarga LOAPF (si público autorizado) · P1 · AGENT+ADMIN · M · Dep: E5-01, E1-01

**DoD:** [ ] Entrada registry nivel 2/1; hash; `vigencia_verificada` acorde verdad;
original local gitignored; **sin** claims normativos sin marca.

### R1-E5-03 · Registry LFEP · P1 · AGENT+ADMIN · M · Dep: E5-02 patrón

Análogo E5-02.

### R1-E5-04 · Registry Reglamento Interior IMSS (público) · P1 · AGENT+ADMIN · M · Dep: E5-03

Análogo; si no hay consolidado confiable → PARCIAL + no forzar.

### R1-E5-05 · Slice lookup: 1 disposición por instrumento · P1 · AGENT · M · Dep: E5-02..04

**Salida:** JSON derived mínimos + tests lookup.  
**DoD:** [ ] ids estables; golden tests; sizes; sin inventar texto (extraer de
fuente con hash).

### R1-E5-06 · Adversarial H5 · P0 · AGENT · multi

**DoD:** [ ] proceed corpus.

---

## Epic E6 — GitHub Actions y protección · H6

### R1-E6-01 · Detectar Actions vivo · P1 · ADMIN/AGENT · S · Dep: billing

**DoD:** [ ] Checklist `ops-github.md` §5.1 documentado en issue/PR comment con
evidencia (run id, duración).

### R1-E6-02 · PR humo CI · P1 · AGENT+ADMIN · S · Dep: E6-01

**DoD:** [ ] Check “Tests + gate de tamaño” = success en GitHub.

### R1-E6-03 · Branch protection main · P2 · ADMIN · S · Dep: E6-02

**DoD:** [ ] Protection según `ops-github.md` §5.3; **no** si E6-02 falla.  
**Emergencia:** DELETE protection si billing vuelve a caer (§5.5).

### R1-E6-04 · Cerrar modo DoD-local en docs + supersede fact · P1 · AGENT · S · Dep: E6-02

**DoD:** [ ] `ops-github.md` estado actualizado; AN-KLA supersede fact billing;
AGENTS sin “suspendido” eterno.

### R1-E6-05 · Adversarial H6 · P2 · AGENT · quorum-lite

---

## Epic E7 — Router harness (condicional) · H7

> Solo si se acerca material interno o se exige sandbox real.

### R1-E7-01 · Diseño harness egress/log/bundle · P2 · AGENT · S

**Salida:** doc &lt;150 L; no código de exploits; fail-closed.  
**DoD:** [ ] Lista de controles; fuera de alcance explícito.

### R1-E7-02 · Log append-only path + tests · P2 · AGENT · M · Dep: E7-01, HUMAN auth

### R1-E7-03 · Bundle sellado de review · P2 · AGENT · M · Dep: E7-02

### R1-E7-04 · Adversarial H7 · P1 · multi · Dep: E7-02..03

---

## Epic E8 — Memoria y continuidad (transversal)

### R1-E8-01 · Fact puntero plan R1 · P1 · AGENT · S

**DoD:** [ ] Fact `plan-r1-90d-2026-08-10` con `indexable_text` + puntero a este
archivo; `committed: true`.

### R1-E8-02 · Al cierre de cada hito: fact estado · P1 · AGENT · S

**DoD:** [ ] Un fact resumen hito (o supersede estado anterior); sin volcar reviews
verbatim a memoria.

### R1-E8-03 · Limpieza facts stale opcionales · P3 · AGENT · S

Usar `supersede` donde haya ids viejos contradictorios (además del alfa ya hecho).

---

## Backlog de tickets (cola para agentes)

Orden de despacho sugerido (saltar `HUMAN` / deps abiertas):

| Orden | ID | Epic | Actor | Pri |
|------:|----|------|-------|-----|
| 1 | R1-E8-01 | E8 | AGENT | P1 |
| 2 | R1-E2-01 | E2 | AGENT | P1 |
| 3 | R1-E2-05 | E2 | AGENT | P2 |
| 4 | R1-E2-04 | E2 | AGENT | P1 |
| 5 | R1-E0-01 | E0 | **HUMAN** | P0 |
| 6 | R1-E0-02 | E0 | **HUMAN** | P0 |
| 7 | R1-E1-01 | E1 | AGENT | P0 |
| 8 | R1-E1-02 | E1 | AGENT+ADMIN | P0 |
| 9 | R1-E1-03 | E1 | AGENT+ADMIN | P0 |
| 10 | R1-E1-04 | E1 | AGENT | P0 |
| 11 | R1-E1-06 | E1 | AGENT multi | P0 |
| 12 | R1-E2-02 | E2 | HUMAN+AGENT | P0 |
| 13 | R1-E3-01 | E3 | AGENT | P0 |
| 14 | R1-E3-02 | E3 | AGENT | P0 |
| 15 | R1-E3-03 | E3 | AGENT | P0 |
| 16 | R1-E3-04 | E3 | AGENT+HUMAN | P1 |
| 17 | R1-E3-05 | E3 | AGENT | P0 |
| 18 | R1-E0-03 | E0 | HUMAN | P1 |
| 19 | R1-E4-01 | E4 | AGENT | P0 |
| 20 | R1-E4-02 | E4 | AGENT | P0 |
| 21 | R1-E4-03 | E4 | AGENT | P1 |
| 22 | R1-E4-04 | E4 | AGENT multi | P0 |
| 23 | R1-E5-01 | E5 | AGENT | P0 |
| 24 | R1-E5-02..05 | E5 | AGENT+ADMIN | P1 |
| 25 | R1-E5-06 | E5 | multi | P0 |
| 26 | R1-E6-* | E6 | cuando billing | P1 |
| 27 | R1-E7-* | E7 | condicional | P2 |
| 28 | R1-E1-05 | E1 | AGENT | P1 |
| 29 | R1-E0-04 | E0 | HUMAN | P2 |

---

## Plantilla de ticket (copiar al abrir trabajo)

```markdown
## Ticket R1-Ex-yy — <título>

**Estado:** pending|in_progress|blocked|done|parcial
**Actor:** AGENT|ADMIN|HUMAN|AGENT+ADMIN
**Pri:** P0|P1|P2|P3 · **Tamaño:** S|M · **Deps:** <ids|none>
**Hito:** Hn · **Adv al cierre hito:** lite|multi

### Contexto (≤5 líneas)
### Entradas (paths)
### Salidas (paths + límite líneas)
### DoD (checks)
- [ ] unittest / check_sizes / …
- [ ] …
### Fuera de alcance
### Git propuesto
- Rama: `feat/R1-Ex-yy-...`
- Commit: `type(scope): ...`
### Bloqueos / espera-humano
### Reanudar: este ticket + AGENTS.md + plan-r1-90d.md §ticket
```

---

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Agente marca `vigencia_verificada: true` sin DOF | DoD E1-04 + adversarial H1 + política §7 |
| Solo meta-infra otra semana | Cola: tras E8-01/E2, **no** abrir E7 antes de E1/E3 |
| Material IMSS a cloud | E0-02 + E5-01; router deniega interno |
| Context overflow | 1 ticket/PR; checkpoint; plan on-demand |
| CI billing | ops-github; no protection prematura |
| Quórum multi-provider frágil | Preferir claude+codex+tercero; si &lt;3 → PARCIAL |
| plan-r0 confunde agentes | E2-01 primero |

---

## Reporte de fin de ticket (mínimo al orquestador)

```markdown
> Estado: OK|PARCIAL|BLOQ · Ticket: R1-… · Modelo: … · Fecha: …
Resumen: …
DoD: [lista checks + evidencia 1 línea]
Git: rama/PR · CI: verde|SUSPENDIDO billing
AN-KLA: rev N / fact ids
Siguiente ticket en cola: …
```

---

## Enlaces

- Política: `docs/politica-agentes.md` (§3 tamaños, §5 git, §6 adv, §7 fidelidad, §9 roles)
- Ops CI: `docs/ops-github.md`
- ADR: `docs/adr/0001-*`, `0002-*`
- Código: `corpus/`, `review_routing/`, `tests/`
- Memoria: `retrieve --query "plan R1 DOF auditor IMSS" --budget 6000`

---

## Changelog del plan

| Fecha | Cambio |
|-------|--------|
| 2026-08-10 | Creación R1 90d desde análisis crítico; tickets E0–E8 |
