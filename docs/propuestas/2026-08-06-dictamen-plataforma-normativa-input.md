# Dictamen + análisis — Plataforma de inteligencia normativa (entrada del humano)

> **⚠️ ENTRADA DEL HUMANO — SIN VERIFICAR (§7 fidelidad documental).**
> Este archivo reproduce verbatim el dictamen y el análisis crítico provistos por el
> orquestador el 2026-08-06. Las afirmaciones normativas aquí contenidas (fechas DOF,
> estructuras de artículos/fracciones, jerarquía de fuentes, obligatoriedad de tesis,
> alcance IMSS, etc.) son afirmaciones **del dictamen** y **NO han sido verificadas**
> contra fuentes oficiales (DOF / Cámara de Diputados / SCJN-SJF). Se almacenan como
> **insumo de análisis y decisión**; no deben citarse como hecho ni usarse con efecto
> normativo hasta su verificación trazable. Este archivo es un **registro de entrada**,
> no un artefacto normativo.
>
> **Procedencia:** orquestador humano (chat 2026-08-06). **Estado:** en análisis crítico
> + adversarial (§6) antes de decidir.

---

## Dictamen general

La propuesta tiene una base técnica sólida, pero todavía describe principalmente un sistema avanzado de recuperación jurídica —un RAG legal con trazabilidad— y no un verdadero sistema de "Leyes como Código".

Su mayor acierto es comprender que el problema no consiste en almacenar documentos, sino en representar disposiciones jurídicas como objetos identificables, versionables, consultables y citables. En particular, son correctas estas decisiones:

- artículo o fracción como unidad jurídica, no fragmentos arbitrarios por número de tokens;
- representación dual en JSON estructurado y Markdown;
- búsqueda híbrida exacta y semántica;
- separación entre texto vigente, reformas y jurisprudencia;
- actualización a partir del DOF;
- herramientas deterministas para agentes;
- obligación de citar y reconocer cuando no existe fundamento.

La arquitectura de cuatro capas, el artículo como unidad de chunking y el uso de jerarquía normativa colocan la propuesta por encima de un RAG documental convencional. No obstante, los problemas pendientes son estructurales, no meramente tecnológicos.

### 1. "Leyes como Código" exige más que JSON

Actualmente, el esquema representa bien el contenido textual, pero todavía no representa suficientemente el comportamiento jurídico.

Una disposición legal debería poder modelarse, como mínimo, con:

```json
{
  "disposicion_id": "LSS:251:I",
  "tipo": "fraccion",
  "texto": "...",
  "norma_id": "LSS",
  "jerarquia_documental": {
    "titulo": "...",
    "capitulo": "...",
    "articulo": "251",
    "fraccion": "I"
  },
  "publicacion_dof": "2025-01-15",
  "vigencia_desde": "2025-01-16",
  "vigencia_hasta": null,
  "estado_vigencia": "vigente",
  "estado_aplicabilidad": "aplicable",
  "ambito": {
    "material": ["seguridad_social"],
    "territorial": ["federal"],
    "personal": ["IMSS"]
  },
  "operadores": {
    "sujeto": "Instituto Mexicano del Seguro Social",
    "modalidad": "facultad",
    "accion": "...",
    "objeto": "...",
    "condiciones": []
  },
  "fuentes_oficiales": [],
  "version_anterior_id": "...",
  "transitorios_relacionados": [],
  "relaciones_normativas": []
}
```

La diferencia es importante: almacenar el texto permite buscarlo; representar sujeto, facultad, obligación, condición, excepción y consecuencia permite razonar controladamente sobre él.

Por tanto, sería más preciso llamar a la primera versión: **Infraestructura normativa estructurada para agentes de IA**. El concepto "Leyes como Código" debería reservarse para una etapa posterior que incluya reglas ejecutables, validación formal y pruebas normativas.

### 2. La fuente oficial debe distinguirse de la compilación de consulta

La Cámara de Diputados es una fuente excelente para obtener textos consolidados, pero su propia compilación señala que tiene carácter informativo. La publicación jurídicamente primaria sigue siendo el Diario Oficial de la Federación.

Por ello, conviene establecer una jerarquía explícita:

| Nivel | Fuente | Función |
|---|---|---|
| 1 | DOF | Publicación primaria, decretos, transitorios y entrada en vigor |
| 2 | Cámara de Diputados | Texto consolidado para consulta y contraste |
| 3 | SCJN/SJF | Interpretación, precedentes, jurisprudencia y aplicabilidad |
| 4 | Repositorios derivados | Semilla, comparación y detección de errores |

El sistema no debería asumir que una sola fuente es perfecta. Debe implementar reconciliación de fuentes:

```
DOF publicado
    ↓
parser del decreto
    ↓
aplicación de operaciones normativas
    ↓
texto consolidado calculado
    ↓
comparación con Cámara de Diputados
    ↓
coincidencia → publicación automática
diferencia → revisión humana
```

Eso convierte a la Cámara en un mecanismo de control independiente, no en una dependencia única.

### 3. Los repositorios mencionados existen, pero no deben ser la fuente de verdad

Los dos proyectos citados sí son localizables actualmente:

- `ingteranalvarez/lex-mx`, que presenta legislación mexicana en Markdown y declara actualización automatizada;
- `JoshuaPozoz/leyes-mexicanas-markdown`, que propone conversión de PDFs oficiales a Markdown y JSON canónico.

Esto corrige una duda planteada en el análisis adjunto, donde se señalaba que no habían podido verificarse.

Sin embargo, su existencia no resuelve preguntas indispensables:

- ¿Cómo procesan reformas complejas?
- ¿Conservan transitorios?
- ¿Representan artículos bis, ter y numeraciones repetidas?
- ¿Cómo manejan fe de erratas?
- ¿Qué tasa de error tiene el parser?
- ¿Existe revisión jurídica?
- ¿Puede reconstruirse la procedencia exacta de cada párrafo?

La recomendación correcta es: **usarlos como datos iniciales, benchmark y detector de diferencias, nunca como autoridad normativa.**

### 4. El modelo temporal propuesto es insuficiente

El campo `"ultima_reforma": "2026-06-02"` no permite responder preguntas jurídicas históricas ni determinar con precisión cuándo produjo efectos una reforma.

Debe diferenciarse al menos entre:

- fecha de publicación;
- fecha de entrada en vigor;
- fecha de fin de vigencia;
- fecha en que el sistema incorporó el cambio;
- reforma que creó la versión;
- versión corregida por fe de erratas;
- vigencia condicionada o diferida.

Esto exige, idealmente, un modelo bitemporal:

```
tiempo jurídico:
vigencia_desde ───────── vigencia_hasta

tiempo del sistema:
registrado_desde ─────── registrado_hasta
```

Así pueden contestarse dos preguntas distintas:

- ¿Qué texto era jurídicamente aplicable el 15 de marzo de 2019?
- ¿Qué versión tenía registrada el sistema el 20 de marzo de 2019?

Git es útil para auditoría y revisión humana, pero no debería ser la base principal para consultas temporales sobre decenas de miles de disposiciones. Para eso conviene una base relacional con versiones inmutables. Esta observación coincide con el análisis del archivo aportado.

### 5. Los artículos transitorios deben ser objetos de primera clase

Este es uno de los vacíos más importantes.

La publicación de un decreto no implica necesariamente que todas sus disposiciones entren en vigor al día siguiente. Puede haber:

- entrada en vigor diferida;
- aplicación escalonada;
- condiciones presupuestales;
- declaratorias posteriores;
- plazos para emitir reglamentos;
- supervivencia temporal de reglas anteriores;
- derogaciones condicionadas.

Por ello, un transitorio no debe conservarse como simple texto al final del documento. Debe tener una estructura propia:

```json
{
  "transitorio_id": "DEC-2026-06-02:T2",
  "tipo_efecto": "entrada_vigor_diferida",
  "afecta": ["LSS:251:I", "LSS:251:II"],
  "fecha_base": "2026-06-02",
  "regla_temporal": {
    "tipo": "dias_despues_publicacion",
    "cantidad": 180
  },
  "fecha_efectiva_calculada": "2026-11-29",
  "requiere_evento_externo": false,
  "texto_original": "..."
}
```

Sin esto, el sistema puede devolver un artículo publicado pero todavía no vigente, o ignorar una norma anterior que continúa produciendo efectos.

### 6. Vigencia y aplicabilidad no son equivalentes

Un texto puede aparecer como vigente en una compilación y, sin embargo, estar afectado por:

- sentencia con efectos generales;
- declaratoria general de inconstitconstitucionalidad;
- acción de inconstitucionalidad;
- controversia constitucional;
- interpretación conforme;
- inaplicación en determinados supuestos;
- régimen especial que desplaza a la regla general.

Por eso deben existir campos separados:

```json
{
  "estado_vigencia": "vigente",
  "estado_aplicabilidad": "parcialmente_inaplicable",
  "alcance_inaplicabilidad": "...",
  "resolucion_origen": "...",
  "fecha_efectos": "..."
}
```

Un agente no debería decir únicamente "el artículo está vigente", sino algo como: *El texto continúa formalmente vigente; no obstante, su aplicación está limitada en el supuesto X por la resolución Y.*

### 7. La jurisprudencia no puede modelarse como una lista de enlaces

La propiedad `"tesis_relacionadas": []` es demasiado plana.

El Semanario Judicial no contiene una colección homogénea. Distingue tesis, ejecutorias, precedentes, órganos emisores, épocas, tipos y estados. Además, el sistema de precedentes obligatorios exige atender a la ejecutoria y a las razones decisorias, no únicamente al encabezado de una tesis. La propia SCJN mantiene módulos diferenciados para tesis y precedentes, e identifica cuándo un criterio adquiere aplicación obligatoria.

El modelo debería registrar:

```json
{
  "criterio_id": "SJF:2027495",
  "tipo_documento": "tesis_jurisprudencial",
  "registro_digital": "2027495",
  "organo": "Pleno",
  "epoca": "Undécima",
  "materias": [],
  "tipo_obligatoriedad": "jurisprudencia",
  "obligatorio_desde": "2023-10-23",
  "estado": "vigente",
  "criterio_superado_por": null,
  "ejecutoria_origen": [],
  "ratio_decidendi": "...",
  "articulos_interpretados": [],
  "relacion": "interpreta"
}
```

Mi recomendación sería tratar la jurisprudencia como un subsistema autónomo, conectado al corpus legislativo mediante relaciones controladas. No incorporarla como simple metadato de un artículo.

### 8. El principal riesgo no se elimina mediante instrucciones al modelo

La regla "Si no hay fundamento exacto, decirlo explícitamente" es correcta como política, pero no garantiza nada por sí sola.

Debe implementarse un verificador de citas posterior a la generación:

- extraer cada referencia normativa de la respuesta;
- comprobar que la disposición existe;
- validar que era vigente en la fecha jurídica relevante;
- verificar que el fragmento citado coincide con el corpus;
- comprobar que la fuente oficial está disponible;
- bloquear o degradar la respuesta si falla alguna validación.

Ejemplo:

```json
{
  "citation_validation": {
    "reference_exists": true,
    "version_valid_for_date": true,
    "quote_exact_match": true,
    "official_source_resolved": true,
    "interpretation_supported": false
  },
  "response_status": "requires_human_review"
}
```

En un sistema jurídico de alto impacto, una respuesta sin citas válidas no debería presentarse como respuesta definitiva.

### 9. La arquitectura inicial está sobrecargada

Para un corpus federal de aproximadamente cientos de leyes y decenas de miles de disposiciones, comenzar simultáneamente con: document database; Elasticsearch o Meilisearch; vector database; knowledge graph; Git; almacenamiento de objetos; añade costos operativos y puntos de falla antes de demostrar valor.

Una arquitectura inicial más proporcionada sería:

```
PostgreSQL
 ├── tablas normativas y temporales
 ├── JSONB para AST
 ├── tsvector para búsqueda léxica
 ├── pgvector para búsqueda semántica
 ├── tablas de relaciones normativas
 └── auditoría/versiones

Object storage
 ├── PDF/Word originales
 ├── decretos DOF
 └── evidencias de extracción

Git
 └── representación Markdown auditable
```

Elasticsearch o un grafo especializado deben incorporarse cuando una métrica demuestre que PostgreSQL ya no satisface latencia, escala o complejidad relacional. La misma simplificación fue señalada en el análisis adjunto.

### 10. Para IMSS, el corpus federal no debe ser la prioridad única

En un contexto institucional de salud, limitar el corpus inicial a leyes federales produciría un sistema jurídicamente correcto pero operativamente incompleto.

El corpus relevante incluye:

```
Constitución
   ↓
Ley General de Salud / Ley del Seguro Social
   ↓
Reglamentos
   ↓
Normas Oficiales Mexicanas
   ↓
Acuerdos del Consejo Técnico
   ↓
Reglamento Interior y manuales de organización
   ↓
Políticas, lineamientos y procedimientos internos
   ↓
Guías, formatos y documentos operativos
```

Para manuales, políticas y procedimientos internos, el riesgo más frecuente no es contradecir directamente la Constitución, sino:

- asignar funciones a un área incompetente;
- utilizar una denominación organizacional obsoleta;
- imponer actividades a otra coordinación;
- citar una NOM cancelada o sustituida;
- duplicar o contradecir otro procedimiento;
- referenciar formatos inexistentes;
- establecer requisitos no autorizados.

Por ello, la Normateca y los manuales de organización deben incorporarse desde la primera fase institucional, no dejarse al final.

### 11. El producto con mayor valor no es el buscador

El endpoint más valioso de la propuesta probablemente sea: `GET /diff/{ley}?desde=YYYY-MM-DD`. Pero debería evolucionar a un servicio de impacto normativo:

```
POST /impact-analysis
Entrada:
{
  "decreto_dof": "DOF:2026-08-06:XYZ",
  "unidad": "División X",
  "fecha_objetivo": "2026-08-07"
}
Salida:
{
  "disposiciones_modificadas": [],
  "procedimientos_afectados": [],
  "citas_obsoletas": [],
  "formatos_afectados": [],
  "responsables_institucionales": [],
  "nivel_riesgo": "alto",
  "acciones_recomendadas": []
}
```

La propuesta de valor institucional sería: *"Una reforma publicada hoy modifica tres fundamentos utilizados por siete procedimientos vigentes y requiere actualizar dos formatos antes de determinada fecha"*. Eso es más defendible presupuestalmente que "un chatbot que responde preguntas legales".

### 12. Faltan evaluación, gobierno y responsabilidad

Antes de desplegar agentes, debe construirse un conjunto de evaluación validado por especialistas.

Métricas mínimas:

| Métrica | Qué detecta |
|---|---|
| Exactitud de lookup | Recuperación del artículo/fracción solicitados |
| Recall de fundamento | Omisiones de normas aplicables |
| Cita inexistente | Alucinaciones |
| Vigencia temporal correcta | Uso de versión equivocada |
| Exactitud de transitorios | Errores de entrada en vigor |
| Clasificación de obligatoriedad | Confusión entre tesis aislada y criterio obligatorio |
| Tasa de falsos hallazgos | Alertas incorrectas |
| Cobertura de corpus | Documentos faltantes |
| Concordancia con juristas | Calidad práctica |

Además, se requiere: responsable del corpus; responsable jurídico; proceso para resolver discrepancias; bitácora de cambios; aprobación humana; niveles de confianza; identificación del agente y versión del modelo; registro de qué evidencia sustentó cada conclusión.

### Arquitectura corregida

Seis componentes:

**A. Registro de fuentes** — Conserva documento original, hash, fecha de descarga, autoridad, tipo de fuente y cadena de procedencia.

**B. Compilador normativo** — Convierte decretos en operaciones explícitas (ADICIONAR, REFORMAR, DEROGAR, ABROGAR, SUSTITUIR, CORREGIR) y las aplica sobre versiones inmutables.

**C. Motor temporal y de aplicabilidad** — Resuelve vigencia histórica/futura, transitorios, fe de erratas, aplicabilidad, efectos generales de resoluciones.

**D. Índice de consulta** — Resolución exacta de identificadores + búsqueda léxica + semántica + filtros por metadatos + expansión jerárquica controlada.

**E. Servicios para agentes** — `resolve_identifier`, `get_provision`, `get_version_at_date`, `search_normative_corpus`, `get_transition_rules`, `get_related_precedents`, `compare_versions`, `analyze_normative_impact`, `verify_citations`.

**F. Compuertas de seguridad** — cita inexistente → bloquear; fecha jurídica no indicada → solicitarla/declarar supuesto; fuentes en conflicto → revisión humana; obligatoriedad indeterminada → no presentar como vinculante; corpus posiblemente incompleto → advertencia explícita; impacto institucional alto → HITL obligatorio.

### Priorización propuesta

- **Fase 0 — Auditor normativo.** No genera contenido. Recibe procedimientos existentes y detecta citas obsoletas, normas derogadas, NOM sustituidas, áreas/puestos inexistentes, formatos no localizados, contradicciones. Es el punto de entrada de menor riesgo y mayor demostrabilidad.
- **Fase 1 — Corpus institucional acotado.** LSS; LGS; Reglamento Interior del IMSS; manual de organización del área piloto; NOM relevantes; acuerdos y normativa interna; 15 a 30 procedimientos de una familia operativa. Incluye desde el principio: temporalidad; transitorios; lookup exacto; verificador de citas; golden set.
- **Fase 2 — Vigilancia e impacto.** DOF → clasificación → actualización → diff → mapa de documentos afectados → alerta.
- **Fase 3 — Asistente de elaboración.** Generación únicamente sobre plantillas institucionales y con compuertas: competencia; marco aplicable; coherencia organizacional; referencias vigentes; consistencia estructural; revisión humana.
- **Fase 4 — Jurisprudencia.** Subsistema propio con modelo de obligatoriedad, ejecutorias, tesis, relaciones y vigencia del criterio.
- **Fase 5 — Expansión.** Corpus federal completo, estatal y otros criterios administrativos.

### Conclusión

La idea es viable, valiosa y estratégicamente correcta, pero requiere cambiar tres supuestos centrales:

1. No construir un RAG de leyes, sino un registro normativo temporal y verificable.
2. No confiar la seguridad a instrucciones del agente, sino a validadores deterministas.
3. No iniciar por amplitud del corpus, sino por un dominio institucional pequeño con garantías fuertes.

La formulación final del proyecto podría quedar así: *Plataforma de inteligencia normativa para agentes de IA, basada en disposiciones versionadas, fuentes oficiales trazables, vigencia temporal, verificación automática de citas y análisis de impacto sobre normativa institucional.*

Su primer producto no debería ser un chatbot jurídico. Debería ser un **auditor de salud normativa y detector de impacto de reformas**. Ese producto genera evidencia cuantificable, minimiza riesgo institucional y construye exactamente la infraestructura necesaria para posteriormente asistir en la elaboración de manuales, procedimientos y políticas.

---

## Análisis crítico y propositivo del Dictamen

El dictamen es de alta calidad. No es una crítica superficial ni un listado de "mejoras deseables": identifica con precisión dónde la propuesta original se queda en un sistema avanzado de recuperación jurídica con trazabilidad y dónde empieza a pretender algo más ambicioso de lo que realmente describe. Eso es valioso.

### Acuerdos estructurales (donde el dictamen es correcto y debe incorporarse)

- **La distinción "Leyes como Código" vs. "Infraestructura normativa estructurada" es pertinente.** Representar el texto + jerarquía + metadatos de vigencia no equivale a modelar el comportamiento jurídico. Llamar "Leyes como Código" a la primera etapa genera expectativas de ejecutabilidad y validación formal que el sistema no puede cumplir todavía.
- **Jerarquía de fuentes y reconciliación es obligatoria.** La Cámara de Diputados es excelente como consolidado de consulta, pero su propio aviso de carácter informativo es claro. El DOF es la fuente primaria de validez. Un sistema serio debe calcular el consolidado a partir de operaciones normativas (ADICIONAR, REFORMAR, DEROGAR…) y usar el texto de Diputados como control independiente, no como dependencia única.
- **Transitorios como objetos de primera clase y separación vigencia/aplicabilidad.** Son dos de los puntos más débiles de la propuesta original. Sin modelar entrada en vigor diferida, efectos condicionados, supervivencia temporal y efectos judiciales, el sistema puede devolver texto "vigente" que aún no produce efectos o que está parcialmente desplazado. Eso es un error jurídico de alto impacto.
- **Verificador determinista de citas post-generación.** Confiar solo en la instrucción del prompt es insuficiente. Extraer referencias, validar existencia, vigencia en la fecha jurídica relevante y coincidencia textual es una capa de seguridad indispensable.
- **El producto de mayor valor institucional no es el chatbot.** Un servicio de impacto normativo genera evidencia cuantificable y justifica presupuesto mucho mejor. El "Auditor normativo" como Fase 0 es una propuesta excelente de bajo riesgo y alta demostrabilidad.
- **Arquitectura inicial sobredimensionada.** Empezar con document DB + Elasticsearch + vector DB + knowledge graph + Git + object storage es costoso y frágil antes de demostrar valor. PostgreSQL + JSONB + tsvector + pgvector + tablas de versiones es una base mucho más proporcionada.

### Matices y desacuerdos parciales

- **Sobre el modelo de "operadores" jurídicos (sujeto, modalidad, acción, objeto, condiciones).** Es conceptualmente correcto a largo plazo. Sin embargo, extraer de forma fiable esa estructura semántica del lenguaje natural de las leyes mexicanas es un problema de NLP difícil, con alta tasa de error y que requiere anotación humana significativa. Intentarlo demasiado pronto introduce un nuevo vector de error (mal parseo deóntico) que puede ser peor que no tenerlo. Conviene tratarlo como capa de enriquecimiento gradual y no como requisito de la Fase 1.
- **Sobre bitemporalidad completa desde el inicio.** Idealmente sí. En la práctica, para un MVP institucional, basta con un modelo de versiones inmutables con `vigencia_desde`/`vigencia_hasta` + `registrado_en` y la capacidad de consultar "versión aplicable en fecha X". La bitemporalidad plena se añade cuando el volumen y los casos de uso lo justifiquen. Git sigue siendo útil para auditoría humana, no como motor de consulta temporal.
- **Sobre el alcance IMSS / institucional.** El dictamen introduce un contexto institucional de salud (LSS, LGS, Reglamento Interior, manuales, NOMs, acuerdos del Consejo Técnico) que no estaba en la consulta original. Es un buen ejemplo de realismo operativo, pero cambia el problema: de "sistematizar las leyes mexicanas para agentes de IA" pasa a "construir inteligencia normativa para un organismo público de alto impacto". Ambos son válidos, pero deben declararse como proyectos de alcance distinto.
- **Sobre los repositorios open source.** Correcto: deben usarse como semilla, benchmark y detector de discrepancias, nunca como autoridad. La pregunta abierta es cuánta revisión jurídica real tienen esos parsers sobre reformas complejas, artículos bis/ter, fe de erratas y numeraciones repetidas. Esa auditoría debe hacerse antes de confiar en ellos.

### Lo que el dictamen subestima o deja implícito

- **Costo de la reconciliación y de la revisión humana.** Cada discrepancia DOF vs. Cámara requiere decisión jurídica. Si el volumen de reformas es alto, el cuello de botella humano puede paralizar la actualización.
- **Dificultad de construir un golden set de evaluación.** Crear un conjunto de casos validados por juristas es en sí mismo un proyecto no trivial.
- **Riesgo de sobre-estructuración temprana.** Un modelo demasiado rico desde el día 1 puede volverse rígido y costoso de mantener cuando aparecen figuras normativas atípicas.

### Síntesis propositiva

La formulación final del dictamen es superior a la original: *Plataforma de inteligencia normativa para agentes de IA, basada en disposiciones versionadas, fuentes oficiales trazables, vigencia temporal, verificación automática de citas y análisis de impacto sobre normativa institucional.* Y el primer producto debería ser un **Auditor de salud normativa + detector de impacto de reformas**, no un chatbot.

Priorización refinada (ajustada):

| Fase | Objetivo | Entregable principal | Riesgo |
|---|---|---|---|
| 0 | Auditor normativo | Detección de citas obsoletas, normas derogadas, NOMs sustituidas, inconsistencias organizacionales en documentos existentes | Bajo |
| 1 | Corpus acotado + temporalidad + verificador | Un dominio pequeño (LSS + reglamentos + normativa interna relevante) con lookup exacto, vigencia y citation verifier | Medio-bajo |
| 2 | Vigilancia e impacto | Pipeline DOF → operaciones normativas → diff → mapa de impacto institucional | Medio |
| 3 | Asistente de elaboración con compuertas | Generación solo sobre plantillas + validaciones de competencia, marco aplicable y coherencia | Medio-alto |
| 4 | Jurisprudencia como subsistema | Modelo propio de obligatoriedad, ejecutorias y relaciones | Alto |
| 5 | Expansión | Federal completo + estatal + más criterios administrativos | Alto |

La arquitectura de seis componentes (Registro de fuentes → Compilador normativo → Motor temporal/aplicabilidad → Índice de consulta → Servicios para agentes → Compuertas de seguridad) es más clara y defendible que las cuatro capas originales.

### Conclusión

El dictamen no invalida la propuesta; la eleva. Convierte un diseño técnicamente competente de RAG jurídico en un diseño con pretensiones de fidelidad normativa institucional. Los tres cambios de supuesto que propone son correctos:

1. De RAG de leyes → registro normativo temporal y verificable.
2. De seguridad por prompt → validadores deterministas.
3. De amplitud del corpus → dominio pequeño con garantías fuertes.

El riesgo principal ahora no es técnico, sino de alcance y gobernanza: quién es el responsable jurídico del corpus, cómo se resuelven las discrepancias de fuentes y cómo se evita que la complejidad del modelo se adelante a la capacidad de mantenerlo con calidad.

Si se adopta esta línea, el siguiente paso concreto debería ser definir el dominio piloto (¿general federal? ¿IMSS? ¿otro?) y el conjunto mínimo de entidades y relaciones que se modelarán en la Fase 1, antes de escribir una sola línea de pipeline de extracción.
