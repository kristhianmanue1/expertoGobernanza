# Metodología de fuentes legales MX (procedencia y vigencia)

**Tipo:** on-demand · **Estado:** vigente 2026-08-10 (rev. adversarial F1–F7)  
**Tickets:** R1-E1-01 · **Ronda:** `docs/propuestas/r1-plan-adversarial-pre-e1/RONDA.md`  
**Autorización de canales:** `docs/autorizacion-fuentes-r1.md`  
**Política:** `docs/politica-agentes.md` §7 · **Registry:** `corpus/registry.yaml`  

**No es asesoría legal.** Define *cómo* el proyecto registra y califica
**procedencia**; no promulga normas ni certifica aplicabilidad a un caso.

---

## 1. Principios

1. **Autorizar un sitio ≠ verificar un instrumento.** (`autorizacion-fuentes-r1.md`)
2. **Ancla federal de publicidad:** para leyes/decretos/reformas **federales** del
   corpus, la fuente **primaria de publicación/reforma** es el **DOF**
   (https://dof.gob.mx/), no el consolidado de Cámara u Orden Jurídico.
3. **No todo el derecho mexicano es DOF federal:** leyes estatales → gaceta
   estatal; municipales → órgano local; jurisprudencia → nivel distinto.
4. **Consolidados = secundarios potentes:** Cámara, Orden Jurídico, portales de
   secretarías: útiles para leer y contrastar; **informativos** respecto del acto
   en gaceta primaria.
5. **En duda:** `vigencia_actual_estado: no_verificada` + `[VIGENCIA-NO-VERIFICADA]`.
6. **Redactar ≠ promulgar:** el agente propone registry/PRs; roles §9 cierran.
7. **Sin copia verbatim masiva a AN-KLA:** puntero + hash + URL.
8. **Tres capas (F1):** no confundir instrumento, disposición y texto de trabajo.
9. **Alcance de traza (F2):** la última reforma del *cuerpo* no valida un artículo
   del slice salvo que la traza lo declare.
10. **Desempate R1 (F7):** no inventar jerarquía doctrinal; ver §1.2.

### 1.1 Tres capas de identidad (obligatorio)

| Capa | Qué es | Ejemplo slice salud |
|------|--------|---------------------|
| **Instrumento** | Cuerpo normativo en el registry | `CPEUM`, `LGS` |
| **Disposición** | Unidad citables (art./párrafo/id) | `CPEUM:4:P4`, LGS Art. 1 |
| **Texto de trabajo** | Bytes/hash del PDF o extracto usado en lookup | `corpus/originals/CPEUM.pdf` sha256… / JSON derived |

Un claim de cita opera sobre **disposición + texto de trabajo**.  
Un claim de publicidad DOF opera sobre un **acto** con **alcance** declarado.

### 1.1-bis Fechas: no confundir cuerpo vs disposición (mejora F5 2026-08-10)

| Campo | Significado | Error típico de agente |
|-------|-------------|------------------------|
| `procedencia_primaria_verificada: true` | Ancla primaria reconciliada (con F5) para el alcance declarado | Vigencia actual de la disposición |
| `vigencia_actual_estado: no_verificada` | No existe comprobación temporal suficiente en R1 | Que la disposición está derogada |
| `traza_disposicion_principal` | Fecha/tipo/acto que **cubre** la disposición del slice (`cubre_disposicion: true`) | Usar 2012/2026 del cuerpo como si fuera del Art. 1 |
| `ultima_reforma_cuerpo` | Última reforma del **ordenamiento** (`cubre_disposicion: false` si no toca el slice) | Concluir “LSS:5 proviene de 2026-01-15” |
| `fecha_ultima_reforma_dof_declarada` | Claim nivel 2 del índice (legado); preferir los dos campos de arriba | Tratarlo como traza del artículo |

**Regla:** un agente **nunca** debe reportar la fecha de `ultima_reforma_cuerpo` como
procedencia de una disposición si `cubre_disposicion: false`.

### 1.2 Desempate entre fuentes en R1 (F7)

El agente **no** resuelve conflictos con “lex superior/specialis/posterior” sin
cita verificada (la política §7.2 aún marca jerarquía `[VERIFICAR-FUENTE]`).  
Orden permitido en R1:

1. Preferir evidencia de **nivel 1** (acto en órgano de publicidad) sobre nivel ≥2.
2. Preferir **fecha de acto** documentada sobre claim secundario sin acto.
3. Si persiste duda o discrepancia → `procedencia_primaria_verificada: false` +
   `coherencia_multi_fuente: discrepancia` + **decisión humana** (§9) en notas/ADR-lite.

### 1.3 Procedencia primaria y vigencia actual (enmienda 2026-10-10)

| Campo | Significa | Límite |
|-------|-----------|--------|
| `procedencia_primaria_verificada` | Resumen instrumental de anclas primarias revisadas con F5; la cobertura de cada disposición se resuelve aparte | No acredita continuidad, vigencia actual ni aplicabilidad |
| `vigencia_actual_estado: no_verificada` | R1 carece de comprobación temporal suficiente | No afirma derogación |
| `vigencia_verificada: false` | Campo legado conservador para consumidores previos | Nunca se deriva de `procedencia_primaria_verificada` |

`resolve_disposicion_procedencia` determina cobertura histórica exacta. El resultado
de `resolve_disposicion_vigencia` expone esa señal por separado y devuelve
`verificada=false` para vigencia actual. R1 no admite un estado positivo de
vigencia actual: requiere contrato temporal, transitorios, revisión humana y
ronda adversarial propios. Los JSON derivados conservan la procedencia en
`vigencia.procedencia_primaria_verificada`; sus campos legados de vigencia
quedan en `false`/`no_verificada`.

Campos de apoyo recomendados:

- `fecha_revision_procedencia` (YYYY-MM-DD)
- `vacatio_o_transitorio`: `unknown` \| `no` \| `si` (+ nota)
- Glosa en salidas de producto: *procedencia primaria reconciliada (alcance X)* —
  nunca “certificado de aplicabilidad”.

---

## 2. Niveles de fuente (canónicos del proyecto)

| Nivel | Nombre | Qué acredita | Ejemplos |
|------:|--------|--------------|----------|
| **1** | Primaria (publicidad del acto) | Que un texto/reforma **se publicó** en el órgano oficial | DOF; periódico oficial estatal; gaceta municipal |
| **2** | Consolidada / institucional | Texto “vigente” armado por institución; a menudo con aviso informativo | Cámara de Diputados (LeyesBiblio); Orden Jurídico Nacional; portales oficiales de consolidado |
| **3** | Jurisprudencial / interpretativa | Criterio de tribunales; **no** sustituye el texto legal | SCJN, SJF, tesis |
| **4** | Derivada | Extractos del propio corpus, resúmenes, salida de agentes | `corpus/derived/`, borradores |

**Regla de oro:** un acto primario histórico puede acreditar procedencia, pero
no convierte por sí solo `vigencia_actual_estado` en verificada. La evidencia
de nivel ≥2 tampoco acredita procedencia primaria sin acto de publicación.

---

## 3. Tipo de norma → primaria → secundaria → campos registry

| Tipo de norma (ámbito) | Fuente **primaria** (nivel 1) | Fuentes **secundarias** típicas (nivel 2+) | Campos mínimos en `registry.yaml` |
|------------------------|------------------------------|--------------------------------------------|-----------------------------------|
| Constitución federal (CPEUM) y reformas | DOF (acto de publicación/reforma) | Cámara, Orden Jurídico | `id`, `tipo`, `nivel` (archivo), acto DOF, `sha256`, `fecha_consulta`, `procedencia_primaria_verificada`, `vigencia_actual_estado` |
| Ley federal / reglamentaria (p. ej. LGS) | DOF | Cámara, Orden Jurídico, DOF consolidados si los hubiera | igual + `autoridad` |
| Reglamento federal / decreto del Ejecutivo | DOF | Sitio de la dependencia, Orden Jurídico | igual |
| NOM / acuerdos administrativos federales | DOF u órgano que el propio instrumento señale | Sitio de la dependencia | `tipo` específico + primaria documentada |
| Ley **estatal** | Periódico oficial del **estado** | Portales estatales, Orden Jurídico (si indexa) | `organo_publicidad_primaria`, URL gaceta, **no** fingir DOF federal |
| Norma municipal | Gaceta / bando municipal | Portales municipales | idem local |
| Jurisprudencia / tesis | Publicación oficial del criterio (SJF etc.) | Resúmenes doctrinales | `nivel: 3`; **no** usar para procedencia primaria de una ley |
| Manual / procedimiento **interno** IMSS | N/A como “ley”; es **dato institucional** | — | **No** al corpus normativo público sin auth; router §7.4 deniega interno v1 |

### Canales autorizados hoy (R1)

| Canal | URL | Nivel por defecto al citar |
|-------|-----|----------------------------|
| DOF | https://dof.gob.mx/ | **1** (si el registro apunta al **acto** concreto, no solo a la home) |
| Orden Jurídico Nacional | https://www.ordenjuridico.gob.mx/ | **2** (análisis/consulta) hasta trazar acto DOF |
| Cámara Diputados LeyesBiblio | https://www.diputados.gob.mx/LeyesBiblio/index.htm | **2** (índice, consolidado y páginas de reformas informativos) |

---

## 4. Campos del registry (contrato de datos)

### 4.1 Ya en uso (mantener)

- `id`, `nombre_oficial`, `tipo`, `autoridad`
- `fuente_archivo`, `nivel` ← nivel del **archivo bytes** cargado
- `url_descarga`, `archivo_local`, `bytes`, `sha256`, `fecha_consulta`
- `fecha_publicacion_dof`, `fecha_ultima_reforma_dof_declarada`
- `url_dof_nivel1`, `procedencia_primaria_verificada`, `vigencia_actual_estado`, `notas`
- `vigencia_verificada: false` (legado, sin promoción automática)

### 4.2 Extensión recomendada (R1+, rellenar cuando exista evidencia)

Usar nombres estables; omitir o `null` si no aplica:

```yaml
# ejemplo ilustrativo — no copiar como verdad de un instrumento real
fecha_revision_procedencia: "YYYY-MM-DD"
procedencia_primaria_verificada: false
vigencia_verificada: false
vigencia_actual_estado: no_verificada
vacatio_o_transitorio: unknown   # unknown | no | si
trazas_publicacion:
  - tipo_acto: reforma   # publicacion | reforma | fe_de_erratas
    organo: DOF
    nivel: 1
    alcance: articulo    # instrumento | articulo | parrafo
    cubre_disposiciones: ["CPEUM:4:P4"]   # ids del slice; [] si no aplica
    no_cubre_slice: false
    url: "https://dof.gob.mx/..."   # permalink del acto si existe
    # si no hay permalink (M8): diario_fecha + edicion/decreto en nota
    identificadores_diario: "DOF fecha=… decreto=… sección=…"
    fecha_dof: "YYYY-MM-DD"
    nota: "reforma en materia de … — alcance Art. 4 …"
fuentes_secundarias_consultadas:
  - organo: Camara_Diputados
    nivel: 2
    claim_secundario: true    # M3: no es hecho de vigencia primaria
    url: "https://www.diputados.gob.mx/..."
    fecha_consulta: "YYYY-MM-DD"
  - organo: Orden_Juridico
    nivel: 2
    claim_secundario: true
    url: "https://www.ordenjuridico.gob.mx/..."
    fecha_consulta: "YYYY-MM-DD"
coherencia_multi_fuente: alineado | discrepancia | no_evaluado
discrepancia_notas: null
# Doble control (F5) antes de true:
revision_procedencia:
  revisado_por: "nombre o handle"
  fecha: "YYYY-MM-DD"
  auto_revision_declarada: false  # true solo si no hay segundo revisor
```

**Campos legados en registry actual (M3):**  
`fecha_ultima_reforma_dof_declarada` y similares tomados de Cámara son
**claims nivel 2** hasta reconciliar con traza DOF de alcance adecuado. No bastan
para `procedencia_primaria_verificada: true`.

**Condición mínima de `procedencia_primaria_verificada: true`:**

1. ≥1 entrada en `trazas_publicacion` nivel 1 con fecha + (URL **o**
   `identificadores_diario` suficientes — M8).
2. `alcance` + `cubre_disposiciones` (o `no_cubre_slice`) **explícitos**.
3. Si el KPI es el slice salud: la traza debe **cubrir** `CPEUM:4:P4` y/o LGS Art. 1
   según el ticket; no basta una reforma de otro título del mismo cuerpo (F2).
4. `revision_procedencia` completada (F5).
5. `coherencia_multi_fuente` ≠ `discrepancia` (o desempate humano documentado).
6. Secundarias pueden apoyar; **no bastan solas**.

R1 **no** implementa vigencia bitemporal plena (“¿vigente el día D?”).

---

## 5. Procedimiento de traza (agentes + admin) — slice federal

### Paso A — Identificar instrumento y disposición

1. `id` del registry (CPEUM, LGS, …) y, si aplica, `disposicion_id` (p. ej. `CPEUM:4:P4`).
2. No afirmar el contenido del artículo sin leer la fuente del corpus o primaria.

### Paso B — Consolidado (nivel 2) — orientación

1. Cámara y/o Orden Jurídico (autorizados).
2. Anotar URL + `fecha_consulta` + qué reforma **declaran** (como *claim secundario*).

### Paso C — Primaria DOF (nivel 1) — ancla

1. En https://dof.gob.mx/ localizar el **acto** de publicación o reforma
   **relevante al alcance** (artículo/párrafo del slice, no “cualquier reforma
   reciente del mismo cuerpo”) — F2.
2. Preferir **permalink** del acto. Si no existe (M8): `identificadores_diario`
   (fecha DOF, número de decreto/edición, sección) + ruta de búsqueda en `nota`.
   **No inventar URL.**
3. Registrar `trazas_publicacion[]` con `alcance` y `cubre_disposiciones` /
   `no_cubre_slice`. Opcional: `url_dof_nivel1` si hay un único enlace principal.
4. Home del DOF **nunca** basta como prueba.

### Paso D — Integridad del texto de trabajo (capa 3)

1. Si hay PDF/local: `sha256` recomputado = declarado.
2. El archivo puede ser consolidado **nivel 2**: es el **texto de trabajo**, no la
   prueba de publicidad.
3. **(F4)** Match de cita sobre consolidado + traza DOF de otro alcance **no**
   autoriza nivel `alto` en el gate. Mientras `nivel` del archivo ≥ 2 y no haya
   apoyo primario del **texto de la disposición**, el techo de confianza de cita
   sigue siendo **medio** (reason `texto_trabajo_no_primario`).

### Paso E — Coherencia multi-fuente

1. Comparar claims nivel 2 (Cámara/OJ) vs actos nivel 1 (fechas y materia del acto).
2. Límite (M1): la coherencia por fechas **no** prueba identidad de texto.
3. `coherencia_multi_fuente`:
   - `alineado` si no hay choque material;
   - `discrepancia` → **no** `true` hasta desempate humano (§1.2).

### Paso F — Cierre

1. Completar `revision_procedencia` (F5 / `roles-r1.md`).
2. PR pequeño registry + notas (+ tests E1-04).
3. DoD base: tests + `check_sizes`.
4. CI: verde o `SUSPENDIDO (billing)` + DoD local (`docs/ops-github.md`).

### Anti-patrones

- Marcar `true` solo porque “ya autorizamos dof.gob.mx”.
- Usar la home del DOF o una reforma **ajena al artículo** del slice.
- Tratar Orden Jurídico o Cámara como nivel 1 sin traza al acto.
- Confundir claim secundario de “última reforma” con traza primaria.
- Scraper agresivo al DOF en R1; epic vigilancia DOF solo post-H3.
- Subir secretos o material interno IMSS a proveedores.
- Desempatar con jerarquía no citada (F7).

---

## 6. Calificación de confianza del *claim* (multi-eje)

Complementa el gate de citas (`corpus/verify_citations.py`). Diseño detallado:
`docs/propuestas/gate-confianza-multieje-v1.md`.

| Eje | Código | Pregunta | Señal actual / R1 |
|-----|--------|----------|-------------------|
| A | `existencia` | ¿La disposición está en el corpus? | `lookup` / `reference_exists` |
| B | `procedencia` | ¿Nivel de fuente del texto citado? | `registry.nivel` + trazas |
| C | `match_textual` | ¿La cita aparece en el texto? | substring normalizado (gate v1) |
| D | `vigencia` | ¿Vigencia actual comprobada? | `vigencia_actual_estado` (R1: no verificada) |
| E | `coherencia` | ¿Secundarias alineadas? | `coherencia_multi_fuente` |

**Agregación (política R1 — honesta, post-F4):**

| Etiqueta | Condición orientativa | Uso |
|----------|----------------------|-----|
| **bajo** | Falla A o C, o fuente irresoluble | No usar como respaldo |
| **medio** | A+C+hash OK; **o** D false; **o** archivo nivel ≥2 sin texto de disposición apoyado en primaria (`texto_trabajo_no_primario`) | Borrador / trabajo interno |
| **alto** | A+C OK; D true tras comprobación temporal de la disposición; E ≠ discrepancia; y no aplica techo por texto no primario | **Inalcanzable en R1**; exige contrato temporal, ticket código y ronda nueva |

El LLM **no** puede subir solo el eje D ni inventar nivel 1.

---

## 7. Evolución: vigilancia DOF (post-R1, visión)

```text
Hoy (R1):  búsqueda asistida en DOF + secundarias → registry (E1-02/03)
Después:   job acotado "novedades DOF" → cola de actos candidatos
           → hash + propuesta de reforma → revisión custodio/jurídico
           → update registry (nunca silencio en producción)
```

Fuera de alcance de este doc: scraper completo del DOF, bitemporalidad plena.

---

## 8. Checklist rápido E1-02 / E1-03 (por instrumento + disposición)

- [ ] Capas: instrumento + disposición del slice (`CPEUM:4:P4` / LGS-001) + hash texto
- [ ] Secundaria: URL Cámara y/o OJ + fecha (`claim_secundario: true`)
- [ ] Primaria: acto DOF con **alcance** y `cubre_disposiciones` / `no_cubre_slice`
- [ ] Permalink **o** `identificadores_diario` (M8) — no home DOF
- [ ] Hash del archivo de trabajo coherente si hay original local
- [ ] `coherencia_multi_fuente` evaluada
- [ ] `revision_procedencia` (F5)
- [ ] `procedencia_primaria_verificada: true` **solo** si §4.2 se cumple
- [ ] `vigencia_actual_estado: no_verificada` hasta existir contrato temporal propio
- [ ] PR + tests + sin secretos · sin promesa de aplicabilidad casuística

---

## 9. Enlaces

- Auth: `docs/autorizacion-fuentes-r1.md`
- Roles: `docs/roles-r1.md`
- Plan: `docs/plan-r1-90d.md`
- Score: `docs/propuestas/gate-confianza-multieje-v1.md`
- Código gate v1: `corpus/verify_citations.py`
- Ops CI: `docs/ops-github.md`
