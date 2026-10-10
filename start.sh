#!/usr/bin/env bash
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

if [[ ! -d ".venv" ]]; then
	echo "Creating .venv"
	python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r backend/requirements.txt
python ai/train.py
python backend/app.py
