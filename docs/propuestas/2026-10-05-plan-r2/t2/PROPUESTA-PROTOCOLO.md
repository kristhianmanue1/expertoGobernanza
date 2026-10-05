# Propuesta de protocolo posterior a T2

No es el protocolo congelado. No está ejecutado. No sustituye a `PROTOCOLO.md` ni a `RESULTADOS.json`. Una corrida con este texto necesita otra delegación que lo nombre, y tiene que quedar fechada antes de ver números nuevos. El cierre administrativo de T2 y el quórum de H1/H2 siguen en sus propios carriles.

## Qué alinear

El prompt de `692bdd9` pidió un fragmento verbatim y un id solo si el texto lo escribía. No dijo tres cosas que el juez ya usa:

1. **Extracción.** El alineador cuenta la predicción solo cuando ella cabe dentro del gold. Un gold que cabe dentro de una predicción más larga es un fallo. El control `test_texto_completo_no_cuenta` fija esa dirección. El mínimo normalizado es 20 caracteres.
2. **Identificación.** Si la predicción trae id y el gold también, tienen que ser el mismo identificador de corpus (`LGS:1`, `CPEUM:4:P4`). Una glosa como «artículo primero» no es ese id. Un id null todavía puede ser verdadero positivo del alineador.
3. **Gate.** Va después y no mueve el recall. Sin id, `evaluate` asigna `bajo` sin consultar el corpus. Con id, `verify_claim` exige que la disposición exista en el índice derivado; si no existe, `bajo` y no mide la cita. El gate v1 sigue con `alto` inalcanzable y `version_valid_for_date` en `N/A_v1`. Su mínimo de cita es 40, distinto del 20 del alineador.

## Prompt propuesto

El marcador `{{TEXTO}}` no se rellena en este archivo.

```text
Extrae citas del texto. Responde solo con un objeto JSON, sin markdown y sin explicacion.
Esquema: {"predictions":[{"disposicion_id": string o null, "cita_texto": string}]}
Reglas:
- Cada cita_texto es una sola oracion del texto, copiada verbatim, del inicio de la oracion a su punto final inclusive, sin la oracion siguiente y sin una atribucion añadida despues.
- No alargues la cita. El evaluador acepta la prediccion solo si ella cabe dentro de la cita de referencia. Si la referencia cabe dentro de una prediccion mas larga, esa prediccion no cuenta.
- disposicion_id es el identificador de corpus que el propio texto escriba con forma INSTRUMENTO:numero, por ejemplo LGS:1 o CPEUM:4:P4. Si el texto no escribe ese identificador, usa null. No parafrasees «articulo primero» ni otro nombre.
- No inventes citas ni identificadores. Si no hay cita, predictions es [].
- No uses herramientas ni leas archivos.
Texto:
{{TEXTO}}
```

La reparación, si hiciera falta en una corrida futura, repetiría este mismo criterio y el código de error del validador. No incluiría el gold.

## Lo que esta propuesta no decide

- No fija un umbral de aceptación ni un 0.8.
- No declara regresión contra los ceros de T2: cambiar el prompt crea otra medición. La regresión del protocolo ya ejecutado sigue siendo la de `PROTOCOLO.md`.
- No cierra T2. La casilla de roles §9 en el PR #53 sigue abierta.
- No adelanta el `proceed` de H1/H2. El quórum de esos hitos no usa este archivo.
