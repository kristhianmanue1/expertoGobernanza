# Alcance IMSS — público vs interno (R1-E5-01)

**Fecha:** 2026-08-10 · **Estado:** vigente como mapa de alcance (no ingesta aún)  
**Auth datos:** `docs/autorizacion-fuentes-r1.md` (multi-provider solo público; interno denegado)  
**Antecedente:** `docs/propuestas/marco-paraestatal-analisis-2026-08-06.md`  
**No es asesoría legal.** Nombres y URLs de índice = nivel 2 / orientación; vigencia
DOF por instrumento = tickets E5-02+ (mismo patrón H1 del slice salud).

## 1. Por qué este documento

El piloto institucional es el **IMSS** (ADR-0001). Antes de bajar PDFs hay que
separar:

1. Normas **federales públicas** (aptas a corpus + multi-provider).  
2. Normas **orgánicas del IMSS publicadas** (aptas si están en DOF/portal oficial
   abierto).  
3. Material **interno/confidencial** (manuales, procedimientos no publicados) —
   **fuera** de R1 y del router v1.

## 2. Tres ejes (recordatorio)

| Eje | Cadena (simplificada) | En corpus hoy |
|-----|------------------------|---------------|
| 1 Salud | CPEUM Art.4 → LGS | **Slice H1** ✓ (`CPEUM:4:P4`, `LGS:1`) |
| 2 Seguridad social | CPEUM Art.123 → **LSS** | No ingerido |
| 3 Estructura entidad | CPEUM Art.90 → **LOAPF** → **LFEP** → LSS (naturaleza) → **Reglamento Interior IMSS** → acuerdos/manuales | No ingerido |

El auditor de **manuales** del dictamen vive sobre todo en el **eje 3**.

## 3. Matriz de clasificación (R1)

| Instrumento | ¿Público federal? | Primaria típica | Secundaria (índice) | ¿Ingerir en R1? | Router / multi-provider |
|-------------|-------------------|-----------------|---------------------|-----------------|-------------------------|
| **LOAPF** — Ley Orgánica de la Administración Pública Federal | **Sí** | DOF | [Cámara LOAPF](https://www.diputados.gob.mx/LeyesBiblio/ref/loapf.htm) | **Sí** (E5-02) tras traza | Público |
| **LFEP** — Ley Federal de las Entidades Paraestatales | **Sí** | DOF (orig. 14-05-1986; reformas en índice Cámara) | [Cámara LFEP](https://www.diputados.gob.mx/LeyesBiblio/ref/lfep.htm) | **Sí** (E5-03) | Público |
| **LSS** — Ley del Seguro Social | **Sí** | DOF | Índice Cámara LSS | **Sí** (recomendado eje 2/3; ticket propio) | Público |
| **Reglamento Interior del IMSS** | **Sí si** publicado en DOF / portal oficial abierto | DOF u órgano de publicidad del acto | Portal IMSS / DOF (buscar “Reglamento Interior” IMSS) | **Sí condicionado** (E5-04): solo texto **publicado**; no versiones internas | Público **solo** el publicado |
| Acuerdos del Consejo Técnico **publicados** en DOF | **Sí** (acto por acto) | DOF | — | Caso por caso | Público |
| Manuales, lineamientos, procedimientos **no publicados** | **No** (interno institucional) | N/A | — | **No** en R1 | **Denegado** (`interno_institucional` v1) |
| Datos personales / expedientes | **No** | — | — | **No** | **Denegado** (`personal`) |

### URLs de trabajo (nivel 2 — no equivalen a vigencia true)

| id propuesto | URL secundaria |
|--------------|----------------|
| LOAPF | https://www.diputados.gob.mx/LeyesBiblio/ref/loapf.htm |
| LOAPF PDF (ejemplo portal salud; verificar hash al ingerir) | orientativo — preferir PDF Cámara LeyesBiblio al ingestar |
| LFEP | https://www.diputados.gob.mx/LeyesBiblio/ref/lfep.htm |
| LGS (ya en corpus) | https://www.diputados.gob.mx/LeyesBiblio/ref/lgs.htm |
| CPEUM (ya en corpus) | https://www.diputados.gob.mx/LeyesBiblio/ref/cpeum.htm |

## 4. Naturaleza jurídica del IMSS

- Texto de trabajo **LSS:5** (consolidado Cámara): el IMSS es **organismo público
  descentralizado** con personalidad jurídica y patrimonio propios, tripartita y
  organismo fiscal autónomo.  
- Ancla DOF de ese artículo: **pendiente F5** (`vigencia_verificada: false` en
  registry LSS). Hasta entonces: citar como texto de trabajo nivel 2, no como
  vigencia primaria cerrada.

## 5. Reglas operativas para agentes

1. **No descargar** a `corpus/originals/` ni indexar manuales IMSS sin auth nueva.  
2. Ingesta R1 del eje 3: **LOAPF → LFEP** primero (leyes federales, mismo pipeline
   que CPEUM/LGS: registry + hash + exploración DOF + F5 humano para `true`).  
3. **Reglamento Interior:** solo si se localiza acto **público**; registrar nivel y
   URL; si solo hay PDF en intranet → **bloquear**.  
4. Multi-provider: solo tras clasificar el path como **público** en
   `review_routing/config.json` (añadir globs al permitir nuevos paths).  
5. Cada instrumento nuevo: `slice_mvp` o `eje: estructura_imss` en notas registry.

## 6. Orden de tickets siguientes (sin abrir internos)

| Orden | Ticket | Acción |
|------:|--------|--------|
| 1 | E5-02 | **HECHO 2026-08-10** — LOAPF.pdf + registry + `LOAPF:1` (false hasta F5) |
| 2 | E5-03 | **HECHO 2026-08-10** — LFEP.pdf + registry + `LFEP:1` (false hasta F5) |
| 3 | LSS | **HECHO exploración 2026-08-10** — LSS.pdf + `LSS:5` (OPD) + `LSS:1` (false) |
| 4 | E5-04 | **HECHO 2026-08-10** — RIIMSS.pdf portal IMSS + `RIIMSS:1` (false hasta F5) |
| 5 | E5-05 | 1 disposición lookup por instrumento + tests |
| 6 | E5-06 | Adversarial multi del paquete corpus |

## 7. Fuera de alcance R1 (explícito)

- Manuales de organización / procedimientos operativos no publicados.  
- Expedientes, nómina, datos de derechohabientes.  
- Enviar internos a Claude/Codex/etc.  
- Prometer auditoría de manuales IMSS sin eje 3 público mínimo.

## 8. DoD de este ticket (E5-01)

- [x] Matriz público/interno  
- [x] URLs de índice LOAPF/LFEP  
- [x] Reglas de no-ingesta interna  
- [x] Cola E5-02+ sin ambigüedad  
