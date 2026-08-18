# Enmienda — promulgación es potestad institucional del IMSS

**Estado:** propuesta (aplicación gateada por el humano + ronda §6).
**Fecha:** 2026-08-18 · **Origen:** aclaración del humano en sesión.
**Fuentes:** RIIMSS arts. 6-VI y 75-I/IV/XVI (`docs/fuentes/imss/RIIMSS.pdf`,
extractos verbatim en `RIIMSS-PROCEDENCIA.md`); Marco Normativo IMSS
(secciones Leyes/Reglamentos/Normas y Manuales, con fechas DOF).

## Corrección de fondo

La redacción vigente (política §7.2, ADR-0005, roles-r1) llama
"humano-promulgador" al humano del repo y dice que éste "ejerce la autoridad
de promulgación". **Incorrecto**: la promulgación/emisión de normas es
potestad **institucional del IMSS** — la ejercen sus áreas normativas y sus
titulares (personal IMSS) por la cadena RIIMSS: propuesta del área →
validación de la Dirección Jurídica → Director General → Consejo Técnico →
publicación (DOF cuando corresponde, autorizada por la DJ, art. 75-XVI).
Las "Normas y Manuales" institucionales (códigos tipo 0503-001-001) se emiten
por las direcciones del Instituto.

**Este proyecto (agentes y humanos del repo) sólo realiza trabajo técnico**:
redactar borradores, verificar fuentes, mantener trazabilidad. Nunca promulga.

## Ediciones propuestas

1. **política-agentes.md §7.2** — sustituir la frase final del párrafo:
   ~~"En este proyecto, el rol humano es justamente ese — aportar los
   documentos/iniciativas y ejercer la autoridad de promulgación; el trabajo
   de redacción, verificación y trazabilidad lo ejecuta el agente…"~~
   por: "La promulgación/emisión de normas es potestad institucional del IMSS
   (áreas normativas y sus titulares; cadena RIIMSS art. 6-VI y 75). En este
   proyecto, el rol humano aporta documentos/iniciativas y hace la interface
   institucional; agentes y humanos del repo sólo ejecutan el trabajo técnico
   de redacción, verificación y trazabilidad. **Nadie en este repo promulga.**"
2. **§9 política** y **roles-r1.md** — renombrar el rol "humano-promulgador"
   → **"enlace institucional"** (interino): aporta fuentes, decide criterios
   internos del repo, y canaliza (nunca emite) actos normativos. Conservar la
   prohibición de autoasignación por agentes.
3. **ADR-0005** — reclasificar la capa e.firma: la e.firma sólo firmaría actos
   **cuando el instituto lo disponga por la cadena competente**; por sí sola,
   la tenencia de e.firma por un miembro del equipo NO constituye autoridad de
   promulgación. Mantener las dos capas (proveniencia git / firma legal).
4. **AGENTS.md** pie: sin cambios sustantivos (ya no usar "promulgador").

## Reglas de adopción

- Cambio de política → requiere decisión humana + ronda adversarial (§6).
  Por ser corrección que **estrecha** pretensiones (alinea con fuente y con la
  realidad institucional) se propone quorum-lite; si el humano lo pide,
  multi-provider.
- Al aprobarse: aplicar ediciones 1–3 en un PR `docs(enmienda)`, actualizar
  `roles-r1.md` (nueva fila de renombrado, sin borrar historia) y superseder
  el fact AN-KLA correspondiente.

## Pendiente adicional

- `0503-001-001.pdf` (norma/manual institucional serie 05xx): bloqueado por
  Incapsula y sin capture en Wayback. El humano lo depositará en
  `docs/fuentes/imss/`; al llegar, se registra con su procedencia.
