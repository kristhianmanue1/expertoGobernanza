# Consulta IMSS mediante Skopos: prueba bilateral local

**Observado:** 2026-10-08, este Mac, ramas
`codex/skopos-imss-local-function` (expertoGobernanza) y
`codex/skopos-labels-v05-operational` (Skopos), antes de commit.
Fuente oficial: <https://www.imss.gob.mx/sites/all/statics/pdf/manualesynormas/2000-002-001.pdf>;
PDF local SHA-256 `719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323`.

## Recorrido desde el consumidor

Se invocó `.venv/bin/python -m scripts.skopos_imss` en secuencia:

| Consulta | Resultado observado |
| --- | --- |
| `page 1` | `ok`, 20 líneas OCR, `runtime=stopped` |
| `page 188` | `ok`, texto nativo con IDs y cajas, `runtime=stopped` |
| `search 'MANUAL DE ORGANIZACIÓN' --limit 2` | `matched`, dos candidatos, `runtime=stopped` |
| `item 188 <item_id>` | Ítem nativo exacto cotejado con manifiesto fijado, `runtime=stopped` |
| `label 21 --node n5` | Literal `…SALUID`; normalización `…SALUD`; ID y render fijados |
| `item 188 <ID ausente>` | Error `evidence_unavailable`, exit distinto de cero, sin texto citable |
| `label 21 --node n5` tras el error | Recuperación `ok`, mismo literal y normalización |

Después de la secuencia se observaron `document.sock` y
`graph-labels-v05.sock` ausentes, sin listener TCP en `127.0.0.1:37034`.
El productor ejecutó además smoke v0.5 de páginas 18–22, recuperación por
ID, cinco controles negativos y replay determinista, con recibo `stopped`.
El cliente falla cerrado al recibir identidades distintas; la configuración
local privada v0.5 está fijada por SHA-256
`b9333d73a7eabf4ed8bc5e272de20ad81954f9edeaa3eb2c82f708b2e916888f`.

`./scripts/ci_check.sh` completó 219 tests y el gate de tamaños/registro;
Skopos completó 457 tests (seis omisiones de suite), tamaños y planes.
Una primera secuencia de aceptación detectó que el manifiesto OCR declara
188 páginas físicas aunque contiene seis derivadas; se corrigió la
comprobación del cliente y se repitió el recorrido completo en verde.

## Decisión de revisión y promoción

El Operador autorizó el 2026-10-08 una excepción **sólo para este alcance
local**: revisión con dos agentes/modelos externos en vez del quórum general
de tres proveedores de `docs/politica-agentes.md`. OpenCode con
`zai-coding-plan/glm-5.3-flash` revisó Skopos v0.5 y Muse CLI con
`muse-spark-1.3` revisó productor y consumidor; tras las correcciones ambos
emitieron `proceed` dentro de sus métodos. Codex hizo autorrevisión adicional,
sin contarla como tercer proveedor verificado. La excepción permite fusionar
el consumidor local; no modifica la política general para otros hitos.

## Límite de aceptación

La función queda probada para recuperación, procedencia y apagado bajo demanda
en este Mac. El cotejo visual fue no ciego y sólo cubrió 86 rótulos de p18–22
y ocho funciones de p23–188; toda cita nueva exige leer el fragmento visible
en el PDF y comprobar su vigencia por separado. No se admite el manual al
corpus ni se habilitan vectores. La política vence
`2026-11-08T00:00:00Z`; la prueba no constituye renovación.
