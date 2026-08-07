# Review adversarial — kimi (Moonshot) — componente F (verificador)

> Ronda multi-provider sobre D+F · 2026-08-06. Conflicto de interés: proveedor del quórum.

---

• Voy a leer los archivos relevantes para la revisión.

• ## Hallazgos

  - [BLOCKER] **v1 emite nivel `alto`, violando la prohibición expresa del Cambio 2** — `verify_citations.py:56`: `result["response_status"] = "alto" if vig_ok else "medio"`, con `vig_ok` leído en línea 54 de `m.get("vigencia", {}).get("verificada_contra_dof_nivel1", False)`. La enmienda (enmienda.md:31) dice para **v1: "Prohibido emitir nivel `alto`"**, sin excepción: en v1 no hay corpus temporal y la vigencia **no se verifica** contra DOF; aquí basta con que el JSON del corpus auto-declare `verificada_contra_dof_nivel1: true` (un bit editable por el mismo pipeline que se audita) para que el gate emita `alto`. El propio docstring (línea 10) contradice el código: "tope 'medio' cuando (a)+(c)+(d) OK". — Fix: en v1, forzar tope `medio` incondicional (`response_status = "medio"` cuando (a)+(c)+(d) OK, nota `[VIGENCIA-NO-VERIFICADA]`) y mover la rama `alto` a v2.
  - [HIGH] **Falso positivo con cita de sólo espacios/blancos** — `verify_citations.py:50-51`: `if cita:` evalúa `" "` como truthy y `_normalize(" ")` devuelve `""`; luego `"" in _normalize(texto)` es `True`, por lo que (c) pasa con una cita efectivamente vacía y, si (d) pasa, se emite `medio`. — Fix: `nc = _normalize(cita); result["quote_exact_match"] = bool(nc) and nc in _normalize(texto)`.
  - [HIGH] **El match es subcadena, no "exacto" como declara el docstring (línea 11)** — línea 51: `_normalize(cita) in _normalize(texto)`. Un fragmento trivial ("la ley definirá", o una sola palabra) pasa como "cita verificada". El Cambio 2 exige que "el fragmento citado **coincida** con el corpus" — subcadena es una lectura defendible, pero el gate está etiquetado como "exacto normalizado", promete más de lo que hace, y es gameable con citas mínimas fuera de contexto. — Fix: renombrar a `quote_substring_match` y/o exigir umbral mínimo (p. ej. ≥ N palabras o ratio de cobertura), declarado en docstring.
  - [MED] **`source_resolved` (d) sólo verifica presencia truthy de sha256, no resolución** — línea 52: `any(f.get("sha256") ...)`. Acepta cualquier cadena no vacía (incl. `" "`); no valida formato (64 hex) ni que el archivo referenciado exista ni que el hash coincida con él. Para v1 "fuente resuelta (sha256)" es marginalmente aceptable como chequeo de presencia, pero un sha256 inválido pasa el gate. — Fix: validar formato (`re.fullmatch(r"[0-9a-f]{64}", ...)`) y, si es viable, existencia del archivo en `fuentes_oficiales[].archivo`.
  - [MED] **Crashes (traceback) ante JSON con nulos en lugar de fail-closed limpio** — líneas 49, 52, 54: si el modelo trae `"texto_verbatim": null`, `"fuentes_oficiales": null` o `"vigencia": null`, `m.get("vigencia", {})` devuelve `None` y `.get(...)` lanza `AttributeError`. El proceso sale con código ≠ 0 (fail-closed por accidente, no por diseño) y sin el `response_status: bajo` que el Cambio 2 (enmienda.md:36) exige ante fallo del verificador. Igual si `claim` no es un objeto (línea 31). — Fix: normalizar con `or {}`/`or []` y envolver la verificación en try/except que devuelva `bajo` + nota de error.
  - [LOW] **Marcadores de vigencia inconsistentes entre artefactos** — resultado usa `"N/A_v1"` (línea 40), la nota usa `[VIGENCIA-NO-VERIFICADA contra DOF nivel 1]` (línea 58) y la enmienda define el default como `[VIGENCIA-NO-VERIFICABLE]` (enmienda.md:31). Tres cadenas distintas para el mismo estado dificultan parsing downstream. — Fix: unificar al marcador de la enmienda.
  - [LOW] **JSON de entrada malformado aborta con traceback** — línea 71: `json.loads` sin manejo de error; sale código 1 pero sin salida estructurada `bajo`. — Fix: try/except → emitir resultado `bajo` con nota.

  ## Punto fuerte

  Determinismo real extremo a extremo dentro del gate: sólo stdlib (`unicodedata`, string ops), cero LLM, cero heurística oculta; la normalización NFKD + strip de diacríticos + lower + colapso de espacios (líneas 22-27) está **declarada** en el docstring (línea 11). La dirección de fallo es la correcta en los caminos felices: cita vacía, `disposicion_id` ausente o no encontrado, y ausencia de fuentes degradan a `bajo` (líneas 44-47, 60), y el exit code (línea 74) es coherente con `bajo` = no-emisión (exit 1 sólo para `bajo`, 0 para `medio`/`alto`). La normalización insensible a acentos/mayúsculas es la elección correcta para texto jurídico mexicano extraído por parser (casing con artefactos, como advierte el propio `lineage.notas` del JSON).

  ## Decisión: [ ] proceed | [x] fix-and-retry | [ ] escalate

  El BLOCKER de la línea 56 (emisión de `alto` en v1) bloquea por sí solo según la regla de agregación del Cambio 1 (enmienda.md:20). Los fixes son acotados y mecánicos; no hace falta escalación humana, sí re-verificación tras el fix (incl. tests ejecutables del gate, que el propio Cambio 2 exige como DoD, enmienda.md:37).

  ## Nota residual (conflicto de interés)

  Soy Kimi/Moonshot, proveedor que participa en el quórum §6 de esta gobernanza: mi veredicto sobre el componente F incide en un corpus que eventualmente auditará salidas mías. Adicionalmente, la ronda multi-provider pendiente sobre "otro artefacto" (DoD transversal, enmienda.md:60) podría usar precisamente este verificador como artefacto — esta revisión cuenta como un lente de ese quórum, no como validación completa. Mitigación declarada: hallazgos citados línea a línea y verificables de forma determinista por cualquier otro proveedor o por el humano reconciliador.

