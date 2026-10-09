# Cotejo visual de 86 rótulos y muestra de funciones del manual IMSS

**Resultado técnico:** 85/86 rótulos candidatos v0.4 reproducen literalmente
lo visible en p18–22; uno normaliza una errata impresa. Ocho funciones
seleccionadas de p23–188 coinciden, línea por línea, con el texto registrado
en el manifiesto nativo de Skopos. **Observado:** 2026-10-08 (México). Esta es una revisión
visual no ciega hecha por una sola instancia de Codex; no es revisión humana
ni aceptación institucional.

## Fuente, versión y método

Original [PDF IMSS](../fuentes/imss/2000-002-001.pdf), SHA-256
`719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`.
La [ficha de procedencia](../fuentes/imss/2000-002-001-PROCEDENCIA.md)
conserva la URL oficial y el cotejo de bytes. Manifiesto de etiquetas Skopos
v0.4 SHA-256
`07018142b74249edf0bc056f3b10bee5d1d004e43e77f556b3ef745027efaa98`;
derivación
`54ef4a35842a22896b1f881eb9a1c4c6076ac80e469d83dcbafa81f32e6c7e45`.
Manifiesto nativo de 188 páginas SHA-256
`7f81b1616b10549439cd536737e76663cfea7cec3bf7a6ec3fbf10241d8292ed`.
El manifiesto y su contrato siguen siendo candidatos; este cotejo no los
reescribe ni cambia su estado.

Rendericé las páginas físicas 18–22 con Poppler `pdftoppm 26.05.0`,
`-scale-to 4200 -png`. Recorté cada `bbox` normalizada del manifiesto,
añadí sólo el identificador de nodo a hojas de contacto, leí las 86 cajas y
comparé su grafía con `label_candidate`. Fue un cotejo posterior y no ciego:
el candidato podía influir en la lectura. El
[registro por recuadro](imss-graph-labels-v04-visual-audit-2026-10-08.jsonl)
conserva página, nodo, `item_id`, caja, candidato, lectura visible y
resultado. Los PNG temporales no se incorporan al repositorio; estos son
sus SHA-256 de render, en orden p18–22:

| Página | Recuadros | Coincidencia literal | SHA-256 PNG de 4200 px |
| --- | ---: | ---: | --- |
| 18 | 8 | 8 | `3a00f9c9d2515515e203f7702d65a23989d4a44594735ec067c405977b14a242` |
| 19 | 32 | 32 | `80b306bd0d54177383637e1bbaaee2c942953ce73f20a69f5aae4d85a94b157a` |
| 20 | 10 | 10 | `aa73f09a5503646428f65e5102e7ec5eb427d1ef24c037e0ef4ad43a5695b14f` |
| 21 | 19 | 18 | `51c097a89dbb6f75b78445a9f876621d0c5351b3b6415168553604cfd1da8953` |
| 22 | 17 | 17 | `9c634dd17aae6c77816ec07875a767af7a7f2124f7a71698697bd96c5b3c6e38` |

**Diferencia:** p21 `n5` muestra «COORDINACIÓN DE INFORMACIÓN E
INTELIGENCIA EN SALUID». El candidato reemplaza `SALUID` por `SALUD`;
su propio `native_joined_label` conserva `SALUID`. El reemplazo puede
servir para búsqueda o lectura normalizada, pero una cita literal del
recuadro debe conservar `SALUID` y, si procede, señalar la errata
impresa. No se observó otra discrepancia literal en estas 86 cajas. El
aparente acento de p19 `n23` en la hoja de contacto se descartó al
ampliar ese recuadro: la imagen dice `DIAGNOSTICO`, igual que v0.4.

## Muestra de funciones p23–188

Elegí ocho páginas distribuidas a lo largo de la sección: los extremos
p23/p188, tres páginas con diferencias entre extractores documentadas en
el [inventario completo](imss-full-188-page-coverage-2026-10-08.md)
(p61, p111, p167) y tres puntos intermedios (p44, p88, p139).
Es una muestra dirigida, no aleatoria. Rendericé cada página a 2600 px,
leí la función numerada completa y la comparé con todas sus líneas
`native_text` de Skopos. El
[registro de ocho funciones](imss-functions-visual-sample-2026-10-08.jsonl)
guarda número, texto y `item_id` de cada línea.

| Página; numeral | Contenido comprobado, resumido | Resultado |
| --- | --- | --- |
| 23; 2 | Aprobar normatividad y regulación de servicios de salud que deriven de unidades a cargo | Coincide |
| 44; 2 | Seguimiento de acciones de atención multidisciplinaria, estomatología y enfermería en atención primaria y SPPSTIMSS | Coincide |
| 61; 17 | Promover proyectos y protocolos de investigación en UMAE y unidades complementarias, sujetos a registro y autorización | Coincide |
| 88; 13 | Autorizar programas de investigación científica y desarrollo tecnológico en salud | Coincide |
| 111; 20 | Coordinar análisis y pruebas de tecnologías innovadoras en salud para su propuesta al GTIETS | Coincide |
| 139; 10 | Mantener instrumentos y equipos y seguir calibración y calificación en laboratorios de prueba | Coincide |
| 167; 11 | Proponer convenios nacionales de intercambio de servicios con el sector | Coincide |
| 188; 12 | Verificar participación de coordinaciones en control interno y administración de riesgos | Coincide |

La coincidencia permite atribuir **estos ocho numerales** al texto
impreso del manual, con página física, texto exacto e identificadores
recuperables. No demuestra que sus funciones estén vigentes hoy, que una
unidad conserve esa atribución ni que los demás numerales de p23–188
sean exactos. Cualquier cita nueva requiere recuperar y cotejar su propio
fragmento. Una cita de p21 `n5` requiere distinguir texto visible y
normalización. No se promueve la fidelidad global del PDF ni se admite al
corpus por este muestreo.
