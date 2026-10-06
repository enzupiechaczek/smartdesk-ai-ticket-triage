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

Group A1 completes this section on Day 4 (task A1-4.2). Until then, follow your task in Azure Boards.

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
- Anaconda or Miniconda (Python 3.8 or newer)

### 1. Get the code

```bash
git clone <repository-url>
cd <repository-folder>
git checkout a1-<githubusername>-day1-foundation
```

### 2. Create and activate the environment (first time only)

Open **Anaconda Prompt** and run, from the repository root:

```bash
conda create -n smartdesk python=3.11 -y
conda activate smartdesk
pip install -r backend/requirements.txt
```

In every new Anaconda Prompt, run `conda activate smartdesk` again before starting the server.

### 3. Start the server

From the repository root:

```bash
python backend/app.py
```

Mac: `python3 backend/app.py`

You should see `Running on http://127.0.0.1:5000`. Leave this window open.

### 4. Check it works

Open http://127.0.0.1:5000/api/health in a browser. You should see:

```json
{ "service": "SmartDesk local API", "status": "ok" }
```

Stop the server with `Ctrl+C`.

### Without Anaconda (alternative)

```bash
python -m venv .venv
.venv\Scripts\activate        # Mac: source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/app.py
```
