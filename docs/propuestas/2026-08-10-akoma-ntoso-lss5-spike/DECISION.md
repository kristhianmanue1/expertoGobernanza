# Decisión propuesta — Akoma Ntoso en R1

**Resultado final:** `adaptador` experimental · **No:** migración/adopción/dependencia

## Qué funciones nuevas aporta

1. estructura legislativa XML validable por esquema;
2. identificación estándar de fragmentos mediante `eId`;
3. separación Work/Expression/Manifestation para distinguir obra, versión y
   archivo concreto;
4. IRIs y referencias entre documentos/fragmentos;
5. idioma y autores editoriales explícitos;
6. base potencial de intercambio con herramientas LegalDocML; ningún consumidor
   real fue probado en este spike.

## Qué no aporta

- no prueba que una disposición esté vigente;
- no verifica que una cita cubra sujeto, objeto o relación;
- no reemplaza EvidenceEdge ni el gate de fidelidad;
- no convierte interpretación jurídica en hecho;
- no es motor Law as Code ni grafo de conocimiento;
- no resuelve bitemporalidad por el solo hecho de usar FRBR.

## Recomendación

Conservar JSON/YAML como modelo autoritativo interno. Mantener el adaptador como
exportador experimental sin runtime y sólo ampliarlo cuando exista un consumidor
concreto que exija AKN. Cualquier exportación debe viajar junto con un sidecar de
procedencia/EvidenceEdge o con una extensión explícita; nunca inferir `verified`
desde la validez XSD.

La Expression identifica el consolidado de cuerpo 2026-01-15; la fecha
2001-12-20 describe únicamente la última reforma conocida de la porción `LSS:5`.
Ni una fecha FRBR ni `FRBRauthoritative=false` en la Expression certifican
vigencia: este último sólo marca que la conversión editorial no es oficial.

Regla de abandono: si el primer consumidor exige extensiones propietarias para
F5/EvidenceEdge pero no aprovecha estructura, IRIs o versionado FRBR, eliminar el
adaptador y conservar únicamente este spike como evidencia de evaluación.
