# Diseño — Gate de confianza multi-eje (v1 → v1.1)

**Estado:** propuesta de diseño (no implementado en código salvo v1 actual).  
**Fecha:** 2026-08-10 · **Plan:** R1-E1-05 / metodología `docs/fuentes-legal-mx.md`  
**Implementación código:** ticket futuro; **default R1:** no habilitar `alto` hasta
H1 con vigencia real + aceptación del rol jurídico.

## Problema

El gate v1 (`verify_citations.py`) mezcla en la práctica:

- existencia de disposición,
- match de subcadena,
- resolución de hash de fuente,

y deja **vigencia** como N/A (`alto` inalcanzable). Eso es correcto como freno, pero
no expone **por qué** un claim es medio/bajo ni permite multi-fuente.

## Propuesta

### Ejes (salida JSON estable)

```json
{
  "gate_version": "v1.1-design",
  "ejes": {
    "existencia": {"ok": true, "detail": "CPEUM:4:P4"},
    "procedencia": {"nivel_archivo": 2, "tiene_traza_nivel1": false},
    "match_textual": {"ok": true, "match_len": 120},
    "vigencia": {"verificada": false, "marcador": "VIGENCIA-NO-VERIFICADA"},
    "coherencia": {"estado": "no_evaluado"}
  },
  "nivel_agregado": "medio",
  "reasons": ["vigencia_no_verificada", "archivo_nivel_2"]
}
```

### Agregación (determinista, sin LLM) — post F4 adversarial

1. Si `existencia` o `match_textual` fallan → **bajo**.
2. Si hash de fuente irresoluble / inválido → **bajo** (como v1).
3. Si A+C OK y `vigencia.verificada` false → techo **medio**.
4. Si A+C OK y el **archivo de trabajo** es nivel ≥2 **y** no hay apoyo primario
   del texto de la **disposición** citada → techo **medio** + reason
   `texto_trabajo_no_primario` (aunque el instrumento tenga traza DOF de otro
   alcance).
5. Si `coherencia` = `discrepancia` → techo **medio** + `discrepancia_fuentes`.
6. **alto** (solo código v1.1 + H1): A+C OK; `vigencia.verificada` true con
   traza cuyo `cubre_disposiciones` incluye el id citado; E ≠ discrepancia;
   y no aplica (4).

Ejes JSON ampliados (diseño):

```json
"procedencia": {
  "nivel_archivo": 2,
  "tiene_traza_nivel1": true,
  "traza_cubre_disposicion": false,
  "reason": "texto_trabajo_no_primario"
}
```

### Compatibilidad

- CLI actual: exit codes `0=alto, 2=medio, 1=bajo`.
- Tests golden: no romper; añadir casos v1.1 después.
- `alto` **prohibido** en producción hasta F1–F4 en datos + ticket código + H1.

## Fuera de alcance de este diseño

- Scoring semántico del LLM.
- Bitemporalidad plena.
- Auto-upgrade de vigencia por scraper.

## Criterio de aceptación del diseño (doc)

- [x] Ejes A–E definidos en `fuentes-legal-mx.md` §6
- [ ] Implementación: ticket futuro `feat(corpus): gate v1.1 multi-eje`
- [ ] Adv multi si se habilita `alto` en código
