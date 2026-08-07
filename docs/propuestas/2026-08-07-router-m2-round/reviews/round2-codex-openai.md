> **Estado:** BLOQ  
> **Modelo subyacente:** OpenAI GPT-5 (Codex)  
> **Autor excluido:** opencode/GLM-5.2  
> **Lente:** B — seguridad de datos / viabilidad operativa

## Hallazgos

- [BLOCKER] Un symlink desde una ruta `publico` hacia un archivo confidencial dentro del repositorio evade la clasificación. `_confined()` resuelve el destino y sólo comprueba que permanezca dentro del repo, pero `classify()` evalúa la ruta pública original y luego `read_bytes()` lee el destino resuelto. Reproducción: `public/leak.md → personal.md` fue incorporado al bundle — evidencia [router.py:86](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:86), [router.py:90](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:90), [router.py:99](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:99) — fix: rechazar cualquier componente symlink o reclasificar también la ruta canónica resuelta aplicando la clase más restrictiva; abrir con protección `NOFOLLOW`/equivalente para evitar TOCTOU y añadir regresión público→personal dentro del repo.

- [BLOCKER] `--authorize-internal-ref` sigue siendo auto-afirmable: cualquier string truthy, incluso `"   "` o `"agent-self-asserted"`, permite leer el archivo. Además, se envía el contenido interno crudo sin comprobar anonimización, contrario a §7.4 — evidencia [router.py:93](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:93), [router.py:142](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:142), [politica-agentes.md:393](/Users/krisnova/www/expertoGobernanza/docs/politica-agentes.md:393) — fix: validar la autorización contra un registro externo no controlado por el agente o una aprobación firmada, y exigir evidencia verificable de anonimización; sin ambas condiciones, denegar.

- [HIGH] El hash de bundle y configuración sí queda registrado, pero el log no es inmutable ni autosuficiente para auditoría: el agente elige `--log` y puede modificar/truncar el JSONL posteriormente. Sin conservar el bundle exacto tampoco puede recomputarse históricamente su hash — evidencia [router.py:114](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:114), [router.py:130](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:130), [router.py:150](/Users/krisnova/www/expertoGobernanza/review_routing/router.py:150) — fix: resolverlo en el harness con bundle sellado, configuración/digest fijados por el runner y log append-only externo. Deuda declarada; no se eleva a BLOCKER.

## Verificación positiva

Quedaron cerrados los casos literales del ciclo 1: colisión de prefijo, `..`, ruta absoluta, default-deny, archivo faltante y exit `1` ante cualquier denegado. Diez pruebas ejecutables sin escritura pasaron; los casos focalizados confirmaron `exit 1` y los dos bypasses anteriores. La suite completa fue inconclusa porque el sandbox de revisión no permite crear los directorios temporales requeridos por los tests, no por fallos de aserción.

Para operar una ronda real todavía se requiere que el harness fije configuración y argumentos, valide la aprobación humana, selle el bundle antes del proveedor, compruebe exit code antes de enviar, restrinja egress/retención y escriba la evidencia en almacenamiento append-only externo.

**Decisión: fix-and-retry**
