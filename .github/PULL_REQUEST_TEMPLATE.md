<!-- Plantilla de PR — ExpertoGobernanza (politica-agentes.md §5/§6/§7) -->

## Qué hace este cambio
<!-- 1-3 líneas, sin marketing. -->

## Contrato (DoD) y verificación
- [ ] `python -m unittest discover -s tests` verde (**local** si Actions está suspendido)
- [ ] `python scripts/check_sizes.py` exit 0 (**local** si Actions está suspendido)
- [ ] Cada afirmación normativa cita fuente verificable (§7); o marca `[VIGENCIA-NO-VERIFICADA]`
- [ ] Sin secretos / datos personales en claro (§7.1)
- [ ] Si el agente envió contenido a proveedores externos: router §7.4 clasificó + log de hash
- [ ] CI remoto: `verde` / `SUSPENDIDO (billing)` — si suspendido, no fingir verde; ver `docs/ops-github.md`

## Impacto y adversarial (§6)
- [ ] Clasificación: `menor` (quorum-lite) / `alto` (≥3 proveedores distintos)
- Si `alto`: enlace a la ronda adversarial (reviews verbatim) y decisión `proceed`/`fix-and-retry`/`escalate`.
  Alto impacto = cambia política / ADR estratégico / compuertas de fidelidad / corpus / despliegue.

## Fidelidad documental (riesgo #1, §7)
- [ ] Toda cita↔fuente verificada; o declarado `[VERIFICAR-FUENTE]` con justificación.

## Notas para el revisor
<!-- Decisiones de subagentes, supuestos, deuda abierta. -->
