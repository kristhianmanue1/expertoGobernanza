"""Gateway: ruta sancionada de revisión multi-provider (plan router-harness §2, RH-T05).

Orquesta router → fail-closed → sello → verificación propia. Es la ruta
fácil: un agente que la usa obtiene sellado + verificación gratis.

RH-T05 implementa SÓLO `--dry-run` (determinista, sin red ni CLI externo):
clasifica, sella, verifica su propio sello y lo retorna. La invocación real
(bundle a temp + CLI externo + audit_log.append) es RH-T07 (gated por
proveedor autorizado); pedir `dry_run=False` falla cerrado con motivo
explícito en vez de fingir una invocación.

LÍMITE DECLARADO (F3): el bypass (invocar al proveedor fuera del gateway) NO
es detectable de forma fiable. El control es disciplina operativa: esta es la
única ruta documentada y `audit_log` el único registro sancionado.
"""
import hashlib
import json
import pathlib

from . import router, seal

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _config_digest(config):
    # Mismo algoritmo que router.main: hashes de config compatibles en todo el proyecto.
    return "sha256:" + hashlib.sha256(
        json.dumps(config, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _canonical_config_digest(canonical_config_path=None):
    """Digest de la config canónica (default: review_routing/config.json).

    H-01 (ronda RH-T08): la clasificación ex-ante la hace la CONFIG canónica,
    no una config arbitraria que el agente supervise pueda inyectar por --config.
    `canonical_config_path` sólo lo usan los tests con sandbox propio; la
    superficie CLI nunca lo expone → siempre pinea contra la del repo.
    """
    if canonical_config_path:
        return _config_digest(router.load_config(canonical_config_path))
    return _config_digest(router.load_config())


def run(files, provider, model, config, dry_run=True, allow_partial=False,
         repo_root=None, config_sha256=None, canonical_config_path=None):
    """Ejecuta el pipeline dry-run. Devuelve dict con `ok` y motivo/según caso.

    - config ≠ canónica → ok=False reason=config_no_canonica (H-01, fail-closed).
    - `denied` sin `allow_partial` → ok=False reason=denegado_fail_closed.
    - bundle vacío (nada ruteable) → ok=False reason=bundle_vacio.
    - sella (lectura única vía read_bundle) y verifica su propio sello;
      cualquier fallo de sello/verificación → ok=False fail-closed.
    - `dry_run=False` → ok=False reason=invocacion_real_no_disponible_rh_t07.
    """
    if not dry_run:
        return {"ok": False, "reason": "invocacion_real_no_disponible_rh_t07"}
    # H-01 (ronda RH-T08): pinning de config — sólo se sella bajo la config
    # canónica. Una --config distinta (aunque sea un superconjunto) fail-closed.
    if _config_digest(config) != _canonical_config_digest(canonical_config_path):
        return {"ok": False, "reason": "config_no_canonica"}
    root = pathlib.Path(repo_root) if repo_root else ROOT
    decision = router.route(files, config, repo_root=root)
    result = {
        "denied": decision["denied"],
        "denied_count": len(decision["denied"]),
        "bundle_count": len(decision["bundle"]),
        "bundle_sha256": decision["bundle_sha256"],
        "config_sha256": config_sha256 or _config_digest(config),
        "dry_run": True,
    }
    if decision["denied"] and not allow_partial:
        result.update(ok=False, reason="denegado_fail_closed")
        return result
    if not decision["bundle"]:
        result.update(ok=False, reason="bundle_vacio")
        return result
    try:
        content = seal.read_bundle(decision, repo_root=root)
        s = seal.build_seal(decision, config, provider, model,
                            result["config_sha256"], repo_root=root,
                            bundle_content=content)
    except seal.SealError as exc:
        result.update(ok=False, reason=f"seal_error:{exc}")
        return result
    ok, why = seal.verify_seal(s, content)
    if not ok:
        result.update(ok=False, reason=f"seal_no_verifica:{why}")
        return result
    result.update(ok=True, verify="ok", seal=s)
    return result
