# Ronda adversarial R3 — F5 LFEP, LOAPF P3 y gate

**Fecha:** 2026-08-10 · **Impacto:** alto · **Autor excluido:** OpenAI/Codex  
**Estado:** cerrada · **Regla:** cualquier BLOCKER bloquea; retry tras fixes

## Secuencia

| Paso | Proveedor/modelo | Resultado | Acción |
|---|---|---|---|
| Pass 1 | Zhipu / GLM-5.2 | `block` | aceptar BLOCKER y corregir |
| Retry | Moonshot / Kimi K3 256k | `proceed` | contar |
| Retry | Zhipu / GLM-5.2 | `proceed` | contar |
| Retry | xAI / Grok 4.5 | `proceed` | contar |

El quórum final tiene tres proveedores/modelos subyacentes distintos. Google no
participó. Anthropic, DeepSeek, OpenCode/Grok y Cline/Qwen tuvieron intentos
inválidos documentados y no se contabilizaron.

## Fixes entre pass y retry

1. limpieza de whitespace que hacía fallar el gate;
2. cuotas exactas `3 answerable / 2 blocked / 5 negativos` en el runner;
3. Q5 sin cobertura de objeto ni relación y test de mutación;
4. `ultima_reforma_cuerpo.cubre_disposicion: false` para LFEP;
5. aclaraciones LOW sobre salida resumida, cached-check y cobertura ¶3.

## Agregación

El retry terminó 3/3 `proceed`, sin BLOCKER. Las reservas de proceso —espera
admin, CI remoto suspendido y archivos nuevos no cubiertos por diff hasta
staging— permanecen explícitas y no se convierten en falsa aprobación Git.

