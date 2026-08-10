# Metodología de fuentes legales MX (procedencia y vigencia)

**Tipo:** on-demand · **Estado:** vigente 2026-08-10 · **Tickets:** R1-E1-01  
**Autorización de canales:** `docs/autorizacion-fuentes-r1.md`  
**Política:** `docs/politica-agentes.md` §7 · **Registry:** `corpus/registry.yaml`  

**No es asesoría legal.** Define *cómo* el proyecto registra y califica
procedencia; no promulga normas. Afirmaciones sobre un artículo concreto exigen
traza en el registry + marca de vigencia.

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
5. **En duda:** `vigencia_verificada: false` + `[VIGENCIA-NO-VERIFICADA]`.
6. **Redactar ≠ promulgar:** el agente propone registry/PRs; roles §9 cierran.
7. **Sin copia verbatim masiva a AN-KLA:** puntero + hash + URL.

---

## 2. Niveles de fuente (canónicos del proyecto)

| Nivel | Nombre | Qué acredita | Ejemplos |
|------:|--------|--------------|----------|
| **1** | Primaria (publicidad del acto) | Que un texto/reforma **se publicó** en el órgano oficial | DOF; periódico oficial estatal; gaceta municipal |
| **2** | Consolidada / institucional | Texto “vigente” armado por institución; a menudo con aviso informativo | Cámara de Diputados (LeyesBiblio); Orden Jurídico Nacional; portales oficiales de consolidado |
| **3** | Jurisprudencial / interpretativa | Criterio de tribunales; **no** sustituye el texto legal | SCJN, SJF, tesis |
| **4** | Derivada | Extractos del propio corpus, resúmenes, salida de agentes | `corpus/derived/`, borradores |

**Regla de oro:** un claim de **vigencia federal** no puede ser `vigencia_verificada: true`
si solo hay evidencia de nivel ≥2, salvo decisión documentada del rol jurídico
(ADR-lite) que lo justifique — default R1: **no**.

---

## 3. Tipo de norma → primaria → secundaria → campos registry

| Tipo de norma (ámbito) | Fuente **primaria** (nivel 1) | Fuentes **secundarias** típicas (nivel 2+) | Campos mínimos en `registry.yaml` |
|------------------------|------------------------------|--------------------------------------------|-----------------------------------|
| Constitución federal (CPEUM) y reformas | DOF (acto de publicación/reforma) | Cámara, Orden Jurídico | `id`, `tipo`, `nivel` (archivo), `url_dof_nivel1` o lista de actos, `fecha_publicacion_dof`, `fecha_ultima_reforma_dof_*`, `sha256`, `fecha_consulta`, `vigencia_verificada` |
| Ley federal / reglamentaria (p. ej. LGS) | DOF | Cámara, Orden Jurídico, DOF consolidados si los hubiera | igual + `autoridad` |
| Reglamento federal / decreto del Ejecutivo | DOF | Sitio de la dependencia, Orden Jurídico | igual |
| NOM / acuerdos administrativos federales | DOF u órgano que el propio instrumento señale | Sitio de la dependencia | `tipo` específico + primaria documentada |
| Ley **estatal** | Periódico oficial del **estado** | Portales estatales, Orden Jurídico (si indexa) | `organo_publicidad_primaria`, URL gaceta, **no** fingir DOF federal |
| Norma municipal | Gaceta / bando municipal | Portales municipales | idem local |
| Jurisprudencia / tesis | Publicación oficial del criterio (SJF etc.) | Resúmenes doctrinales | `nivel: 3`; **no** usar para `vigencia_verificada` de una ley |
| Manual / procedimiento **interno** IMSS | N/A como “ley”; es **dato institucional** | — | **No** al corpus normativo público sin auth; router §7.4 deniega interno v1 |

### Canales autorizados hoy (R1)

| Canal | URL | Nivel por defecto al citar |
|-------|-----|----------------------------|
| DOF | https://dof.gob.mx/ | **1** (si el registro apunta al **acto** concreto, no solo a la home) |
| Orden Jurídico Nacional | https://www.ordenjuridico.gob.mx/ | **2** (análisis/consulta) hasta trazar acto DOF |
| Cámara Diputados LeyesBiblio | https://www.diputados.gob.mx/LeyesBiblio/ | **2** (consolidado informativo) |

---

## 4. Campos del registry (contrato de datos)

### 4.1 Ya en uso (mantener)

- `id`, `nombre_oficial`, `tipo`, `autoridad`
- `fuente_archivo`, `nivel` ← nivel del **archivo bytes** cargado
- `url_descarga`, `archivo_local`, `bytes`, `sha256`, `fecha_consulta`
- `fecha_publicacion_dof`, `fecha_ultima_reforma_dof_declarada`
- `url_dof_nivel1`, `vigencia_verificada`, `notas`

### 4.2 Extensión recomendada (R1+, rellenar cuando exista evidencia)

Usar nombres estables; omitir o `null` si no aplica:

```yaml
# ejemplo ilustrativo — no copiar como verdad de un instrumento real
trazas_publicacion:
  - tipo_acto: reforma   # publicacion | reforma | fe_de_erratas
    organo: DOF
    nivel: 1
    url: "https://dof.gob.mx/..."   # permalink del acto si existe
    fecha_dof: "YYYY-MM-DD"
    nota: "reforma en materia de ..."
fuentes_secundarias_consultadas:
  - organo: Camara_Diputados
    nivel: 2
    url: "https://www.diputados.gob.mx/..."
    fecha_consulta: "YYYY-MM-DD"
  - organo: Orden_Juridico
    nivel: 2
    url: "https://www.ordenjuridico.gob.mx/..."
    fecha_consulta: "YYYY-MM-DD"
coherencia_multi_fuente: alineado | discrepancia | no_evaluado
discrepancia_notas: null
```

**Semántica de `vigencia_verificada` (booleano de instrumento en R1):**

| Valor | Condición mínima |
|-------|------------------|
| `true` | ≥1 traza nivel 1 usable (URL/id de acto + fecha) **y** rol/custodio no marcó disputa; secundarias pueden apoyar pero no bastan solas |
| `false` | Default; falta primaria, duda, o solo nivel ≥2 |

R1 **no** implementa aún vigencia *bitemporal* (“¿vigente el día D?”); el booleano
es “**reconcilamos primaria para la versión de trabajo del corpus**”. Evolución
futura: vigencia con `fecha_juridica` de consulta (fuera de E1-01).

---

## 5. Procedimiento de traza (agentes + admin) — slice federal

### Paso A — Identificar instrumento y disposición

1. `id` del registry (CPEUM, LGS, …) y, si aplica, `disposicion_id` (p. ej. `CPEUM:4:P4`).
2. No afirmar el contenido del artículo sin leer la fuente del corpus o primaria.

### Paso B — Consolidado (nivel 2) — orientación

1. Cámara y/o Orden Jurídico (autorizados).
2. Anotar URL + `fecha_consulta` + qué reforma **declaran** (como *claim secundario*).

### Paso C — Primaria DOF (nivel 1) — ancla

1. En https://dof.gob.mx/ localizar el **acto** de publicación o de la reforma
   relevante (no solo la home).
2. Preferir permalink / identificador estable del diario o del decreto.
3. Registrar en `url_dof_nivel1` y/o `trazas_publicacion[]`.
4. Si no hay permalink estable: documentar ruta de búsqueda + fecha + identificadores
   visibles del diario en `notas` (mejor que inventar URL).

### Paso D — Integridad del archivo de trabajo

1. Si hay PDF/local: `sha256` recomputado = declarado.
2. El archivo puede seguir siendo consolidado nivel 2: **eso es válido** si la
   **vigencia** se ancla con traza nivel 1 (el consolidado es el texto de trabajo;
   el DOF es la prueba de publicidad/reforma).

### Paso E — Coherencia multi-fuente

1. Comparar fechas de “última reforma” Cámara vs DOF vs Orden Jurídico.
2. `coherencia_multi_fuente`:
   - `alineado` si no hay choque material de fechas/actos;
   - `discrepancia` si chocan → **no** `vigencia_verificada: true` hasta
     desempate del rol jurídico (§9).

### Paso F — Cierre

1. PR pequeño solo registry + notas (+ tests E1-04 si aplica).
2. DoD base: tests + `check_sizes`.
3. CI: verde o `SUSPENDIDO (billing)` + DoD local (`docs/ops-github.md`).

### Anti-patrones

- Marcar `vigencia_verificada: true` solo porque “ya autorizamos dof.gob.mx”.
- Usar la home del DOF como única “prueba”.
- Tratar Orden Jurídico o Cámara como nivel 1 sin traza al acto.
- Scraper agresivo al DOF en R1 (fase posterior: cola de novedades + humano).
- Subir secretos o material interno IMSS a proveedores.

---

## 6. Calificación de confianza del *claim* (multi-eje)

Complementa el gate de citas (`corpus/verify_citations.py`). Diseño detallado:
`docs/propuestas/gate-confianza-multieje-v1.md`.

| Eje | Código | Pregunta | Señal actual / R1 |
|-----|--------|----------|-------------------|
| A | `existencia` | ¿La disposición está en el corpus? | `lookup` / `reference_exists` |
| B | `procedencia` | ¿Nivel de fuente del texto citado? | `registry.nivel` + trazas |
| C | `match_textual` | ¿La cita aparece en el texto? | substring normalizado (gate v1) |
| D | `vigencia` | ¿Vigencia anclada a primaria? | `vigencia_verificada` + trazas |
| E | `coherencia` | ¿Secundarias alineadas? | `coherencia_multi_fuente` |

**Agregación (política R1 — honesta):**

| Etiqueta legible | Condición orientativa | Uso |
|------------------|----------------------|-----|
| **bajo** | Falla A o C, o sin fuente resuelta | No usar como respaldo |
| **medio** | A+C+hash OK; D falso o solo nivel ≥2 | Borrador / trabajo interno |
| **alto** | A+C+B≤2 con traza; **D true** y E ≠ discrepancia | Reservado; **inalcanzable en gate código v1** hasta ticket que habilite `alto` con D |

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

## 8. Checklist rápido E1-02 / E1-03 (por instrumento)

- [ ] `id` CPEUM o LGS
- [ ] Secundaria: URL Cámara y/o Orden Jurídico + fecha consulta
- [ ] Primaria: acto DOF (URL/id + fecha) en `url_dof_nivel1` o `trazas_publicacion`
- [ ] Hash del archivo de trabajo coherente si hay original local
- [ ] `coherencia_multi_fuente` evaluada
- [ ] `vigencia_verificada` true **solo** si D se sostiene; si no, false + notas
- [ ] PR + tests + sin secretos

---

## 9. Enlaces

- Auth: `docs/autorizacion-fuentes-r1.md`
- Roles: `docs/roles-r1.md`
- Plan: `docs/plan-r1-90d.md`
- Score: `docs/propuestas/gate-confianza-multieje-v1.md`
- Código gate v1: `corpus/verify_citations.py`
- Ops CI: `docs/ops-github.md`
