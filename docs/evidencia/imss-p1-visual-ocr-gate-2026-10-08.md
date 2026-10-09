# Página 1 IMSS: lectura visual candidata frente a OCR de Skopos

**Estado:** cotejo técnico bajo demanda; referencia visual de un solo agente,
sin segunda revisión. La cita literal permanece bloqueada. **Última
comprobación:** 2026-10-09T01:30Z (2026-10-08 en México).

## Contrato y procedencia

- Original local: `docs/fuentes/imss/2000-002-001.pdf`, SHA-256
  `719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`.
  La ficha `docs/fuentes/imss/2000-002-001-PROCEDENCIA.md` conserva el vínculo
  puntual con el sitio oficial. El hash identifica esta copia, no su vigencia.
- [Referencia visual candidata](imss-p1-visual-candidate-2026-10-08.json),
  SHA-256 `53918240b3ac3c494cc9c462c7c2e95971e48d0ecdd4c493f6dcfd1afd7a1b80`.
  Codex la transcribió desde un render propio a 300 dpi antes de reabrir el
  manifiesto OCR en esta ronda. Ya conocía resultados previos de Skopos:
  **no fue una anotación ciega**. Los `item_id` se vincularon después. Su
  estado es `codex_visual_candidate_unconfirmed`.
- Derivado OCR Skopos v0.1: manifiesto SHA-256
  `3ca9d7a5be5e451f63608015585a4eee92d2109046d390de99d793ac2f83651d`;
  PNG p1 SHA-256
  `015546b16f8d9edfb04679687e12683c9b8924ef59f38b588219dc8d34514e40`.
  El manifiesto tiene 20 líneas OCR y ninguna línea de texto nativo en p1.

## Prueba bilateral

El [cliente](../../scripts/skopos_p1_visual_gate.py) inició una sesión contra
el host documental v0.1 de Skopos y recuperó manifiesto, PNG y una línea
individual mediante `fetch_evidence`. Cotejó bytes y SHA de original,
referencia, manifiesto y PNG, las identidades de fuente y política, y los
`item_id` de cinco regiones. El resultado fue `p1_layers_recovered` y
`literal_quote_status=blocked_pending_independent_review`.

| Región | Palabras candidatas | Ediciones de palabra frente al OCR | Estado |
| --- | ---: | ---: | --- |
| Título | 9 | 0 | Coincidencia en el cotejo acotado |
| Nombre impreso | 5 | 0 | Coincidencia; no autentica la firma |
| Cargo | 7 | 1 | `Dirección` frente a `Dirécción` |
| Campos impresos del sello | 16 | 0 | Coincidencia; no prueba validez del sello |
| Párrafo inferior | 63 | 9 | OCR deformado; puntuación candidata sin adjudicar |

Las ediciones usan NFKC, minúsculas y palabras Unicode; omiten diferencias de
puntuación. **No son una tasa de error certificada:** el texto visual todavía
no tiene segunda revisión. La lectura propia de OCR también usó macOS Vision,
el mismo motor que Skopos; su acuerdo no es validación independiente.

Las pruebas locales alteraron estados de la referencia, un `item_id` y bytes
PNG. La promoción unilateral a `independently_confirmed`/
`literal_quote_allowed=true` fue rechazada, igual que el localizador o PNG
alterado. Hubo control positivo con las capas completas.
El host y Mongo terminaron; después no existía el socket y el puerto 37034
estaba cerrado. Los JSON/sobres de solicitud siguen bajo la retención del
piloto; las respuestas y los bytes de entrega temporal no se guardaron por
este cliente.

## Frontera de revisión

Skopos conserva OCR bruto y original; expertoGobernanza conserva **aparte**
esta anotación candidata. No se reescribió el OCR ni se añadió una corrección
al almacén de Skopos. Esta separación mantiene identificable quién produjo
cada capa. La recomendación previa de guardar ambas capas en Skopos se ajustó
por esta razón: una eventual ingestión de anotaciones del consumidor necesita
un contrato nuevo de autoría, revisión, retención y recuperación, no una
edición del derivado v0.1.

Para autorizar una cita literal de p1 falta una revisión visual independiente
del texto y puntuación, con dictamen y vínculo a las mismas regiones. Después
haría falta un contrato versionado de promoción y una prueba bilateral nueva;
el estado actual no se promueve por cambiar una bandera del JSON.
