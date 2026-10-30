#!/usr/bin/env bash
# YAP-IS — Single-process launcher (Linux/macOS)
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"

# Try python3, then python.
if command -v python3 >/dev/null 2>&1; then PYCMD=python3
elif command -v python  >/dev/null 2>&1; then PYCMD=python
else
  echo "ERROR: Python was not found. https://python.org/downloads"
  exit 1
fi

echo "[1/2] Installing dependencies..."
$PYCMD -m pip install -q -r requirements.txt

echo "[2/2] Starting YAP-IS: http://127.0.0.1:8000/"
exec $PYCMD main.py
