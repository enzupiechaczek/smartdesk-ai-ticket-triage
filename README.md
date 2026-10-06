# SmartDesk

A local AI-powered support-ticket triage application, built by the EARTech Information Technology interns.

A user submits a support ticket (subject and description). A Python Flask server checks it, a locally trained machine learning model predicts the category (access, billing or technical) with a confidence score, a documented rule sets the priority (urgent or normal), and the ticket is saved in SQLite. The web page shows tickets as cards with urgent tickets first.

## Tech stack

Python 3.11 or newer, Flask, SQLite, scikit-learn (TF-IDF and Logistic Regression), HTML, CSS, JavaScript, Git and GitHub.

## Project structure

```
frontend/   Web page (HTML, CSS, JavaScript)          Group A1
backend/    Flask server, database, priority rule     Group A1
ai/         Dataset, training, predictor              Group A2
tests/      Test plan, held-out data, bug template    Group B
docs/       Architecture, model card, reports         All groups
```

## How to run SmartDesk

Please set up a [venv](https://www.w3schools.com/python/python_virtualenv.asp) and source it according to your shell.
to launch the frontend:
```python
python -m http.server 8000 -d frontend
```

to launch the backend:
```python
python backend/app.py
```

## How we work

Read [CONTRIBUTING.md](CONTRIBUTING.md) before you push anything. The short version:

1. Never push to `main`.
2. Work on your task branch.
3. Sync with `main` before you push.
4. Open a pull request. Enzu reviews and merges.

## Rules

- Synthetic data only. No real names, emails or customer data.
- No keys, tokens or passwords in code, screenshots or chat.
- The model works offline and never calls a paid or cloud AI service.

## How to run SmartDesk

### Requirements

- Git
- Python 3.11 or newer ([python.org](https://www.python.org/downloads/))
- On Windows, tick **"Add python.exe to PATH"** during the Python installer

### 1. Get the code

```bash
git clone <repository-url>
cd <repository-folder>
git checkout a1-day1-foundation
```

### 2. Create the virtual environment (first time only)

Run from the repository root.

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

**Mac / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Your prompt should now start with `(.venv)`. In every new terminal, activate the environment again before starting the server.

### 3. Start the server

From the repository root:

**Windows:** `python backend/app.py`
**Mac / Linux:** `python3 backend/app.py`

You should see `Running on http://127.0.0.1:5000`. Leave the terminal open.

### 4. Check it works

Open http://127.0.0.1:5000/api/health in a browser. You should see:

```json
{ "service": "SmartDesk local API", "status": "ok" }
```

Stop the server with `Ctrl+C`.

### Troubleshooting

- **PowerShell blocks the activate script:** run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use `.venv\Scripts\activate.bat` in cmd.
- **`No module named 'flask'`:** the environment isn't active. Activate it and run `pip install -r backend/requirements.txt` again.
- **Python version is older than 3.11:** install a newer Python, then create the environment with `py -3.11 -m venv .venv` (Windows) or `python3.11 -m venv .venv` (Mac).
- **Port 5000 already in use:** stop the other program, or stop the old server with `Ctrl+C`.
