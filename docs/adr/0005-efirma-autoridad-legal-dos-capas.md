# ADR-0005 — Autoridad de firma legal vía e.firma (SAT); dos capas de firma

> **Estado:** Aceptado (2026-08-13).
> **Clase:** Estratégico (firma, fidelidad §7, gobernanza de promulgación).
> **Fecha:** 2026-08-13. **Autor:** agente (síntesis). **Autoridad que adopta:** humano orquestador.
> **Relacionados:** ADR-0002 (proveniencia/firma de agentes), `docs/roles-r1.md`
> (humano-promulgador), `docs/politica-agentes.md` §7.2 (redactar ≠ promulgar),
> CAGF-A10 (Integridad del Sustrato).

## Contexto

El proyecto distingue **redactar ≠ promulgar** (§7.2): los agentes producen
borradores; el **humano** responde y pone en vigor. ADR-0002 cubrió la
**proveniencia de código** (commits firmados por el admin vía SSH). Faltaba la
capa de **firma con autoridad legal** para actos normativos: promulgar una norma,
sellar un dictamen o salida oficial al exterior.

La **e.firma (FIEL)** del SAT es la firma electrónica con **plena validez legal**
en México (equivalente a la firma autógrafa; Código de Comercio art. 89-114). El
humano-promulgador designado interino (`docs/roles-r1.md`: Kristhian Manuel
Jiménez) es titular de una. Es el mecanismo de mayor jerarquía para este dominio.

## Decisión

**Modelo de firma de dos capas, no mezcladas:**

| Capa | Mecanismo | Alcance | ADR |
|---|---|---|---|
| Proveniencia de código | SSH ed25519 | Commits git (qué humano aplicó el cambio) | ADR-0002 |
| Autoridad legal | e.firma SAT | Promulgación de normas, dictámenes, salida oficial | **este ADR** |

1. **La e.firma NO firma commits git rutinarios.** Un commit no es un acto legal;
   mezclar capas infla el uso de la llave privada y confunde jerarquía. La firma
   SSH (ADR-0002) basta para proveniencia de código.
2. **La e.firma es la firma de promulgación.** Cuando el proyecto emita una norma,
   dicte un dictamen o produzca un artefacto con efectos externos, la firma del
   humano-promulgador con e.firma es la que vincula el acto a su identidad legal.
3. **El proyecto referencia, no custodia.** El repo registra del certificado sólo
   los datos públicos para verificación (RFC, serial, huella SHA-256, emisor). La
   llave privada `.key` y la contraseña **nunca** entran al repo (`.gitignore`
   cubre `*.key *.cer *.pem *.p12 *.pfx`); quedan en control exclusivo del humano.

## Identidad y certificado (datos públicos)

| Campo | Valor |
|---|---|
| Titular | KRISTHIAN MANUEL JIMENEZ SANCHEZ |
| RFC (x500UniqueIdentifier) | `JISK800210B31` |
| CURP (serialNumber) | `JISK800210HDFMNR01` |
| Emisor | AUTORIDAD CERTIFICADORA — SAT (`SAT970701NN3`) |
| Serial | `3030303031303030303030353131363332333339` |
| SHA-256 | `AD4C38DA09580D37014FB0376C8F4AC48B01AFA3142010E768A40D32B0E78BEB` |
| Vigencia | 2022-02-25 → **2026-02-25** |

Coincide con el humano-promulgador interino de `docs/roles-r1.md`.

## ⚠ Vencimiento (excepción de fase alfa)

**El certificado venció el 2026-02-25.**

**Excepción de fase (vigente mientras el proyecto sea alfa de pruebas/desarrollo):**
el vencimiento **no bloquea** el desarrollo. Durante alfa no hay promulgación real
ni salida oficial firmada; el ejercicio de cablear el modelo de dos capas, registrar
la identidad y dejar lista la infraestructura de verificación es válido y útil para
cuando la e.firma se renueve. La restricción de "no firmar actos nuevos" aplica a
**promulgación legal real**, no a pruebas, ejercicios ni desarrollo.

- **No puede firmar actos legales nuevos** con validez jurídica hasta renovarse.
- Sí verifica firmas hechas **durante** su vigencia, y sirve de referencia de
  identidad del humano-promulgador.
- El modelado, la integración y los ejercicios de firma en desarrollo proceden.

**Acción requerida (humana, antes de salir de alfa / promulgar):** renovar la
e.firma ante el SAT. La renovación actualiza serial + vigencia en este ADR (nueva
fila, sin borrar historia).

## Consecuencias

- **+** Jerarquía de firma clara: SSH = código, e.firma = ley. Sin confusión.
- **+** §7.2 queda operacionalizado: el agente redacta; el humano promulga con
  su firma legal verificable.
- **+** CAGF-A10 (Integridad del Sustrato) reforzado: el sustrato que pone en
  vigor está en control de una identidad legal criptográfica del humano.
- **−** La promulgación real queda bloqueada hasta renovar la e.firma (no bloquea
  el desarrollo en alfa — ver excepción de fase).
- **−** Costo operativo futuro: la renovación periódica (cada 4 años) es tarea
  humana fuera del repo.

## Alternativas consideradas

- **e.firma para commits git:** descartada; mezcla capas (commit ≠ acto legal),
  uso pesado (contraseña por acto) y confunde jerarquía de firma.
- **Sólo SSH, sin capa legal:** descartada; la firma SSH no tiene validez legal
  en MX y no satisface §7.2 para promulgación.
- **Custodiar el `.key` en el repo (cifrado):** descartada; la llave privada
  legal nunca vive en git. El repo referencia, no custodia.

## Criterio de cumplimiento (DoD)

- [x] `.gitignore` cubre `*.key *.cer *.pem *.p12 *.pfx`.
- [x] Datos públicos del certificado registrados (RFC, serial, SHA-256, emisor).
- [x] Vencimiento declarado con excepción de fase alfa (desarrollo no bloqueado).
- [x] Modelo de dos capas documentado y separado de ADR-0002.
- [ ] (Humano) Renovar e.firma antes de cualquier promulgación real (no bloquea alfa).

## Ítems abiertos

- Renovación de la e.firma (humana; desbloquea promulgación).
- Flujo concreto de promulgación (qué artefacto, qué herramienta firma con
  e.firma) — se diseña cuando exista una norma lista para promulgar.
