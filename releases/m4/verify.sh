#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
PYTHON_BIN="${PYTHON:-python3}"
"$PYTHON_BIN" verifiers/verify_all_n_stdlib.py
"$PYTHON_BIN" verifiers/verify_all_n_sympy.py
"$PYTHON_BIN" src/derive_parametric_family.py
