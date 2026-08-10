#!/usr/bin/env bash
set -euo pipefail

if [[ -x .venv/bin/python ]]; then
  EG_GATE_PY=.venv/bin/python
else
  EG_GATE_PY=python3
fi

"$EG_GATE_PY" -m py_compile corpus/*.py scripts/*.py review_routing/*.py
"$EG_GATE_PY" -m unittest discover -s tests
"$EG_GATE_PY" scripts/benchmark_imss_edges.py
"$EG_GATE_PY" scripts/check_sizes.py
git diff --check
