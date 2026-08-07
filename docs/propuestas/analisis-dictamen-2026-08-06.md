# Síntesis de análisis — Dictamen Plataforma de inteligencia normativa (2026-08-06)

> **Artefacto de decisión.** Síntesis de dos análisis independientes en contexto fresco
> (subagentes) + este sintetizador. **Brecha single-provider (CAGF-A2) declarada**: el
> quórum alcanzable es débil en sustancia (misma arquitectura/mismo proveedor), aunque
> tenga la *forma* del §6. Las **claims normativas del dictamen NO están verificadas**
> (§7): se listan aparte las que deben validarse contra fuentes oficiales antes de
> adoptarse como hecho. Este documento **no adopta** la propuesta; expone qué decidir.
> Autoridad que adopta = el humano orquestador (§5/§7.2).

**Input:** `docs/propuestas/2026-08-06-dictamen-plataforma-normativa-input.md` (verbatim).

## Veredicto conjunto
**Adoptar-con-condiciones.** La dirección arquitectónica es sólida (registro normativo
temporal + verificador determinista de citas + PostgreSQL-first + no-chatbot-primero),
PERO: (a) el dictamen confunde "visión de estado final" con "primer paso ejecutable";
(b) la "Fase 0 de bajo riesgo" arrastra ~70 % de la Fase 1; (c) presenta claims
normativas específicas como hechos; (d) la **gobernanza actual no ampara decidir esto
ni gobernar el sistema futuro** (7 de 11 requisitos en vacío). No adoptar bajo el
quórum single-provider actual sin antes formalizar las extensiones 1–3 (ver Gobernanza).

## Adoptar (alta confianza — principios de diseño/proceso, no requieren verificación legal)
- Separar **vigencia** de **aplicabilidad** (evita devolver texto "vigente" desplazado por sentencia).
- **Verificador determinista de citas** post-generación (la política §7 ya exige verificación externa, no introspección).
- **PostgreSQL + JSONB + tsvector + pgvector** como base; Elasticsearch/grafo sólo cuando una métrica lo justifique.
- **Transitorios como objetos de primera clase** (entrada en vigor diferida, supervivencia temporal).
- **Reconciliación DOF↔Cámara** como control cruzado (Cámara = detector de errores, no dependencia).
- **Lookup exacto** de identificadores + artículo como unidad + "no chatbot primero" (auditor/impacto > chatbot).

## Desafiar (sobreestimado, costoso o no verificado)
- **"Fase 0 — Auditor normativo, bajo riesgo" es circular:** detectar citas obsoletas/NOM sustituidas requiere corpus indexado + lookup + motor temporal + registro de NOM ≈ componentes B+C+D de la propia arquitectura. Reduce riesgo *de generación*, no de infraestructura.
- **Falsos positivos del auditor:** marcar como obsoleta una cita válida tiene coste reputacional directo en un organismo público. Sin umbral de "tasa de falsos hallazgos" ni plan si se excede, el riesgo no es bajo; es *diferente*.
- **Operadores jurídicos deónticos** (sujeto/modalidad/acción/objeto/condiciones): NLP difícil, alta tasa de error; capote diferible, no requisito de Fase 1.
- **Bitemporalidad plena "desde el inicio":** sobre-ingeniería. Fijar *versiones inmutables + vigencia_desde/hasta + registrado_en*; bitemporalidad plena gated by caso de uso real.
- **"Jerarquía DOF>Cámara>SCJN" mezcla ejes** (publicación vs consolidado vs fuerza interpretativa); ordenar por *función*, no por "nivel".
- **"Coincidencia → publicación automática":** DOF y Cámara coincidir no descarta bug del parser ni error compartido; en alto impacto, auto-publicar sin revisión es riesgo evitable.
- **Golden set "validado por juristas":** hoy no hay equipo jurídico (1 humano + agentes); es dependencia humana oculta.
- **Parser de decretos asumido resoluble:** las reformas MX ("recorriéndose la numeración…") son notoriamente difíciles; sin tasa de error base ni plan de medición, el compilador normativo es la parte más riesgosa.

## Ciega — lo que el dictamen NO resuelve
- **Gobernanza del corpus:** ¿quién tiene autoridad jurídica sobre qué entra y con qué criterio? Sin mandato ni proceso de desempate.
- **Licenciamiento/procedencia de los repos OSS** (`ingteranalvarez/lex-mx`, `JoshuaPozos/leyes-mexicanas-markdown`) antes de usarlos como semilla.
- **Datos institucionales IMSS** (Normateca, manuales): no son ni norma pública ni secreto; sin gobernanza de alcance/acceso/retención (§7.1).
- **Sostenibilidad del cuello de botella humano** de reconciliación ante volumen de reformas.
- **Sin DoD verificable** para el primer entregable (§2 de la política exige contrato ejecutable, no fases).

## §7 — claims del dictamen que DEBEN verificarse antes de adoptarse como hecho
- `"publicacion_dof": "2025-01-15"`, `"vigencia_desde": "2025-01-16"` → DOF (¿ilustrativas o reales?).
- Identificador `"LSS:251:I"` y su jerarquía (art. 251 fracción I, "seguridad_social/IMSS") → LSS vigente (Cámara/DOF).
- "La Cámara de Diputados declara carácter informativo" → aviso legal vigente de la Cámara.
- `"obligatorio_desde": "2023-10-23"`, `"epoca": "Undécima"`, registro `SJF:2027495` → SJF.
- Jerarquía y fuerza de tesis/jurisprudencia/precedente → legislación orgánica del Poder Judicial + reglas del Semanario.

## Gobernanza — veredicto
La gobernanza actual basta para **el trabajo del agente en el repo** (artefactos, fidelidad
documental §7, git §5, adversarial de corrección §6). **No basta para (1) DECIDIR esta
propuesta ni (2) GOBERNAR el sistema futuro.** Adoptar el dictamen = hito de alto impacto
(§6); el quórum-3 exigido es alcanzable en forma pero débil en sustancia (single-provider).

| Requisito (dictamen §12/F) | Estado | Brecha |
|---|---|---|
| Responsable del corpus | VACÍO | sin rol continuo de data steward |
| Responsable jurídico | VACÍO/PARCIAL | hay revisión puntual, no rol permanente |
| Resolución de discrepancias de fuentes | VACÍO | §7.2 resuelve entre *leyes*, no entre *fuentes* de la misma ley |
| Bitácora de cambios normativos | PARCIAL | AN-KLA beta (sólo `add`) no es registro estructurado |
| Aprobación humana | PARCIAL | normas: cubierto; **despliegue: vacío** |
| Niveles de confianza en respuestas | VACÍO | §7 es binario (cita/no-cita) |
| Identificación agente+modelo | PARCIAL | en reportes al orquestador; no en runtime |
| Registro de evidencia por conclusión | PARCIAL | linaje de artefactos, no de conclusión servida |
| Golden set / evaluación jurídica | VACÍO | las DoD son técnicas, no de dominio jurídico |
| Datos institucionales/personales | PARCIAL | personales cubiertos; confidenciales institucionales no |
| Compuertas deterministas (verificador) | VACÍO | la política sólo conoce gates adversariales (§6) |

**5 extensiones críticas antes de ejecutar cualquier fase:** (1) proceso de decisión
estratégica (ADR) + rol product owner; (2) roles operativos continuos (corpus owner,
responsable jurídico, data steward); (3) compuertas deterministas + niveles de confianza;
(4) gobernanza de evaluación/golden set jurídico; (5) capa de gobernanza de sistema
desplegado/runtime.

## Decisiones que SÓLO el humano puede tomar (bloquean avanzar)
1. **Dominio piloto:** ¿federal general? ¿IMSS? ¿otro organismo? ¿una sola ley?
2. **Alcance funcional:** ¿sólo lectura/auditoría, o también generación de texto normativo?
3. **Responsable jurídico del corpus** (persona/rol con autoridad para desempatar discrepancias).
4. **Custodio del corpus** (data steward continuo).
5. **Usar o no repos OSS** como semilla (implica auditar licencia/procedencia antes).
6. **Asumir el riesgo del quórum single-provider** para esta decisión, o posponer hasta fortalecer gobernanza.

## Checklist de documentos/solicitudes (lo que necesito del humano)
- **La propuesta ORIGINAL** que evalúa el dictamen (no la tengo; el dictamen la referencia).
- **El "análisis adjunto"** que el dictamen cita ("coincide con el análisis del archivo aportado").
- Confirmación de si los identificadores/fechas del dictamen (`LSS:251:I`, `2025-01-15`, `SJF:2027495`…) son **ilustrativos o reales**.
- Si **IMSS**: autorización institucional para Normateca/manuales internos; inventario de **15–30 procedimientos piloto** de una familia operativa; organigrama/denominaciones vigentes.
- Confirmar acceso a fuentes públicas (DOF, Cámara de Diputados, SCJN/SJF) y el texto exacto del aviso "informativo" de la Cámara.
- Disponibilidad de **equipo jurídico** para el golden set (si no hay, declarar Fase 3/4 diferidas).
- Decisión sobre los **repos OSS** (auditar antes de usar).

## MVP honesto (mínimo demostrable hoy: 1 humano + agentes, sin backend)
1. **Una sola norma** (p. ej. LSS o CPEUM), texto consolidado en Markdown en git, particionado por artículo/fracción con identificadores estables.
2. **Lookup exacto determinista** `artículo:fracción → texto + metadatos mínimos (vigencia_desde/hasta, fuente DOF)` como CLI/scripts (sin Elasticsearch, sin vector todavía).
3. **Verificador de citas determinista** (no LLM) sobre ese corpus único: dada una cita en un documento piloto, responde existe/no-existe + vigente/derogado. Validation set pequeño (decenas de casos), alcanzable por 1 humano.
4. **Auditor de UN documento piloto** real contra esa norma: detectar citas obsoletas y **medir tasa de falsos positivos antes de prometer nada**. Entregable = evidencia, no infraestructura.
5. Cada elemento ambicioso del dictamen (bitemporalidad, operadores deónticos, jurisprudencia como subsistema) queda **gated by "cuando el MVP lo justifique"**.

## Próximo paso recomendado
**No construir plataforma todavía.** Secuencia sugerida:
1. El humano responde las **decisiones 1–6** (sobre todo dominio piloto + alcance + responsable jurídico).
2. Se **extiende la gobernanza** (extensiones 1–3 mínimas) y se registra la decisión en un **ADR** (nuevo artefacto).
3. Se ejecuta el **MVP honesto** sobre una sola norma como spike de aprendizaje, midiendo falsos positivos.
4. Con esa evidencia, se decide si se adopta formalmente la hoja de ruta del dictamen (Fases 0–5).

> Este artefacto es **soporte de decisión**, no la decisión. La adopción es autoridad del humano (§7.2: redactar/analizar ≠ promulgar).
