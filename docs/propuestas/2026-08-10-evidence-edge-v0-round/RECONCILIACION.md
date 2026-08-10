# Reconciliación — EvidenceEdge v0 — 2026-08-10

## Decisión

**`proceed` unánime** después de cuatro pases. El contrato queda propuesto para
adopción interna R1; no habilita serving externo ni adopción de Akoma Ntoso.

## Hallazgos cerrados

| ID | Severidad máxima | Riesgo | Resolución |
|---|---|---|---|
| H1 | HIGH | evidencia nivel 3/4 podía sostener `verified` | nivel 1/2 obligatorio |
| H2 | HIGH | `not_applicable` eludía cobertura de objeto | `covers_object is True` |
| H3 | HIGH | sujeto instrumento heredaba traza de artículo | subject disposición exacta |
| H4 | HIGH | interpretación recorrible igual que texto | allowlist no interpretativa |
| H5 | HIGH | fechas futuras/invertidas | `trace <= review <= hoy` |
| H6 | HIGH | F5 por disposición sin fecha/locator/revisión | conjunción completa + tests |
| M1 | MED | alcance instrumento resolvía disposición | sólo artículo/párrafo |
| M2 | MED | coverage string hacía match por substring | lista exacta obligatoria |
| M3 | MED | duplicados dependían del orden | duplicado falla cerrado |
| M4 | MED | URL vacía satisfacía traza | HTTPS + hostname |
| M5 | MED | IDs con `|` colisionaban | léxico cerrado |
| M6 | MED | traza principal sin locator | fecha + URL/identificador |

## Fronteras aceptadas

- `validate_evidence_edge` valida una atestación estructural; no abre el archivo
  citado ni recompone el hash. Esa verificación pertenece al gate de citas.
- `inheritance: prohibited` y `gate_version` se conservan como invariantes y
  procedencia explícitos, no como subsistema de versionado.
- Las clases interpretativas se pueden registrar, pero no recorrer en v0.
- Una reforma posterior a `reviewed_at` obliga revalidación; v0 no implementa
  vigilancia automática ni bitemporalidad.

## Resultado verificable

- `LFEP:1=true`, `LFEP:5=false`, `LSS:5=true`, `LSS:1=false` permanecen.
- Entrada inválida, tabla duplicada o traza incompleta devuelve `false`.
- Sólo afirmaciones verificadas, no interpretativas y con cobertura/traza exacta
  pasan `is_traversable`.
