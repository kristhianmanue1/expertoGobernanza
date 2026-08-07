# Marco normativo de organismos descentralizados / entidades paraestatales (2026-08-06)

> **§7 Fidelidad documental:** nombres y existencia de las leyes **verificados** contra el índice
> oficial de la Cámara de Diputados (`LeyesBiblio/index.htm`, consulta 2026-08-06). La **naturaleza
> jurídica exacta del IMSS** (descentralizado vs desconcentrado) y los **números de artículo**
> están `[VERIFICAR-FUENTE]` hasta ingestar la CPEUM/LSS (componente A). Las fechas son «últ.
> reforma declarada por la Cámara» (nivel 2); a reconciliar con DOF (nivel 1).

## 0. Discrepancia de numeración resuelta
Dos pasadas de verificación discreparon (off-by-one en la 2ª). Resolución contra el texto crudo
del índice: **el número precede a su ley**. Confirmados en crudo: LFEP=148, LOPSRM=085, LAASSP=015,
LFRCF=052, Planeación=087, Coordinación Fiscal=039, LSS=125, LGS=214. LOAPF/LGBN no visibles en el
crudo (salida truncada antes de la zona) → existencia confirmada, número exacto `[VERIFICAR-FUENTE]`.

## 1. «Desconcentrado» vs «descentralizado» (§7 — figura jurídica)
No son lo mismo (doctrina administrativa general):
- **Órgano administrativo desconcentrado:** jerárquicamente subordinado a una dependencia, **sin**
  personalidad jurídica ni patrimonio propios (regulado por la **LOAPF**). Ej.: delegaciones,
  unidades administrativas.
- **Organismo público descentralizado (OPD / entidad paraestatal):** **con** personalidad jurídica
  y patrimonio propios, autonomía técnica/operativa; integra el **sector paraestatal** (régimen
> general en la **LFEP**).
- **IMSS:** `[VERIFICAR-FUENTE en LSS]` — probablemente **organismo público descentralizado**
  (no desconcentrado). La denominación coloquial «desconcentrado» es imprecisa; el corpus debe
  registrar la **figura jurídica exacta** al ingestar la LSS (naturaleza del IMSS).

## 2. Marco normativo aplicable a la entidad IMSS (verificado por nombre)
| Instrumento | Rol en el marco | Publicación / últ. reforma DOF (Cámara) |
|---|---|---|
| **CPEUM** (n.º 001) — Art. 90 `[VERIFICAR]` | base constitucional: administración pública centralizada/paraestatal | 05/02/1917 / 02/06/2026 |
| **LOAPF** — Orgánica de la Administración Pública Federal | define dependencias, entidades paraestatales y órganos desconcentrados | `[VERIFICAR-FUENTE n.º]` |
| **LFEP** — Federal de las Entidades Paraestatales (148) | régimen general de OPDs (definición, órganos de gobierno, control) | 14/05/1986 / 16/07/2025 |
| **LGBN** — General de Bienes Nacionales | patrimonio de las entidades | `[VERIFICAR-FUENTE n.º]` |
| **LAASSP** (015) — Adquisiciones del Sector Público | compras/contratos del sector paraestatal | 16/04/2025 / sin reforma |
| **LOPSRM** (085) — Obras Públicas | obras/contratación OPD | 04/01/2000 / 14/11/2025 |
| **LFRCF** (052) — Fiscalización y Rendición de Cuentas | control/fiscalización OPD | 18/07/2016 / 15/05/2026 |
| **Planeación** (087) / **Coordinación Fiscal** (039) | planeación y coordinación fiscal | varias |
| **Responsabilidades** (General ≈213 / Federal ≈162) `[VERIFICAR n.º]` | servidores públicos | varias |
| **LSS** (125) — del Seguro Social | naturaleza jurídica del IMSS `[VERIFICAR Art.]` | 21/12/1995 / 15/01/2026 |
| **Reglamento Interior del IMSS** + **Acuerdos del Consejo Técnico** `[VERIFICAR-FUENTE]` | estructura operativa, competencias, denominaciones | no en índice de leyes federales |

## 3. Implicación para el corpus: **tres ejes**, no uno
El piloto IMSS no se modela con una sola cadena. Hay **tres ejes normativos**:
1. **Sustantivo — salud:** CPEUM Art. 4 `[VERIFICAR]` → **LGS** (214).
2. **Sustantivo — seguridad social:** CPEUM Art. 123 `[VERIFICAR]` → **LSS** (125).
3. **Estructural — la entidad IMSS (objeto de este análisis):** CPEUM Art. 90 `[VERIFICAR]` →
   **LOAPF** → **LFEP** → **LSS** (naturaleza del IMSS) → **Reglamento Interior IMSS** →
   Acuerdos del Consejo Técnico / manuales.

**Por qué importa para el producto:** el auditor de manuales del dictamen (Fase 0) detecta
«áreas incompetentes, denominaciones obseletas, funciones impuestas a otra coordinación, NOM
sustituidas». Esos defectos viven en el **eje 3**: un manual IMSS se valida contra el
Reglamento Interior + LFEP + LOAPF, no sólo contra CPEUM/LGS. Sin modelar este eje, el
auditor no puede razonar sobre competencia/estructura.

## 4. Próximo paso — iniciar el MVP (componente A sobre CPEUM)
- Ingerir el **texto oficial de la CPEUM** (hash SHA-256 + `fecha_consulta` +
  `fecha_última_reforma_DOF` 02/06/2026) → **cierra `[VERIFICAR-FUENTE]` de Art. 4, 90 y 123**.
- Modelo mínimo de la **rebanada vertical del eje salud** (Art. 4 → LGS) como spike, más el
  **eje 3** cuando entre la normativa interna IMSS (Reglamento Interior, Acuerdos CT).
- Cada afirmación del corpus lleva su cita (instrumento + artículo + fecha de reforma) — el
  patrón §7 ya demostrado (verificación de nombres + disclaimer Cámara).

> Este análisis es **soporte de decisión de alcance**; la adopción del eje 3 y la confirmación
> de naturalezas/artículos se resuelven al ingestar las fuentes (§7.2).
