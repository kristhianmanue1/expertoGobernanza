# Checklist F5 — eje IMSS público (LOAPF / LFEP / LSS / RIIMSS)

**Fecha guía:** 2026-08-10 · **Uso:** verificación humana antes de
`vigencia_verificada: true` (metodología `docs/fuentes-legal-mx.md`, F2/F5).  
**No es asesoría legal.** Plantilla de contraste repo ↔ DOF/portal público.

**Criterio OK:** el acto (o consolidado + traza de reforma del **artículo** del
slice) cuadra materialmente con el texto de trabajo; las reformas **del cuerpo**
que no tocan el artículo se marcan `no_cubre_slice`.

**Plantilla de respuesta** (cópiala al final de cada bloque o al final del doc):

```text
INSTRUMENTO: LOAPF | LFEP | LSS | RIIMSS
disposición: …
DOF/URL final: …
¿Cubre la disposición del slice? sí/no/parcial
¿Texto cuadra con el repo? sí/no/parcial
notas: …
revision_vigencia:
  revisado_por: Kristhian Manuel Jiménez
  fecha: YYYY-MM-DD
  auto_revision_declarada: true
Decisión: dejar false | true para esta disposición
```

---

## 0. Orden sugerido (≈ 45–90 min)

1. **LSS:5** (naturaleza IMSS — más valioso para el piloto)  
2. **RIIMSS:1** (objeto del Instituto)  
3. **LFEP:1** (marco paraestatal)  
4. **LOAPF:1** (APF centralizada/paraestatal)  
5. Opcional: **LSS:1** (observancia general)

Home DOF para búsquedas: https://www.dof.gob.mx/

---

## A) LSS — `LSS:5` (prioridad)

### Texto en el repo (lookup)

> La organización y administración del Seguro Social, en los términos consignados en esta Ley, están a cargo del organismo público descentralizado con personalidad jurídica y patrimonio propios, de integración operativa tripartita, en razón de que a la misma concurren los sectores público, social y privado, denominado Instituto Mexicano del Seguro Social, el cual tiene también el carácter de organismo fiscal autónomo.

Marcador consolidado: *Artículo reformado DOF **20-12-2001***.

### Ligas

| Prioridad | Qué | URL |
|-----------|-----|-----|
| 1 | PDF consolidado Cámara (texto de trabajo) | https://www.diputados.gob.mx/LeyesBiblio/pdf/LSS.pdf |
| 2 | Índice reformas LSS | https://www.diputados.gob.mx/LeyesBiblio/ref/lss.htm |
| 3 | DOF — buscar reforma Art. 5 | https://www.dof.gob.mx/ → fecha **20/12/2001** + *“Ley del Seguro Social”* + *“artículo 5”* / *“Instituto Mexicano”* |
| 4 | Publicación ley (antecedente) | DOF **21/12/1995** + *Ley del Seguro Social* |
| NO a ciegas | Última reforma cuerpo **15-01-2026** | Solo si el decreto toca Art. 5; si no → `no_cubre_slice` |

### Checklist

- [ ] ¿El decreto de **20-12-2001** (o el que confirmes) reforma el **Art. 5**?  
- [ ] ¿Aparece **organismo público descentralizado**, personalidad/patrimonio propios, **IMSS**, tripartita / fiscal autónomo?  
- [ ] ¿Cuadra con el párrafo del repo?  
- [ ] ¿15-01-2026 **no** es la traza del Art. 5 (si no lo modifica)?

### También en repo: `LSS:1` (menor prioridad)

Texto:

> La presente Ley es de observancia general en toda la República, en la forma y términos que la misma establece, sus disposiciones son de orden público y de interés social.

Basta contrastar con el consolidado Art. 1; traza primaria = publicación **21-12-1995** o reforma que toque Art. 1.

---

## B) RIIMSS — `RIIMSS:1`

### Texto en el repo

> El Instituto Mexicano del Seguro Social, en los términos consagrados en Ley del Seguro Social, tiene por objeto organizar y administrar el Seguro Social, que es el instrumento básico de la seguridad social, establecido como un servicio público de carácter nacional, para garantizar el derecho a la salud, la asistencia médica, la protección de los medios de subsistencia y los servicios sociales necesarios para el bienestar individual y colectivo, así como el otorgamiento de una pensión que, en su caso y previo cumplimiento de los requisitos legales, será garantizada por el Estado.

### Ligas (todas **públicas**)

| Prioridad | Qué | URL |
|-----------|-----|-----|
| 1 | **PDF portal IMSS** (archivo de trabajo) | https://www.imss.gob.mx/sites/all/statics/pdf/reglamentos/RIIMSS.pdf |
| 2 | Orden Jurídico (HTML) | https://www.ordenjuridico.gob.mx/Documentos/Federal/html/wo88802.html |
| 3 | Índice reglamentos Cámara | https://www.diputados.gob.mx/LeyesBiblio/norma/reglamento.htm |
| 4 | WORD Cámara n323 | https://www.diputados.gob.mx/LeyesBiblio/regla/n323.doc |
| 5 | DOF publicación | https://www.dof.gob.mx/ → **18/09/2006** + *Reglamento Interior* + *IMSS* |
| 6 | DOF última reforma claim | **23/08/2012** + mismo título |

### Checklist

- [ ] ¿El PDF/HTML contiene el **Art. 1** con el objeto del Instituto (organizar/administrar el Seguro Social)?  
- [ ] ¿Cuadra con el texto del repo?  
- [ ] ¿Confirmas pub. **18-09-2006** y, si aplica, reforma **23-08-2012**?  
- [ ] (Si 2012 no toca Art. 1) marcar esa reforma como `no_cubre_slice` para `RIIMSS:1`.

---

## C) LFEP — `LFEP:1`

### Texto en el repo

> La presente Ley, Reglamentaria en lo conducente del artículo 90 de la Constitución Política de los Estados Unidos Mexicanos, tiene por objeto regular la organización, funcionamiento y control de las entidades paraestatales de la Administración Pública Federal. Las relaciones del Ejecutivo Federal, o de sus dependencias, con las entidades paraestatales, en cuanto unidades auxiliares de la Administración Pública Federal, se sujetarán, en primer término, a lo establecido en esta Ley y sus disposiciones reglamentarias y, sólo en lo no previsto, a otras disposiciones según la materia que corresponda.

### Ligas

| Prioridad | Qué | URL |
|-----------|-----|-----|
| 1 | PDF consolidado | https://www.diputados.gob.mx/LeyesBiblio/pdf/LFEP.pdf |
| 2 | Índice reformas | https://www.diputados.gob.mx/LeyesBiblio/ref/lfep.htm |
| 3 | DOF publicación | **14/05/1986** + *Entidades Paraestatales* |
| 4 | DOF última reforma claim | **16/07/2025** (índice `LFEP_ref19`) — solo si toca Art. 1 |

### Checklist

- [ ] ¿Art. 1 habla de **entidades paraestatales** y del **Art. 90 CPEUM**?  
- [ ] ¿Cuadra con el repo?  
- [ ] ¿16-07-2025 cubre o no el Art. 1? (si no → `no_cubre_slice`)

---

## D) LOAPF — `LOAPF:1`

### Texto en el repo

> La presente Ley establece las bases de organización de la Administración Pública Federal, centralizada y paraestatal. La Oficina de la Presidencia de la República, las Secretarías de Estado y la Consejería Jurídica del Ejecutivo Federal, integran la Administración Pública Centralizada. Los organismos descentralizados, las empresas de participación estatal, las instituciones nacionales de crédito, las organizaciones auxiliares nacionales de crédito, las instituciones nacionales de seguros y de fianzas y los fideicomisos, componen la administración pública paraestatal.

### Ligas

| Prioridad | Qué | URL |
|-----------|-----|-----|
| 1 | PDF consolidado | https://www.diputados.gob.mx/LeyesBiblio/pdf/LOAPF.pdf |
| 2 | Índice reformas | https://www.diputados.gob.mx/LeyesBiblio/ref/loapf.htm |
| 3 | DOF publicación | **29/12/1976** + *Ley Orgánica de la Administración Pública Federal* |
| 4 | DOF última reforma claim | **~07/05/2026** (índice `LOAPF_ref81`) — solo si toca Art. 1 |

### Checklist

- [ ] ¿Art. 1 distingue APF **centralizada** y **paraestatal** (organismos descentralizados…)?  
- [ ] ¿Cuadra con el repo?  
- [ ] ¿La reforma reciente del cuerpo cubre o no el Art. 1?

---

## Hashes (integridad del PDF local)

| Archivo | sha256 (registry) |
|---------|-------------------|
| LOAPF.pdf | `3edf486e601217f5f595f94f56832d8845cbd9193b6494af52473237252bcc5f` |
| LFEP.pdf | `c0f203a9c6ebb990db8a2a43559ecf19e904f7c0757d0f334f7f4fb044aa6a12` |
| LSS.pdf | `8a28a16e1dce1f8e666f4cce5ed19745bc912b2ab1ca49787d5d4bef229398ed` |
| RIIMSS.pdf | `cd79b9644431626cddcf218cd71ec5d24a4fd5ecbe7755cf5b614649a2ea08b0` |

```bash
# ejemplo
shasum -a 256 corpus/originals/LSS.pdf
```

---

## Bloque único de respuesta (pegar al orquestador)

```text
=== F5 eje IMSS público ===

LSS:5
  URL final: …
  ¿Cubre disposición? sí/no
  ¿Texto cuadra? sí/no
  Decisión: false | true

LSS:1 (opcional)
  …

RIIMSS:1
  URL final: …
  ¿Cubre disposición? sí/no
  ¿Texto cuadra? sí/no
  Decisión: false | true

LFEP:1
  …

LOAPF:1
  …

revision_vigencia:
  revisado_por: Kristhian Manuel Jiménez
  fecha: YYYY-MM-DD
  auto_revision_declarada: true
```

Con ese bloque se puede aplicar el mismo PR de registry que en el slice salud (sin inventar decretos).

## Notas

- Texto de trabajo de leyes federales = **nivel 2 Cámara**; RIIMSS = **nivel 2 portal IMSS**.  
- `true` = ancla de **procedencia** del artículo del slice, no aplicabilidad casuística (F3).  
- Manuales IMSS no publicados: **siguen fuera**.
