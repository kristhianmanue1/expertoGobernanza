# ADR-0002 — Proveniencia y firma de contribuciones de agentes

> **Estado:** Propuesto. **Clase:** Estratégico (toca gobernanza de git y fidelidad §7).
> **Fecha:** 2026-08-07. **Autor:** agente (opencode/glm-5.2). **Autoridad que adopta:** humano (§7.2).
> **Adopción requiere (actos humanos):** (1) generar/importar clave GPG del admin;
> (2) activar `commit.gpgsign=true` o branch protection `Require signed commits` en `main`.

## Contexto
La §7.2 establece que **redactar ≠ promulgar**: los agentes producen borradores; el
**humano** aplica commit/push y responde. Hoy (2026-08-07) los commits del repo **no están
firmados** (`sig: N`) y el `git-author` es la cuenta humana (`devcdmx`), no el agente. La
proveniencia del agente vive en: (a) texto del mensaje de commit, (b) el bloque `authority`
de AN-KLA (`issuer.id` + `configuration_fingerprint`), (c) declaraciones verbatim en reviews
adversariales y reportes. **Ninguna es firma criptográfica** — un modelo puede
autodeclararse otro.

Surgió (diálogo con un abogado, 2026-08-07) la pregunta: *¿cómo firman los agentes su
participación?* Este ADR formaliza la respuesta y el camino a firma verificable.

## Decisión (propuesta)
1. **Los agentes NO tienen claves de firma.** Toda firma (commits, releases) corresponde al
   **humano/admin**. Es consistente con §7.2 y CAGF-A10 (el sustrato que pone en vigor queda
   en control humano).
2. **Commits firmados por el admin con GPG** (a habilitar): `commit.gpgsign=true` + branch
   protection `Require signed commits` en `main`. La firma vincula el cambio a la identidad
   humana que responde, no a un modelo.
3. **Proveniencia del agente declarada, no criptográfica**, pero trazable: cada commit lleva
   en su mensaje el modelo/versión (cuando el agente lo redactó); AN-KLA lleva
   `configuration_fingerprint` (hash de la triada `{agente, modelo, proveedor}`); las reviews
   declaran proveedor + **modelo subyacente** + conflicto de interés.
4. **Futuro (no bloquea v1.2):**
   - **cosign / Sigstore** para firmar **artefactos de release** (snapshots del corpus,
     modelos derivados) con procedencia SLSA.
   - **Content provenance** estilo **C2PA** para atar cada artefacto normativo generado a su
     modelo/versión + sello de tiempo.
   - **Registro externo (no autodeclarado)** del modelo que corrió (p. ej. log del router
     §7.4 firmado o atestiguado por el harness tmux).

## Consecuencias
- **+** Responsabilidad clara: el que firma (y responde) es un humano identificable; se
  evita la ficción de "la IA se autentifica".
- **+** Trazabilidad suficiente hoy para auditoría (hashes de contenido + identidad del modelo
  declarada en tres lugares).
- **−** Hoy **no** se prueba criptográficamente qué modelo escribió qué — sólo qué humano
  aplicó el cambio y qué modelo *se declara* autor. Deuda declarada.
- **−** Costo operativo: gestión de clave GPG del admin (rotación, respaldo).

## Alternativas consideradas
- **Dar claves de firma a los agentes:** descartada; contradice §7.2 y reintroduce el riesgo
  de auto-autenticación (un agente firma su propia revisión).
- **Firma solo con hashes (status quo):** insuficiente; un digest no es firma verificable.
- **C2PA/cosign desde ya:** descartada para v1.1; requiere infra (Sigstore, keystore) y no
  bloquea la salida a v1.2. Se agenda.

## Ítems abiertos (decisión humana)
- Generar/importar clave GPG del admin y activar firma obligatoria en `main`.
- Decidir proveedor del quórum §6 estable (gemini/qwen cayeron por auth) — afecta la
  proveniencia declarable.
- Cuando existan releases: adoptar cosign + definir el keystore de firma de artefactos.
