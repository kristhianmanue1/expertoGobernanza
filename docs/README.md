# Docs — mapa de lectura (R1)

**Vigente (empieza aquí):**

| Doc | Para qué |
|------|----------|
| [`../AGENTS.md`](../AGENTS.md) | Always-on agentes |
| [`plan-r1-90d.md`](plan-r1-90d.md) | Plan y tickets R1 (cola vigente) |
| [`plan-r2.md`](plan-r2.md) | Borrador R2 afinado el 2026-10-05. Sin `proceed`: no es la cola |
| [`fuentes-legal-mx.md`](fuentes-legal-mx.md) | Procedencia / vigencia / checklist E1 |
| [`autorizacion-fuentes-r1.md`](autorizacion-fuentes-r1.md) | Canales DOF/OJ + multi-provider |
| [`roles-r1.md`](roles-r1.md) | Jurídico / custodio / PO |
| [`politica-agentes.md`](politica-agentes.md) | Política v1.1 |
| [`ops-github.md`](ops-github.md) | CI billing + DoD local |
| [`plantillas-agente.md`](plantillas-agente.md) | Plantillas plan/contrato/reporte |
| [`gobernanza/expediente-probatorio-rondas-2026-08-10.md`](gobernanza/expediente-probatorio-rondas-2026-08-10.md) | Ejemplo probatorio de gobernanza adversarial aplicada |
| [`relatorias/2026-08-10-arquitectura-evidence-edge-gobernanza.md`](relatorias/2026-08-10-arquitectura-evidence-edge-gobernanza.md) | Relatoría de ejecución arquitectura→EvidenceEdge |
| [`propuestas/2026-08-10-benchmark-imss-evidenceedge/RECONCILIACION.md`](propuestas/2026-08-10-benchmark-imss-evidenceedge/RECONCILIACION.md) | Benchmark IMSS falsable: cierre adversarial |
| [`propuestas/2026-08-10-benchmark-imss-evidenceedge/RESULTADOS-R3.md`](propuestas/2026-08-10-benchmark-imss-evidenceedge/RESULTADOS-R3.md) | R3: F5 LFEP, LOAPF por párrafo y gate permanente |
| [`propuestas/2026-08-10-benchmark-imss-evidenceedge/RECONCILIACION-R3.md`](propuestas/2026-08-10-benchmark-imss-evidenceedge/RECONCILIACION-R3.md) | R3: cierre adversarial 3/3 y reservas administrativas |
| [`propuestas/2026-08-10-akoma-ntoso-lss5-spike/RECONCILIACION.md`](propuestas/2026-08-10-akoma-ntoso-lss5-spike/RECONCILIACION.md) | Spike AKN LSS:5: decisión y límites |
| [`relatorias/2026-08-10-benchmark-imss-akoma-ntoso.md`](relatorias/2026-08-10-benchmark-imss-akoma-ntoso.md) | Relatoría benchmark→spike AKN |
| [`gobernanza/paquete-admin-2026-08-10-imss-f5-gate.md`](gobernanza/paquete-admin-2026-08-10-imss-f5-gate.md) | Paquete de adopción administrativa de los pasos 1–4 |
| [`relatorias/2026-08-10-cierre-f5-lfep-loapf-gate.md`](relatorias/2026-08-10-cierre-f5-lfep-loapf-gate.md) | Relatoría de ejecución R3 |

**Archivo / histórico:**

| Doc | Nota |
|------|------|
| [`plan-r0.md`](plan-r0.md) | **Cerrado** — arranque; no usar como cola actual |
| [`propuestas/`](propuestas/) | Evidencia de rondas, diseños, no siempre vigente |
| [`adr/`](adr/) | ADR-0001/0002 (estado en cada archivo) |
| [`fuentes/`](fuentes/) | Extractos de trabajo del slice (no primarios DOF) |

**Código corpus:** `corpus/registry.yaml`, `corpus/lookup.py`, `corpus/verify_citations.py`,
`corpus/evidence_edge.py` (contrato EvidenceEdge v0, no-herencia),
`scripts/audit_document.py` (auditor v0), `scripts/eval_extraction.py` (fake offline).  
**Eval:** `docs/propuestas/auditor-v0-matriz-fpfn.md`, `docs/propuestas/recall-extraccion-v12.md`.  
**IMSS:** `docs/propuestas/imss-alcance-publico.md` (público vs interno; no manuales).  
**F5 estructura:** `docs/propuestas/f5-checklist-eje-imss-publico.md` (ligas + texto a contrastar).
