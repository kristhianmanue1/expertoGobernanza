# DPM e infraestructura médica: trazabilidad entre dos manuales

**Estado:** análisis documental acotado, no dictamen de vigencia. Fuentes
independientes: manual general IMSS `0500-002-001_3.pdf` (sello 2022) y manual
de la DPM `2000-002-001.pdf` (sello 2025). La procedencia, bytes y límites de
cada uno constan en `docs/fuentes/imss/*-PROCEDENCIA.md`.

| Pregunta | Fuente y localizador | Observación comprobada | Alcance de la relación |
|---|---|---|---|
| ¿Dónde aparece la DPM en la estructura general? | 0500, p37, organigrama | Caja «Dirección de Prestaciones Médicas» bajo la línea de Dirección General. | Estructura representada en el manual general de 2022; requiere lectura visual del diagrama. |
| ¿Qué función general toca infraestructura? | 0500, §8.1.3 función 2, p45 | Incluye infraestructura y equipamiento médico entre las materias cuya normatividad, planes y lineamientos aprueba la DPM. | Función de la Dirección; no transfiere automáticamente competencia particular a una coordinación. |
| ¿Qué criterio de planeación dicta la DPM? | 0500, §8.1.3 función 16, p46 | Criterios para planeación de servicios médicos indirectos e infraestructura médica. | Relación temática con las funciones técnicas de la CTIM; no prueba vigencia ni equivalencia entre ediciones. |
| ¿Dónde se ubica la CTIM? | 2000, p22, organigrama | Secuencia visual DPM → Unidad de Infraestructura, Servicios Médicos Indirectos e Integración Sectorial → Coordinación de Planeación de Infraestructura Médica → Coordinación Técnica de Infraestructura Médica. | La lectura de p22 debe cotejarse visualmente para cada relación que se cite. |
| ¿Qué hace la CTIM? | 2000, §7.1.4.4.1, pp172–173 | Quince funciones numeradas: planeación de obra, capacidad, elementos técnicos, diagnóstico/priorización, indicadores, modelos y diseño, procesos y plantillas de personal, presupuesto de plazas y equipamiento médico. | Enumeración resumida; cada afirmación específica debe enlazar función, página y fragmento literal. |

**Inferencia limitada:** las funciones generales 2 y 16 de la DPM en 0500 y
las funciones 1–15 de la CTIM en 2000 comparten el tema de planeación de
infraestructura. La línea jerárquica concreta de la CTIM se observa en el
organigrama de 2000, no en la página 37 de 0500. La relación no resuelve
prelación, reformas o vigencia de estos manuales. La fecha impresa en un
documento y su disponibilidad en el portal no bastan para resolverlo.

## Requisito de consulta por agentes

Una respuesta combinada debe conservar por cada fragmento: `source_sha256`,
`source_url`, clave documental, página física, región o línea, modalidad
(texto nativo/OCR/lectura visual), identidad del derivado de Skopos y
verificación contra el PDF custodiado. Ágora puede proponer la relación entre
fragmentos, con sus dos referencias; esa relación es una inferencia, no texto
literal de uno de los manuales. Un resultado ausente de extracción en p37
no equivale a ausencia de la DPM en el organigrama.
