# Autorización de fuentes y multi-provider (R1-E0-02)

**Estado:** vigente · **Fecha:** 2026-08-10 · **Quién autoriza:** Kristhian Manuel
Jiménez (roles interinos §9 — `docs/roles-r1.md`).  
**Plan:** `docs/plan-r1-90d.md`. **No sustituye** verificación artículo por artículo.

## 1. Canales autorizados para **analizar** y registrar procedencia

| Canal | URL | Uso autorizado en R1 |
|-------|-----|----------------------|
| DOF (Diario Oficial de la Federación) | https://dof.gob.mx/ | Consulta / descarga de evidencia de **publicación y reforma** (candidato a **nivel 1** primario cuando el permalink/acto concreto se registre en `corpus/registry.yaml`) |
| Orden Jurídico Nacional | https://www.ordenjuridico.gob.mx/ | Consulta / análisis de textos y referencias **públicas**; **no** se asume automáticamente = DOF nivel 1 sin trazar el acto en DOF |
| Cámara de Diputados, Biblioteca de Leyes | https://www.diputados.gob.mx/LeyesBiblio/index.htm | Consulta / análisis de índice, textos consolidados y páginas de reformas **públicos** (nivel 2 informativo); cada publicación o reforma federal requiere traza del acto DOF para sostener un claim de nivel 1 |

### Reglas

1. **Autorizar el canal ≠ verificar un artículo.**  
   `procedencia_primaria_verificada: true` en el registry solo tras evidencia
   concreta del acto y su alcance; no acredita vigencia actual.
2. Jerarquía y duda: política §7; en duda → `[VIGENCIA-NO-VERIFICADA]`.
3. Preferir **permalink o identificador estable** del acto (DOF) al copiar URLs de
   búsqueda genéricas.
4. Hash SHA-256 + `fecha_consulta` al cargar archivos al corpus (metodología:
   **`docs/fuentes-legal-mx.md`**; campos en `corpus/registry.yaml`).
5. **Sin copia verbatim masiva** a memoria AN-KLA; la memoria apunta al doc.
6. Niveles y score multi-eje: `docs/fuentes-legal-mx.md` §2 y §6;
   diseño gate: `docs/propuestas/gate-confianza-multieje-v1.md`.

## 2. Multi-provider (rondas adversarial / extracción)

**Autorizado:** rutear a proveedores del quórum **únicamente**:

- docs de gobernanza del repo;
- textos y extractos de **fuentes públicas** federales ya clasificadas como
  públicas en el corpus / esta autorización.

**Allowlist de proveedores/CLIs (M5) — ampliar solo por enmienda a este doc:**

| CLI / superficie | Familia / notas |
|------------------|-----------------|
| `claude` (Anthropic) | Revisión adversarial |
| `codex` (OpenAI) | Revisión adversarial |
| `opencode` con `zai-coding-plan/glm-5.3-flash` (Z.ai / GLM) | Únicamente revisión adversarial del **diff filtrado** de cuatro archivos de este expediente frente a `main` `51b3580`: `corpus/registry.yaml`, `docs/autorizacion-fuentes-r1.md`, `docs/fuentes-legal-mx.md` y `docs/evidencia/fuentes-publicas-complementarias-2026-10-10.md`, con extractos públicos estrictamente necesarios. Excluir la nota de la ronda anterior para preservar revisión ciega. No enviar archivos completos, CTIM, PDF locales, material interno ni datos personales. Usar ruta directa Z.ai y registrar modelo/proveedor reportados |
| `ollama` local con `qwen3:8b` (familia Qwen, desarrollada por Qwen/Alibaba Cloud) | Únicamente revisión adversarial del mismo diff filtrado y extractos públicos; endpoint loopback `127.0.0.1:11434`. No autoriza Ollama Cloud, otros modelos, archivos completos, CTIM, PDF locales, material interno, datos personales ni ingesta. Registrar modelo reportado y digest del artefacto local; el digest identifica el artefacto observado, no certifica origen de pesos |
| Otros (kimi, gemini, otros modelos de Qwen, cline, otras combinaciones de opencode/modelo, …) | Solo si el admin confirma disponibilidad y se añade fila aquí |

Si un CLI no está en la tabla: **no** enviar corpus legal hasta enmienda.

**No autorizado (default):**

- manuales, procedimientos o datos **internos / confidenciales IMSS** u otras
  entidades;
- datos personales;
- cualquier path que el router §7.4 clasifique como `personal` o
  `interno_institucional` (v1: denegado).

Cuando se necesite material interno: **nueva autorización escrita** + harness
router (plan E7), no ampliar esta nota en silencio.

## 3. R1-E0-03 — Umbral de falsos positivos del auditor

**Decisión (2026-08-10):** la idea del umbral FP es **aceptada en principio**, pero
**diferida** hasta que existan trabajos concretos del auditor (H3: CLI + fixtures +
al menos una matriz FP/FN con pasadas reales).

Hasta entonces:

- no se publican promesas de “auditor confiable” al exterior;
- el piloto es **exploratorio**;
- el PO (interino) fijará umbral numérico o cualitativo en ticket futuro
  `R1-E0-03` cuando haya datos.

## 4. Historial

| Fecha | Evento |
|-------|--------|
| 2026-08-10 | Autorización canales DOF + Orden Jurídico; multi-provider solo público; E0-03 diferido |
| 2026-10-10 | El Operador autorizó incorporar LeyesBiblio como canal complementario público de consulta y análisis; se conserva DOF como ancla de publicación/reforma y la restricción de material interno/proveedores |
| 2026-10-10 | El Operador indicó usar GLM por OpenCode/Z.ai para revisar este cambio si Ollama no está disponible; esta autorización del proveedor no altera por sí misma los canales: LeyesBiblio se incorporó mediante la decisión precedente |
| 2026-10-10 | El Operador autorizó Qwen local `qwen3:8b` como tercera familia subyacente para la ronda de este expediente; sonda loopback HTTP 200 con respuesta `PONG`, sin ampliar autorización de fuentes o ingesta. `/api/tags` reportó digest local `500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41`; Qwen atribuye la familia a Qwen/Alibaba Cloud en https://github.com/QwenLM/Qwen3 |
