#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
PYTHON_BIN="${PYTHON:-python3}"
"$PYTHON_BIN" verifiers/verify_m5_restoration_stdlib.py
"$PYTHON_BIN" verifiers/verify_m5_restoration_sympy.py
"$PYTHON_BIN" src/derive_parametric_family.py
"$PYTHON_BIN" counterexamples/verify_n5_lower_counterexample.py
