# Resultados R3 — F5 LFEP:5, LOAPF:1:P3 y gate permanente

**ID:** `R1-BENCH-IMSS-EE-01-R3` · **Fecha:** 2026-08-10  
**Estado técnico:** OK · **Adversarial:** 3/3 `proceed`, sin BLOCKER

## Integridad del prerregistro y entradas

El prerregistro fue creado antes de cambiar corpus y fixtures. Su SHA-256
observado después de la ejecución permanece:
`5a52b8bc11ee53e2306c72af9b413e87acf614f9ca0146b2567d3d13caeb0b7b`.

| Artefacto | SHA-256 R3 |
|---|---|
| `imss_evidence_edge_cases.json` | `e3fd54521992f868c42295a91dba816f4ff3189ea356bb69001cacf4ecac6617` |
| `imss_evidence_edges.json` | `73957208bf77e59ba576465dc66d8d90505071a755330cd0c86757e57df41d8f` |
| `benchmark_imss_edges.py` | `581985e22cdc2975b7b8a5f19d7987e2692110f7057aa1442f2184990ab8228e` |
| `ci_check.sh` | `1267d4956158d7fc086b91a92e1260cf8e66b00360094ec2a5e86702a6a7b965` |
| `registry.yaml` | `c7c00911cec9697cb46d62696851da773ede50917ae4555c0cebf5f446f5b443` |
| `LFEP-005.json` | `cae3831392000ec83ef89e6d6c20eed7ec03c6c9011ddc45362e06028cbca2a9` |
| `LOAPF-001.json` | `5dd682f52d579cd35231bcdeb1d7f9d6572f775a5acb1b67d69847a61b1f2014` |
| `LOAPF-001-P3.json` | `10a897340c0d8aac3ccbef9985883b591e82f8464c7c81e1b526435b4df94d1d` |

## Resultado falsable

| Métrica prerregistrada | Esperado | Observado |
|---|---:|---:|
| Casos aprobados | 5/5 | 5/5 |
| Respondibles | 3 | 3 |
| Bloqueados | 2 | 2 |
| Negativos rechazados | 5/5 | 5/5 |
| Falsos positivos | 0 | 0 |
| Falsos negativos | 0 | 0 |

`LFEP:5` ya supera F5 contra el decreto DOF del 16-07-2025. Q4 permanece
bloqueada porque el artículo dice “sus leyes específicas” y no identifica
textualmente a la LSS. Q2 ahora recorre exclusivamente
`LOAPF:1:P3|ubica_clase|administracion_publica_paraestatal`.

## Ejecución del gate

La primera invocación del nuevo wrapper usó el Python del sistema y falló al
intentar escribir caché fuera del workspace. Se corrigió el wrapper para elegir
`.venv/bin/python` cuando existe; no se relajó ningún criterio.

Resumen reproducible —no transcripción literal del JSON emitido—:

```text
./scripts/ci_check.sh
124 tests OK
benchmark passed=true; 5/5; 3 answerable; 2 blocked; 5 negativos rechazados
check_sizes: 66 archivos dentro de límites
git diff --check: OK
```

El workflow remoto ejecuta el benchmark con `--allow-missing-originals` porque
los PDF no se versionan. El gate local exige los originales y verifica sus
hashes; esta diferencia está declarada en `docs/ops-github.md`.

Durante la primera pasada adversarial se corrigieron espacios finales, se
endurecieron a igualdad exacta las cuotas 3/2/5 y se negó explícitamente a Q5
la cobertura de objeto y relación. Los hashes de la tabla corresponden al retry.
Tras el retry Moonshot se amplió, sin cambio semántico, la descripción de
cobertura del decreto para mencionar la adición del párrafo tercero; el hash
`LFEP-005.json` de la tabla es el posterior a esa mejora LOW.
