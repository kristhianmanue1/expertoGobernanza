# Ronda adversarial — arquitectura y posicionamiento — 2026-08-10

> **Estado general:** BLOQ para adopción — quórum válido, decisión `fix-and-retry`.
> **Autor excluido:** OpenAI/Codex. **Reconciliador:** OpenAI/Codex, cuarto
> proveedor; agrega hallazgos y justifica cualquier ajuste.
> **Objeto:** `INPUT.md`. **Impacto:** alto por dirección arquitectónica.

## Proveniencia y egress §7.4

| Destino | Modelo | Bundle SHA-256 | Resultado |
|---|---|---|---|
| Anthropic | `claude-sonnet-5` | `2c27b6036b84faf5074a9f5049c042e684853f59e275fdd8fbd2a399b15ce09f` | revisión válida |
| Moonshot | `k3-256k` | `54494ec2acc6c03f23f8e3e0b93fcb8c56f8eb2e1d1de756125bc9e78fd55de2` | revisión válida |
| ZhipuAI/OpenCode | `zai-coding-plan/glm-5.2` | `ee7ccc1ec575b96a4d57796782093dfd3c0e49c0ac7254b011e3016497273584` | revisión válida |
| Google | `gemini-3.1-pro-high` | `4e4f85d3298a51c47e64c94ce24930e83a96ddcd9daa75b37003d49d9786034c` | inválida: timeout/contaminación |
| Google recuperación | `gemini-3.1-pro-high` | `8f744b732e67b5dd7eaba462ae9bcb41a4fa915878ec81d13374133f4426573c` | descartado por el humano |

Todos los bundles fueron `publico`, `denied: []`, antes del envío. No se envió
el adjunto original, manuales IMSS ni contenido interno/confidencial. Los hashes
y destinos están en `logs/review-routing.jsonl` (log local ignorado por Git).

## Quórum

- Anthropic + Moonshot + Zhipu: tres familias/modelos subyacentes válidos.
- Google: no produjo una revisión pertinente; su salida ajena al bundle se
  conserva verbatim en `reviews/google-invalid-context-contamination.md`.
- El humano indicó “Google queda descartado por ahora”.
- Resultado estructural: **3 proveedores válidos** para alto impacto; autor
  OpenAI excluido. Quórum cumplido, con brecha residual de entrenamiento §6.

## Decisiones individuales

| Revisor | Decisión | BLOCKER | HIGH |
|---|---|---:|---:|
| Anthropic | `fix-and-retry` | 0 | 2 |
| Moonshot | `fix-and-retry` | 0 | 2 |
| ZhipuAI | `proceed` | 0 | 1 |
| Google | inválida | NA | NA |

## Decisión agregada

**`fix-and-retry` con quórum válido**.

No hay BLOCKER. La mayoría de revisores válidos (2/3) rechazó `proceed`; los tres
coincidieron en el hazard instrumento→disposición y en la falta de alcance del
edge. Antes de una nueva ronda deben cerrarse los fixes de consenso en
`RECONCILIACION.md`.
