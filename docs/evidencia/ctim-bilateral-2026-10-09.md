# CTIM: prueba bilateral local de cinco fuentes

**Observado:** 2026-10-09 UTC. Ejecutor: `python3 -m scripts.ctim_source_bilateral`
desde expertoGobernanza. Recibo completo: `ctim-bilateral-receipt-2026-10-09.json`.
Skopos se ejecutó primero desde `codex/skopos-source-profile-v03` y después
desde `main` (`d24e4bf`); los recibos de las ejecuciones sobre `44bd4d2`,
`3ce0e3a`, `7847228`, `b4b603e` y el merge fueron idénticos. Ágora se
ejecutó desde `main` con PR #4 fusionado.

Skopos recuperó los cinco originales con SHA esperado tras reinicio y rechazó
cinco SHA falsos (`material_not_allowed`). Consultó DA p282, procedimiento
CTIM p6 y POBALINES 2022 p75. Los dos HTML se cotejaron por offset y hash
contra los originales; Ágora verificó los cinco SHA originales y produjo dos
comparaciones candidatas sin admisión ni llamadas a proveedor. La sustitución
de POBALINES se sustenta en el transitorio de la fuente oficial y la matriz
humana; el bundle no adjudica direccionalidad. Rechazó página
PDF 0 y rango HTML invertido. El controlador compartido de Skopos terminó
detenido; el script comprobó que su socket y `127.0.0.1:37034` cerraron.

**Límite:** los fragmentos PDF siguen `unreviewed`; la matriz de análisis
documenta cotejos visuales parciales, no fidelidad completa. La versión DOF
2021 es histórica frente al transitorio posterior. La relación de identidad
DPM/DA sigue sin resolver. El script depende del contrato v0.3 de Skopos y
de rutas locales;
DOCX, conversaciones, cobertura documental total, vigencia general y escritura
AN-KLA no fueron probados ni activados.
