# Relatoría — benchmark IMSS → spike Akoma Ntoso

**Estado global:** OK técnico / PARCIAL administrativo  
**Autor/modelo:** OpenAI Codex; revisores Anthropic, Moonshot, Zhipu/GLM  
**Plan/fase:** R1 · fidelidad EvidenceEdge y evaluación AKN  
**Fecha/hito:** 2026-08-10 · benchmark falsable seguido de spike unitario

## Resumen ejecutivo

Se ejecutó en el orden prerregistrado: primero cinco preguntas IMSS que sólo
admiten EvidenceEdge válidos; después, y sólo tras `proceed` unánime, un spike
Akoma Ntoso sobre `LSS:5`. El benchmark quedó 5/5 con cinco negativos rechazados;
el spike conserva identidad/texto y valida contra AKN 1.0, pero sólo justifica un
adaptador experimental acompañado por evidencia, no adopción del estándar.

## Secuencia y decisiones

1. El benchmark inicial fue invalidado porque confundía recorrido estructural
   con fidelidad documental. El retry prerregistró el gate compuesto.
2. R2 obtuvo tres positivas, dos bloqueadas, 5/5 negativos rechazados y 0 FP/FN.
3. El quórum autorizó únicamente un spike local sobre `LSS:5`.
4. El pass 1 AKN detectó errores de versión, autoridad y transformación inversa.
5. Los retries separaron Work/Expression/Manifestation, añadieron la inversa,
   vendorización XSD, matriz exhaustiva y resolución `#lss` al Work contenedor.
6. La confirmación final fue `proceed` unánime. La decisión sustantiva es
   `adaptador`; migración, runtime y afirmaciones de vigencia quedan prohibidos.

Fuentes técnicas: [OASIS AKN Part 1](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part1-vocabulary.html),
[Part 2 y XSD](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/akn-core-v1.0-part2-specs.html)
y [Naming Convention](https://docs.oasis-open.org/legaldocml/akn-nc/v1.0/akn-nc-v1.0.html).

## DoD y evidencia

| Componente | Evidencia | Resultado |
|---|---|---|
| Benchmark | 5 preguntas; 5 negativos; 4 PDF rehasheados | OK |
| EvidenceEdge | 36 tests del benchmark + contrato | OK |
| AKN | 7 tests; XSD válido; inversa exacta | OK |
| Tamaño | generador AKN 248 líneas (<250) | OK |
| Adversarial | tres proveedores; autor excluido; sin BLOCKER | OK |
| Alcance | una disposición; corpus/registry no mutados por AKN | OK |

## Estado canónico

| Área | Estado | Nota |
|---|---|---|
| Git / PR / push | PARCIAL | espera-admin; no se hizo commit ni push |
| AN-KLA | OK | sin escritura: la documentación es el hogar durable |
| DoD local | OK | benchmark, tests, hashes, XSD y tamaños reproducidos |
| Adversarial | OK | `proceed` unánime en benchmark y spike |

## Próximo hito recomendado

No ampliar el XML por inercia. El siguiente hito AKN sólo procede cuando exista
un consumidor LegalDocML concreto: probar importación real de este mismo archivo
y medir qué capacidades usa. En paralelo, la deuda LOAPF de metadata agregada
permanece fuera de este spike y debe resolverse como tarea independiente.

**Actualización posterior:** la deuda LOAPF fue resuelta en la ronda R3 mediante
`LOAPF:1:P3`; esta relatoría conserva la secuencia histórica benchmark→AKN.
