# Router harness — Índice

> **Plan técnico** para cerrar la deuda de egress del router §7.4.
> **Estado:** borrador para ejecución por agentes de IA. **Fecha:** 2026-08-13.
> **Linaje:** política §7.4 (CAGF-A10), `review_routing/router.py` (deuda declarada
> en su docstring), ADR-0002 (proveniencia), plan R1 (E7).

## Qué resuelve este plan

El router actual clasifica y bitacora, pero corre **en-proceso con el agente**: es
una advertencia + auditoría, **no** una frontera de egreso enforceada. Un agente
determinado puede bypasearlo (copiar contenido a ruta pública, invocar el CLI
externo directo). Este plan construye el **harness** que hace el egress
**verificable y trazable**: bundle sellado, gateway como ruta sancionada y
bitácora append-only con cadena de hash (tamper-evident).

## Archivos de este plan (lee en orden)

| Archivo | Cuándo leerlo |
|---|---|
| `01-analisis-y-alcance.md` | Siempre primero: el gap, qué entra y qué no |
| `02-arquitectura.md` | Antes de implementar: sellado, gateway, log encadenado |
| `03-tareas.md` | Durante la ejecución: desglose con DoD ejecutable por tarea |

## Reglas de aplicación (de política §2 + Skevi)

1. **1 tarea = 1 PR = 1 contrato verificable.** DoD con checks ejecutables.
2. **Stdlib sólo** (consistente con el router actual: sin LLM, sin deps).
3. **Fail-closed:** cualquier denegado → exit ≠ 0 (ya en el router; se conserva).
4. **Honestidad de límites:** el harness **no** es un sandbox OS-level (ver §2
   de análisis). Lo que entrega es cadena de custodia verificable + ruta
   sancionada fácil + bypass detectable por ausencia de log.
5. **Archivos pequeños** (gate §3: código < 800, doc < 800).
6. **Ronda adversarial** al cerrar el hito (política §6; quorum-lite mínimo).

## Fuera de alcance (explícito)

- Sandbox OS-level / proxy de red (overkill para alfa; se agenda si hay multi-usuario).
- Anonimización automática de `interno_institucional` (pipeline separado; aquí se
  sigue denegando hasta que exista).
- Firma criptográfica del bundle con e.firma (capa legal, ADR-0005; el sello aquí
  es SHA-256 determinista, no firma legal).
