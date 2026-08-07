# Análisis del corpus inicial — ¿es correcto el conjunto propuesto? (2026-08-06)

> **§7 Fidelidad documental:** las denominaciones y la vigencia de los instrumentos NO están
> verificadas — la Cámara de Diputados devuelve **403 a fetch automatizado** y el DOF no se
> consulted automáticamente. Todo va marcado **`[VERIFICAR-FUENTE]` / `[VIGENCIA-NO-VERIFICADA]`**.
> Esto lo resuelve el **componente A (Registro de fuentes)** con texto oficial + hash +
> fecha de consulta + fecha de última reforma. Este doc es **análisis de diseño**, no aserción normativa.

## 1. Decisiones registradas (del orquestador)
- **Dominio:** federal (leyes públicas). **IMSS = piloto de prueba** (no corpus propietario).
- **Responsable jurídico del corpus:** **DEUDA** (diferido). Mientras tanto aplica la enmienda
  Cambio 4: **interino = humano-promulgador**. Implicación: las **discrepancias de fuentes** que
  requieran desempate jurídico quedarán `[VIGENCIA-NO-VERIFICADA]` / `PARCIAL (espera-humano)`
> hasta designarse — el agente no las resuelve unilateralmente.

## 2. ¿Es correcto el conjunto propuesto?
**Principio "traza desde el origen": CORRECTO.** Modelar la cadena jerárquica desde la
Constitución hasta normas internas IMSS coincide con el dictamen (jerarquía normativa +
artículo como unidad) y da base para resolver conflictos (Cambio §7.2). Es un buen principio
de **diseño del corpus**.

**Nomenclatura §7 (a verificar — NO afirmar como hecho):**
| Lo dicho | Denominación probable | Estado |
|---|---|---|
| "Constitución de los Estados Unidos" | **CPEUM** — Constitución Política de los Estados Unidos Mexicanos | `[VERIFICAR-FUENTE]` |
| "Ley Federal de Salud" | denominación inusual; el instrumento federal de salud es probablemente la **Ley General de Salud (LGS)** | `[VERIFICAR-FUENTE]` — **posible error de nombre a confirmar por el humano** |
| "Ley del IMSS" | probablemente **Ley del Seguro Social (LSS)** | `[VERIFICAR-FUENTE]` |
| "referentes a IMSS, carácter especial" | Reglamento Interior del IMSS, Acuerdos del Consejo Técnico, Normas Oficiales Mexicanas (NOM) en salud, reglamentos de la LGS/LSS | `[VERIFICAR-FUENTE]` |

**Como conjunto de TRAZA:** correcto (cubre el eje constitución → ley general → ley sectorial →
normativa institucional). **Como MVP inicial:** no cargar todo a la vez — el dictamen y el
análisis previo concluyen **start-small** (una infraestructura pequeña primero).

## 3. Recomendación: reconciliar "traza desde el origen" con "start-small" vía rebanada vertical
- **Corpus piloto TARGET (orden jerárquico, a construir progresivamente):** CPEUM → LGS → LSS →
  Reglamento Interior IMSS / Acuerdos del Consejo Técnico / NOM de salud.
- **MVP SPIKE (primer entregable):** una **rebanada vertical** — un tema/provisión modelado a lo
  largo de la jerarquía (p. ej. el eje "derecho a la protección de la salud") encadenando
  CPEUM → LGS → LSS → norma interna IMSS. Esto valida a la vez: **traza desde el origen,
  lookup exacto, verificador de citas, relaciones jerárquicas y transitorios**, con mínimos datos.
- Los **artículos/fracciones concretos** del slice se definen **tras verificar la fuente** en la
> ingesta (no se afirman aquí).

## 4. Bloqueo §7 + componente A (Registro de fuentes)
- El fetch automatizado de la Cámara = **403** (bot-block); DOF no consultado automáticamente.
- **No se afirman nombres ni vigencia** hasta ingesta con fuente oficial. El componente A debe
  obtener el texto oficial por un **canal que funcione** (descarga asistida/API, o texto provisto
  por el humano) y registrar **hash SHA-256 + URL + fecha_consulta + fecha_última_reforma_declarada**.
- Esto convierte el "403" en un **requisito de diseño** del componente A, no en un obstáculo ad hoc.

## 5. Decisiones / acciones
- **Humano:** (a) confirma si "Ley Federal de Salud" = **Ley General de Salud**; (b) provee o
  autoriza obtener el **texto oficial** (DOF/Cámara) del instrumento raíz del slice; (c) elegirá
  el tema del slice (p. ej. derecho a la salud) al proveer las fuentes.
- **Agente:** en cuanto haya texto oficial + hash, inicia el **MVP** (lookup exacto determinista
  + verificador de citas) sobre el slice, y lo somete a **ronda multi-provider** ( = el artefacto
  distinto que valida la enmienda v1.1-revisada, rompiendo la circularidad).

> Este análisis es **soporte de decisión**; la elección del instrumento/tema del slice y la
> confirmación de nombres son del humano (§7.2).
