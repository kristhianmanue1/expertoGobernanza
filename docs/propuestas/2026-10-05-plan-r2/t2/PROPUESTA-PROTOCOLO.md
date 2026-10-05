# Revisión para decisión, antes de otro protocolo

No es un protocolo congelado. No está ejecutado. No sustituye a `PROTOCOLO.md`, `predicciones.json`, `corrida.json` ni `RESULTADOS.json`. Esos cuatro archivos no se editan. No se invoca un modelo con este texto.

La versión anterior de este archivo pedía «una sola oración, del inicio a su punto final, sin la oración siguiente». Esa regla se retira. No coincide con los límites del gold actual, y el tramo que sobra en dos de los tres rechazos es continuación de la misma oración.

## Por qué una oración con punto no es el gold

Los límites se leen en los fixtures, no en una corrida nueva.

- `synth-01`, gold `g1`. Abarca dos tramos separados por un punto interno («salud. La Ley…») y omite el punto final que el texto sí tiene. El gold termina en «salud», sin punto.
- `synth-01`, gold `g2`. Corta en «Mexicanos», antes de la coma que sigue en la misma oración («, establece…»). El «4o.» interior es una abreviatura, no un fin de oración. El punto de la oración está más adelante, después de «salud».
- `synth-02`, gold `g1`. Corta en «social», antes de « según», todavía en la misma oración. El punto del texto está después de «primero».

Quien copiara cada oración del texto hasta su punto sacaría spans distintos de estos tres gold. Quien copiara el gold tal cual tampoco entregaría «una oración cerrada por punto». Exigir esa forma en el prompt no alinea la extracción con este gold.

## Unidad propuesta, identificable desde el texto

Un segmento verbatim del texto, cortado solo por un límite que el texto muestra.

- Un límite es `.`, `?`, `!` o `;` cuando esos signos no cierran una abreviatura escrita en el propio texto (`4o.`, `art.`, `núm.`).
- La coma no es límite. «, establece» y « según» se quedan en el mismo segmento.
- Si el texto trae el signo de cierre, el segmento lo incluye.
- El corte no consulta el gold. Por eso un modelo puede aplicarlo viendo solo `texto`.

Esta unidad no es el gold de T2. Adoptarla pide gold nuevo en una corrida futura. Los fixtures de T2 se quedan como están.

## Criterio coherente con esa unidad

Tres controles, sobre la misma normalización del juez actual: NFKD, sin diacríticos, espacios colapsados. El acierto de extracción exige los tres. Ninguno usa el id.

1. **Puntuación.** El punto final que el texto trae forma parte del segmento. Quitarlo o añadir un punto que el texto no trae es fallo de puntuación. `4o.` no abre otro segmento. Una coma no abre otro segmento.
2. **Cobertura.** El gold, escrito con esta misma unidad, es subcadena de la predicción. Mide si el contenido de referencia fue recuperado.
3. **Sobreextensión.** La predicción no es subcadena del gold: hay caracteres de más. Un punto de más cuenta aquí y en el control de puntuación. La continuación tras una coma también cuenta aquí. No se llama «oración siguiente» a esa continuación.

El recall de extracción sale solo de estos controles. El alineador de T2 mezcla el fallo de sobreextensión con un único `tp` de contención en un sentido. Esta revisión no cambia ese código ni las métricas ya publicadas.

## Resolución de IDs, separada

Otra métrica y otro denominador. No entra en el recall de extracción.

- Exacto: el id de la predicción es el id de corpus del gold (`LGS:1`, `CPEUM:4:P4`).
- Ausente: null. No quita un acierto de extracción. Se cuenta aparte.
- Incompatible: cualquier otra cadena, incluida «artículo primero». Cuenta aunque el span esté sobreextendido.

El juez de T2 no hace eso. `id_incorrecto` sigue exigiendo que el span quepa en el gold, y por eso el piloto publicó 0. Un protocolo futuro tendría que cambiar el contador. Esta revisión no lo cambia.

El gate v1 tampoco es esta resolución. Sin id, `evaluate` asigna `bajo` sin abrir el corpus. Con un id que no está en el índice, `verify_claim` devuelve `bajo` antes de medir la cita. `alto` sigue inalcanzable.

## Controles que habría que añadir antes de medir

Todavía no están en `tests/`. No se ejecutan ahora.

- Puntuación: punto final sobrante; punto final omitido; `4o.` no parte el segmento; la coma no lo parte.
- Cobertura: el segmento completo recupera un gold escrito con la misma unidad; un prefijo que corta en la coma no lo recupera.
- Sobreextensión: el segmento más la continuación tras la coma no es un acierto exacto; el segmento más el segmento posterior tampoco.
- IDs, en su propia cuenta: null no mueve el recall de extracción; «artículo primero» es incompatible aunque el span sobre; `LGS:1` exacto no se mezcla con el span.

## Decisión pendiente

Antes de congelar un protocolo o de lanzar otra corrida, hace falta una de estas tres:

1. Adoptar esta unidad, encargar gold nuevo y los controles de arriba, y solo después escribir el protocolo.
2. Conservar el gold y el alineador de T2. En ese caso el prompt no puede pedir «una oración con punto», porque ese corte no es el gold.
3. Nombrar otra unidad, por escrito, antes de medir.

## Carencia de evidencia de aislamiento

Sigue ausente del repositorio el stderr del canario de Seatbelt, el stderr de las tres invocaciones, el entero de tokens y el script de orquestación. `tool_exec: false` es un flag del parser, no el log. El párrafo de `PROTOCOLO.md` afirma `Operation not permitted`; no hay un log original junto a esa frase. Esta revisión no reconstruye esos archivos. Una corrida futura tiene que archivar el stderr en el repo antes de dar el proceso por aislado.

## Qué queda cerrado y qué no

T2 queda cerrado en lo administrativo. H1 y H2 siguen en quórum PARCIAL. El PR #53 sigue basado en la rama del PR #52.
