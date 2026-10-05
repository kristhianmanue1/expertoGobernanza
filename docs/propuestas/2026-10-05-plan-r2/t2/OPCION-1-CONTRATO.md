# Opción 1 enmendada, todavía sin adoptar

No está adoptada. No es un protocolo congelado. No autoriza otra corrida. No modifica los fixtures `tests/fixtures/extraction_gold/` ni `PROTOCOLO.md`, `predicciones.json`, `corrida.json` o `RESULTADOS.json`. Esos artefactos siguen históricos.

Esta enmienda corrige el contrato previo a una adopción. Las listas léxicas no son verdad normativa. La literalidad y los offsets son precondiciones del acierto.

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

`L(texto, inicio, fin, cita)` es verdadero solo si `0 <= inicio <= fin <= len(texto)` y `texto[inicio:fin] == cita`, carácter por carácter, antes de `N`. Los índices son los de la cadena Python, intervalo semiabierto.

`L` del gold y `L` de la predicción son precondiciones. Sin las dos, esa pareja no es acierto, aunque `N` coincida.

El acierto de una pareja que ya cumplió `L` es `N(prediccion.cita) == N(gold.cita)`. No es contención.

## Diagnósticos

Se calculan sobre las cadenas aunque falte `L`. No convierten un fallo en acierto.

- Cobertura: `N(gold) in N(prediccion)`.
- Sobreextensión: `N(prediccion) not in N(gold)`.
- Puntuación: `quitar(N(prediccion)) == quitar(N(gold))` y `N(prediccion) != N(gold)`. `quitar` elimina los caracteres `.,;:!?¿¡«»"'()[]-`.

Si `N` coincide: cobertura sí, sobreextensión no, puntuación no. Cobertura sí y sobreextensión sí quiere decir que la predicción contiene al gold y lo rebasa: no hay acierto.

## Emparejamiento y duplicados

El emparejamiento es uno a uno, de cardinalidad máxima, entre predicciones y gold `benchmark_positivo`. Hay arista solo si ambas cumplen `L` y `N` es igual. Una predicción sin `L` no tiene arista.

Desempate: la tupla de índices de gold más pequeña en orden lexicográfico. Los gold se ordenan por `(inicio, fin)`.

Cada gold aporta como máximo un verdadero positivo. Una segunda predicción con la misma cita y los mismos offsets, o con la misma `N` y otra pareja de offsets que ya no encuentra gold libre, es falso positivo. No sube el recall. Un gold sin pareja es falso negativo. Una predicción literal sin gold es falso positivo.

`recall = tp / |gold positivo|`. Si el denominador es 0, `recall` es null y la razón es `denominador_cero`. `precision = tp / (tp + fp)`. Si no hay predicciones ni gold positivo, `precision` es null con la misma razón. Si hay predicciones y el denominador de recall es 0, esas predicciones son falsos positivos y la precisión es 0.

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

## Controles

No están en `tests/`. No se ejecutan. No usan el juez de T2. «Sí» en un diagnóstico quiere decir que la fórmula de arriba es verdadera.

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
| B2 | `baseline` sobre `synth-03` | cero predicciones, recall null | | | | |
| B3 | `baseline` no emite C13 | | | | | |
| B4 | Las tres salidas de B1 más una copia de 79:159 | tp 3, fp 1, recall 1, precisión 0.75 | | | | el duplicado no sube el recall |
| B5 | La cita de 79:159 con offsets corridos un carácter | no | | | | falla `L`; no hay arista |

## Paquete de una ejecución futura

No se arma ahora. T2 no lo tiene y no se reconstruye: faltan el stderr del canario, el stderr de las tres invocaciones, el entero de tokens y el script. `tool_exec: false` no sustituye al log.

Si más adelante hay adopción y un protocolo congelado, la orquestación es esta secuencia, cada paso con exit code, y se archiva junto con `SHA256SUMS`:

1. Directorio de payload con solo el `texto` de cada documento. Manifiesto: id y SHA-256 del `texto`.
2. El perfil Seatbelt, su SHA-256 y el comando completo.
3. Control negativo: bajo ese perfil, abrir un fixture del repo. El exit tiene que ser distinto de 0 y el log tiene que mostrar la denegación. Si el exit es 0, la orquestación se detiene y no hay corrida aislada.
4. Control positivo: bajo el mismo perfil, leer el `texto` del payload. El exit tiene que ser 0.
5. Una invocación allowlisted por documento, directorio de trabajo el payload, stdin cerrado. Luego el medidor de este contrato, no el juez de T2.
6. Predicciones con `cita_texto`, `inicio` y `fin`, y el gold de benchmark, distinto de los fixtures de T2.

Los logs se archivan saneados. Se eliminan claves, cabeceras `Authorization` y secretos. El cuerpo del `texto` y cualquier cita dentro del stderr se sustituyen por `sha256` y número de bytes. Se conserva el encabezado: exit, provider, modelo, sesión, tokens, líneas de herramienta y la línea de denegación del control negativo. No se archiva el razonamiento del modelo. El archivo de predicciones sí conserva las citas, porque es el artefacto puntuable, y no es un log.

Sin los pasos 3 y 4 archivados, la ejecución no se declara aislada. Este archivo no es ese paquete.

## Qué se decide después

Adoptar esta enmienda, rechazarla, o cambiar las listas del benchmark antes de congelar un protocolo. Hasta entonces no hay gold nuevo, no hay tests nuevos y no hay corrida.
