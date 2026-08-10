# Reconciliación — arquitectura y posicionamiento — 2026-08-10

> **Decisión:** `fix-and-retry`.
> **Estado de gate:** quórum válido — Anthropic + Moonshot + Zhipu; voto 2/3
> `fix-and-retry`, 1/3 `proceed`.
> **Regla:** no se descartó ningún hallazgo válido; los solapados se fusionan.

## Hallazgos consolidados

### H1 — HIGH — La verificación agregada del instrumento puede contaminar disposiciones

Los tres revisores coinciden: `LFEP.vigencia_verificada: true` convive con
`LFEP:5.f5: false`. El derivado lo representa correctamente, pero un consumidor
del registry podría heredar el agregado.

**Fix requerido:** antes de adoptar la arquitectura, declarar y probar una regla
fail-closed: ningún estado se hereda instrumento→disposición ni
disposición→relación. Deprecar el booleano agregado o marcarlo explícitamente
como resumen no autoritativo derivado de estados por disposición.

### H2 — HIGH — `EvidenceEdge v0` carece de alcance probatorio explícito

Los tres revisores piden no esconder el alcance dentro de `evidence` libre.

**Campos mínimos adicionales:**

```yaml
evidence_scope:
  source_level: 1 | 2 | 3 | 4
  covers_subject: true | false
  covers_object: true | false | not_applicable
  covers_relation: true | false
inheritance: prohibited
```

`verification_status` pertenece a la afirmación completa, no a sus nodos.

### H3 — MED — La taxonomía de afirmaciones debe ser cerrada

`menciona`, `remite_a_ley_especifica` y `relaciona_con` no tienen el mismo peso.
Un solo `verificada` no distingue texto de interpretación.

Los tres revisores llegaron a este punto de forma independiente.

**Fix requerido:** enumeración versionada mínima, por ejemplo:
`textual`, `remision_normativa`, `jerarquia_interpretativa`, `vigencia`,
`eficacia`, `aplicabilidad`. Toda clase no reconocida falla cerrado.

### H4 — MED — La diferenciación de producto necesita falsificador

Moonshot exige un criterio de muerte; Zhipu coincide en que “verificable” sólo
describe capacidad y no prueba el producto. Hoy la pregunta “¿por qué el IMSS es OPD?”
no puede responderse como cadena completamente verificada porque LFEP:5 y varias
aristas siguen pendientes; eso la vuelve un buen benchmark, no una demostración
comercial.

**Fix requerido:** preregistrar cinco preguntas del eje IMSS, score binario de
procedencia/cobertura y una regla de abandono o reformulación. Comparar sólo con
fuentes/productos para los que exista acceso y autorización vigentes.

### H5 — MED — Conviene anteponer EvidenceEdge al spike AKN

Moonshot propone este ajuste: EvidenceEdge corrige un riesgo presente; AKN
conserva valor de opción. Anthropic y Zhipu no lo consideran bloqueante.

**Fix requerido:** orden revisado:

1. cerrar F5 LFEP:5 y deuda H1/H5;
2. corregir semántica por disposición/no-herencia;
3. especificar `EvidenceEdge v0` como YAML/JSON plano + validador;
4. ejecutar benchmark IMSS falsable;
5. sólo entonces spike AKN acotado.

### H6 — LOW — El spike AKN necesita salida cuantificable

**Fix requerido:** una disposición, sin tocar registry, máximo un ticket; matriz
de pérdida/duplicación para id, texto, jerarquía, expresión temporal, fuente,
hash, modificación y revisión. El resultado decide `adaptador | diferir | no
adoptar`; no habilita por sí solo migración XML.

## Ajustes de reconciliación

- El benchmark competitivo de Moonshot se acepta, pero no se exige acceso
  gratuito: puede usarse acceso autorizado; sin acceso se marca `no evaluado`.
- `gate_version` por arista se conserva como string de procedencia, no como
  subsistema de versionado. Esto atiende el riesgo de sobrearquitectura.
- La salida Google sobre VerPorMexico se excluye por falta total de pertinencia,
  con justificación y evidencia preservada; no se interpreta como voto.
- El `proceed` de Zhipu no se descarta: se conserva como voto minoritario. Su
  argumento distingue dirección estratégica (aceptable) de implementación del
  edge (aún requiere fixes); la mayoría aplica `fix-and-retry` al paquete.

## Dirección revisada

Se mantiene la tesis como **hipótesis**, no como decisión adoptada:

> Infraestructura verificable de legislación mexicana para auditoría y agentes
> de IA, basada en afirmaciones con evidencia y sin promoción implícita.

No se autoriza todavía Akoma Ntoso, knowledge graph, embeddings, API general ni
Law as Code. Una nueva ronda requiere primero H1–H3; H4–H6 alimentan el contrato
del benchmark/spike, pero no sustituyen los fixes de consistencia del corpus.
