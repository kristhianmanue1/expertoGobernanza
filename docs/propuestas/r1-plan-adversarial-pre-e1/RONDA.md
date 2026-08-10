# Adversarial — Plan R1 + metodología fuentes (pre E1-02/03)

**Fecha:** 2026-08-10  
**Alcance:** `docs/plan-r1-90d.md`, `docs/fuentes-legal-mx.md`,
`docs/propuestas/gate-confianza-multieje-v1.md`, `docs/roles-r1.md`,
`docs/autorizacion-fuentes-r1.md`, estado corpus `registry.yaml` (CPEUM/LGS).  
**No incluye:** implementación de traza DOF ya hecha (aún no existe).  
**Revisor:** ronda en contexto de análisis (un proveedor en esta pasada).  
**Quórum §6:** **PARCIAL / quorum-lite** — hito de alto impacto (compuertas de
fidelidad + plan de corpus). Para `proceed` formal de H1 se recomienda **re-ronda
≥3 proveedores** sobre el paquete corregido.  
**Lentes:** (L) lógica de producto/ingeniería · (J) fidelidad jurídica / técnica normativa.

## Decisión

- [ ] proceed
- [x] **fix-and-retry** → corregir hallazgos BLOCKER/HIGH listados antes de
      ejecutar E1-02/03 con `vigencia_verificada: true`
- [ ] escalate

**Regla práctica:** se puede seguir con **E2 higiene** y con **borradores de
búsqueda DOF** (`vigencia_verificada: false` + notas), pero **no** cerrar H1 ni
marcar vigencia true hasta absorber fixes F1–F6 (abajo).

---

## Hallazgos

### BLOCKER

#### B1 · (J+L) Confusión instrumento vs disposición vs texto de trabajo
**Problema:** El KPI de H1 habla de “disposición del slice” (`CPEUM:4:P4`), el
registry solo tiene booleano **por instrumento** (CPEUM/LGS), y el archivo de
trabajo es un **consolidado Cámara** completo. Marcar `vigencia_verificada: true`
en CPEUM **no** prueba que el párrafo de salud del Art. 4 esté anclado al acto
DOF correcto ni que el bytes del consolidado coincida con ese acto.  
**Evidencia:** `plan-r1-90d.md` KPI H1; `registry.yaml` campos a nivel `fuentes[]`;
`fuentes-legal-mx.md` §4–5 paso D (“consolidado OK si DOF ancla vigencia”).  
**Fix prescrito (F1):**
1. Definir **tres capas** en metodología + plan:
   - `instrumento` (CPEUM),
   - `disposicion` (`CPEUM:4:P4`),
   - `texto_trabajo` (hash del PDF/extracto).
2. KPI H1: vigencia verificada al menos a nivel **disposición del slice** (o
   “instrumento + nota explícita de que la traza cubre/no cubre el artículo”).
3. Prohibir `vigencia_verificada: true` solo por “última reforma del cuerpo
   entero” si la reforma no toca la disposición citada (ver B2).

#### B2 · (J) Error de categoría: última reforma del cuerpo ≠ vigencia del artículo
**Problema:** Registry ya anota `fecha_ultima_reforma_dof_declarada: 2026-06-02`
(Cámara: Poder Judicial…). Un agente puede enlazar ese DOF y “verificar”
CPEUM entero, **sin** que eso valide el texto del derecho a la salud (Art. 4).  
**Evidencia:** `registry.yaml` CPEUM notas 2026-06-02; slice = Art. 4 salud.  
**Fix prescrito (F2):**
1. Exigir traza de **cadena de reformas del artículo/párrafo** (o declaración
   explícita: “traza a nivel instrumento; disposición no reconciliada”).
2. Campos sugeridos: `trazas_publicacion[].alcance: instrumento|articulo|parrafo`
   + `cubre_disposiciones: [CPEUM:4:P4]` o `no_cubre_slice: true`.
3. Tests E1-04: si `vigencia_verificada: true` y hay slice MVP, exigir metadata
   de alcance o fallar.

---

### HIGH

#### H1 · (J) Booleano de vigencia subespecifica el derecho (vacatio, abrogación, transitorios)
**Problema:** `vigencia_verificada: true` sugiere “está vigente” sin fecha
jurídica, sin *vacatio legis*, sin transitorios, sin derogaciones parciales.  
**Evidencia:** `fuentes-legal-mx.md` §4 admite no-bitemporal; política §7.2 pide
confirmar no abrogada/transición.  
**Fix prescrito (F3):**
1. Renombrar semántica en docs a  
   `procedencia_primaria_reconciliada` **o** documentar glosa obligatoria:  
   “true = ancla DOF de trabajo reconciliada; **no** certifica aplicabilidad
   casuística ni ausencia de vacatio”.
2. Añadir `fecha_consulta_vigencia` y, si se conoce, `vacatio_o_transitorio: unknown|no|si+nota`.
3. En salidas del auditor/gate: nunca traducir `true` a “norma aplicable al caso”.

#### H2 · (L) Gate multi-eje puede dar falsa confianza (alto a nivel instrumento, match a nivel cita)
**Problema:** Diseño v1.1: `alto` si vigencia de instrumento true + match cita.
Puede haber match en consolidado desactualizado respecto del acto DOF enlazado.  
**Evidencia:** `gate-confianza-multieje-v1.md` reglas 3–4; paso D metodología.  
**Fix prescrito (F4):**
1. Eje B/D deben distinguir `nivel_archivo` vs `nivel_traza_vigencia`.
2. Regla: si `nivel_archivo >= 2` y no hay hash del **texto de la disposición**
   extraído/apoyado en primaria, techo **medio** aunque D true a nivel
   instrumento (o reason `texto_trabajo_no_primario`).
3. No implementar `alto` en código hasta F1+F2+F4.

#### H3 · (J+L) Separación de funciones rota (3 roles = 1 persona)
**Problema:** El mismo interino es jurídico, custodio y PO: autoriza canales,
desempata fuentes y prioriza. Choca con el espíritu CAGF-A5 (verificación no
solo introspectiva) aunque esté declarado.  
**Evidencia:** `roles-r1.md`.  
**Fix prescrito (F5):**
1. Documentar **control compensatorio** obligatorio en H1/H3:
   - checklist firmado (aunque sea el mismo humano) con fecha;
   - o quorum-lite **externo** (segundo modelo/revisor) antes de
     `vigencia_verificada: true` y antes de cualquier promesa exterior.
2. En plan: ticket `R1-E0-05` “doble control vigencia” (AGENT prepara, HUMAN
   marca casilla `revisado_por` distinta del autor del PR si es posible; si no,
   `auto_revision_declarada: true` + adversarial multi).

#### H4 · (L) H3 (auditor) no depende duro de H1
**Problema:** Grafo dice H1 “recomendado” antes de H3; un agente puede construir
auditor y matrices sobre corpus solo nivel 2 y generar sensación de producto.  
**Evidencia:** `plan-r1-90d.md` hitos H1/H3.  
**Fix prescrito (F6):**
1. H3 v0 puede existir, pero DoD debe exigir banner
   `CORPUS_VIGENCIA_NO_VERIFICADA` en salida del CLI mientras D false.
2. Prohibir en plan lenguaje de “auditor confiable” hasta H1 mínimo (ya en E0-03;
   reforzar en E3-01 contrato).

#### H5 · (J) Jerarquía normativa aún `[VERIFICAR-FUENTE]` en política
**Problema:** Plan asume desempates por jerarquía; la política §7.2 aún marca la
cita exacta de jerarquía como pendiente de verificar. Riesgo de que agentes
“desempaten” con doctrina no anclada.  
**Evidencia:** `politica-agentes.md` §7.2 párrafo jerarquía.  
**Fix prescrito (F7):** En R1, desempate **solo** por: (1) traza primaria vs no,
(2) fecha de acto, (3) decisión humana documentada — **no** por ensayo del agente
sobre lex superior sin fuente. Añadir a `fuentes-legal-mx.md`.

---

### MED

#### M1 · (L) `coherencia_multi_fuente` solo por fechas
No detecta textos distintos con la misma “última reforma”.  
**Fix:** documentar límite; opcional más tarde: hash de disposición entre fuentes.

#### M2 · (L) E1-04 tests solo estructurales
No validan que la URL DOF sea del acto correcto ni el alcance artículo.  
**Fix:** tras F1, tests de presencia de `alcance` / `cubre_disposiciones` si true.

#### M3 · (J) Fechas “declaradas por Cámara” en registry parecen hechos
Campos `fecha_ultima_reforma_dof_declarada` sin prefijo `claim_secundario_`.  
**Fix:** renombrar o prefijar en notas que son **claims nivel 2** hasta reconciliar.

#### M4 · (L) Plan sigue `Estado: borrador` con E0/E1-01 hechos
Agentes pueden dudar qué es ley del plan.  
**Fix:** `Estado: en-curso` + changelog de tickets cerrados al inicio.

#### M5 · (L) Auth multi-provider lista proveedores de forma vaga (“y otros ya usados”)
**Fix:** allowlist explícita de CLIs/modelos en `autorizacion-fuentes-r1.md`.

#### M6 · (J) Riesgo de redistribución / ToS de portales al versionar extractos
No bloquea R1 slice pequeño; sí al ampliar corpus.  
**Fix:** nota en metodología: extractos mínimos necesarios; no republicar DOF entero.

#### M7 · (L) Visión “vigilancia DOF” sin ticket acotado de no-metas
Puede distraer.  
**Fix:** mantener en anti-roadmap R1 (ya está espíritu); una línea “no abrir epic
vigilancia hasta cierre H3”.

#### M8 · (L) Falta criterio de “permalink usable” del DOF
URLs de búsqueda con sesión/query frágiles.  
**Fix:** aceptar `notas` con identificadores de diario (fecha, edición, decreto)
si no hay permalink; checklist de campos mínimos en E1-02.

---

### LOW

#### L1 · Duplicación metodología / auth / gate (tres docs)
Aceptable si hay un “read order”; añadir al plan: orden de lectura E1.

#### L2 · Nombre Jiménez vs Jimenez en historial de chat
Unificar grafía en docs.

#### L3 · ADR-0001 sigue propuesta mientras el plan lo asume
E2-02 sigue P0; no bloquear E1 pero sí narrativa de producto.

---

## Matriz fix → antes de qué

| Fix | Antes de… | Severidad |
|-----|-----------|-----------|
| F1 capas instrumento/disposición/texto | cualquier `vigencia_verificada: true` | BLOCKER |
| F2 alcance de traza (artículo/slice) | E1-02/03 cierre H1 | BLOCKER |
| F3 glosa semántica vigencia | promesas / gate alto | HIGH |
| F4 techo medio si texto no primario | implementar gate v1.1 alto | HIGH |
| F5 doble control / auto_revision | merge H1 | HIGH |
| F6 banner auditor si corpus no verificado | E3-03 | HIGH |
| F7 desempate sin jerarquía no citada | cualquier desempate agente | HIGH |
| M3–M5, M8 | calidad E1-02 | MED |

---

## Qué está bien (no romper)

- Separar canal autorizado vs verificación (E0-02).
- Nivel 2 Cámara/OJ vs nivel 1 DOF.
- `alto` inalcanzable en código v1 hasta evidencia.
- Anti-roadmap (bitemporalidad, leyes-como-código, scraper masivo).
- 1 ticket = 1 PR = DoD; DoD local bajo billing.
- Interno IMSS denegado por default.
- Umbral FP diferido hasta trabajo real (E0-03).

---

## Veredicto ejecutivo

El plan es **dirección correcta** y maduro en gobernanza de agentes, pero **aún no
es seguro ejecutar H1 (vigencia true)** sin corregir la semántica
instrumento/disposición/alcance de reforma. Aplicar E1-02/03 **solo con
`vigencia_verificada: false` + notas de búsqueda** es aceptable como exploración;
**fix-and-retry** de la metodología/plan (F1–F7) antes de afirmar reconciliación
primaria del slice salud.

## Notas

- Esta ronda **no** sustituye quórum ≥3 de §6 para el cierre formal de H1.
- No se modificó código ni registry de vigencia en esta ronda (solo el informe).
