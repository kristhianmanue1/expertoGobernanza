# Opción 1 para decisión

No está adoptada. No es un protocolo congelado. No autoriza otra corrida. Los fixtures `tests/fixtures/extraction_gold/` y los archivos `PROTOCOLO.md`, `predicciones.json`, `corrida.json` y `RESULTADOS.json` permanecen históricos.

Prepara la opción 1 pedida después del cierre administrativo de T2. La adopción, y solo después un protocolo nuevo, quedan para una instrucción posterior.

## Unidad

Un segmento es un tramo verbatim de `texto`. Se corta en `.`, `?`, `!` o `;`, y ese signo entra en el segmento. El espacio que sigue al signo no entra: es el separador.

Una abreviatura no corta. El token inmediato anterior al punto, en mayúsculas o minúsculas, está en esta lista cerrada: `4o`, `art`, `núm`, `num`, `inc`, `fracc`, `sr`, `sra`, `dr`, `dra`, `etc`, `op`. El punto de `4o.` no es cierre. Una abreviatura fuera de la lista sí cierra en el primer punto. Ampliar la lista es enmendar este contrato.

La coma, los dos puntos y las comillas no cortan. Si el texto se acaba sin signo de cierre, el último segmento llega hasta el final y no se le inventa un punto. Ese caso lleva el diagnóstico `cierre_ausente`.

Los offsets son índices de la cadena Python de `texto`, intervalo semiabierto. Literalidad: `texto[inicio:fin] == cita_texto`, carácter por carácter, antes de normalizar.

## Coma

Toda continuación que queda dentro del segmento pertenece al gold nuevo. «, establece…» y « según…» no son sobreextensión frente a ese gold. Un corte en la coma deja fuera parte del gold: falla la igualdad y falla la cobertura. No es el acierto.

## Acierto y diagnósticos

La normalización es la del juez de T2: NFKD, sin marcas combinantes, minúsculas, espacios colapsados. Los signos de puntuación se conservan.

El acierto de extracción es solo la igualdad de esas dos cadenas normalizadas. No es contención.

Tres diagnósticos, calculados siempre, sin poder convertir un fallo de igualdad en acierto:

- Cobertura: el gold normalizado es subcadena de la predicción normalizada.
- Sobreextensión: la predicción normalizada no es subcadena del gold normalizado.
- Puntuación: al quitar `.,;:!?¿¡«»"'()[]-` de ambas cadenas ya normalizadas, los restos coinciden, y las cadenas normalizadas no. Un punto de más o de menos cae aquí.

Si las cadenas normalizadas son iguales, los tres diagnósticos quedan en no. Cobertura verdadera con sobreextensión verdadera describe una predicción que contiene al gold y lo rebasa: no es acierto.

## Normativo frente a negativo

La etiqueta se aplica al segmento entero. No lo recorta.

Es negativo, y gana aunque también traiga un predicado, si el segmento contiene alguna de estas señales: `documento sin citas`, `artículo inventado`, `no debe inventar`.

Es normativo si no es negativo y contiene alguna de estas señales: `tiene derecho`, `definirá`, `reglamenta`, `es de aplicación`, `orden público`.

Si no cae en ninguna lista, no es gold. No se inventa un tercer estado. Ampliar las listas es enmendar este contrato.

El gold nuevo de un segmento normativo es el segmento completo, marco incluido cuando la coma lo deja dentro, signo de cierre incluido cuando existe. El recall de extracción usa solo esos gold. Un segmento negativo no entra al denominador. Si no hay ningún normativo, el recall es null y la razón es `denominador_cero`. Una predicción en ese caso es falso positivo.

La resolución de ids no entra en este acierto. Null, `LGS:1` y «artículo primero» se anotarían en otra métrica, el día que se adopte. El `id_incorrecto` publicado por T2 no se recalcula.

## Ejemplos anotados

Los textos son los históricos. Los cortes son ilustración de este contrato. No se escriben en los fixtures.

`synth-salud-01`

| Segmento | Offsets | Clase | Por qué |
|---|---|---|---|
| `Según la Constitución, Toda Persona tiene derecho a la protección de la salud.` | 0:78 | normativo | Hay `tiene derecho`. La coma no saca el marco del gold. El punto cierra y entra. |
| `La Ley definirá las bases y modalidades para el acceso a los servicios de salud.` | 79:159 | normativo | Hay `definirá`. El punto entra. |
| `La Ley General de Salud indica: La presente ley reglamenta el derecho a la protección de la salud que tiene toda persona en los términos del artículo 4o. de la Constitución Política de los Estados Unidos Mexicanos, establece las bases y modalidades para el acceso a los servicios de salud.` | 160:449 | normativo | Hay `reglamenta`. `4o.` no corta. La coma no corta: «, establece…» pertenece al gold. `indica:` no corta. El punto final entra. |

`synth-salud-02`. Un solo segmento, 0:172, normativo por `es de aplicación` y `orden público`. «Solo referencia a LGS:» y « según la ley general de salud en su artículo primero.» pertenecen al mismo gold. El punto final entra.

`synth-salud-03`. Un solo segmento, 0:59, negativo por `documento sin citas`. El punto entra en el segmento y, aun así, no hay gold de extracción.

## Controles

Ninguno está en `tests/`. No se ejecutan. No usan el juez de T2.

| Id | Qué se compara | Acierto | Cobertura | Sobreextensión | Puntuación | Literalidad |
|---|---|---|---|---|---|---|
| C1 | Gold 79:159 de `synth-01` contra esa misma cadena | sí | no | no | no | sí, 79:159 |
| C2 | Ese gold contra la misma cadena sin el punto final | no | no | no | sí | sí, si los offsets de la predicción son el tramo sin punto |
| C3 | Gold 160:449 contra un corte en «Mexicanos» | no | no | no | no | sí para ese prefijo; no cubre el gold |
| C4 | Gold 79:159 contra esa cadena más ` Texto ajeno.` | no | sí | sí | no | sí solo si los offsets abarcan también lo añadido y esa suma está en el texto |
| C5 | `El artículo 4o. reconoce el derecho a la salud.` | un segmento 0:47 | | | | `4o.` no corta; el punto de `salud.` sí entra |
| C6 | `Véase el art. 4 y el deber de prestar salud.` | un segmento 0:44 | | | | `art.` no corta |
| C7 | `El núm. 5 continúa hasta el cierre.` | un segmento 0:35 | | | | `núm.` no corta |
| C8 | `¿La Ley define el acceso?` | un segmento 0:25, cierre `?` incluido | | | | |
| C9 | `Inciso a; sigue el deber.` | 0:9 `Inciso a;` y 10:25 `sigue el deber.` | | | | `;` cierra e entra |
| C10 | `La Ley definirá las bases y modalidades para el acceso a los servicios de salud` | un segmento 0:79, `cierre_ausente` | | | | no se inventa el punto; no es igual a 79:159 de `synth-01` |
| C11 | `Dice «salud». Luego sigue.` | 0:13 incluye el punto; 14:26 es el segmento siguiente | | | | la comilla antes del punto no impide el cierre |
| C12 | `Dice «salud.» Sigue el deber.` | 0:12 cierra en el punto interior; el `»` cae en el segmento siguiente | | | | el punto corta aunque vaya entre comillas |
| C13 | `El artículo inventado 999 garantiza vacaciones eternas.` | negativo, 0:55 | | | | no es gold; emitirlo con cero normativos es falso positivo |
| C14 | `Documento sin citas normativas del corpus de salud del MVP.` | negativo | | | | recall null, `denominador_cero` |

C3 es el control de la coma: la continuación dentro de la unidad es gold, y el prefijo no es acierto. C4 es sobreextensión de verdad, texto de otro segmento. C2 es solo puntuación.

## Paquete de evidencia para una ejecución futura

No se arma con esta nota. T2 no lo tiene, y no se reconstruye. Siguen ausentes el stderr del canario de Seatbelt, el stderr de las tres invocaciones, el entero de tokens y el script de orquestación. `tool_exec: false` es un flag, no el log.

Una corrida posterior, si el Operador adopta este contrato y congela un protocolo, archiva en el repo un directorio con estos archivos y un `SHA256SUMS` de todos ellos:

- el protocolo congelado y su hash;
- el perfil Seatbelt y el comando exacto;
- el stderr del canario que intenta leer el repo, con la denegación;
- el stderr de cada invocación, con exit, provider, modelo, sesión, tokens y cualquier línea de herramienta;
- las predicciones, cada una con `cita_texto`, `inicio` y `fin`;
- el gold nuevo, distinto de los fixtures de T2, con los mismos offsets;
- la versión del juez que implemente la igualdad normalizada y los tres diagnósticos.

Sin ese paquete, la corrida no se declara aislada. Este archivo no es ese paquete.

## Qué se decide después

Adoptar este contrato, rechazarlo, o enmendar las listas antes de congelar un protocolo. Hasta entonces no hay gold nuevo, no hay tests nuevos y no hay corrida.
