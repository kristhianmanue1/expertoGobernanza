# Plan R1 — 90 días: verdad jurídica + auditor usable

**Contexto:** análisis crítico 2026-08-10: gobernanza fuerte, cadena DOF abierta,
sin auditor de documento. **Fecha:** 2026-08-10.  
**Estado:** **en-curso** (E0 + E1-01 + fix adversarial pre-E1 aplicados).  
**Roadmap:** R1. **Fuente:** plan + `docs/fuentes-legal-mx.md` + ronda
`docs/propuestas/r1-plan-adversarial-pre-e1/RONDA.md`.  
**Ejecutores:** agentes de IA + admin humano (CODEOWNERS). **No es** promulgación
normativa ni asesoría legal.

## Objetivo y criterio de cierre global

**Objetivo:** en ~90 días, (1) al menos una **disposición** del slice salud con
**traza primaria DOF de alcance que la cubra** (no solo reforma del cuerpo),
(2) roles §9 designados, (3) auditor de documento medible con banner si corpus
no verificado, (4) higiene planes/ADR, (5) IMSS **público** sin romper §7.4,
(6) reanudación Actions cuando haya presupuesto.

**Cierre global (verificable):**

| KPI | Meta R1 |
|-----|---------|
| Vigencia slice | **HECHO 2026-08-10:** CPEUM:4:P4 + LGS:1 con `true`, traza alcance + F5 (Jiménez) |
| Roles §9 | 3/3 en `docs/roles-r1.md` (interinos OK con fecha) |
| CLI auditor + piloto + matriz FP/FN | existe; salida con banner si vigencia slice false |
| ADR-0001 | aceptado / superado / rechazado |
| `plan-r0.md` | cerrado/histórico |
| CI remoto | humo verde **o** DoD local documentado |
| Golden recall LLM | diseño + ≥1 fixture (ideal suite) |

**Tickets cerrados (changelog):** E0-01, E0-02, E0-03 diferido, E1-01, E1-05 diseño,
fix adversarial F1–F7 (docs 2026-08-10).  

Sin traza de **alcance** al slice, **no** se promete “auditoría confiable” al exterior.

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

### R1-E0-01 · Designar roles §9 · P0 · HUMAN · S · **HECHO 2026-08-10**

**Salida:** `docs/roles-r1.md` — Kristhian Manuel Jiménez **interino** en los tres
roles (jurídico, custodio, PO); revisión interinato 2026-11-10.  
**DoD:**

- [x] Archivo existe y lista 3 roles
- [x] Fecha límite de designación formal / revisión de interinato
- [x] Merge a main (admin)
- [x] Fact AN-KLA puntero (AGENT): `roles-r1-designados-2026-08-10`

**Git:** `docs/roles-r1.md`. **Adv:** quorum-lite al merge del paquete E0.

### R1-E0-02 · Autorizar canal DOF + multi-provider público · P0 · HUMAN · S · **HECHO 2026-08-10**

**Salida:** `docs/autorizacion-fuentes-r1.md` — canales
https://dof.gob.mx/ y https://www.ordenjuridico.gob.mx/ para **analizar**;
multi-provider **solo** textos públicos; interno IMSS no autorizado.  
**DoD:**

- [x] Autorización explícita (quién, qué, canales)
- [x] Lista permitido / prohibido (multi-provider + interno)
- [x] Interno IMSS: **no autorizado** por defecto
- [ ] Recordar: no implica `vigencia_verificada: true` automático (E1)

**Bloquea (levantado para abrir E1):** R1-E1-* puede arrancar; cada vigencia
sigue requiriendo evidencia por instrumento.

### R1-E0-03 · Umbral FP del auditor (exploratorio) · P1 · HUMAN · S · **DIFERIDO**

**Decisión 2026-08-10 (PO interino):** idea **aceptada**, umbral numérico **cuando
existan trabajos del auditor** (post H3 / matriz FP/FN), no antes.  
**Salida provisional:** §3 de `docs/autorizacion-fuentes-r1.md`.  
**DoD (cuando se reactive):** [ ] Número o regla cualitativa firmada.  
**Bloquea aún:** promesas externas de calidad del auditor en H3/H4.

### R1-E0-04 · Decisión OSS leyes MX · P2 · HUMAN · S

**Salida:** sí/no a semillas `lex-mx` / similares + razón licencia/procedencia.  
**DoD:** [ ] ADR-lite o sección en corpus-inicial. Default si empty: **no usar** OSS.

### R1-E0-05 · Doble control vigencia (F5) · P0 · HUMAN+AGENT · S · **DOC HECHO**

**Salida:** control en `docs/roles-r1.md` + campos `revision_vigencia` en
metodología.  
**DoD operativo en cada PR de `vigencia_verificada: true`:**

- [ ] `revision_vigencia` rellenado por humano
- [ ] multi-provider en H1 **o** `auto_revision_declarada: true` explícito

---

## Epic E1 — Vigencia DOF nivel 1 (slice salud) · H1

### R1-E1-01 · Procedimiento de procedencia DOF (doc) · P0 · AGENT · S · Dep: E0-02 · **HECHO 2026-08-10**

**Entradas:** `corpus/registry.yaml`, política §7, auth E0-02.  
**Salida:** `docs/fuentes-legal-mx.md` (niveles 1–4, tipo→primaria→secundaria,
campos registry, procedimiento A–F, multi-eje, visión vigilancia DOF) +
`docs/propuestas/gate-confianza-multieje-v1.md` + comentarios en registry.  
**DoD:**

- [x] Archivo metodología existe; sin afirmar vigencia de artículo concreto
- [x] `check_sizes` OK
- [x] Auth y plan enlazan a la metodología

**Git:** `docs/fuentes-legal-mx.md`. **Adv:** con H1 (al cerrar E1-02..04).

### R1-E1-02 · Ingerir evidencia DOF CPEUM Art.4 slice · P0 · **HECHO H1 2026-08-10**

**Salida:** `vigencia_verificada: true`; traza principal DOF 08-05-2020
`codigo=5593045` cubre `CPEUM:4:P4`; F5 Jiménez; 2026-06-02 `no_cubre_slice`.  
**DoD:** [x] Humano OK + registry + rules tests.

### R1-E1-03 · Ingerir evidencia DOF LGS Art.1 · P0 · **HECHO H1 2026-08-10**

**Salida:** `vigencia_verificada: true`; traza principal DOF 29-05-2023 cubre
`LGS:1` (lectura F5 vía acervo Cámara del decreto); 1984=nacimiento; 2026-01-15
`no_cubre_slice`.  
**DoD:** [x] Humano OK + registry + rules tests.

### R1-E1-04 · Tests de no-regresión de vigencia · P0 · AGENT · S · **HECHO 2026-08-10**

**Salida:** `corpus/registry_rules.py` + `tests/test_registry_vigencia.py`.  
**DoD:**

- [x] Falla si `true` sin traza/alcance/cover/revision (F2/F5)
- [x] Pasa registry actual (todo `false`; exploraciones con trazas candidatas OK)
- [x] `unittest discover` verde

### R1-E1-05 · Gate v1.1 — ¿habilitar `alto`? (diseño) · P1 · AGENT · S · **DISEÑO HECHO 2026-08-10**

**Salida:** `docs/propuestas/gate-confianza-multieje-v1.md` + §6 de
`fuentes-legal-mx.md`. **Default:** no habilitar `alto` en código hasta H1 +
aceptación jurídica.  
**DoD:** [x] Doc existe; no cambia código de gate aún.  
**Implementación código** = ticket futuro `feat(corpus): gate v1.1 multi-eje`.

### R1-E1-06 · Ronda adversarial H1 · P0 · AGENT (multi) · M · Dep: E1-02..04

**Salida:** `docs/propuestas/r1-h1-dof-round/` (RONDA + reviews).  
**DoD:** [ ] ≥3 proveedores si se tocó corpus/vigencia; `proceed` antes de merge final
del hito; BLOCKER = no merge.

---

## Epic E2 — Higiene de verdad operativa · H2

### R1-E2-01 · Cerrar plan-r0 · P1 · AGENT · S · **HECHO 2026-08-10**

**Salida:** `plan-r0.md` **CERRADO/HISTÓRICO** + puntero a plan-r1.  
**DoD:** [x] Encabezado cerrado; tamaños OK.

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

### R1-E2-05 · Índice de docs vigentes · P2 · AGENT · S · **HECHO 2026-08-10**

**Salida:** `docs/README.md` (mapa vigente vs histórico).  
**DoD:** [x] Archivo existe; enlaza plan-r1 y fuentes-legal-mx.

### R1-E2-06 · Adversarial H2 · P1 · AGENT · S · quorum-lite

**DoD:** [ ] proceed sobre docs de higiene.

---

## Epic E3 — Auditor de documento (MVP honesto) · H3

> **F6:** H3 puede avanzar en paralelo a H1, pero el CLI **debe** emitir banner
> `CORPUS_VIGENCIA_NO_VERIFICADA` (o equivalente) mientras el slice no tenga
> disposición con vigencia true + alcance. Prohibido marketing “confiable”.

### R1-E3-01 · Contrato de interfaz del auditor · P0 · AGENT · S · **HECHO 2026-08-10**

**Salida:** `docs/propuestas/auditor-v0-contrato.md` (banner F6 documentado).  
**DoD:** [x] Contrato con entrada/salida/exit codes.

### R1-E3-02 · Fixture documento piloto · P0 · AGENT · S · **HECHO 2026-08-10**

**Salida:** `tests/fixtures/piloto-salud-citas.json` (2 citas slice + 1 inventada).  
**DoD:** [x] Ids `CPEUM:4:P4` / `LGS:1`; sin pretender DOF verificado.

### R1-E3-03 · Implementar `scripts/audit_document.py` · P0 · AGENT · M · **HECHO 2026-08-10**

**DoD:**

- [x] CLI + banner `CORPUS_VIGENCIA_NO_VERIFICADA`
- [x] `tests/test_audit_document.py` (4 tests)
- [x] unittest suite verde; sizes OK; sin red/LLM

### R1-E3-04 · Matriz FP/FN · P1 · AGENT+HUMAN · M · **HECHO pasada-1 2026-08-10**

**Salida:** `docs/propuestas/auditor-v0-matriz-fpfn.md` (2 TP + 1 TN; N=3).  
**DoD:** [x] Plantilla + pasada 1; E0-03 umbral sigue diferido; sin marketing 100%.

### R1-E3-05 · Adversarial H3 · P0 · AGENT · S–M

Quorum-lite interno OK (CLI). Multi si se publicitan métricas.  
**DoD:** [ ] proceed formal opcional (pasada-1 ya documentada).

---

## Epic E4 — Recall extracción LLM (v1.2) · H4

### R1-E4-01 · Diseño golden set extracción · P0 · **HECHO 2026-08-10**

**Salida:** `docs/propuestas/recall-extraccion-v12.md`.  
**DoD:** [x] Formato gold, métricas, fake/CI, §7.4.

### R1-E4-02 · Fixtures gold · P0 · **HECHO 2026-08-10**

**Salida:** `tests/fixtures/extraction_gold/synth-0{1,2,3}.json`.  
**DoD:** [x] ≥3 fixtures; ids CPEUM:4:P4 / LGS:1.

### R1-E4-03 · Harness eval offline · P1 · **HECHO mínimo 2026-08-10**

**Salida:** `scripts/eval_extraction.py` + `tests/test_eval_extraction.py` (fake).  
**DoD:** [x] Sin red; fake perfect recall en gold; plugin real = futuro.

### R1-E4-04 · Adversarial H4 · P0 · AGENT · multi · Dep: E4-01..03

**DoD:** [ ] proceed multi cuando se conecte extractor real (fake no exige multi).

---

## Epic E5 — Eje IMSS público (estructura OPD) · H5

### R1-E5-01 · Alcance público vs interno (matriz) · P0 · **HECHO 2026-08-10**

**Salida:** `docs/propuestas/imss-alcance-publico.md` (matriz LOAPF/LFEP/LSS/RI/
manuales; cola E5-02+; no internos).  
**DoD:** [x] Clasificación + URLs índice + reglas router/auth.

### R1-E5-02 · Registry + descarga LOAPF · P1 · **HECHO exploración 2026-08-10**

**Salida:** LOAPF.pdf (local), registry, `LOAPF:1`, art-001.txt.  
**DoD:** [x] Hash `3edf486e…`; nivel 2; vigencia **false**; lookup+test.  
**Pendiente F5:** traza DOF con alcance para eventual `true`.

### R1-E5-03 · Registry LFEP · P1 · **HECHO exploración 2026-08-10**

**Salida:** LFEP.pdf (local), registry, `LFEP:1`, art-001.txt.  
**DoD:** [x] Hash `c0f203a9…`; nivel 2; vigencia **false**; lookup+test.  
**Pendiente F5:** traza DOF con alcance para eventual `true`.

### R1-E5-03b · Registry LSS (naturaleza IMSS) · P1 · **HECHO exploración 2026-08-10**

**Salida:** LSS.pdf, registry, `LSS:5` (OPD) + `LSS:1`, extractos.  
**DoD:** [x] Hash `8a28a16e…`; vigencia **false**; tests lookup.  
**Pendiente F5:** DOF Art.5 (2001-12-20 candidato) + cuerpo.

### R1-E5-04 · Registry Reglamento Interior IMSS (público) · P1 · AGENT+ADMIN · M · Dep: E5-03b

Solo si hay texto **público** (DOF/portal); si no → PARCIAL + no forzar.

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
| 2026-08-10 | Creación R1 90d; tickets E0–E8 |
| 2026-08-10 | E0-01/02 hechos; E0-03 diferido; E1-01 metodología |
| 2026-08-10 | Ronda adversarial pre-E1 → **fix-and-retry**; F1–F7 aplicados en docs |
| 2026-08-10 | Estado **en-curso**; KPI vigencia a nivel disposición+alcance; E0-05; E3 banner |
