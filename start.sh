#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

if [[ ! -d ".venv" ]]; then
	python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install -r backend/requirements.txt
python ai/train.py
python backend/app.py
