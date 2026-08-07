# Análisis del corpus inicial — ¿es correcto el conjunto propuesto? (2026-08-06)

> **§7 Fidelidad documental — denominaciones VERIFICADAS 2026-08-06** contra el índice oficial
> de la Cámara de Diputados (`https://www.diputados.gob.mx/LeyesBiblio/index.htm`). La Cámara es
> **fuente consolidada (nivel 2 del dictamen)**: las fechas son «últ. reforma declarada por la
> Cámara», **no** reconciliadas con DOF (fuente primaria, nivel 1) — eso lo hace el componente A.
> Las normas internas IMSS (Reglamento Interior, Acuerdos CT, NOM) **no figuran** en este índice
> de leyes federales → siguen `[VERIFICAR-FUENTE]` (se buscan en secciones de reglamentos/NOM).

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

**Nomenclatura §7 — VERIFICADA contra la Cámara de Diputados (índice de leyes federales vigentes):**
| Lo dicho | Denominación OFICIAL (entrada) | Publicación DOF | Últ. reforma (decl. Cámara) |
|---|---|---|---|
| "Constitución de los Estados Unidos" | **CONSTITUCIÓN Política de los Estados Unidos Mexicanos** (CPEUM) · n.º 001 | 05/02/1917 | 02/06/2026 |
| "Ley Federal de Salud" ❌ **no existe** | **LEY General de Salud** (LGS) · n.º 214 — *corrección de nombre* | 07/02/1984 | 15/01/2026 |
| "Ley del IMSS" | **LEY del Seguro Social** (LSS) · n.º 125 | 21/12/1995 | 15/01/2026 |
| (contexto salud) | LEY de los Institutos Nacionales de Salud · n.º 079 | 26/05/2000 | 11/05/2022 |
| "referentes a IMSS, carácter especial" | **No** en este índice: Reglamento Interior IMSS, Acuerdos del Consejo Técnico, NOM de salud → secciones `regla.htm` / `norma/reglamento.htm` / NOM | — | `[VERIFICAR-FUENTE]` |

> **Correcciones clave del análisis:** (a) **no existe «Ley Federal de Salud»** → el instrumento es
> la **Ley General de Salud** (n.º 214); (b) el **IMSS no es una ley autónoma**, su marco es la
> **Ley del Seguro Social** (n.º 125). *Fuente: Cámara de Diputados, índice citado, consulta 2026-08-06.*

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

## 4. §7 + componente A (Registro de fuentes) — verificación realizada
- **Denominaciones verificadas 2026-08-06** contra la Cámara (`index.htm` **es** accesible; la
  alerta previa de «403» era sólo de la ruta `/LeyesBiblio/` sin `index.htm`). DOF (nivel 1) no
  consultado automáticamente todavía.
- La Cámara es **fuente consolidada (nivel 2)**: las fechas aquí son «últ. reforma declarada por
  la Cámara», **no** confrontadas con DOF. El componente A debe **reconciliar con DOF (nivel 1)** y
  registrar **hash SHA-256 + URL + fecha_consulta + fecha_última_reforma_DOF + texto oficial**.
- Normas internas IMSS (Reglamento Interior, Acuerdos CT, NOM de salud) **no figuran** en el
  índice de leyes federales; se consultan en `regla.htm` (reglamentos de leyes) /
  `norma/reglamento.htm` (reglamentos federales) / listados de NOM — quedan `[VERIFICAR-FUENTE]`.
- **Primera instancia real de §7 del proyecto:** verificar una afirmación (nombre de ley) contra
  fuente oficial citada con fecha — el patrón a escalar en el corpus.

## 5. Próximas acciones
- **Verificado:** "Ley Federal de Salud" → **Ley General de Salud** (n.º 214). No requiere confirmación del humano.
- **Humano (aún):** (a) proveer o autorizar obtener el **texto oficial** (DOF/Cámara) del
  instrumento raíz del slice; (b) elegir el **tema del slice** (p. ej. derecho a la protección de
  la salud) al proveer las fuentes; (c) normativa interna IMSS (Reglamento Interior, Acuerdos CT) para el piloto.
- **Agente:** en cuanto haya texto oficial + hash, inicia el **MVP** (lookup exacto determinista
  + verificador de citas) sobre el slice, y lo somete a **ronda multi-provider** (= el artefacto
  distinto que valida la enmienda v1.1-revisada, rompiendo la circularidad).

> Este análisis es **soporte de decisión**; la elección del instrumento/tema del slice y la
> confirmación de nombres son del humano (§7.2).
