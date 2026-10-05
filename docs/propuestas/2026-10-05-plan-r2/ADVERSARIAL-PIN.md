# Adversarial — pin Skevi — 2026-10-05

**Artefacto:** `.skevi/corpus-pin.json` y las frases de Skevi en `docs/plan-r2.md`.
**Quórum:** lite. Un revisor en contexto fresco, proveedor Grok, autor excluido. Bajo impacto: no cambia compuerta legal ni política. No es `proceed` de H1 ni de H2.

## Hallazgos

- [MED] T2 decía «commit del pin» y el pin tiene dos revisiones. La guía `06` no está en `944e72e`. Fix aplicado: citar `https://github.com/kristhianmanue1/skevi.git@d7a80b26962cd66a806943ff46f779de14c16708`.
- [MED] `not_installed` se leía como rutas de este repo. Fix aplicado: la lista se llama `canon_no_copiado` y el pin dice que los homónimos locales no se borran.
- [LOW] `944e72e` es del 2026-08-12 (`-0600`); 2026-08-13 es la fecha de vendor. Fix aplicado en el plan.

No hubo BLOCKER ni HIGH. El revisor comprobó que `944e72e` es ancestro de `d7a80b2`, que el sha256 del estándar en ese origen coincide con el pin, y que el schema no es `skevi/corpus-install/v1`.

## Decisión

- [x] proceed del borrador de este ticket, después de aplicar los MED y el LOW.
- [ ] proceed de merge de H1 o H2.
