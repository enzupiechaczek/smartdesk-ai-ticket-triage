#!/usr/bin/env bash
# Bash launcher for SmartDesk: creates .venv if missing, installs requirements,

# trains the model and starts the server. Needs bash and Python 3.
# This is not a PowerShell script; Windows PowerShell users follow README step 3.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

if [[ ! -d ".venv" ]]; then
	# On Windows, python3 may be the Microsoft Store stub, so fall back to python
	PYTHON=python3
	if ! python3 -c "" >/dev/null 2>&1; then
		PYTHON=python
	fi
	"$PYTHON" -m venv .venv
fi

# Linux and macOS venvs use bin/, Windows venvs (Git Bash) use Scripts/
if [[ -f ".venv/bin/activate" ]]; then
	source .venv/bin/activate
else
	source .venv/Scripts/activate
fi
python -m pip install -r backend/requirements.txt
python ai/train.py
python backend/app.py
