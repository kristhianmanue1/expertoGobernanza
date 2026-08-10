# Pass 1 — Moonshot / Kimi

**Decisión:** `fix-and-retry` · **Máxima severidad:** MED

- La promesa de marcar Manifestation era imposible en core AKN; el test tenía
  nombre engañoso.
- La matriz no enumeraba todos los campos perdidos.
- La Expression 2001 podía inducir una falsa inferencia de última versión.
- El número transformaba `5.` a `Artículo 5.` sin una inversa real.
- `GUID` era redundante y `FRBRname=LSS` no coincidía con el IRI `/lss`.
- XSD temporal y ausencia de consumidor probado debían declararse.

El revisor no refutó la dirección `adaptador`; pidió cerrar trazabilidad y
matriz antes de votar `proceed`.
