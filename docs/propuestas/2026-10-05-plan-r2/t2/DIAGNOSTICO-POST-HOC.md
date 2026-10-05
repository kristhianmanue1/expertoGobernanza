# Diagnóstico post hoc de T2

Este archivo se escribió después de observar `RESULTADOS.json`. No modifica `PROTOCOLO.md`, `predicciones.json`, `corrida.json` ni las métricas. No hubo otra invocación al modelo. T2 sigue siendo un piloto ejecutado, con resultados reproducibles, y con el cierre administrativo abierto: falta la anotación de roles §9 en el PR #53. Ese cierre no es el quórum de H1/H2.

## Tres rechazos por límite de extracción

El alineador `t1b-containment-min20` acepta una predicción solo si, ya normalizada, mide al menos 20 caracteres y es subcadena del gold (`scripts/eval_extraction.py`, `_compatible`). La dirección inversa no cuenta: que el gold quepa dentro de la predicción es un fallo. Los tres gold con `must_find` fallan así. Las longitudes son de la cadena normalizada.

| Caso | Predicción | Gold | La predicción cabe en el gold | El gold cabe en la predicción | Caracteres de más |
|---|---|---|---|---|---|
| `synth-salud-01` predicción 0 | id null | `g1` `CPEUM:4:P4` | no | sí | 1 |
| `synth-salud-01` predicción 1 | id null | `g2` `LGS:1` | no | sí | 76 |
| `synth-salud-02` predicción 0 | id presente | `g1` `LGS:1` | no | sí | 54 |

El carácter de más del primer par es el punto final: el gold de `g1` termina en «salud» y la predicción añade «.». El segundo par continúa después de «Mexicanos» con la oración siguiente. El tercero continúa después de «social» con la atribución a la ley. `synth-salud-03` no entra en estos tres: no tiene gold `must_find` y la predicción fue `[]`. Su recall null es `denominador_cero`, no un rechazo.

Un id null no provoca estos tres rechazos. `_compatible` solo compara ids cuando los dos están presentes. El control `test_tp_sin_id_puede_tener_gate_bajo` obtiene un verdadero positivo con id null si el texto sí cabe en el gold.

## Identificación, aparte de la extracción

La predicción de `synth-salud-02` trae `disposicion_id` «artículo primero». El gold de ese caso es `LGS:1`. Esas dos etiquetas no son el mismo identificador.

`RESULTADOS.json` deja `id_incorrecto` en 0. El contador del juez también exige que la predicción esté contenida en el gold; como el span ya no cabe, no llega a comparar las etiquetas. El 0 publicado es el del juez. Esta lectura no lo cambia.

## Gate, aparte de las dos capas anteriores

- En `synth-salud-01` las dos predicciones no tienen id. `evaluate` no llama a `verify_claim`: asigna `bajo` por la ausencia del id. Los dos `gate_bajo` de ese caso son ese atajo, no una búsqueda en el corpus.
- En `synth-salud-02` el id sí existe, así que `verify_claim` corre. Sobre la predicción conservada devuelve `response_status` `bajo`, `reference_exists` false y la nota «disposicion no encontrada en el corpus». Sale antes de medir la cita: `match_len` 0, `quote_substring_match` false, `source_check` y `registry_check` null. `version_valid_for_date` queda `N/A_v1`.
- El gate no decide el recall. El recall lo decide el alineador.

## Controles positivos del evaluador

Son los de `tests/test_eval_extraction.py`, clase `TestJuezT1b`. Usan la cita sintética «texto compartido de la cita que supera los veinte caracteres», no los fixtures de T2. Una corrida local de esa clase el 2026-10-05 dio 10 tests OK. No recalculó T2.

| Test | Lo que queda demostrado |
|---|---|
| `test_ids_distintos_recuperan_los_dos_gold` | Dos ids distintos y el mismo texto dan recall 1. |
| `test_tp_sin_id_puede_tener_gate_bajo` | Un id null puede ser verdadero positivo y, a la vez, `gate_bajo`. |
| `test_texto_completo_no_cuenta` | Una predicción que envuelve la cita y la alarga no es verdadero positivo. Es el mismo límite que los tres rechazos de T2. |
| `test_id_incorrecto_y_vacio` | Si el texto sí cabe y el id es otro (`C:9`), `id_incorrecto` es al menos 1 y el tp es 0. |
| `test_diez_copias_no_inflan_recall` | Diez copias del mismo acierto cuentan un tp. |
| `test_nulo_no_recupera_el_otro_gold` | Un id null no se queda con el gold que ya cubre otra clase. |

El juez sabe devolver recall 1 y sabe contar un id incompatible cuando el span cabe. Los ceros de T2 no salen de un juez que siempre devuelve cero.

## Procedencia de los hashes

Recomputados el 2026-10-05 contra los archivos de esta rama. Coinciden con `RESULTADOS.json`. No los emitió el modelo.

| Campo | Qué es |
|---|---|
| `texto_sha256` | SHA-256 de los bytes UTF-8 del valor JSON `texto`. No incluye `gold_claims` ni `traps`. |
| `gold_file_sha256` | SHA-256 de los bytes del archivo fixture completo. |
| `protocolo.sha256` | SHA-256 de los bytes de `PROTOCOLO.md`. El commit que lo congeló es `692bdd9`. |
| `predicciones.sha256` | SHA-256 de los bytes de `predicciones.json`. |
| `corrida.sha256` | SHA-256 de los bytes de `corrida.json`. |
| `juez.blob_sha256` y `gate.blob_sha256` | Valores de 40 hexadecimales obtenidos con `git rev-parse HEAD:<ruta>`. Son el id Git del blob, no un SHA-256 del archivo. El nombre del campo en `RESULTADOS.json` dice `blob_sha256`. Este diagnóstico no renombra ese campo. Hoy esas rutas siguen en `61d288ddeb5e51a5a10f2510dbabaaef80ccc058` y `f54afe927b86f59cd43d8f6cbca60b3c8896e22c`. |

## Evidencia de Seatbelt y de herramientas

Conservado en git:

- `PROTOCOLO.md`, commit `692bdd9`, describe el perfil `(allow default)` con denegación de lectura del repo, de `aria` y de las sesiones de Grok, y afirma que un `open` del fixture devolvió `Operation not permitted` antes de la corrida.
- `corrida.json` guarda, por cada caso, `tool_exec: false`, el exit 0, el modelo `gpt-6.1-sol`, el provider `openai` y el id de sesión. `tokens` es null, con la nota de que el parser no guardó el entero.

No está en el repositorio, y esta nota no lo reconstruye como si lo estuviera:

- El stderr del canario previo, tanto el `open` de Python como la respuesta del CLI.
- El stderr de las tres invocaciones puntuadas. `tool_exec: false` es la salida de un parser que buscaba una línea igual a `exec`. Sin el stderr no se puede volver a leer si esa línea existió y el parser la perdió.
- El entero de tokens.
- El script de orquestación, que vivió en `/tmp` y se borró.
- Cualquier transcript del modelo.

La afirmación del protocolo sobre `Operation not permitted` queda como texto del protocolo. No hay un log original junto a ella.
