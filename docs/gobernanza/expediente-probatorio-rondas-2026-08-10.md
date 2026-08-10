# Expediente probatorio — rondas adversariales de gobernanza — 2026-08-10

**ID:** `EG-GOV-PROB-2026-08-10-01`  
**Proyecto:** ExpertoGobernanza · **Fase:** R1 · **Estado:** propuesta para Git  
**Autor material:** OpenAI/Codex (GPT-5) · **Autoridad de adopción:** humana  
**Objeto:** arquitectura/posicionamiento, no-herencia de vigencia y `EvidenceEdge v0`

## 1. Propósito y alcance

Este expediente reúne evidencia reproducible de cómo el proyecto aplicó su
política de gobernanza adversarial a dos hitos de alto impacto:

1. evaluación de arquitectura y posicionamiento frente al mercado legal-tech;
2. diseño e implementación del contrato `EvidenceEdge v0` y de la regla que
   prohíbe heredar vigencia instrumento→disposición→relación.

El documento reúne evidencia de la existencia, secuencia y resultado técnico de
las rondas dentro del repositorio. **No es acta notarial, firma digital, sello de tiempo de
tercero ni certificación jurídica.** Hasta que un administrador cree el commit,
los hashes de §7 identifican el estado local propuesto, todavía mutable.

## 2. Proposiciones respaldadas

| ID | Proposición | Evidencia principal | Fuerza |
|---|---|---|---|
| P1 | La ronda de arquitectura usó tres proveedores/modelos válidos y excluyó al autor | `arquitectura-mercado-round/RONDA.md` + reviews | A |
| P2 | Google produjo una salida inválida; el intento de recuperación también fue descartado por decisión humana | `RONDA.md` + review inválida preservada | A |
| P3 | La decisión agregada inicial fue `fix-and-retry`, no adopción | `arquitectura-mercado-round/RECONCILIACION.md` | A |
| P4 | Tres revisores coincidieron en el riesgo de herencia y falta de alcance probatorio | tres reviews externas + reconciliación | A |
| P5 | La no-herencia quedó materializada en código y datos, no sólo en prosa | `registry_rules.py`, `registry.yaml`, tests | C |
| P6 | `EvidenceEdge v0` falla cerrado y separa texto de interpretación | `evidence_edge.py` + tests | C |
| P7 | Los hallazgos HIGH/MED se corrigieron mediante retries | round `EvidenceEdge` + reconciliación | B |
| P8 | El gate final obtuvo `proceed` de Anthropic, Moonshot y Zhipu/GLM | `evidence-edge-v0-round/RONDA.md` | B |
| P9 | La suite local final pasó 107 pruebas | comando reproducible de §6 | C |
| P10 | Akoma Ntoso no quedó autorizado por estas rondas | ambas reconciliaciones | A |

### Escala de fuerza

- **A — evidencia contemporánea directa:** entrada común, revisión externa
  preservada verbatim, decisión o reconciliación escrita durante la ronda.
- **B — evidencia contemporánea resumida:** metadata, decisiones y fixes
  preservados, pero sin transcripción verbatim completa del proveedor.
- **C — evidencia ejecutable:** código, datos y pruebas que permiten reproducir
  el comportamiento alegado.
- **D — dato operativo no incorporado:** logs locales ignorados por Git; sirven
  para investigación, pero no sostienen por sí solos una proposición de este
  expediente.

## 3. Cadena documental

### 3.1 Ronda de arquitectura y posicionamiento

- Entrada común: [`../propuestas/2026-08-10-arquitectura-mercado-round/INPUT.md`](../propuestas/2026-08-10-arquitectura-mercado-round/INPUT.md).
- Registro del quórum, bundles y decisiones: [`../propuestas/2026-08-10-arquitectura-mercado-round/RONDA.md`](../propuestas/2026-08-10-arquitectura-mercado-round/RONDA.md).
- Reviews verbatim válidas:
  [Anthropic](../propuestas/2026-08-10-arquitectura-mercado-round/reviews/anthropic-claude-sonnet-5.md),
  [Moonshot](../propuestas/2026-08-10-arquitectura-mercado-round/reviews/moonshot-kimi-k3-256k.md) y
  [Zhipu/GLM](../propuestas/2026-08-10-arquitectura-mercado-round/reviews/zhipu-glm-5.2.md).
- Primera salida Google inválida preservada:
  [`google-invalid-context-contamination.md`](../propuestas/2026-08-10-arquitectura-mercado-round/reviews/google-invalid-context-contamination.md).
- Segundo intento de recuperación y descarte humano registrados en
  [`RONDA.md`](../propuestas/2026-08-10-arquitectura-mercado-round/RONDA.md);
  no existe una segunda review válida que forme parte del quórum.
- Agregación y orden de fixes:
  [`RECONCILIACION.md`](../propuestas/2026-08-10-arquitectura-mercado-round/RECONCILIACION.md).

### 3.2 Implementación y ronda EvidenceEdge v0

- Entrada ciega: [`../propuestas/2026-08-10-evidence-edge-v0-round/INPUT.md`](../propuestas/2026-08-10-evidence-edge-v0-round/INPUT.md).
- Declaración de fixes para retry:
  [`RETRY.md`](../propuestas/2026-08-10-evidence-edge-v0-round/RETRY.md) y
  [`FINAL-RETRY.md`](../propuestas/2026-08-10-evidence-edge-v0-round/FINAL-RETRY.md).
- Registro de proveedores y veredictos:
  [`RONDA.md`](../propuestas/2026-08-10-evidence-edge-v0-round/RONDA.md).
- Hallazgos cerrados y fronteras aceptadas:
  [`RECONCILIACION.md`](../propuestas/2026-08-10-evidence-edge-v0-round/RECONCILIACION.md).
- Implementación: [`../../corpus/evidence_edge.py`](../../corpus/evidence_edge.py) y
  [`../../corpus/registry_rules.py`](../../corpus/registry_rules.py).
- Pruebas: [`../../tests/test_evidence_edge.py`](../../tests/test_evidence_edge.py) y
  [`../../tests/test_registry_vigencia.py`](../../tests/test_registry_vigencia.py).

## 4. Correspondencia política → evidencia

| Regla de gobernanza | Forma de cumplimiento observada |
|---|---|
| Plan/entrada común | `INPUT.md` separado de las respuestas |
| Autor excluido del voto | Codex/OpenAI figura como autor/reconciliador, no revisor |
| ≥3 proveedores para alto impacto | Anthropic + Moonshot + Zhipu/GLM |
| Modelo subyacente, no sólo CLI | modelos registrados en cada `RONDA.md` |
| Cualquier BLOCKER bloquea | no hubo BLOCKER final; cada HIGH reabrió retry |
| Hallazgos no se descartan por veredicto | findings de votos `proceed` también se reconciliaron |
| Fidelidad documental primero | cobertura y traza por disposición son obligatorias |
| Fail-closed | entrada inválida, duplicada, incompleta o interpretativa no se recorre |
| Proponer/aplicar | artefactos locales sin commit/push; adopta administrador humano |

## 5. Resultado técnico probado

El contrato resultante impide promover una arista cuando ocurra cualquiera de
estas condiciones: herencia distinta de `prohibited`, evidencia nivel 3/4,
alcance instrumento, objeto no cubierto, fecha incoherente, sujeto distinto de
la disposición fuente o clase interpretativa. El resolver de vigencia también
rechaza tablas duplicadas, coverage escalar, trazas sin fecha/localizador/revisión
y trazas de alcance instrumento usadas para una disposición.

Los estados congelados por las pruebas son:

| Disposición | Resultado |
|---|---|
| `LFEP:1` | verificada |
| `LFEP:5` | no verificada |
| `LSS:5` | verificada |
| `LSS:1` | no verificada |

Esto acredita comportamiento del software y consistencia del corpus; **no
constituye por sí solo una opinión jurídica sobre vigencia o aplicabilidad**.

## 6. Procedimiento de reproducción

Desde la raíz del repositorio:

```bash
python3 -m unittest discover -s tests -q
PYTHONPYCACHEPREFIX=/tmp/experto-gobernanza-pycache \
  python3 -m py_compile corpus/evidence_edge.py corpus/registry_rules.py \
  tests/test_evidence_edge.py tests/test_registry_vigencia.py
python3 scripts/check_sizes.py
ruby -ryaml -e 'doc = YAML.load_file("corpus/registry.yaml"); abort unless doc.fetch("fuentes").size == 6'
git diff --check
```

Resultado observado al cerrar el expediente: **107 pruebas OK**, compilación OK,
YAML con seis fuentes, límites de tamaño OK y diff-check limpio. La CI remota no
se invoca como evidencia de este hito; el DoD reportado es local.

## 7. Manifest SHA-256 del estado propuesto

### 7.1 Arquitectura/mercado

| SHA-256 | Archivo |
|---|---|
| `2fdc232a0cc595728cc690d66880cd16e4f083b38b1c4aaeb882c43f709026f8` | `docs/propuestas/2026-08-10-arquitectura-mercado-round/INPUT.md` |
| `924ef367bb63398e4b00739c14bcc1d6b5c11e4b182d063c7509d0fa06fc8973` | `docs/propuestas/2026-08-10-arquitectura-mercado-round/RONDA.md` |
| `4d16c3b1e6ffd2c77bb59c7891302c9ee80c7a2f0690f973579b901f6b12af9b` | `docs/propuestas/2026-08-10-arquitectura-mercado-round/RECONCILIACION.md` |
| `06876837616d37aa02a353a727b30941467ecfc0087f1f6b9e69519e80c884d3` | `docs/propuestas/2026-08-10-arquitectura-mercado-round/reviews/anthropic-claude-sonnet-5.md` |
| `65c5f90b432853e729dc25d068a2a939053cdb588b14f8aab57f053fef16a250` | `docs/propuestas/2026-08-10-arquitectura-mercado-round/reviews/moonshot-kimi-k3-256k.md` |
| `7fd698181320ec65b45657b15c35f14922173835f5f2f6bbd1b6bc6270ab9a47` | `docs/propuestas/2026-08-10-arquitectura-mercado-round/reviews/zhipu-glm-5.2.md` |
| `3cff034e429185c502c032b8a63490106ba7620560b43fd62c2fac10ea3478ee` | `docs/propuestas/2026-08-10-arquitectura-mercado-round/reviews/google-invalid-context-contamination.md` |

### 7.2 EvidenceEdge y resultado ejecutable

| SHA-256 | Archivo |
|---|---|
| `48eea27320bb31a22c5e33fe7b7659b39b91dfed49c616a2620cb3632cadb82d` | `docs/propuestas/2026-08-10-evidence-edge-v0-round/INPUT.md` |
| `2812318109a3ff28b66e46a2b7eee1173593d715afa2ceb919dfebb6dd1fa8fa` | `docs/propuestas/2026-08-10-evidence-edge-v0-round/RETRY.md` |
| `3aecbf81cf321041ef058a7d01c2bb41e1a2a389dcff6d9abb64031cd299992d` | `docs/propuestas/2026-08-10-evidence-edge-v0-round/FINAL-RETRY.md` |
| `e1d4d1b3d8cb0c132ff9b27563e57adb4c41eb7da57ca57568f55c488d27ed96` | `docs/propuestas/2026-08-10-evidence-edge-v0-round/RONDA.md` |
| `701a7816005cf22521501e76c15a7bfd929de56c376c482c706f6c319ba49636` | `docs/propuestas/2026-08-10-evidence-edge-v0-round/RECONCILIACION.md` |
| `2fe5b075928a8a8b73344254ebbb3bbbe9ecdf6882c8300055b71a7bdd5ce77f` | `corpus/evidence_edge.py` |
| `b15f398d0807f914667a91f84f858a96ddc5b8c179a69acb4abde02ddb790f00` | `corpus/registry_rules.py` |
| `026a2b7f2930c016f353a61bfe5117cf2299c4d0f8158a81630dd1416a9b2b8b` | `tests/test_evidence_edge.py` |
| `1f0b52859f41c1c59fd3b4ac02fd719416c81c1b7fa4a272d9276e6822343104` | `tests/test_registry_vigencia.py` |
| `62071f16d42df89e41468e8300d56052d0c9d8da7a836a84e8c925401d385a91` | `corpus/registry.yaml` |

Los hashes deben recalcularse si cualquiera de esos archivos cambia antes del
commit. El commit futuro será el mecanismo que vincule este expediente, la
relatoría y los artefactos a una revisión Git identificable.

## 8. Limitaciones y reservas

1. Las revisiones de arquitectura sí están preservadas verbatim. En la ronda de
   implementación `EvidenceEdge`, las salidas completas de CLI no se copiaron a
   archivos; se conservan entradas, decisiones, fixes y reconciliación. Por eso
   P8 tiene fuerza B, no A.
2. `validate_evidence_edge` valida estructura y atestación; no abre el archivo
   citado ni recompone su hash. Esa verificación pertenece al gate de citas.
3. Los logs `review-routing.jsonl` son locales e ignorados por Git; este
   expediente no depende de ellos para el quórum final.
4. No se afirma independencia total de entrenamiento entre proveedores; sólo
   decorrelación parcial por familias/modelos.
5. Ninguna ronda promulga normas, sustituye revisión jurídica humana ni autoriza
   el despliegue a usuarios finales.

## 9. Cierre solicitado

Acción del administrador: revisar el diff, recalcular §7 y, si coincide, aplicar
un commit que incluya expediente, relatoría, rondas, código y pruebas. Sólo ese
commit convertirá el snapshot local en evidencia Git inmutable por contenido.
