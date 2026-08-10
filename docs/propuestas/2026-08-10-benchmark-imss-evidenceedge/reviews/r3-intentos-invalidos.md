# R3 — intentos no contados en el quórum

**Fecha:** 2026-08-10

| Intento | Motivo de invalidez | ¿Cuenta? |
|---|---|---|
| Anthropic / Claude CLI | límite de sesión antes de leer evidencia | no |
| DeepSeek vía OpenCode | credencial inválida | no |
| xAI/Grok vía OpenCode | credencial del adaptador inválida | no |
| Cline / Alibaba Qwen | SQLite readonly; retry seguro sin autoaprobación quedó interactivo; retry temporal no conectó API | no |
| Grok CLI, primer intento sandbox | sin credenciales/sesión y permiso FS; se detuvo | no |

No se reutilizó ninguna salida parcial como voto. Google permaneció descartado
por decisión del usuario. El asiento final xAI/Grok sólo se ejecutó después de
autorización explícita de egreso y sí consta en `r3-retry-grok.md`.

