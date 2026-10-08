#!/bin/env bash
if [[ ! -d "backend/.venv" ]]; then
	echo "Initiating .venv for backend"
	python3 -m venv backend/.venv
	exit 0
fi
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
python ai/train.py
python backend/app.py
