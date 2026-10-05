# Opción 1 adoptada para el corte offline

El Operador adoptó el contrato de `4ea52b6` el 2026-10-05 exclusivamente para implementar y verificar el corte offline. No es un protocolo congelado. No autoriza una corrida con modelo. No cierra H1 ni H2. No modifica los fixtures `tests/fixtures/extraction_gold/` ni `PROTOCOLO.md`, `predicciones.json`, `corrida.json` o `RESULTADOS.json`. Esos artefactos siguen históricos.

La adopción incorpora tres precisiones: segmento no vacío (`inicio < fin`), predicción inválida contada como falso positivo con diagnóstico `prediccion_invalida`, y gold sin ocurrencias duplicadas. Las listas léxicas no son verdad normativa. La literalidad y los offsets son precondiciones del acierto. La identidad del acierto es la ocurrencia `(inicio, fin)`, no la misma `N` en otra posición.

## Unidad

Un segmento es un tramo verbatim de `texto`. Se corta en `.`, `?`, `!` o `;`, y ese signo entra en el segmento. El espacio siguiente no entra.

El punto no corta si el token inmediato anterior, sin distinguir mayúsculas, está en la lista cerrada `4o`, `art`, `núm`, `num`, `inc`, `fracc`, `sr`, `sra`, `dr`, `dra`, `etc`, `op`. Fuera de esa lista, el primer punto sí corta. La coma, los dos puntos y las comillas no cortan. Sin signo al final del texto, el segmento llega hasta el último carácter y no se inventa un punto: diagnóstico `cierre_ausente`.

`N(s)` es la normalización del juez de T2: NFKD, sin marcas combinantes, minúsculas, espacios colapsados. La puntuación se conserva.

## Benchmark léxico, no verdad normativa

Las listas de abajo etiquetan segmentos de un benchmark sintético. Dicen qué tramos de estos textos de prueba el medidor espera recuperar. No dicen qué es una norma, qué está vigente ni qué debe citar un dictamen. Cambiarlas es enmendar este contrato, no promulgar.

Sea `S` el conjunto de segmentos. Para cada `s`:

- `neg(s)` si `s` contiene, ya en minúsculas, alguna de: `documento sin citas`, `artículo inventado`, `no debe inventar`.
- `pos(s)` si no `neg(s)` y `s` contiene alguna de: `tiene derecho`, `definirá`, `reglamenta`, `es de aplicación`, `orden público`.
- Si `neg(s)`, la clase es `benchmark_negativo`.
- Si `pos(s)`, la clase es `benchmark_positivo`.
- Si no, la clase es `fuera_de_benchmark`.

`neg` gana sobre `pos`. La etiqueta cubre el segmento entero y no lo recorta. El gold del benchmark es solo la clase `benchmark_positivo`, con su `cita_texto = texto[inicio:fin]`. La continuación tras una coma, si sigue dentro del segmento, forma parte de ese gold. Un `benchmark_negativo` no entra al denominador.

## Literalidad, offsets y acierto

`L(texto, inicio, fin, cita)` es verdadero solo si se cumplen las tres condiciones, antes de `N`. Los índices son los de la cadena Python, intervalo semiabierto.

- `inicio` y `fin` son enteros reales. Un booleano, un flotante, una cadena o un campo ausente no lo son. `bool` es subclase de `int` y se rechaza.
- `0 <= inicio < fin <= len(texto)`. El tramo vacío no cumple `L`.
- `texto[inicio:fin] == cita`, carácter por carácter.

`L` del gold y `L` de la predicción son precondiciones. Sin las dos, esa pareja no es acierto, aunque `N` coincida.

El acierto es la misma ocurrencia: ambas cumplen `L` y `inicio` y `fin` son iguales. La misma `N` en otros offsets no es esa ocurrencia. La contención tampoco lo es. El tramo es el mismo, así que `N` coincide; esa igualdad no empareja otra posición.

Si algún registro de gold no cumple `L`, el medidor rechaza la evaluación entera, no emite métricas y la razón es `gold_invalido`. No cuenta ese registro como falso negativo y no lo omite para puntuar el resto. Dos registros con el mismo `(inicio, fin)` también se rechazan, con detalle `ocurrencia_duplicada`. La salida del baseline cumple `L` por construcción: su cita es el tramo y cada ocurrencia aparece una vez.

## Diagnósticos

Se calculan sobre las cadenas aunque falte `L`. No convierten un fallo en acierto.

- Cobertura: `N(gold) in N(prediccion)`.
- Sobreextensión: `N(prediccion) not in N(gold)`. Es un diagnóstico de par de cadenas, no la regla de emparejamiento. Es verdadero solo cuando la predicción normalizada tiene material que el gold normalizado no tiene. Si `N` coincide, no hay sobreextensión. Un prefijo más corto, contenido en el gold, tampoco: falla la cobertura y la sobreextensión es no. El gold más caracteres ajenos sí es sobreextensión, y la cobertura puede seguir siendo sí. No describe la coma interior de la unidad: esa continuación pertenece al gold, y cortarla es un fallo de cobertura contra ese gold.
- Puntuación: `quitar(N(prediccion)) == quitar(N(gold))` y `N(prediccion) != N(gold)`. `quitar` elimina los caracteres `.,;:!?¿¡«»"'()[]-`.

Si `N` coincide: cobertura sí, sobreextensión no, puntuación no. Cobertura sí y sobreextensión sí quiere decir que la predicción contiene al gold y lo rebasa: no hay acierto.

## Emparejamiento y duplicados

El emparejamiento es uno a uno entre predicciones y gold `benchmark_positivo`. Hay arista solo si ambas cumplen `L` y `inicio` y `fin` son los mismos. La misma `N` en otra posición no es arista y no puede tomar el otro gold. Una predicción sin `L` no tiene arista y cuenta como falso positivo. Su diagnóstico es `prediccion_invalida` y su razón es `tipo`, `rango`, `vacio`, `cita` o `ausente`. Una predicción no produce dos verdaderos positivos.

Cada gold aporta como máximo un verdadero positivo. Varias predicciones con los mismos offsets: la primera de la lista es el verdadero positivo y las demás son falsos positivos. No suben el recall. Un gold sin arista es falso negativo. Una predicción que cumple `L` y no tiene gold en esos offsets es falso positivo.

`recall = tp / |gold positivo|`. Si ese denominador es 0, `recall` es null y la razón es `denominador_cero`. `precision = tp / (tp + fp)` solo si la lista de predicciones no está vacía. Si está vacía, `precision` es null y la razón es `denominador_cero`, haya o no gold positivo. No se sustituye ese denominador vacío por 0.

Cero predicciones y gold positivo: `tp` 0, `fp` 0, `fn = |gold|`, recall 0, precisión null. Cero predicciones y cero gold positivo: recall null y precisión null. Hay predicciones y cero gold positivo: esas predicciones son falsos positivos y la precisión es 0.

Los ids no entran en estas fórmulas. El `id_incorrecto` de T2 no se recalcula.

## Baseline determinista

`baseline(texto)` emite, una vez cada uno, los segmentos `benchmark_positivo`, con la cita igual al tramo y con sus offsets. No emite `benchmark_negativo` ni `fuera_de_benchmark`. No llama a un modelo ni a la red. Sobre los textos históricos usados abajo como ilustración, ese baseline empata todos sus gold: recall 1 cuando hay gold positivo. Es el piso del medidor, no una medida de calidad jurídica.

## Ejemplos anotados

Los textos son los históricos. Los cortes ilustran este contrato y no se escriben en los fixtures. La columna de clase es etiqueta de benchmark, no calificación jurídica.

`synth-salud-01`

| Offsets | Clase de benchmark | Señal léxica |
|---|---|---|
| 0:78 | positivo | `tiene derecho`. La coma deja el marco dentro del gold. El punto entra. |
| 79:159 | positivo | `definirá`. El punto entra. |
| 160:449 | positivo | `reglamenta`. `4o.` no corta. La coma no corta. `indica:` no corta. El punto entra. |

`synth-salud-02`, 0:172, positivo por `es de aplicación` y `orden público`. El marco y « según…» van en el mismo gold. El punto entra.

`synth-salud-03`, 0:59, negativo por `documento sin citas`. No hay gold de benchmark. El punto no crea un gold.

## Contraejemplo de dos segmentos idénticos

La oración `La Ley definirá las bases y modalidades para el acceso a los servicios de salud.` mide 80 caracteres. El texto que la repite, con un espacio entre las copias, mide 161. Las ocurrencias son 0:80 y 81:161. Las dos son `benchmark_positivo` por `definirá`. Una predicción solo de 0:80 es verdadero positivo de la primera y falso negativo de la segunda. No toma la segunda por igualdad de `N`. La misma cita con offsets 81:161, si cumple `L`, es acierto solo de la segunda.

## Controles

Están en `tests/test_option1_offline.py`, con expectativas explícitas en `tests/fixtures/option1_offline/controles.json`. No usan el juez de T2. «Sí» en un diagnóstico quiere decir que la fórmula de arriba es verdadera.

| Id | Comparación | Acierto | Cobertura | Sobreextensión | Puntuación | L |
|---|---|---|---|---|---|---|
| C1 | Gold 79:159 contra esa misma cadena y esos offsets | sí | sí | no | no | sí |
| C2 | Ese gold contra la cadena sin el punto, con offsets del tramo sin punto | no | no | no | sí | sí |
| C3 | Gold 160:449 contra el prefijo que corta en «Mexicanos» | no | no | no | no | sí para el prefijo |
| C4 | Gold 79:159 contra esa cadena más un tramo ajeno que sí está en el texto | no | sí | sí | no | sí |
| C5 | `El artículo 4o. reconoce el derecho a la salud.` | un segmento 0:47 | | | | `4o.` no corta; el punto de `salud.` entra |
| C6 | `Véase el art. 4 y el deber de prestar salud.` | un segmento 0:44 | | | | `art.` no corta |
| C7 | `El núm. 5 continúa hasta el cierre.` | un segmento 0:35 | | | | `núm.` no corta |
| C8 | `¿La Ley define el acceso?` | un segmento 0:25 | | | | `?` entra |
| C9 | `Inciso a; sigue el deber.` | 0:9 y 10:25 | | | | `;` entra |
| C10 | La cadena de 79:159 sin su punto | un segmento, `cierre_ausente` | | | | no se inventa el punto; `N` no iguala a 79:159 |
| C11 | `Dice «salud». Luego sigue.` | 0:13 y 14:26 | | | | la comilla anterior no impide el punto |
| C12 | `Dice «salud.» Sigue el deber.` | 0:12 y el resto | | | | el punto corta dentro de las comillas |
| C13 | `El artículo inventado 999 garantiza vacaciones eternas.` 0:55 | no es gold | | | | negativo de benchmark |
| C14 | El texto de `synth-03` | recall null | | | | `denominador_cero` |
| B1 | `baseline` sobre el texto de `synth-01` | tres aciertos, recall 1, precisión 1 | sí en cada pareja | no | no | sí |
| B2 | `baseline` sobre `synth-03` | cero predicciones, recall null, precisión null | | | | las dos con `denominador_cero` |
| B3 | `baseline` no emite C13 | | | | | |
| B4 | Las tres salidas de B1 más una copia de 79:159 | tp 3, fp 1, recall 1, precisión 0.75 | | | | el duplicado no sube el recall |
| B5 | La cita de 79:159 con offsets corridos un carácter | no; cuenta como fp | | | | `prediccion_invalida`, razón `cita` |
| B6 | Lista de predicciones vacía contra los tres gold de `synth-01` | tp 0, fp 0, fn 3, recall 0, precisión null | | | | no es precisión 0 |
| B7 | `inicio` o `fin` booleano, flotante o cadena | no; cuenta como fp | | | | `prediccion_invalida`, razón `tipo` |
| E1 | Las dos copias de 80 caracteres; predicción solo 0:80 | tp 1, fn 1, recall 0.5 | | | | no hay arista hacia 81:161 |
| E2 | La cita de esa oración con offsets 81:161 | acierto de 81:161; fn de 0:80 | | | | `L` sí solo en la segunda |
| E3 | Dos predicciones de la primera copia, 0:80 | tp 1, fp 1, fn 1 | | | | la segunda ocurrencia queda sin par |
| E4 | Una predicción de 0:80 y otra de 81:161 | tp 2, fp 0, fn 0 | | | | cada ocurrencia tiene su arista |
| G1 | Un gold con cita distinta del tramo, offsets invertidos, tipo no entero, tramo vacío o campos ausentes | sin métricas | | | | `gold_invalido`; no es FN ni se omite |
| G2 | Dos gold con el mismo `(inicio, fin)` | sin métricas | | | | detalle `ocurrencia_duplicada` |

## Paquete de una ejecución futura

No se arma ahora. T2 no lo tiene y no se reconstruye: faltan el stderr del canario, el stderr de las tres invocaciones, el entero de tokens y el script. `tool_exec: false` no sustituye al log.

Esa corrida es distinta del corte offline. Si más adelante hay un protocolo congelado, la orquestación es esta secuencia, cada paso con exit code, y se archiva junto con `SHA256SUMS`:

1. Directorio de payload con solo el `texto` de cada documento. Manifiesto: id y SHA-256 del `texto`.
2. El perfil Seatbelt, su SHA-256 y el comando completo.
3. Control negativo: bajo ese perfil, abrir un fixture del repo. El exit tiene que ser distinto de 0 y el log tiene que mostrar la denegación. Si el exit es 0, la orquestación se detiene y no hay corrida aislada.
4. Control positivo: bajo el mismo perfil, leer el `texto` del payload. El exit tiene que ser 0.
5. Una invocación allowlisted por documento, directorio de trabajo el payload, stdin cerrado. Luego el medidor de este contrato, no el juez de T2.
6. Predicciones con `cita_texto`, `inicio` y `fin`, y el gold de benchmark, distinto de los fixtures de T2.

Los logs se archivan saneados. Se eliminan claves, cabeceras `Authorization` y secretos. El cuerpo del `texto` y cualquier cita dentro del stderr se sustituyen por `sha256` y número de bytes. Se conserva el encabezado: exit, provider, modelo, sesión, tokens, líneas de herramienta y la línea de denegación del control negativo. No se archiva el razonamiento del modelo. El archivo de predicciones sí conserva las citas, porque es el artefacto puntuable, y no es un log.

Sin los pasos 3 y 4 archivados, la ejecución no se declara aislada. Este archivo no es ese paquete.

## Adopción del corte offline

El Operador adoptó este corte para implementar y verificar el segmentador, `L` estricto, el emparejamiento por ocurrencia, los diagnósticos, el rechazo `gold_invalido`, el baseline y los controles. El código está en `corpus/option1_offline.py`. Esta adopción no incluye una corrida con modelo, no congela un protocolo, no reescribe los fixtures ni los resultados de T2 y no cierra H1 ni H2.

Una corrida con modelo sigue requiriendo un protocolo posterior, escrito y congelado antes de medir.
