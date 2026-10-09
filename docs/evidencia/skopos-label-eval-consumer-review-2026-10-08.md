# Revisión del consumidor: candidatos de rótulo IMSS p20

**Estado:** revisión acotada de una proyección experimental; no acepta
fidelidad general, servicio v0.2, retención ni admisión al corpus.
**Observación:** 2026-10-08, hora de México (2026-10-09 UTC).

## Fuentes y comprobación

- Original PDF IMSS `2000-002-001`, SHA-256
  `719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`;
  derivado visual v0.1 SHA de manifiesto
  `8a1880b84b0e52f934f09759f3a83efb5a3a752afda914d6c5cce9c7803aaaee`.
- Productor Skopos, `main` commit
  `f00684430103c618efe0fd57971219e202b7751f`: expediente
  `docs/evidencia/pdf-imss-label-candidates-evaluation-2026-10-08.md`,
  referencia `docs/evidencia/pdf-imss-page20-visual-reference-2026-10-08.json`
  y CLI `scripts/evaluate_pdf_labels.py`. El commit y `origin/main`
  coincidieron al consultarlos; el árbol Skopos estaba limpio.
- Ejecuté el CLI documentado contra el manifiesto y render locales. La
  referencia canónica devolvió SHA-256
  `c04f78e2ee4d800ee9f077c02728d0e285474a561a8d7b71193c0c1b10ab9b6a`;
  la proyección calculada, SHA-256
  `ce876b0e4e2e3f9283fdfa7e135b51443d09807d5deb14f09761c67376be85ef`.
  Abrí el PNG físico p20 fijado por SHA
  `5302c61d5db9f8843d41dd2f67a18e2dc17960e9680eb0d5bec9b3483a4d34b8`
  y cotejé sus diez rótulos con la referencia. Esta revisión visual no fue
  ciega ni independiente de la selección de cajas del productor.

## Resultado reproducido para p20

| Medida | Texto nativo | OCR selectivo |
| --- | ---: | ---: |
| Rótulo exacto tras normalización declarada | 7/10 (70 %) | 1/10 (10 %) |
| CER, tasa de error | 4/437 (0,92 %) | 269/437 (61,56 %) |
| WER, tasa de error | 8/64 (12,50 %) | 44/64 (68,75 %) |

El cotejo manual de candidatos confirmó tres fallos nativos por espacios
internos de palabra (`M ÉDICAS`, `FORM ACIÓN`/`HUM ANOS`, `PERM ANENTE`).
El único rótulo OCR completo es el de la Unidad de Educación e
Investigación; `n3` está vacío y `n4` dice `COBRARON BE`. El método conserva
las dos lecturas con sus localizadores, sin elegir una como verdad.

El evaluador informa 10/10 cajas y 9/9 conexiones topológicas en p20. **No
se aceptan esos porcentajes como detección independiente**: las cajas de la
referencia se aproximaron desde el grafo v0.1. No hay flechas observadas
para adjudicar dirección. La referencia fue anotada por el productor; este
cotejo posterior es del consumidor, sin segunda anotación ciega. Ni el
resultado de una página ni el CER normalizado describen las 188 páginas.

## Decisión y siguiente gate

Se acepta sólo que el CLI reproduce estas medidas acotadas sobre los bytes
locales identificados y que los diez textos de referencia se leen en el
render inspeccionado. No se acepta v0.2 como servicio: la proyección vive en
memoria y carece de contrato de socket y política de retención propios.
Para una cifra de fidelidad de organigramas 18–22, congelar anotaciones
visuales de todas esas páginas sin usar predicciones para dibujar cajas,
revisarlas por separado, registrar exclusiones y ejecutar los mismos
numeradores y denominadores por página. Contrato y retención requieren
decisión expresa antes de servir o conservar el nuevo derivado.
