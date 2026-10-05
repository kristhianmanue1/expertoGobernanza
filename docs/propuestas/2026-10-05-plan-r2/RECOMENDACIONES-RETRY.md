# Ronda sobre recomendaciones R2 — 2026-10-05

**Alcance:** revisar las recomendaciones del análisis sobre `main@8410075`
y aplicar correcciones al borrador `docs/plan-r2.md`. Autorización del
Operador: ronda y edición del plan; no adopción ni implementación de tickets.
**Estado:** revisión parcial; no `proceed` multi-provider.

## Procedencia y método

- Productor/reconciliador: Codex, proveedor declarado OpenAI; modelo efectivo
  sin telemetría independiente.
- Revisor: subagente `/root/adversarial_r2`, contexto separado del productor,
  mismo proveedor declarado. Recibió el historial, incluidas recomendaciones:
  no fue una revisión ciega a la propuesta ni decorrelación de proveedor.
- Inspeccionó política, plan y código; no ejecutó pruebas ni editó archivos.
  Primera decisión: `fix-and-retry` de las recomendaciones. No hay votos de
  proveedores adicionales.
- Intento Claude: CLI con herramientas limitadas a lectura, sin escritura.
  Resultado: exit 1, `403 oauth_not_allowed_for_organization`, cero tokens de
  entrada/salida y `modelUsage={}`. No generó revisión. La organización tiene
  deshabilitado el acceso por suscripción según el error; no se intentó otra
  vía de autenticación ni se inspeccionaron credenciales.
- La revisión histórica Grok de `ADVERSARIAL.md` corresponde a otro artefacto;
  no se agrega como voto sobre estas modificaciones.

## Hallazgos y tratamiento

| ID | Severidad | Hallazgo | Corrección al borrador |
|---|---|---|---|
| R01 | BLOCKER | Llamar v2 a un gate sin fecha jurídica contradice §7.3, aunque sólo emita medio | Conservar v1/N/A_v1, alto inalcanzable y diagnóstico aditivo |
| R02 | HIGH | Uno-a-uno greedy puede depender del orden; inclusión inversa permite citas sobredimensionadas | T1b: máxima cardinalidad, desempate estable, criterio versionado y pruebas de permutación/duplicados |
| R03 | MED | Hacer ID obligatorio alteraría la evaluación textual vigente | Conservar ID opcional, métricas principales y diagnóstico de IDs |
| R04 | HIGH | Hashes sin predicciones accesibles no permiten recalcular | Importación offline y artefactos recuperables autorizados en T2 |
| R05 | HIGH | Una sola fila nueva no garantiza quórum con autor excluido | T5 exige configuración completa de proveedores, datos y reconciliación |
| R06 | HIGH | YAML seguro no evita duplicados; fallo operativo no es evidencia faltante | Rechazo de duplicados/estructura y estados explícitos con precedencia |
| R07 | MED | Prueba local no demuestra arreglo del runner remoto | T0 exige run y SHA del cambio; ausencia de run deja cierre parcial |
| R08 | MED | Firma de un argumento no prueba aislamiento del proceso | Afirmación limitada a interfaz, inspección del extractor y contexto fresco T2 |

No se descartaron hallazgos. La corrección R03 ajusta la recomendación inicial
del productor: un TP textual con ID ausente y gate bajo puede ser válido por
contrato; no se vuelve un error por definición.

## Límites y decisión

El texto conserva los límites de fuente/fecha y no convierte hashes en prueba
de fidelidad de extracción. No altera política, trazas, código ni allowlist.
R1 sigue vigente. El cierre de infraestructura se distingue del experimento T2.
La autorización de editar este borrador no constituye adjudicación de R2.

Quórum de alto impacto insuficiente: autor y revisor son del mismo proveedor;
Claude no participó. La revisión final del texto se registra a continuación;
cualquier conformidad local no sustituye §6 ni habilita merge/adopción.

## Verificación final

La relectura del revisor detectó dos puntos adicionales: maximum matching aún
podía aumentar recall al duplicar una cita compatible con dos gold (HIGH), y
el JSON de T2 parecía incluir las predicciones pese a excluir cadenas (MED).
Se corrigieron: clases de equivalencia antes del matching, copias extra como
FP y caso de prueba ambiguo; resultados con referencias/hashes y artefactos
recuperables fuera del JSON publicado. No se descartaron observaciones.

El revisor confirmó posteriormente que T1b y T2 atienden los dos hallazgos,
sin nuevos bloqueantes en esa comprobación acotada. Fue validación documental,
sin ejecución de código; no constituye `proceed` multi-provider.

Plan revisado en esa relectura: SHA-256
`70c3567016024e0203e0f070e3f448dac7a59177b04e1da632c1543ecad24fd2`.

## Incorporación posterior

Instrucción del Operador del 2026-10-05: incorporar las precisiones y empezar por T0. El plan queda así:

- `missing_evidence` con substring y hash declarado en `missing|match` es `medio`; disposición ausente del modelo es `bajo`; hash distinto o PDF ilegible siguen en `bajo`.
- Los puntos 8 y 9 quedan sujetos a adopción por revisión y ticket. Esta instrucción adopta solo T0.
- T1b define la clase como texto normalizado más ID exacto, nulo incluido. `A:1` con `B:1` puede dar recall 1. `A:1` con nulo frente a dos gold del mismo texto queda en recall 0.5.

Esa incorporación no es `proceed` de H1/H2 ni sustituye la cola R1.
Checks: `git diff --check` limpio; gate de tamaños 161 archivos versionados
OK; expediente nuevo comprobado por separado (72 líneas, límite 800) y
diff-check contra `/dev/null` sin errores. No se repitió la suite de software:
los cambios son sólo documentales. AN-KLA verifica en rev 28; sin escritura.
