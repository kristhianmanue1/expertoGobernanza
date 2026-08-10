## Revisión ciega — lente producto/viabilidad

**Proveedor:** Moonshot AI (Kimi). **Modelo subyacente:** `k3-256k` (identificador exacto expuesto por este entorno; la revisión interna del checkpoint no es visible desde el CLI, lo declaro como límite de transparencia). **Conflicto de interés:** Moonshot AI desarrolla agentes que serían consumidores potenciales de una "infraestructura jurídica verificable"; ningún interés financiero en ExpertoGobernanza ni en los proveedores citados. Sesgo posible: simpatía estructural hacia la tesis de infraestructura-para-agentes; lo compenso exigiendo falsabilidad empírica.

---

[HIGH] Diferenciación no falsable tal como está formulada — INPUT.md:66-68 declara el posicionamiento como "hipótesis interna" pero ninguna sección define criterio de muerte ni experimento que la invalide; la propia evidencia (INPUT.md:28) admite que no hay datos sobre competidores — fix: adoptar como experimento mínimo la pregunta demo ya existente "¿por qué el IMSS es OPD?": ejecutarla end-to-end sobre LSS:5 + LFEP:5 + RIIMSS:1 exigiendo que toda arista esté verificada contra traza nivel-1 que cubre la disposición, y repetirla contra Orden Jurídico y un tier gratuito de suite jurídica; si un competidor gratuito responde con igual procedencia verificable, la tesis de diferenciación queda refutada. Hoy el test falla internamente (LFEP-005.json:15 `verificada_contra_dof_nivel1: false`, relaciones `verificada: false` en :41-55), lo cual lo convierte en el falsificador correcto.

[HIGH] `EvidenceEdge v0` omite el campo que prevendría el bug real ya presente en los datos — registry.yaml:323 marca LFEP `vigencia_verificada: true` a nivel instrumento mientras LFEP:5 conserva `f5: false` (registry.yaml:314-321) y el propio INPUT.md:57-59 identifica el riesgo de herencia; el contrato propuesto (INPUT.md:76-79) incluye "estado de verificación" pero no desambigua el alcance — fix: campos mínimos obligatorios `nivel_fuente_evidencia` (1/2) y `cubre_disposicion: bool` por arista, más regla dura de no-herencia: ningún estado de verificación se propaga instrumento→disposición ni disposición→relación; alinear con la regla 4 del gate v1.1 (gate-confianza-multieje-v1.md:43-46), que ya codifica exactamente este techo.

[MED] La secuencia de apuestas antepone el spike AKN (paso 2) a `EvidenceEdge v0` (paso 3) — INPUT.md:92-96; el spike AKN es valor-opción sin usuario, mientras EvidenceEdge es el mecanismo que cierra el riesgo de herencia vigente en producción de datos y habilita el experimento de falsación — fix: invertir a 1 → 3 → 2, o condicionar el spike AKN a que el experimento-IMSS pase; el spike debe quedar estrictamente acotado (1 disposición, sin tocar registry, matriz de pérdida pre-registrada) como ya sugiere INPUT.md:85-86.

[MED] Mapa competitivo sin instrumento de decisión — INPUT.md:97-99 lista 12 dimensiones pero no muestra, ni scoring, ni umbral que vincule el resultado a adoptar/abandonar el posicionamiento; riesgo de producir un documento narrativo más — fix: muestra fija de 5 preguntas del eje IMSS, 3 comparables máximo (OpenLaws, Orden Jurídico, una suite comercial con cobertura México), scoring binario por dimensión, y regla explícita: si ≥2 comparables igualan procedencia+cobertura en ≥4/5 preguntas, el posicionamiento se reformula o se abandona.

[MED] Riesgo de sobrearquitectura en `EvidenceEdge v0` si se implementa como subsistema — el corpus actual son ~8 disposiciones en YAML/JSON con gates deterministas (INPUT.md:53-54); versionar "el gate" por arista y gestionar clases de afirmación ad hoc puede costar más que el valor en R1 — fix: implementarlo como esquema plano YAML validado por el gate determinista existente, con taxonomía cerrada y enumerada de `clase_afirmacion` (p. ej. {texto_verificado, claim_secundario, derivada}) para que no degrade a texto libre; prohibida cualquier base de grafos en R1 (la propuesta ya lo difiere correctamente, INPUT.md:87-88 — mantenerlo).

[LOW] "OpenLaws como comparable arquitectónico más próximo" (INPUT.md:19-20, 38-39) descansa en su página comercial y cobertura no mexicana — el INPUT ya advierte (INPUT.md:46-47) que las páginas de proveedor no prueban exactitud ni cobertura; correcto, pero entonces OpenLaws no debe anclar la arquitectura, solo figurar como hipótesis a verificar en el experimento del mapa competitivo.

[LOW] La respuesta implícita a la pregunta 2 (compatibilidad AKN en el borde) es la proporcional: conservar JSON/YAML interno y hacer spike aislado con matriz de pérdida es lo adecuado para alfa/R1; no conserva "demasiado poco" porque lo que se pierde (FRBR completo, `temporalData`) corresponde justamente a bitemporalidad que R1 prohíbe abrir (INPUT.md:51-52).

---

**Decisión: fix-and-retry**

No hay BLOCKER: la decisión difiere correctamente grafo/API/ejecutables y es honesta sobre la evidencia. Pero `proceed` requiere (a) el experimento de falsación con criterio de muerte, (b) `nivel_fuente_evidencia` + `cubre_disposicion` + no-herencia en EvidenceEdge v0, y (c) reordenar EvidenceEdge antes del spike AKN — todo realizable sin salirse de R1.

