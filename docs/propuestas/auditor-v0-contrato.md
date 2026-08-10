# Contrato — Auditor de documento v0 (R1-E3-01)

**Estado:** vigente diseño · **Fecha:** 2026-08-10 · **Implementación:** `scripts/audit_document.py`  
**No LLM.** Citas **pre-etiquetadas**. No es auditoría jurídica certificada.

## Entrada

Archivo JSON:

```json
{
  "documento_id": "piloto-salud-v0",
  "claims": [
    {"disposicion_id": "CPEUM:4:P4", "cita_texto": "…≥40 chars…"}
  ]
}
```

O lista raíz `[{disposicion_id, cita_texto}, …]`.

## Salida

```json
{
  "auditor_version": "v0",
  "gate_version": "v1",
  "corpus_vigencia_banner": "CORPUS_VIGENCIA_NO_VERIFICADA",
  "documento_id": "…",
  "claims": [ /* verify_claim por cada una */ ],
  "summary": {
    "n": 1,
    "alto": 0,
    "medio": 0,
    "bajo": 0,
    "peor": "bajo"
  }
}
```

**Banner F6:** si ninguna fuente del registry tiene `vigencia_verificada: true`
(clave YAML), `corpus_vigencia_banner` = `CORPUS_VIGENCIA_NO_VERIFICADA`.  
Si hubiera alguna `true` (futuro H1): `CORPUS_VIGENCIA_PARCIAL_O_OK` (sin afirmar
aplicabilidad casuística).

## Exit codes

- `0` — peor nivel `alto` (inalcanzable en gate v1 hoy)
- `2` — peor `medio`
- `1` — peor `bajo` o entrada inválida

## Fuera de alcance v0

Extracción LLM, umbral FP (E0-03 diferido), red, multi-provider.
