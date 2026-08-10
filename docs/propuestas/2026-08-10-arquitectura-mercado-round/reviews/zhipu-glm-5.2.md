**Revisión ciega — Zhipu/GLM vía OpenCode**

Proveedor: **Zhipu (GLM)**. Modelo subyacente exacto: **glm-5.2** (`zai-coding-plan/glm-5.2`).
Conflicto de interés: ninguno además de ser uno de tres revisores externos; el autor (OpenAI/Codex) está excluido de votar y no contribuí al `INPUT.md`.

---

[HIGH] Hazard de agregación instrumento↔disposición ya presente y sin mitigación de consumo — evidencia (registry.yaml:323 `vigencia_verificada:true` a nivel *instrumento* LFEP; :320 `f5:false` para LFEP:5; INPUT.md:55-59 lo identifica) — fix prescrito: antes de servir cualquier `EvidenceEdge` a agentes, migrar/anotar el booleano de instrumento a nivel disposición (o marcar LFEP:5 como no-heredable); el cambio de «unidad autoritativa» (INPUT.md:71-72) debe materializarse en datos, no sólo en tesis.

[MED] `EvidenceEdge v0` omite el alcance de la traza a nivel disposición, reintroduciendo el hazard que el proyecto ya padece — evidencia (INPUT.md:76-78 enumera campos sin alcance de traza; gate-confianza-multieje-v1.md:48-50 exige que `cubre_disposiciones` incluya el id citado para `alto`) — fix prescrito: añadir `traza_cubre_disposicion` (bool + `disposicion_id` + `identificadores_diario`) al contrato del edge; sin este campo una arista hereda vigencia de instrumento y contradice la regla `alto` del gate.

[MED] `clase_de_afirmacion` listada pero la taxonomía no distingue extracto textual de inferencia jurídica interpretativa — evidencia (LFEP-005.json:33-36 `menciona` verificada:true = hecho textual; :38-43,:45-49,:50-55 `remite`/`relaciona` verificada:false = inferencia; INPUT.md:76 «clase de afirmación» sin taxonomía) — fix prescrito: enum mínimo `{extracto_textual, referencia_normativa_explicita, inferencia_juridica}`; la semántica de verificación y el default de traversabilidad dependen de la clase.

[MED] «Tiempo de validez» del edge sin granularidad ni vinculación a la traza de la disposición — evidencia (INPUT.md:77 «tiempo de validez»; registry.yaml:299-305 traza LFEP:1 publicación vs :314-321 LFEP:5 reforma 2025-07-16) — fix prescrito: el campo temporal del edge debe referir la traza de la disposición concreta (fecha + `identificadores_diario` + `cubre`), nunca `ultima_reforma_cuerpo`.

[LOW] Posicionamiento «verificable» (capacidad) es defendible; «verificada»/«infraestructura probada» no lo es aún — evidencia (gate-confianza-multieje-v1.md:67 `alto` prohibido hasta F1-F4+H1; registry.yaml:320 f5:false) — fix prescrito: mantener el adjetivo «verificable», evitar «verificada»/«probada» en comunicaciones hasta que la cadena IMSS (LFEP:5 incluido) alcance F5=true; el orden propuesto (INPUT.md:92) ya secuencia esto.

---

**Decisión: proceed**

La decisión es epistémicamente disciplinada (hipótesis no hecho; evita claims de competencia), respeta R1 (difiere bitemporalidad, ejecutable y dependencia AKN) y secuencia el cierre de deuda (F5 LFEP:5, H1/H5) antes del serving a agentes. Los hallazgos son especificaciones requeridas para `EvidenceEdge v0` y mitigación de datos —no compuertas sobre la dirección— y deben cumplirse al ejecutar los pasos 3-4 del orden propuesto.

