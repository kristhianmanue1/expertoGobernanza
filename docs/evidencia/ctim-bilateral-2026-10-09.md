# CTIM: prueba bilateral local de cinco fuentes

**Observado:** 2026-10-09 UTC. Ejecutor: `python3 -m scripts.ctim_source_bilateral`
desde expertoGobernanza. Recibo completo: `ctim-bilateral-receipt-2026-10-09.json`.
Skopos se ejecutó desde `codex/skopos-source-profile-v03` commits `44bd4d2`,
`3ce0e3a` y `7847228` (tres ejecuciones, recibo idéntico; PR #5 en
borrador); Ágora desde `main` con PR #4 fusionado.

Skopos recuperó los cinco originales con SHA esperado tras reinicio y rechazó
cinco SHA falsos (`material_not_allowed`). Consultó DA p282, procedimiento
CTIM p6 y POBALINES 2022 p75. Los dos HTML se cotejaron por offset y hash
contra los originales; Ágora verificó los cinco SHA originales y produjo dos
relaciones candidatas sin admisión ni llamadas a proveedor. Rechazó página
PDF 0 y rango HTML invertido. El controlador terminó detenido; el puerto
`127.0.0.1:37034` se comprobó cerrado tras la ejecución.

**Límite:** los fragmentos PDF siguen `unreviewed`; la matriz de análisis
documenta cotejos visuales parciales, no fidelidad completa. La versión DOF
2021 es histórica frente al transitorio posterior. La relación de identidad
DPM/DA sigue sin resolver. El script depende del PR #5 y de rutas locales;
DOCX, conversaciones, cobertura documental total, vigencia general y escritura
AN-KLA no fueron probados ni activados.
