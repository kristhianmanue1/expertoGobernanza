# CTIM: referencia de adjudicación para comparación documental

**Estado:** referencia provisional, autorrevisada el 9 de octubre de 2026.
No es una respuesta generada por los candidatos ni una declaración de vigencia
institucional. Los originales, sus URL y SHA-256 están en
`ctim-source-register-2026-10-08.json`; se verifican con
`python3 -m scripts.verify_source_inventory`. Los localizadores siguientes se
cotejaron en las imágenes de las páginas originales indicadas. El HTML de DOF
2023 se contrastó con los bytes locales y su texto visible.

## Casos y evidencia esperada

| Caso | Pregunta evaluada | Evidencia suficiente | Falsación o límite |
| --- | --- | --- | --- |
| C1 | ¿Qué unidades intervienen en el procedimiento CEPI y cuál es el traspaso hacia infraestructura? | `2900-003-001.pdf` p6 §§5.4–5.6, 5.10–5.12: CPIM actúa por CTIM; OOAD/UMAE detectan necesidades y presentan solicitudes. p15 actividades 18–22: CPIM envía CEPI Médica, PM y GEMIQECC a CII; CTIM recibe y revisa anteproyecto y sigue el proyecto ejecutivo con División de Proyectos de CII. | Es incorrecto atribuir a CTIM el envío de la actividad 18, que está bajo CPIM. La p15 es una tabla de responsables y actividades; las flechas añadidas son interpretación. |
| C2 | ¿El nombre de la coordinación en Administración p282 demuestra identidad con CTIM DPM? | `1000-002-001_1.pdf` p282 funciones 11–12 nombra «Coordinación Técnica de Planeación de Infraestructura Médica»; `2000-002-001.pdf` p172 §7.1.4.4.1 nombra «Coordinación Técnica de Infraestructura Médica». Respuesta correcta: identidad no demostrada con estas páginas. | No igualar entidades por parecido de nombre o función. La ausencia de un acto de reorganización impide adjudicar equivalencia; tampoco prueba que sean distintas entidades históricas. |
| C3 | ¿Qué documento deja sin efectos la versión POBALINES de 2021? | `1000-001-029.pdf` p75, transitorio Segundo, y `dof-5686058.html`, acuerdo Tercero, identifican la versión de 2021 y condicionan el efecto a la entrada en vigor de las POBALINES posteriores. | No usar el acuerdo 2021 como texto vigente sin revisión temporal. Estos pasajes no descartan reformas posteriores ni autorizan afirmar vigencia general a 2026. |
| C4 | ¿A qué nivel se atribuye la función 16 del manual `0500-002-001_3.pdf`? | p45 §8.1.3 encabeza «Dirección de Prestaciones Médicas»; p46 continúa la lista y la función 16 trata criterios para servicios médicos indirectos e infraestructura médica. La atribución al nivel DPM se funda en la continuidad visual de la lista entre páginas. | p46 por sí sola no repite el encabezado; llamar literal a esa continuidad es impreciso. Las dos páginas no asignan la función directamente a CTIM. |

## Reglas de puntuación

1. Separar **localización del original**, **lectura de un fragmento ya
   suministrado**, **integridad/custodia**, **clasificación de relación** y
   **control temporal**. Una página entregada al modelo no cuenta como hallazgo
   de recuperación libre.
2. Exigir identificador del original, SHA-256, página física o rango HTML,
   fragmento y cobertura real. No puntuar como acierto una cita con página
   correcta pero texto diferente, ni una respuesta correcta sin fuente
   resoluble. Registrar no evaluado cuando el candidato no tuvo el input.
3. Los rechazos de hash, página y rango se atribuyen al componente que
   efectivamente los ejecutó. Una abstención del modelo no demuestra control
   técnico de acceso; un control local no demuestra capacidad nativa del modelo.
4. El denominador de recuperación sobre los siete originales es distinto del
   denominador de lectura de nueve páginas PDF y tres rangos HTML. Reportar
   ambos sin agregarlos en una sola nota. La cobertura total de los PDF no fue
   cotejada para esta referencia.
5. Un acierto en C2 o C3 debe incluir la reserva correspondiente; afirmar
   equivalencia orgánica o vigencia posterior sin fuente es falso positivo.
   La adjudicación definitiva de vigencia y organización requiere revisión
   humana de fuentes adicionales.

**Método y límites:** cotejo visual propio de pp6/15, 45/46, 75, 172 y 282;
lectura del HTML 2023 local. Esta referencia no revisó todas las páginas ni
prueba independencia de un segundo adjudicador. Si se modifica después de
conocer resultados, conservar la versión anterior y explicar la enmienda.
