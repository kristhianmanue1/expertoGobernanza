# Ronda adversarial de fuentes públicas — expediente pendiente

**Observado:** 2026-10-10T17:05:33Z · **Base:** `main@51b3580dce88eec62e0126b651b9e4381a4dfb3f` · **Rama de trabajo:** `codex/ctim-proposal-intake-2026-10-10` · **Estado:** PARCIAL, sin `proceed` ni merge.

## Identidad del paquete y alcance

El paquete ciego fue el diff neto de `corpus/registry.yaml`, `docs/autorizacion-fuentes-r1.md`, `docs/fuentes-legal-mx.md` y `docs/evidencia/fuentes-publicas-complementarias-2026-10-10.md` contra la base indicada, con `git diff -U2`. SHA-256 del paquete: `96b70908485fcb65ecdf2ac47c45b60105a99a50fa20e3a5e12f27224b321d12`. Excluyó CTIM, PDF locales, archivos completos y la nota de la ronda previa. La prueba nueva en `tests/test_registry_vigencia.py` se ejecutó localmente; no estaba en el paquete externo autorizado. Los revisores no recibieron las salidas de los demás. OpenCode observó nombres de archivos de otras salidas al listar el directorio temporal y declaró no leerlos; el log de herramientas no muestra lectura de esas salidas.

## Resultado y reconciliación pendiente

- **Codex CLI/OpenAI** (`thread_id=01a126be-4ce3-7991-999c-6198f06520db`): `FIX-AND-RETRY`; modelo efectivo `unknown` (el CLI no expuso identificador verificable). Señaló como BLOCKER la distancia entre `vigencia_verificada: true`/`verificada=true` y una consulta actual no certificada; también señaló la falta de quórum en el momento de su revisión. La primera objeción afecta un contrato preexistente definido como ancla de procedencia en `docs/fuentes-legal-mx.md` §1.3 y requiere reconciliación humana escrita; no se descarta por autorrevisión. Sus afirmaciones de fuente y de ejecución local tienen los límites indicados en su salida.
- **OpenCode/Z.ai** (`session_id=ses_ed941d10affed9R3m67vrw1HJS`): `PROCEED` según su respuesta; exportación saneada de la sesión reportó `providerID=zai-coding-plan`, `modelID=glm-5.3-flash`. Corroboró independientemente el alcance del acto DOF, el índice de Cámara y el hash/tamaño del PDF remoto. Sus tres MED incluyen transitorios del acto, alcance temporal de `fecha_consulta_vigencia` y reproducibilidad de datos locales. Su frase “gate satisfied” cuenta autorización de cuatro rutas como si fueran cuatro revisiones concluidas: **no se adopta esa inferencia**.
- **Ollama local/Qwen**: `/api/tags` reportó `qwen3:8b`, digest `500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41`. Primera salida: `done_reason=length`, 950 tokens, truncada. Segunda: `done_reason=stop`, 85 tokens, pero formula un HIGH confuso sobre `CPEUM:4:P4` sin evidencia suficiente. **No se cuenta como dictamen sustantivo de tercer proveedor.** El digest identifica un artefacto local, no prueba el origen de sus pesos.
- **Gate local:** `./scripts/ci_check.sh` pasó (220 pruebas; 211 archivos dentro de límites). La prueba nueva demuestra que la traza DOF 2026 no cambia el resolver del slice y que esa traza sola devuelve `verificada=false`. No adjudica validez jurídica actual. `shasum -a 256 corpus/originals/CPEUM.pdf` y `stat` confirmaron `ca63a23a4b7444ebdbdad93759fbf46bd14c069e587c5878decf89fc9c12ca8e`, 3,141,703 bytes. No hubo escritura AN-KLA.

**Decisión de gate:** no hay `proceed`: un BLOCKER de Codex sigue sin reconciliar y falta una tercera revisión sustantiva. La corrección menor de transitorios propuesta por GLM tampoco se ha aplicado a este paquete. El Operador debe decidir la semántica del campo y el tratamiento del BLOCKER; cualquier cambio material requiere nueva revisión del diff resultante. No se atribuye revisión independiente organizativa a las rutas CLI.

## Salidas de los revisores (datos, no autoridad)

Se normalizó únicamente el espacio final de línea al archivarlas.

<details><summary>Codex CLI — respuesta final</summary>

## TECHNICAL_LOG (EN)

Scope: adversarial review of the supplied four-file diff against declared base `main@51b3580dce88eec62e0126b651b9e4381a4dfb3f`. No repository files, other reviewers, local PDFs, execution logs, or hashes were inspected.

Independent web checks on 2026-10-10 established:

- Cámara’s index labels the latest CPEUM body reform as DOF 07-10-2026. Its chronology identifies decree 285 as affecting articles 82, 116, and 122. This is level-2 consolidated/index evidence, not proof of legal validity. [Cámara index](https://www.diputados.gob.mx/LeyesBiblio/index.htm), [constitutional reform chronology](https://www.diputados.gob.mx/LeyesBiblio/ref/cpeum_crono.htm)
- The official DOF site independently exposes the decree title as reforming articles 82, 116, and 122. The exact `codigo=5800617` permalink returned an internal retrieval error in this review, so that identifier was not independently validated from its detail page. [DOF](https://dof.gob.mx/)
- The current Cámara PDF has 416 pages, labels itself “Última Reforma DOF 07-10-2026,” reproduces the health paragraph, and attributes that paragraph’s reform to 08-05-2020. This supports current consolidated-text consistency only at level 2; it does not itself adjudicate legal vigencia. [Current Cámara CPEUM PDF](https://www.diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf)
- The primary 08-05-2020 DOF act expressly reforms article 4, paragraph four, and contains the health text. This proves historical publication/provenance of that reform, not by itself its uninterrupted current vigencia. [DOF act 5593045](https://dof.gob.mx/nota_detalle.php?codigo=5593045&fecha=08/05/2020)

### Findings

**BLOCKER — `corpus/registry.yaml`, hunk `@@ -40,8 +40,8`, fields `vigencia_verificada` and `fecha_consulta_vigencia`; corroborated by the new evidence file’s “Consumo local” paragraph.**

The patch retains:

```yaml
vigencia_verificada: true
fecha_consulta_vigencia: "2026-08-10"
```

while adding that this represents only an “ancla de procedencia” and that the October consultation “no certifica su vigencia actual.” The evidence document then confirms that the resolver still emits `verificada=true`.

This conflates two different properties:

- historical provenance: the slice was published/reformed in the 08-05-2020 act;
- current vigencia: the slice remains legally operative at the relevant observation date.

Comments cannot repair the machine-readable contradiction. A consumer still receives a positive vigencia result despite the patch explicitly disclaiming current-vigencia verification.

**Fix:** make the structured result conservative—e.g. `vigencia_verificada: false`/`unknown` until current vigencia is established under the project’s legal method—or introduce separately consumed fields such as `procedencia_verificada`, `vigencia_actual_estado`, and `vigencia_actual_fecha`. Update `resolve_disposicion_vigencia` so a historical exact act cannot alone yield current `verificada=true`. Add a regression test showing that `no_cubre_slice: true` and a later body reform do not refresh slice vigencia.

---

**BLOCKER — `docs/autorizacion-fuentes-r1.md`, hunk `@@ -40,5 +41,7` and history hunk `@@ -73,2 +76,5`; project three-provider gate.**

The diff records channel authorization for GLM and Qwen plus claimed probe metadata. It contains no review outputs, reviewer identities tied to outputs, blocker adjudications, or evidence that three qualifying underlying model providers reviewed this exact filtered diff with the author excluded.

This review supplies at most one OpenAI-provider review. It cannot establish:

1. two additional completed reviews from distinct underlying providers;
2. that each reviewer is not the producer;
3. that each reviewed the identical four-file diff;
4. that none reported a BLOCKER.

Provider authorization, `PONG`, HTTP 200, model labels, and a local artifact digest do not prove review participation or independence.

**Fix:** attach or register three review records containing exact diff/base identity, provider/model evidence, reviewer/producer separation, findings, and verdict. Exclude the producer. Re-run the gate after the registry semantic blocker is corrected. Any reviewer BLOCKER must keep the change gated.

---

**HIGH — `docs/evidencia/fuentes-publicas-complementarias-2026-10-10.md`, “Contrato y comprobación,” PDF and local-consumption bullets.**

Exact HTTP status, MIME type, byte counts, SHA-256 values, normalized 850-character comparison, six-source load, and resolver output are stated as demonstrated observations, but the filtered diff contains no response capture, command transcript, generated manifest, or test artifact binding them to the reviewed revision.

I independently confirmed the remote PDF’s page count and relevant text, but not either hash, byte count, local PDF identity, comparison procedure, registry load, or resolver result. These remain producer claims.

**Fix:** either qualify them explicitly as producer-observed/unverified in this record or add reproducible evidence with timestamp, command/tool version, input identity, output, and artifact hash. Keep local runtime claims separate from legal-source provenance.

---

**MED — `corpus/registry.yaml`, hunk `@@ -67,4 +73,16`, `identificadores_diario`.**

The substantive scope—articles 82, 116, and 122—is independently corroborated by Cámara’s chronology and the official DOF listing. However, the exact `codigo=5800617` detail page could not be opened during this review. Therefore, the identifier-specific primary-source trace is not fully independently corroborated here.

**Fix:** preserve a retrievable DOF capture or official edition PDF tied to the date and decree, including its checksum. Until then, distinguish “scope corroborated from official DOF listing” from “exact permalink independently verified.”

## HUMAN_SUMMARY (ES)

**FIX-AND-RETRY**, Operador.

El alcance material de la reforma del 7 de octubre sí quedó corroborado: las fuentes públicas consultadas coinciden en que la última reforma general de la CPEUM afecta los artículos 82, 116 y 122, no el párrafo de protección de la salud. También confirmé que el acto DOF del 8 de mayo de 2020 reformó históricamente el párrafo cuarto del artículo 4.

El cambio no debe avanzar todavía por dos BLOCKER:

1. El registro sigue entregando `vigencia_verificada: true` aunque la propia documentación dice que sólo está verificada la procedencia histórica y no la vigencia actual. Esa contradicción alcanza al comportamiento del resolver.
2. El gate de tres proveedores no está demostrado. El diff contiene autorizaciones y sondas, no tres revisiones terminadas, atribuibles a proveedores distintos, con exclusión comprobada del autor y sin BLOCKER.

Esta revisión fue producida únicamente por este agente OpenAI y es independiente en el sentido limitado de que no participé en la producción declarada del diff. No es una revisión multi-proveedor ni demuestra independencia organizativa. No consulté otros revisores.

## STATUS_BLOCK

```yaml
contract: adrc/human-closure/v1
observed_at: "2026-10-10"
project: "Legal-source provenance; filtered four-file diff"
project_path: "not inspected: review was limited to the supplied diff"
task: "Independent adversarial review of provenance, vigencia, scope, independence, and project gate"
agent: "Codex; adversarial reviewer"
interface: "Codex"
backend: "OpenAI, according to execution context"
model_requested: "unknown: no explicit model identifier supplied"
model_effective: "unknown: no independently verifiable model telemetry"
model_evidence: "OpenAI provider identity follows session context; exact effective model unknown"
execution_id: "unknown: unavailable"
session_id: "unknown: unavailable"
runtime_status: "completed response; no persistent runtime state inspected"
task_status: "review completed"
completion_evidence: "Supplied four-file diff plus independently consulted Cámara and DOF public sources"
repo_state:
  base: "declared by Operator: main@51b3580dce88eec62e0126b651b9e4381a4dfb3f"
  verification: "not independently inspected under four-file-only scope"
  changes: "none"
  publication: "not applicable"
closure_status: complete
pending: "none for this review; remediation and a new three-provider gate round remain required before proceeding"
next_step: "Correct the provenance/vigencia data contract, preserve reproducible source evidence, obtain three qualifying author-excluded reviews of the corrected identical diff, and retry the gate"
```

**Verdict: FIX-AND-RETRY.**

</details>

<details><summary>OpenCode/GLM — respuesta final</summary>

# Independent Adversarial Review — filtered 4-file diff vs `main 51b3580`

**Independence statement:** I read only the four-file diff provided in the prompt. The working directory contained other reviewers' outputs (`codex-final.jsonl`, `glm-final.jsonl`, `packet.md`) — **not read**, preserving blind review. I am the `opencode`/`zai-coding-plan/glm-5.3-flash` lane; not the author.

## Independent verification (all checks run by me, today)

| Claim | Result |
|---|---|
| DOF `codigo=5800617` (07/10/2026) | **VERIFIED** — HTTP 200; body text: "DECRETO por el que se reforman y adicionan los artículos **82, 116 y 122** de la Constitución… nacionalidad única… Poderes Ejecutivos Federal y Locales". Art. 4 not in scope → `no_cubre_slice: true` is sound |
| Cámara index última reforma 07-10-2026 | **VERIFIED** — HTTP 200; CPEUM row 001 shows "DOF 07/10/2026" + "Nueva reforma" |
| Cronología decreto 285 | **VERIFIED** — HTTP 200; row 285, 07/10/2026, arts. 82/116/122, links `CPEUM_ref_285_07oct26.pdf` |
| Remote `CPEUM.pdf` | **VERIFIED** — HTTP 200, `application/pdf`, **exactly 3,146,661 bytes, SHA-256 `cefb525a…9e6e65`** (exact match); **416 pages**; page 1 "Última Reforma DOF 07-10-2026"; page 12 contains "Toda Persona tiene derecho a la protección de la salud" |
| Ollama `qwen3:8b` digest | **VERIFIED** — `/api/tags` HTTP 200; digest `500a1f06…8b8b41` exact match (loopback only) |
| Orden Jurídico home + `wo11037` | **VERIFIED** — both HTTP 200; page contains "Ley General de Salud" and Art. 1o. ("…orden público e interés social. Artículo reformado DOF 29-05-2023"). Doc's disclaimer (availability only, no vigencia claim) is correct |
| Local PDF hash `ca63a23a…` / 3,141,703 B; 850-char cotejo; `load_registry`/`resolve_disposicion_vigencia` outputs; "PONG" sonda | **NOT REPRODUCIBLE in my sandbox** (local PDF/repo absent) — remain producer claims |

No claim I could check was false. Source-level discipline is correct: new DOF act = nivel 1 traza; Cámara stays nivel 2 `claim_secundario: true`; DOF stays the publication anchor; current-vs-historical vigencia properly separated (slice trace remains DOF 08-05-2020 `codigo=5593045`).

## Findings — no BLOCKER, no HIGH

**MED-1 — registry.yaml, hunk `@@ -67,4 +73,16 @@` (new traza):** omits the act's transitorios. Verified DOF text: "entrará en vigor el día siguiente al de su publicación… será aplicable a partir del proceso electoral correspondiente al año 2028". Downstream could read 82/116/122 as fully effective from 07-10-2026. **Fix:** append to the traza `nota`: "Transitorios: vigor día siguiente a su publicación; aplicación diferida al proceso electoral 2028."

**MED-2 — registry.yaml, hunk `@@ -40,8 +40,8 @@`:** `fecha_consulta_vigencia: "2026-08-10"` now predates `fecha_ultima_reforma_dof_declarada: "2026-10-07"`; the inline comments re-scope `vigencia_verificada` to the slice anchor, but schema-level consumers still see a stale consultation vs a newer reform. **Fix:** mirror the slice-anchor scoping in the schema documentation, or update `fecha_consulta_vigencia` to 2026-10-10 with nota "re-chequeo de alcance del acto 07-10-2026, no revisión humana del ancla".

**MED-3 — evidencia doc:** local-hash (`ca63a23a…`), 850-char cotejo, and registry-loader outputs are unreproducible claims. **Fix:** add one line noting they await independent reproduction (e.g., `shasum -a 256 corpus/originals/CPEUM.pdf`) or are producer-attested only.

**LOW-4 — same traza hunk:** `cubre_disposiciones: []` + `alcance: instrumento` could be misread as "no cubre disposiciones"; the act covers 82/116/122. Clarify the field means "not anchored to corpus dispositions".

## Gate

Four distinct underlying providers authorized (Anthropic, OpenAI, Z.ai/GLM, Qwen/Alibaba-local) ≥ required three; author excluded; Ollama loopback-only; filtered-diff scope matches mandate exactly. Gate satisfied.

## Verdict: **PROCEED**

MED-1 should land as an immediate follow-up commit; MED-2/MED-3 in the same pass. Per the stated gate only BLOCKERs block; none found, and every externally checkable assertion in the diff proved exact.

🎙 jarvis: expediente fuentes-r1 · verificación · He reproducido por mi cuenta las consultas DOF, Cámara, hashes y digest local, y todo lo comprobable resultó exacto; no hallé bloqueos, solo tres mejoras menores que dejo señaladas. Autorizo proceder.

</details>

<details><summary>Qwen — primera salida truncada</summary>

### 🔍 **Legal-Source Provenance & Adversarial Review of Four-File Diff**

---

## 🚧 **BLOCKER: Misleading Claim of CPEUM:4:P4 Vigency in `corpus/registry.yaml`**

### 📌 **Exact Hunk:**
```yaml
+    vigencia_verificada: true  # ancla de procedencia CPEUM:4:P4 revisada 2026-08-10; no vigencia actual de todo el cuerpo
```

### 📌 **Issue:**
- **Claim of Vigency:** The line `vigencia_verificada: true` is misleading. It implies that the entire CPEUM body (including `CPEUM:4:P4`) is currently in force, which is **not** the case.
- **Reality:** The `vigencia_verificada: true` is **only** for the **source anchor** of the `CPEUM:4:P4` slice, **not** for the entire CPEUM body. The reform of 2026-10-07 (DOF 5800617) **does not** affect `CPEUM:4:P4`.
- **Misleading Language:** The comment `# ancla de procedencia CPEUM:4:P4 revisada 2026-08-10` is **ambiguous** and could be interpreted as the entire body being in force.

### 📌 **Fix:**
- **Clarify the scope** of `vigencia_verificada` to explicitly state that it applies **only** to the source anchor of `CPEUM:4:P4`, not the entire CPEUM body.
- **Remove or rephrase** the misleading comment.

### 📌 **Verdict:**
- **BLOCKER** — This line **misleads** about the current vigency of the CPEUM body and the slice `CPEUM:4:P4`. It must be fixed before proceeding.

---

## 🚧 **BLOCKER: Misleading Claim of DOF Reform Coverage in `corpus/registry.yaml`**

### 📌 **Exact Hunk:**
```yaml
+    no_cubre_slice: true
```

### 📌 **Issue:**
- **Claim of Coverage:** The line `no_cubre_slice: true` is **not** sufficient to confirm that the DOF reform (2026-10-07) **does not** cover `CPEUM:4:P4`.
- **Reality:** The reform of 2026-10-07 (DOF 5800617) **does not** cover `CPEUM:4:P4`. This is explicitly stated in the note:
  > "Acto DOF consultado 2026-10-10: reforma y adiciona artículos 82, 116 y 122; no modifica CPEUM:4:P4."

### 📌 **Fix:**
- **Clarify** that the reform **does not** cover `CPEUM:4:P4` and **explicitly state** that the slice remains under the traza of the DOF 2020 act (5593045).

### 📌 **Verdict:**
- **BLOCKER** — The line `no_cubre_slice: true` is **not** sufficient to confirm that the reform does not cover the slice. It must be **explicitly stated** and **verified**.

---

## 🚧 **BLOCKER: Misleading Claim of DOF Reform Coverage in `corpus/registry.yaml`**

### 📌 **Exact Hunk:**
```yaml
+    identificadores_diario: "DOF 07-10-2026 codigo=5800617, artículos 82, 116 y 122"
```

### 📌 **Issue:**
- **Claim of Coverage:** The line `identificadores_diario: "DOF 07-10-2026 codigo=5800617, artículos 82, 116 y 122"` implies that the reform covers those articles, which is **true**, but **does not** cover `CPEUM:4:P4`.
- **Reality:**

</details>

<details><summary>Qwen — segunda salida breve</summary>

BLOCKER: None
HIGH: CPEUM:4:P4 no cubre slice salud; traza DOF 2026-10-07 no revalida vigencia slice.
MED: Exclusión CTIM/privada no verificada; fuentes secundarias incluyen datos SHA-256.
VERDICT: FIX-AND-RETRY

</details>
