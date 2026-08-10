# Relatoría — arquitectura, no-herencia y EvidenceEdge v0 — 2026-08-10

> **Estado general:** OK técnico · pendiente commit del administrador  
> **Autor/relator:** OpenAI/Codex (GPT-5) · **Orquestación:** humana  
> **Fase:** R1 · **Quórum final:** Anthropic + Moonshot + Zhipu/GLM  
> **Expediente asociado:** `docs/gobernanza/expediente-probatorio-rondas-2026-08-10.md`

## 1. Motivo

La conversación partió de un análisis externo sobre productos de investigación
jurídica con IA y derivó en dos preguntas: cuál debía ser la diferenciación
arquitectónica del proyecto y si Akoma Ntoso aportaba valor inmediato. La
respuesta provisional fue priorizar afirmaciones verificables y cerrar primero
los riesgos ya presentes en el corpus, dejando AKN como opción posterior.

## 2. Participantes y roles

| Participante | Rol |
|---|---|
| Humano/orquestador | autorizó avances, descartó Google y conserva autoridad de adopción |
| OpenAI/Codex | autor de propuesta, implementación y reconciliación; excluido del voto |
| Anthropic / Claude Sonnet 5 | revisor adversarial externo |
| Moonshot / Kimi K3 256K | revisor adversarial externo |
| Zhipu / GLM-5.2 vía OpenCode | sustituto de Google y revisor externo |
| Google / Gemini | primer intento inválido; recuperación posterior también descartada por el humano |

No se usaron subagentes internos para votar. Las revisiones se ejecutaron con
CLIs externas y modelos subyacentes identificados, conforme al criterio de
decorrelación por proveedor/modelo.

## 3. Cronología

### F0 — Preparación de la ronda de arquitectura

Se construyó una entrada común con panorama competitivo, estado real del corpus,
hipótesis de diferenciación, propuesta `EvidenceEdge` y dudas sobre AKN. El autor
fue excluido de la votación. Los bundles se clasificaron como públicos y no
incluyeron manuales IMSS ni información interna/confidencial.

### F1 — Ronda arquitectura/mercado

Anthropic, Moonshot y Zhipu/GLM emitieron revisiones válidas. El primer intento
Google devolvió contenido ajeno a la entrada; se conservó como evidencia
inválida y no contó como voto. El intento de recuperación también fue descartado
por decisión humana. Zhipu/GLM vía OpenCode completó el tercer proveedor válido.

Decisiones:

| Proveedor | Decisión | Hallazgo convergente |
|---|---|---|
| Anthropic | `fix-and-retry` | no-herencia y alcance probatorio |
| Moonshot | `fix-and-retry` | no-herencia, taxonomía y orden EvidenceEdge→AKN |
| Zhipu/GLM | `proceed` con fixes | materializar la mitigación antes de serving |

La mayoría produjo `fix-and-retry`. Se conservaron también los hallazgos del voto
minoritario. La reconciliación fijó este orden: no-herencia por disposición,
`EvidenceEdge v0`, benchmark IMSS falsable y sólo después spike AKN.

### F2 — Primer fix: vigencia por disposición

Se implementó `resolve_disposicion_vigencia` con default negativo. El booleano
agregado del instrumento quedó documentado como resumen no autoritativo. Se
congelaron estas diferencias:

- `LFEP:1=true` frente a `LFEP:5=false`;
- `LSS:5=true` frente a `LSS:1=false`;
- disposición ausente o entrada incompleta = `false`.

Durante una revisión de sólo lectura, OpenCode instaló PyYAML en `.venv` pese a
la instrucción. La instalación incidental se retiró inmediatamente y se verificó
que el paquete ya no estuviera presente. No hubo modificación versionada por
ese incidente.

### F3 — Contrato inicial EvidenceEdge v0

Se implementó un contrato JSON/YAML plano, sin base de grafos, AKN, LLM ni nueva
dependencia. Las clases se cerraron en seis categorías y los estados de
verificación en cuatro. Sólo `is_traversable` podía autorizar consumo.

La primera ronda de implementación produjo `fix-and-retry` en los tres
proveedores. Los principales defectos encontrados fueron:

- evidencia nivel 3/4 aún podía sostener `verified`;
- `covers_object=not_applicable` eludía cobertura;
- un sujeto instrumento podía usar la traza de una disposición;
- interpretación jurídica y texto devolvían el mismo booleano;
- fechas incoherentes y IDs con `|` no estaban bloqueados.

### F4 — Primer lote de correcciones y retry

Se exigieron nivel 1/2, granularidad artículo/párrafo, cobertura triple, sujeto
disposición exacta, fechas ordenadas y léxico cerrado. Las clases
`jerarquia_interpretativa`, `eficacia` y `aplicabilidad` quedaron registrables
pero no recorribles en v0.

Resultado del retry: Anthropic y Moonshot todavía pidieron fixes; Zhipu/GLM dio
`proceed`. Los hallazgos residuales señalaban URL vacía, coverage escalar por
substring, duplicados dependientes del orden y trazas principales incompletas.

### F5 — Segundo lote de correcciones

Se añadió HTTPS con hostname, membresía exacta sobre listas, rechazo de
duplicados, fecha+localizador para traza principal, raíz no-objeto fail-closed y
búsqueda de una traza válida después de coincidencias de alcance instrumento.

En la confirmación, Moonshot y Zhipu/GLM dieron `proceed`; Anthropic encontró un
último HIGH: `traza_disposiciones.f5=true` podía resolver sin fecha,
localizador ni `revision_vigencia` cuando se llamaba al resolver aisladamente.

### F6 — Cierre del último HIGH

La rama autoritativa por disposición se hizo simétrica con las demás: exige
`f5`, cobertura, fecha, URL o identificador DOF y revisión. El validador exige
los mismos campos aun en slices de una sola disposición. Se añadió regresión
específica.

Veredicto final:

| Proveedor | Decisión final |
|---|---|
| Anthropic | `proceed` |
| Moonshot | `proceed` |
| Zhipu/GLM | `proceed` |

No quedaron BLOCKER/HIGH activos. El autor permaneció fuera del voto.

## 4. Resultado de ingeniería

- `corpus/evidence_edge.py`: contrato, validador y gate de recorrido.
- `corpus/registry_rules.py`: resolución de vigencia por disposición.
- `tests/test_evidence_edge.py`: regresiones anti-promoción.
- `tests/test_registry_vigencia.py`: estados vivos y entradas malformadas.
- `corpus/registry.yaml`: estados explícitos de LFEP y LSS.

DoD final observado:

| Check | Resultado |
|---|---|
| Suite completa | 107 tests OK |
| PyCompile | OK |
| YAML | seis fuentes, OK |
| Tamaños | bajo límites duros |
| `git diff --check` | OK |
| Adversarial | `proceed` unánime |

## 5. Decisiones de diseño que permanecen

1. `EvidenceEdge v0` es una atestación estructural; el gate de citas verifica
   bytes, hashes y correspondencia textual.
2. `verified` no se hereda de instrumentos ni nodos.
3. Una reforma posterior a `reviewed_at` obliga a revalidar.
4. Las inferencias jurídicas no son recorribles automáticamente en v0.
5. No hay autorización de serving externo, knowledge graph, Law as Code o AKN.

## 6. Límites de esta relatoría

- Las revisiones de arquitectura están preservadas verbatim; las de
  implementación se preservan como entradas, decisiones y reconciliación, no
  como transcripciones completas.
- Los hashes del expediente corresponden al worktree local antes de commit.
- La relatoría describe hechos de proceso y resultados de software; no certifica
  vigencia normativa ni sustituye al responsable jurídico del corpus.
- La decorrelación alcanzada es de proveedor/modelo, no prueba independencia de
  datos de entrenamiento.

## 7. Próximo paso

El siguiente hito es preregistrar cinco preguntas falsables del eje IMSS que sólo
puedan recorrer aristas válidas. Después, y sólo si el benchmark aporta valor,
corresponde un spike Akoma Ntoso sobre una disposición, con matriz de pérdida y
decisión `adaptador | diferir | no adoptar`.

## 8. Acción solicitada

El administrador debe revisar expediente y relatoría, recalcular los hashes,
aplicar commit/PR y dejar constancia de la revisión Git. Hasta entonces el estado
es `PARCIAL (espera-admin)` aunque el DoD técnico sea OK.
