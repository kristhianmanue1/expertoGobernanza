#!/usr/bin/env python3
"""CLI route_review — ruta sancionada de revisión (plan router-harness, RH-T05).

Modo T05: `--dry-run` (determinista, sin red ni CLI externo). La invocación
real del proveedor es RH-T07 (gated). Exit codes: 0 ok; 1 denied/vacío/error.
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from review_routing import gateway, router


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Gateway de revisión §7.4 (RH-T05: sólo --dry-run).")
    ap.add_argument("--files", nargs="+", required=True,
                    help="paths relativos a la raíz del repo")
    ap.add_argument("--provider", required=True, help="proveedor destino")
    ap.add_argument("--model", required=True, help="modelo subyacente")
    ap.add_argument("--config", default=str(router.DEFAULT_CONFIG))
    ap.add_argument("--allow-partial", action="store_true",
                    help="no fallar cerrado ante denegados (sólo diagnóstico)")
    ap.add_argument("--dry-run", action="store_true",
                    help="clasifica + sella + verifica + imprime; no invoca ni loguea")
    args = ap.parse_args(argv)
    config = router.load_config(args.config)
    result = gateway.run(args.files, args.provider, args.model, config,
                         dry_run=args.dry_run, allow_partial=args.allow_partial)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
