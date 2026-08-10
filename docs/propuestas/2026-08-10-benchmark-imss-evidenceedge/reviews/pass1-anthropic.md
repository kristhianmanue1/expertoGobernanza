# Pass 1 — Anthropic / Claude

**Proveedor/modelo:** Anthropic / Claude Sonnet · **Lente:** corrección y fidelidad  
**Decisión:** `fix-and-retry`

## Hallazgos

- **BLOCKER B1:** `is_traversable` acepta una cita fabricada porque el contrato
  estructural no abre `source_ref`; el arnés sí verifica la cita, pero el
  prerregistro atribuía el resultado al gate aislado. Fix: evaluar explícitamente
  el compuesto `fidelidad + EvidenceEdge` o llevar la fidelidad al gate.
- **BLOCKER B2:** un `source_ref` inexistente también puede pasar el gate
  estructural. Fix: resolución de fuente como precondición del benchmark y caso
  negativo preregistrado.
- **HIGH H1:** una candidata por pregunta y bloqueos triviales no ejercitan
  citas falsas, hashes divergentes o sujetos desalineados. Fix: añadir trampas
  dentro de las cinco preguntas.
- **HIGH H2:** el hash se compara declarado-contra-declarado, no contra el PDF.
  Fix: recomputar el original local durante la corrida probatoria.
- **HIGH H3:** Q5 usa `verified` para una relación interpretativa. Fix: no
  presentar la inferencia como verificada.
- **MED:** subcadena puede recortar contexto; reloj no inyectable; motivo F5 no
  es consultado por el código; falsos positivos contados por outcome, no arista.
- **LOW:** mutabilidad pre-commit; falta resolver symlinks; `éxito técnico` era
  prematuro antes del gate.

La clasificación de alto impacto se confirmó. No se autorizó el spike AKN.
