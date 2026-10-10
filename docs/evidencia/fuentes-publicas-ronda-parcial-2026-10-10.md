# Ronda adversarial parcial: canales públicos complementarios

**Fecha:** 2026-10-10 · **Base:** commit `0d8cda2` y enmienda acotada a `docs/autorizacion-fuentes-r1.md`. **Estado:** PARCIAL, sin `proceed`.

## Rutas y resultados observados

- OpenCode 1.18.35: configuración local `zai-coding-plan/glm-5.3-flash` con endpoint HTTPS `api.z.ai`. `opencode models zai-coding-plan` listó el modelo; una sonda aislada `PONG` terminó con exit 0 y su sesión exportada reportó `providerID=zai-coding-plan`, `modelID=glm-5.3-flash`. Esto prueba la ruta de esa sonda, no la revisión. El intento de revisión del diff filtrado agotó 120 s sin dictamen.
- Codex CLI 0.161.0: una sonda aislada sin configuración de usuario devolvió `PONG`. El intento de revisión con `gpt-6-sol` fue rechazado por la cuenta ChatGPT (`model not supported`). Un nuevo intento con el modelo predeterminado produjo una revisión de contexto aislado sobre el paquete filtrado. El modelo efectivo de esa revisión quedó `unknown`: no se obtuvo telemetría suficiente.
- Claude Code 2.1.280: `claude auth status` informó `loggedIn=true` mediante `claude.ai`, pero la sonda sin `--bare` fue rechazada porque la organización deshabilitó acceso de suscripción a Claude Code. La sonda previa con `--bare` dio `Not logged in` porque esa opción no lee OAuth. No se ejecutó revisión Anthropic.

## Hallazgos de Codex sobre el paquete anterior

Decisión del revisor: `fix-and-retry`; fue una revisión del paquete suministrado, sin consulta independiente de las URL.

1. **Alta:** la fila propuesta podía interpretarse como permiso para transmitir archivos completos. Corrección aplicada: limitar a diff filtrado y extractos públicos estrictamente necesarios; excluir archivos completos, CTIM, PDF locales, material interno y datos personales.
2. **Media:** el historial “sin ampliar la lista de fuentes” era ambiguo junto a la incorporación de LeyesBiblio. Corrección aplicada: la autorización del proveedor no altera por sí misma los canales; LeyesBiblio deriva de la decisión precedente.
3. **Media:** el acto DOF 07-10-2026 no prueba vigencia actual de `CPEUM:4:P4`. Se conserva `fecha_consulta_vigencia: 2026-08-10`; la nota de fuentes delimita la comparación posterior como secundaria y parcial. No se promovió el estado del slice.

La revisión anterior **no** valida la enmienda corregida. OpenCode/GLM y Claude no entregaron dictamen. Quórum de tres proveedores distintos: **incompleto**. Para reanudar, habilitar acceso Anthropic o autorizar un tercer proveedor distinto; después ejecutar revisión fresca del diff final con atribución del modelo efectivo y resolver sus hallazgos. No hacer merge ni declarar `proceed` desde esta nota.
