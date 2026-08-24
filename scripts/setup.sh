#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
echo "Run: .venv/bin/uvicorn server.main:app --host 127.0.0.1 --port 8780"
