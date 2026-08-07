# Review adversarial — claude (Anthropic, opus-5) — componente F (verificador)

> Ronda multi-provider sobre D+F · 2026-08-06 · artefacto distinto (valida enmienda v1.1-revisada, rompe circularidad). Revisión ejecutada (reproducida). Conflicto de interés: proveedor del quórum.

---

REVISIÓN ADVERSARIAL — Revisor: Claude (Anthropic) / modelo subyacente: claude-opus-5
Artefacto: verificador determinista de citas (MVP) — componentes D (corpus/lookup.py),
           F (verify_citations.py) y modelo derivado CPEUM-004-salud.json
Marco: enmienda de gobernanza v1.1-revisada, Cambio 2 (compuertas deterministas) + DoD.
Lente asumido: CORRECCIÓN / fidelidad del gate (no se me asignó lente; cubro además
           proveniencia y determinismo, y anoto lo que NO pude verificar).
Revisión ciega: no se consultaron salidas de otros revisores (review_kimi.* vacíos).
Fecha: 2026-08-06

CONDICIONES DE EJECUCIÓN
El artefacto entregado es plano (lookup.py, verify_citations.py, un JSON), pero
verify_citations.py importa `from corpus.lookup import load_index` y lookup.py resuelve
DERIVED = <dir de lookup.py>/derived. Para poder ejecutarlo reconstruí el layout implícito
(corpus/__init__.py, corpus/lookup.py, corpus/derived/*.json). Todos los hallazgos marcados
[REPRODUCIDO] se ejecutaron realmente contra ese layout.

VEREDICTO: fix-and-retry (hay BLOCKERs).

======================================================================
BLOCKER
======================================================================

B1. El gate emite nivel `alto`, prohibido en v1 — y lo hace por un booleano
    autodeclarado en el propio artefacto derivado.  [REPRODUCIDO]
    verify_citations.py:56 → `result["response_status"] = "alto" if vig_ok else "medio"`,
    donde `vig_ok = m["vigencia"]["verificada_contra_dof_nivel1"]`.
    Cambio 2, v1: «Default [VIGENCIA-NO-VERIFICABLE]. **Prohibido** emitir nivel `alto`».
    El código no implementa esa prohibición: la implementa el *dato*. Poniendo
    `verificada_contra_dof_nivel1: true` en el JSON derivado —un archivo generado por el
    pipeline de extracción, no por una verificación contra DOF nivel 1— el gate devuelve
    `"response_status": "alto"`, sin notas y con exit 0. Reproducido.
    El eslabón que la enmienda quería sacar del juicio del modelo (la vigencia) queda
    gobernado por un campo que el modelo puede escribir. No hay evidencia asociada al flag
    (ni fecha, ni fuente nivel 1, ni hash del DOF, ni quién lo verificó).
    Fix: (i) constante de versión del gate `GATE_VERSION = "v1"` y `alto` inalcanzable por
    construcción mientras no exista corpus temporal; (ii) cuando exista, que `alto` dependa
    de un registro de verificación con fuente nivel 1 + hash + fecha, no de un booleano.

B2. Bypass total del gate de fidelidad con una cita vacía tras normalización.
    [REPRODUCIDO]
    verify_citations.py:50-51: `if cita:` (verdadero para "   ") y luego
    `_normalize(cita) in _normalize(texto)`. `_normalize("   ")` → `""`, y `"" in cualquier
    cosa` → True. Resultado ejecutado con `cita_texto: "   "`:
      quote_exact_match: true, response_status: "medio", exit 0.
    Igual con una cita compuesta sólo de diacríticos combinantes (p. ej. U+0301), que
    `_normalize` elimina por completo → `""` → match. Reproducido en ambos casos.
    Es decir: un claim sin cita real obtiene el mismo estatus que un claim citado y
    verificado. El gate determinista que sostiene toda la compuerta de fidelidad se evade
    con espacios en blanco.
    Fix: rechazar `cita_texto` cuya forma normalizada sea vacía o menor a un mínimo
    (p. ej. 40 caracteres normalizados) → `bajo` + nota explícita; y tratar la ausencia de
    cita como error de esquema, no como caso silencioso.

B3. (d) «fuente oficial resuelta» no verifica nada: comprueba que el campo sha256 exista,
    nunca lo recalcula.
    verify_citations.py:52: `any(f.get("sha256") for f in m.get("fuentes_oficiales", []))`.
    No se abre `corpus/originals/CPEUM.pdf`, no se comprueba que exista, no se recomputa el
    digest, y no se coteja `lineage.extraido_de_sha256` contra él. Una cadena arbitraria en
    ese campo satisface el gate. Tampoco se usa `extracto_verbatim_en`
    (docs/fuentes/cpeum/art-004.txt), que es el único artefacto humano-cotejable del modelo.
    Consecuencia: la cadena de proveniencia que la enmienda exige (Cambio 3: «log de hash»,
    Cambio 4: custodio/hashes/procedencia) no está cerrada en el único punto donde el código
    podía cerrarla de forma determinista.
    Fix: resolver la ruta, verificar existencia, recomputar sha256 y compararlo con el
    declarado y con `lineage.extraido_de_sha256`; discrepancia → `bajo` + BLOCKER de corpus.

B4. No hay DoD ejecutable: cero tests, cero golden set, y el paquete no importa tal como
    se entrega.
    Cambio 2 cierra con: «Estos gates son **code**: su corrección se prueba (DoD ejecutable)».
    No hay tests unitarios, ni casos negativos, ni el golden set contra el que Cambio 2 exige
    «medir el recall de extracción». Los tres BLOCKERs anteriores son precisamente los casos
    que una suite mínima de casos negativos habría capturado.
    Además, la enmienda define la salida estructurada `claim → cita → id de disposición` y
    aquí el claim se acepta como JSON libre: no hay validación de esquema, y campos
    desconocidos (p. ej. una `fecha_juridica_relevante` que un consumidor de v2 enviaría) se
    ignoran en silencio en vez de rechazarse.
    Fix: suite con casos negativos (B1-B3 como regresiones), validación de esquema estricta
    del claim (rechazar campos desconocidos), y golden set mínimo antes de declarar el gate
    utilizable.

======================================================================
MED
======================================================================

M1. `in` (substring) no es «coincidencia exacta»: habilita cherry-picking por elisión.
    El docstring (líneas 10-11) afirma «el match de cita es exacto normalizado». No lo es:
    es contención de subcadena. Cualquier fragmento contiguo pasa, incluidos los que cortan
    a mitad de oración y suprimen el condicionante. Con este mismo artefacto, citar
    «Toda Persona tiene derecho a la protección de la salud» pasa el gate omitiendo que «La
    Ley definirá las bases y modalidades para el acceso» — la parte que fija el alcance real
    del derecho. El gate valida *procedencia textual*, no *fidelidad del sentido*, y el
    docstring dice lo contrario.
    Esto interactúa con M2: la unidad citable es demasiado grande, así que la elisión tiene
    mucho margen.
    Fix: (a) corregir el docstring —la propiedad garantizada es «el fragmento aparece
    literalmente», no «la cita es exacta»—; (b) devolver offsets del match y marcar cortes
    que no coincidan con límites de oración/párrafo; (c) mínimo de longitud (ver B2).

M2. El modelo derivado concatena en un solo `texto_verbatim` lo que en el artículo 4º
    constitucional son párrafos distintos.  [REPRODUCIDO]
    `jerarquia_documental.elemento` dice «párrafo» (singular), pero el `texto_verbatim`
    reúne el párrafo del derecho a la protección de la salud y el del «sistema de salud para
    el bienestar» (reforma DOF 08-05-2020) bajo un único id `CPEUM:4:Psalud`.
    Verificado: una cita que cruza ese límite —«73 de esta Constitución. La Ley definirá un
    sistema de salud»— obtiene `quote_exact_match: true`. El gate certifica como una sola
    cita literal un texto que en la fuente son dos disposiciones separadas, con historias de
    reforma y vigencia distintas.
    Consecuencia sobre v2: cuando se añada (b) vigencia por fecha, este id no podrá tener una
    respuesta única —los dos párrafos tienen fechas de reforma distintas—, así que el defecto
    de granularidad bloquea la evolución del gate, no sólo su precisión actual.
    Fix: un id por párrafo (`CPEUM:4:P4`, `CPEUM:4:P5`...), aun provisional; y prohibir
    matches que crucen fronteras de disposición.

M3. `load_index()` no es determinista ante ids duplicados y traga corrupción en silencio.
    [REPRODUCIDO]
    corpus/lookup.py:18-26 itera `DERIVED.rglob("*.json")` y hace `idx[did] = m` sin detectar
    colisiones: el último archivo en el orden de recorrido gana, y ese orden no está
    garantizado entre plataformas ni entre ejecuciones. Reproducido: añadiendo un segundo
    JSON con el mismo `disposicion_id` y `texto_verbatim: "TEXTO SUPLANTADO"`, el índice
    devuelve el texto suplantado. Es una vía de suplantación de corpus que no requiere tocar
    el archivo legítimo, y contradice frontalmente el «puramente determinista» del docstring.
    Además, `except (OSError, ValueError): continue` descarta JSON ilegible sin señal alguna:
    un corpus roto se vuelve indistinguible de un corpus donde la disposición no existe
    (ambos → `bajo`). Falla cerrado en el veredicto, pero ciego en el diagnóstico —y el
    custodio del Cambio 4 no tiene cómo enterarse.
    Fix: error duro ante `disposicion_id` duplicado; recorrido ordenado (`sorted(...)`);
    contabilizar y reportar archivos ilegibles en lugar de descartarlos.

M4. `medio` devuelve exit 0, y `medio` está prohibido en contextos de decisión.
    verify_citations.py:74: `return 0 if r["response_status"] in ("medio","alto") else 1`.
    Cambio 2: `medio` = «prohibido en contextos de decisión, consumible sólo como borrador».
    Cualquier integración shell/CI (`if verify_citations.py ...; then`) leerá exit 0 como
    aprobación y promoverá a decisión un resultado que la política prohíbe usar para decidir.
    Con B1 sin arreglar, hoy *todo* resultado verificable es `medio` → el gate señaliza «OK»
    en el 100 % de sus aprobaciones.
    Fix: códigos distintos por nivel (0=alto, 2=medio, 1=bajo) y documentarlos; o exit
    distinto de cero salvo `alto`.

M5. El resultado no es evidencia auditable.
    La salida no incluye el sha256 de la fuente, la versión del gate, la versión/estado del
    corpus, ni el id del artefacto derivado usado. Los Cambios 1, 3 y 4 exigen persistir
    evidencia con proveniencia; un `response_status` sin esos campos no es reproducible ni
    verificable a posteriori. `version_valid_for_date` es la constante `"N/A_v1"`, no un
    hecho computado.
    Fix: incluir `gate_version`, `corpus_hash`, `fuente_sha256`, `derived_file`, y el offset
    del match en cada resultado.

M6. Coste y forma de `load_index()`: se relee y reparsea todo el corpus en cada
    `verify_claim` (verify_citations.py:33). Con un corpus real (CPEUM + LGS + ...) y
    verificación por claim, esto es O(claims × corpus). No es sólo rendimiento: hace que dos
    claims de la misma corrida puedan verse contra estados de disco distintos si el corpus
    cambia entre llamadas —otra fuga del determinismo prometido.
    Fix: cargar una vez por proceso, congelar el índice y sellarlo con un hash reportado (M5).

======================================================================
LOW
======================================================================

L1. `_normalize` aplica NFKD y borra todos los diacríticos: «año»≡«ano», «sólo»≡«solo»,
    «él»≡«el». Para citas jurídicas es probablemente aceptable, pero es una decisión
    sustantiva no declarada. Documentarla explícitamente como política de comparación.
L2. La normalización colapsa espacios pero no toca puntuación ni guiones de corte de línea.
    Como el `texto_verbatim` viene de pypdf y el propio `lineage.notas` advierte
    «artefactos del parser», una cita correcta tomada del DOF puede fallar (falso bloqueo)
    y una cita con los mismos artefactos que el extracto pasar. Sin cotejo del extracto
    contra fuente nivel 1, no hay forma de saber en qué dirección falla.
L3. `relaciones_normativas[1].verificada: false` y el marcador `[VERIFICAR-FUENTE]` no
    influyen en ningún gate: son anotaciones inertes. Si van a existir, que un gate las lea.
L4. `id_scheme_note` reconoce que el id es provisional. Correcto declararlo, pero implica que
    los resultados de hoy no son reproducibles cuando el parser asigne ordinales estables:
    conviene versionar el esquema de ids y registrar `id_scheme_version` en cada resultado.
L5. `instrumento.entrada_camara: 1` no está documentado en ninguna parte del artefacto.
L6. Ambigüedad de la propia enmienda: la «regla fija block/degrade» de Cambio 2 sólo legisla
    (a)/(c) y (b); no dice qué hacer si falla (d). El código bloquea —elección correcta,
    fail-closed— pero la regla debería decirlo explícitamente para que no quede a criterio
    de la implementación.

======================================================================
NO VERIFICADO (declarado, no afirmado)
======================================================================
- No pude cotejar `texto_verbatim` contra fuente nivel 1 (DOF) ni contra el consolidado de
  Cámara: no tengo el PDF ni acceso a corpus temporal. Las fechas declaradas
  (adicionado 1983-02-03, última reforma 2020-05-08) son plausibles para el art. 4º pero
  quedan SIN VERIFICAR por este revisor; el marcador
  `[VIGENCIA-NO-VERIFICADA contra DOF nivel 1]` del artefacto es correcto y honesto.
- No pude recomputar el sha256 declarado (`ca63a23a…`): el original no forma parte del
  material entregado.
- No evalué el pipeline de extracción (recall de claims), fuera del material entregado.

======================================================================
NOTA DE PROCESO (sobre el DoD de la enmienda)
======================================================================
La enmienda dice que el DoD se cumple con hallazgos «registrados y resueltos/aceptados por
escrito, independientemente del veredicto». Consistente con eso: este `fix-and-retry` no
invalida la corrida. Pero sí conviene registrar que B1 —el gate emitiendo un nivel que la
propia enmienda prohíbe en v1— es evidencia de la brecha que Cambio 2 buscaba cerrar: la
compuerta «determinista en código» delegó su decisión más sensible a un campo de datos
producido aguas arriba. Vale la pena preguntar en la reconciliación si otras compuertas
planeadas heredan ese patrón.
