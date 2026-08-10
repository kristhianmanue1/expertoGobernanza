# Matriz FP/FN — Auditor v0 (piloto salud)

**Ticket:** R1-E3-04 · **Fecha pasada:** 2026-08-10  
**Fixture:** `tests/fixtures/piloto-salud-citas.json`  
**Comando:** `python scripts/audit_document.py tests/fixtures/piloto-salud-citas.json`  
**Banner corpus:** `CORPUS_VIGENCIA_PARCIAL_O_OK` (H1 slice 2026-08-10)  
**Umbral FP (E0-03):** aún **diferido** — esta matriz es **exploratoria**, no promesa exterior.

## Pregunta de evaluación (binaria)

> ¿La `cita_texto` está **respaldada** como subcadena en el texto de la
> `disposicion_id` del corpus? (misma noción que el gate v1)

| Etiqueta | Significado |
|----------|-------------|
| **TP** | Humano: sí respaldada; sistema: match (nivel medio/alto) |
| **TN** | Humano: no respaldada; sistema: no match (nivel bajo) |
| **FP** | Humano: no respaldada; sistema: dice match/medio |
| **FN** | Humano: sí respaldada; sistema: no match/bajo |

Nivel `medio` del gate v1 (tope sin bitemporalidad de cita en código) se trata
como **“respaldada en corpus, no apta sola para decisión jurídica final”** — no
como error si el match es correcto.

## Pasada 1 (sistema + primera etiqueta humana de fixture)

Oráculo humano de la pasada 1: diseño conocido del fixture + contraste con
lookup (PO interino / orquestación 2026-08-10). **Revisable** por el humano.

| # | disposicion_id | Cita (resumen) | Sistema (nivel) | match | Humano: ¿respaldada? | Clase |
|---|----------------|----------------|-----------------|-------|----------------------|-------|
| 1 | CPEUM:4:P4 | Protección de la salud + bases/modalidades… | medio | sí | **sí** | **TP** |
| 2 | LGS:1 | Reglamenta derecho Art. 4o CPEUM… | medio | sí | **sí** | **TP** |
| 3 | LGS:1 | Texto inventado que no aparece… | bajo | no | **no** | **TN** |

### Conteos pasada 1

| | n |
|--|--:|
| TP | 2 |
| TN | 1 |
| FP | 0 |
| FN | 0 |
| Precision (TP/(TP+FP)) | 1.0 (n pequeño) |
| Recall (TP/(TP+FN)) | 1.0 (n pequeño) |

**Interpretación:** con N=3 el verificador determinista se comporta como se
diseñó. **No** extrapolar a documentos reales ni a extracción LLM (E4).

## Plantilla (copiar filas)

| # | disposicion_id | cita_ref | sistema_nivel | match | humano_respaldada | clase | notas |
|---|----------------|----------|---------------|-------|-------------------|-------|-------|
| | | | | | sí/no | TP/TN/FP/FN | |

## Próximas pasadas sugeridas

1. Documento sintético más largo (5–10 citas, 1–2 trampas).  
2. Cuando E4 exista: matriz **sobre citas extraídas por LLM** (ahí nacerán FP reales).  
3. E0-03: fijar umbral solo con N≥30 o criterio PO.

## No hacer

- Publicar “accuracy 100 %” al exterior con N=3.  
- Confundir TP de match textual con “norma aplicable al caso”.
