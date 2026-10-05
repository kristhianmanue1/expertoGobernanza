# Protocolo T2 — R2-H1-02

**Fecha de congelación:** 2026-10-05, antes de invocar al modelo sobre los fixtures. **Ticket:** `R2-H1-02`. **Delegación:** el Operador escribió «t2 te lo delego a ti, continua». No nombró un CLI. Grok no está en la allowlist y no recibe el texto. **Revisión del plan que exige esa delegación:** `fe8e31b` en `docs/plan-r2-tres-papeles` (PR #52, todavía no es `main`).

Este archivo no se edita después de observar métricas. Una corrida posterior es otro protocolo.

## Proveedor

- Preflight de `claude` 2.1.280, sin texto de fixture, con `--tools ""`: HTTP 403 `oauth_not_allowed_for_organization`. No hubo modelo ni tokens de inferencia.
- Proveedor congelado por esa disponibilidad, no por una métrica: CLI `codex` 0.160.1, que la allowlist identifica como OpenAI.
- Invocación: `codex exec --ignore-user-config --ephemeral --skip-git-repo-check --sandbox read-only`. No se pasa `-m`. El preflight, también sin fixture, reportó `provider: openai` y `model: gpt-6.1-sol`. Cada caso registra el header real. Si el header cambia, se anota y no se relanza.
- Temperatura y semilla: el modo no las expone. El header del preflight dijo `reasoning effort: none`. No se fija otro valor.

## Muestra

Los tres JSON de `tests/fixtures/extraction_gold/` (`synth-01.json`, `synth-02.json`, `synth-03.json`). El `doc_id` es el campo del archivo. Son fixtures conocidos: piloto exploratorio, no holdout ni evidencia de generalización. El conjunto no se modifica en esta corrida.

## Ceguera al gold

- El proceso recibe solo el campo `texto`. No recibe `gold_claims` ni `traps`.
- Corre con el directorio de trabajo `/tmp/t2-payload`, que contiene únicamente el texto del caso.
- Seatbelt `(allow default)` y denegación de lectura de `/Users/krisnova/www/expertoGobernanza`, `/Users/krisnova/www/aria` y `/Users/krisnova/.grok/sessions`. Un `open` de un fixture desde ese perfil ya devolvió `Operation not permitted` antes de esta corrida.
- Si el stderr de un caso muestra un comando `exec`, el intento queda anulado. No se reintenta para esquivar esa anulación.

## Prompt congelado

Marcador `{{TEXTO}}`. El archivo de protocolo no contiene el texto del fixture.

```text
Extrae citas normativas del texto. Responde solo con un objeto JSON, sin markdown y sin explicacion.
Esquema: {"predictions":[{"disposicion_id": string o null, "cita_texto": string}]}
Reglas:
- cita_texto es un fragmento contiguo y verbatim del texto, tal como aparece.
- disposicion_id es un identificador de disposicion solo si el propio texto lo escribe; si no aparece, null.
- No inventes citas ni identificadores. Si no hay cita, predictions es [].
- No uses herramientas ni leas archivos.
Texto:
{{TEXTO}}
```

Reparación, como máximo una vez, solo si el JSON no cumple el esquema. No incluye gold ni la salida inválida completa; incluye el código de error del validador local.

```text
La salida anterior no es JSON valido contra el esquema. Error: {{ERROR}}.
Devuelve solo el objeto JSON. No uses herramientas.
Esquema: {"predictions":[{"disposicion_id": string o null, "cita_texto": string}]}
Texto:
{{TEXTO}}
```

## Agregación

- Un caso, una invocación. La primera salida que valida el esquema es la que se puntúa.
- La reparación no es un segundo candidato para elegir el mejor número. Si la primera ya valida, no hay reparación.
- Si ninguna valida, o si el intento se anula por `exec`, las predicciones puntuadas de ese `doc_id` son `[]` y el registro marca `extraccion_invalida`. Eso no se presenta como una extracción vacía deliberada.
- Tope: 2 invocaciones por fixture y 6 en total. Agotar el tope deja el caso inválido. No se cambia de proveedor.

## Métricas y regresión

El juez es `scripts/eval_extraction.py` en el blob `61d288ddeb5e51a5a10f2510dbabaaef80ccc058`, versiones `t1b-v1` y `t1b-containment-min20`. El gate es `corpus/verify_citations.py` blob `f54afe927b86f59cd43d8f6cbca60b3c8896e22c`, `GATE_VERSION` `v1`. El recálculo es `--predictions-file`, sin otra invocación al modelo.

Métricas que se registran: `precision`, `recall`, `gate_bajo`, con sus denominadores (`tp`, `fp`, `fn`, `n_pred`, `n_gold`).

No hay umbral de aceptación. El Operador no fijó un mínimo al delegar. No se usa 0.8 ni ningún piso elegido al ver el número. El método de Skevi `06` §2–§3 pide declarar umbral, muestra y regresión antes de medir; aquí el umbral de aceptación queda explícitamente sin declarar, y la muestra y la regresión sí quedan declaradas.

Regresión de una corrida futura, solo si conserva estos `doc_id`, este evaluador y este gate: `recall` agregado menor que el `recall` de `RESULTADOS.json`, o `gate_bajo` agregado mayor. Un empate no es regresión. Cambiar fixtures o juez invalida la comparación.

## Qué se publica

`RESULTADOS.json` lleva proveedor, modelo, ids, hashes de texto y de gold, SHA del juez, versión del gate y las métricas. El prompt y las predicciones entran como hash y ruta. El JSON publicado no copia citas, texto de fixture ni transcript. Las predicciones recuperables viven en `predicciones.json`.
