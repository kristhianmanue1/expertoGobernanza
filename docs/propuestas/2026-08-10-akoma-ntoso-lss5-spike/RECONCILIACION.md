# Reconciliación final — spike Akoma Ntoso LSS:5

**Fecha:** 2026-08-10 · **Estado técnico:** `proceed` unánime  
**Autor excluido:** OpenAI/Codex · **Quórum:** Anthropic + Moonshot + Zhipu/GLM

| Proveedor | Pass 1 | Retry final |
|---|---|---|
| Anthropic | `fix-and-retry` (HIGH) | `proceed` (LOW) |
| Moonshot | `fix-and-retry` (MED) | `proceed` |
| Zhipu/GLM vía OpenCode | `proceed` (LOW) | `proceed` (LOW) |

## Evidencia final

- XML: `afad20a0eaff575a6704f2196cdd34a1d3fe1a7b11a71e3058bb551b10a23826`;
- XSD OASIS: `6f61fe84cbb6f8cb0e8418cd67b74a63da9990e6573b5a3491f623184f45c4fd`;
- `xml.xsd`: `61960fb3131e38022caad5360e2f33a3382578ab3c80cd58bd74320ede61b20c`;
- 7/7 tests; XSD válido; inversa exacta; 248 líneas; una disposición.

## Decisión

Se conserva el resultado como **adaptador experimental de borde**. No se adopta
AKN como modelo interno, dependencia runtime ni prueba de vigencia. El XML sólo
puede viajar con sidecar de procedencia/EvidenceEdge para usos probatorios.

## Reconciliación de hallazgos

1. Work, Expression y reforma de porción quedaron separados.
2. Sólo la Expression editorial se marca no autoritativa.
3. `includedIn=#lss` resuelve `original@eId=lss`; `original@href` apunta al Work.
4. Registro y JSON deben coincidir en la fecha del cuerpo o el generador falla.
5. El XSD oficial y su dependencia se vendorizan y pinnean por hash.
6. La matriz declara pérdidas de F5, hashes fuente, lineage y relaciones.

No queda BLOCKER técnico. Git continúa `PARCIAL (espera-admin)` y ningún voto
adversarial equivale a promulgación, publicación oficial o aceptación jurídica.
