# AGENTS.md

## What this is

Local AI ticket-triage app for interns: Flask + SQLite backend, scikit-learn classifier, plain HTML/CSS/JS frontend. Most files are still placeholders; categories are `access | billing | technical`. Python 3.11+ (local venv may be newer).

## Architecture / contract

Flow: browser form -> Flask API -> `predict_category(text)` -> priority rule -> SQLite -> dashboard (urgent first).

- **Source of truth for API and model shape: `docs/architecture.md`** (`POST/GET /api/tickets`, `GET /api/health`, `predict_category(text) -> {category, confidence 0..1}`).
- Priority rule (urgent/normal) is owned by A1/backend; not implemented yet.

## Commands

Create env:

```
python -m venv backend/.venv
backend/.venv/bin/pip install -r backend/requirements.txt
```

Run backend: `backend/.venv/bin/python backend/app.py` (debug mode, `GET /api/health` is the only endpoint that works today).

Frontend: open `frontend/index.html` or serve `frontend/` statically — Flask does not serve it yet.

- Deps live only in `backend/requirements.txt`.
- **No lint / typecheck / test command exists yet.** Do not invent one. `tests/` holds QA docs (test plan, bug template, held-out CSV) — not a runnable suite.

## Directory ownership (groups)

- A1: `frontend/`, `backend/` (incl. `database.py`, priority rule) — entrypoints `backend/app.py`, `frontend/index.html` + `app.js`
- A2: `ai/` (dataset, training, `predictor.py`, model card)
- B: `tests/` (test plan, bugs, release report)
- `docs/` shared by all

## Git workflow (see CONTRIBUTING.md)

- **Never push to `main`.** Branch name pattern: `{group}-{username}-{day}-{area}` (e.g. `a1-HassanAhmadAli-day1-frontend`).
- Sync with `main` before every push: `git checkout main && git pull`, back to branch, `git merge main`.
- PR into `main`, fill in `.github/pull_request_template.md`; Enzu reviews (CODEOWNERS, sole merger). Branches are one task; ask Enzu for a new one after merge.
- Groups share one branch per task — `git pull origin BRANCH` before starting and before pushing.

## Hard constraints

- Synthetic data only; no real names/emails/customer data.
- No secrets/keys/tokens in code or screenshots.
- Model runs offline — never call paid or cloud AI services.
- `.gitignore` excludes `*.db*`, `model.joblib`, `.venv/`, `__pycache__/` — these are local artifacts, regenerate, never commit.

## Other sources of truth

- `CONTRIBUTING.md` — branching/PR rules.
- `.github/pull_request_template.md` — PR checklist (synced with main, no secrets, ran the code).
- README run section is intentionally unfinished; trust `docs/architecture.md` over prose.
