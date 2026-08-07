# Política de seguridad — ExpertoGobernanza

## Reportar una vulnerabilidad
- Abre un issue privado o contacta al mantenedor (`@kristhianmanue1`). El repo es
  **privado** durante alfa; no publiques exploits en issues públicos.
- Reporta sin copiar contenido normativo confidencial; referencia el archivo/sección.

## Modelo de amenaza y reglas (política §7.1)
- **Secretos:** jamás claves/tokens/credenciales en código o commits. Usa variables de
  entorno + `.env` (gitignored). El CI no tiene secretos de producción.
- **Datos personales:** no se commitean en claro ni se citan verbatim salvo que el
  documento sea público y la cita sea el objeto legítimo del trabajo. Ante duda,
  anonimizar o referenciar.
- **Datos en revisión multi-provider (§7.4):** antes de enviar artefactos a proveedores
  externos, el router (`review_routing/`) clasifica ex-ante: `público` permitido;
  `interno-institucional` sólo anonimizado y con autorización humana;
  `personal/confidencial` **prohibición dura**. Se registra un hash de lo enviado.

## Proveniencia y firma
- Los commits los aplica un **humano** (admin); los agentes no tienen claves de firma
  (política §7.2: redactar ≠ promulgar). Ver ADR-0002.
- Proveniencia por **modelo subyacente**, no por CLI. Cada agente declara proveedor +
  modelo en el reporte (§12) y en cada revisiona adversarial (conflicto de interés).

## Alcance
Esta plataforma **no es asesoría jurídica** ni una norma en vigor; es infraestructura de
inteligencia normativa. No sustituye la promulgación ni el criterio humano/institucional.
