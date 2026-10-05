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

## Corrección de la coma

La coma no parte la unidad. Toda continuación que queda dentro del segmento pertenece al gold nuevo. Cortar en la coma no es el acierto, y conservar «, establece…» o « según…» no es sobreextensión respecto de ese gold. Una versión anterior de esta sección decía lo contrario. Queda retirada.

El contrato enmendado, todavía sin adoptar y sin corrida, está en `OPCION-1-CONTRATO.md`. El acierto exige literalidad y offsets, y después igualdad normalizada. Las listas léxicas son benchmark sintético, no verdad normativa.

## Resolución de IDs, separada

Otra métrica y otro denominador. No entra en el recall de extracción.

- Exacto: el id de la predicción es el id de corpus del gold (`LGS:1`, `CPEUM:4:P4`).
- Ausente: null. No quita un acierto de extracción. Se cuenta aparte.
- Incompatible: cualquier otra cadena, incluida «artículo primero». Cuenta aunque el span esté sobreextendido.

El juez de T2 no hace eso. `id_incorrecto` sigue exigiendo que el span quepa en el gold, y por eso el piloto publicó 0. Un protocolo futuro tendría que cambiar el contador. Esta revisión no lo cambia.

El gate v1 tampoco es esta resolución. Sin id, `evaluate` asigna `bajo` sin abrir el corpus. Con un id que no está en el índice, `verify_claim` devuelve `bajo` antes de medir la cita. `alto` sigue inalcanzable.

## Decisión pendiente

La opción 1 está escrita en `OPCION-1-CONTRATO.md`: contrato, ejemplos anotados y controles. No está adoptada. No se congela otro protocolo y no hay otra corrida hasta que el Operador la adopte. Los fixtures y los resultados de T2 siguen históricos.

## Carencia de evidencia de aislamiento

Sigue ausente del repositorio el stderr del canario de Seatbelt, el stderr de las tres invocaciones, el entero de tokens y el script de orquestación. `tool_exec: false` es un flag del parser, no el log. El párrafo de `PROTOCOLO.md` afirma `Operation not permitted`; no hay un log original junto a esa frase. Esta revisión no reconstruye esos archivos. Una corrida futura tiene que archivar el stderr en el repo antes de dar el proceso por aislado.

## Qué queda cerrado y qué no

T2 queda cerrado en lo administrativo. H1 y H2 siguen en quórum PARCIAL. El PR #53 sigue basado en la rama del PR #52.
