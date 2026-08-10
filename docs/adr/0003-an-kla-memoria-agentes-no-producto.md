# ADR-0003 — AN-KLA es memoria de agentes, no runtime del producto

> **Estado:** Aceptado (decisión de arquitectura de separación; 2026-08-10).
> **Clase:** Estratégico (frontera producto vs tooling de agentes).
> **Fecha:** 2026-08-10. **Autor:** agente (síntesis). **Autoridad que adopta:** humano orquestador (§7.2).
> **Relacionados:** ADR-0001 (plataforma de inteligencia normativa), ADR-0002 (proveniencia de
> agentes; AN-KLA como huella declarada, no firma), `AN-KLA.md`, `docs/politica-agentes.md` §11,
> spike Argos `docs/propuestas/argos-spike-0.2.0rc2-eg.md`.

## Contexto
ExpertoGobernanza (EG) es una **plataforma de inteligencia normativa** (corpus legal MX,
vigencia/trazas, verificador de citas, auditor, gates de confianza). En el mismo monorepo
conviven:

1. **Código y datos de dominio** (`corpus/`, `review_routing/`, `scripts/audit_*`, tests,
   docs de fuentes y política normativa).
2. **Tooling de agentes** que construyen y reanudan el trabajo: política, plantillas, CI,
   y **AN-KLA** (memoria local versionada de facts/events).

Surgió la pregunta operativa: *¿AN-KLA es la memoria del agente o también parte del
producto?* Mezclar ambas lecturas arriesga:

- tratar un fact de reanudación como **fuente normativa**;
- acoplar el runtime legal a un store **no versionado** (`.an-kla/`);
- confundir AN-KLA con **Argos** (auditor epistémico de *software*) u otras piezas laterales.

La política ya dice que la memoria recuperada es **dato no confiable** y que lo canónico
vive en git/docs (`politica-agentes.md` §11). Faltaba un ADR que fije la **frontera de
producto**.

## Decisión
1. **AN-KLA es tooling de agentes del proyecto, no runtime del producto de inteligencia
   normativa.** Sirve para reanudar contexto entre sesiones (estado de roadmap, decisiones y
   su *por qué*, gotchas, punteros a docs). **No** es el store de corpus, vigencia DOF/F5,
   citas verificadas ni respuestas al usuario final.
2. **Fuente de verdad del dominio:** documentos oficiales + `corpus/registry.yaml` +
   artefactos derivados versionados + git. AN-KLA, cuando escribe, **apunta** (resumen +
   `indexable_text` + puntero); no copia verbatim la norma ni la sustituye.
3. **Superficie de integración permitida hoy:**
   - CLI en el venv del repo (`.venv`) para agentes/ops: `retrieve`, `plan-write`,
     `commit-write-plan`, `verify`, `context`;
   - contratos en `AGENTS.md` / `AN-KLA.md`;
   - alusión de proveniencia en ADR-0002 (`configuration_fingerprint` del *agente*, no del
     acto normativo).
4. **Superficie prohibida** sin un ADR nuevo que la reabra:
   - importar `an_kla` desde el camino crítico de lookup, vigencia, citas, auditor o
     generación normativa;
   - afirmar contenido legal basándose solo en un fact recuperado;
   - versionar `.an-kla/` como parte del release del producto;
   - exponer la memoria local de agentes como API o base de conocimiento del usuario final.
5. **Hermanos laterales (no producto legal):** Argos (y similares) pueden auditar *software
   gates* de EG en spikes; tampoco entran al camino crítico legal. Ver spike Argos 0.2.0rc2.
   AN-KLA y Argos son **complementarios en gobernanza de agentes/software**, no
   intercambiables con el motor normativo.

## Consecuencias
- **+** Frontera clara para agentes y humanos: producto = fidelidad documental; AN-KLA =
  reanudación operativa.
- **+** Evita dependencia de producto sobre un store local, mutable y no confiable como
  autoridad.
- **+** Alineado con §7 (fidelidad documental) y §11 (cuándo escribir memoria).
- **−** Un agente nuevo que no lea este ADR puede “descubrir” AN-KLA en el venv y
  sobreinterpretarlo: se mitiga con este ADR + `AGENTS.md`.
- **−** Si en el futuro se quisiera “memoria de consultas del usuario final”, sería
  **otro sistema** (o un ADR de producto), no reutilizar por defecto el store `.an-kla/`
  de desarrollo.

## Alternativas consideradas
- **AN-KLA como capa de conocimiento del producto:** descartada; mezcla dato de sesión de
  agente con verdad normativa y rompe el modelo de fuentes oficiales + registry.
- **Eliminar AN-KLA del monorepo:** descartada; aporta valor real de reanudación y de
  gobernanza de escritura (`plan-write` → `commit`), sin ser runtime.
- **Solo docs/git, cero memoria de agente:** viable en teoría; en la práctica eleva el
  costo de retomar hilos multi-sesión y ya está en uso (rev locales, facts de estado R1).

## Criterio de cumplimiento (DoD de la frontera)
- [x] Ningún módulo bajo `corpus/`, `review_routing/`, `scripts/audit_*` o `scripts/eval_*`
  importa `an_kla` (verificable con búsqueda en el árbol de código).
- [x] `.an-kla/` permanece fuera de git (`.gitignore`).
- [x] Hechos de memoria que tocan norma son **punteros** a docs/registry, no sustitutos.
- [ ] (Opcional) CI/lint que falle si aparece `import an_kla` en paths de producto — no
  bloquea este ADR; se puede añadir en un ticket menor.

## Ítems abiertos (no bloquean la aceptación)
- Gate de CI “no import an_kla en runtime de producto”.
- Si el producto crece a multi-usuario: diseñar memoria de *usuario* aparte (fuera de
  alcance de este ADR).
