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
```

### 2. Create the virtual environment (first time only)

Run from the repository root.

**Windows (PowerShell)**

```powershell
python -m venv .\backend\venv
. .\backend\.venv\Scripts\Activate.ps1
pip install -r .\backend\requirements.txt
```

**Mac / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Your prompt should now start with `(.venv)`. In every new terminal, activate the environment again before starting the server.

### 3. Start SmartDesk

Flask serves both the API and the web page, so you only need **one terminal**. From the repository root, with the virtual environment active (see step 2), run:

**Windows:** `python backend/app.py`
**Mac / Linux:** `python3 backend/app.py`

You should see `Running on http://127.0.0.1:5000`. Leave this terminal open while you use the app.

Then open **http://127.0.0.1:5000** in a browser. You should see the ticket form and the ticket dashboard.

### 4. Check it works

Open http://127.0.0.1:5000/api/health in a browser. You should see:

```json
{ "service": "SmartDesk local API", "status": "ok" }
```

To stop the server, press `Ctrl+C` in the terminal.

### 5. Run the tests

With the virtual environment active, from the repository root:

```bash
python -m unittest discover -s backend -p "test_*.py" -v
```

This runs the API validation tests in [backend/test_api.py](backend/test_api.py) and the priority rule tests in [backend/test_priority.py](backend/test_priority.py). The priority rule itself is documented in [docs/priority.md](docs/priority.md).

## API routes

| Method | Route          | What it does                                                |
| ------ | -------------- | ----------------------------------------------------------- |
| GET    | `/`            | Serves the SmartDesk web page                               |
| GET    | `/api/health`  | Checks that the server is running                           |
| GET    | `/api/tickets` | Returns every saved ticket, urgent first, then newest first |
| POST   | `/api/tickets` | Validates a new ticket, classifies it, saves it             |

> **Note:** The `category` and `confidence` values in the examples below are illustrative. They show the intended output of the trained model. Until that model replaces the temporary stub in [ai/predictor.py](ai/predictor.py), every ticket is returned as `"category": "technical"` with `"confidence": 0.5`.

### `GET /api/health`

A quick check that the Flask server is up.

**Response `200 OK`**

```json
{ "status": "ok", "service": "SmartDesk local API" }
```

### `GET /api/tickets`

Returns all tickets stored in SQLite as a list, with `urgent` tickets first and the newest tickets first within each priority. Returns an empty list `[]` if there are no tickets yet.

**Response `200 OK`** (illustrative values, see the note above)

```json
[
  {
    "id": 2,
    "subject": "Cannot log in",
    "description": "My password reset link has expired.",
    "category": "access",
    "confidence": 0.91,
    "priority": "normal",
    "created_at": "2026-10-07T07:15:42.120000+00:00"
  }
]
```

### `POST /api/tickets`

Creates a new ticket.

**Request body**

```json
{
  "subject": "Cannot log in",
  "description": "My password reset link has expired."
}
```

| Field         | Type   | Rules                         |
| ------------- | ------ | ----------------------------- |
| `subject`     | string | Required, 1–100 characters    |
| `description` | string | Required, 1–500 characters    |

**Response `201 Created`** (illustrative values, see the note above)

```json
{
  "id": 3,
  "subject": "Cannot log in",
  "description": "My password reset link has expired.",
  "category": "access",
  "confidence": 0.91,
  "priority": "normal",
  "created_at": "2026-10-07T07:20:05.481000+00:00"
}
```

**Response `400 Bad Request`**: returned when the body is not a JSON object, or when a field is missing, not a string, empty, or too long. Arrays, `null`, numbers and other non-object bodies are rejected. The `error` message is one of:

```json
{ "error": "Request body must be a JSON object" }
```

```json
{ "error": "Subject must be a string" }
```

```json
{ "error": "Description must be a string" }
```

```json
{ "error": "Subject is required (max 100 characters)" }
```

```json
{ "error": "Description is required (max 500 characters)" }
```

### Ticket fields

| Field         | Type    | Meaning                                                      |
| ------------- | ------- | ------------------------------------------------------------ |
| `id`          | integer | Unique ticket number, set by the database                    |
| `subject`     | string  | Short title written by the user                              |
| `description` | string  | Details of the problem                                       |
| `category`    | string  | Predicted by the model: `access`, `billing` or `technical`   |
| `confidence`  | number  | How sure the model is, from 0 to 1                           |
| `priority`    | string  | `urgent` or `normal`                                         |
| `created_at`  | string  | When the ticket was created (ISO 8601, UTC)                  |

## Troubleshooting

- **PowerShell blocks the activate script:** run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use `.venv\Scripts\activate.bat` in cmd.
- **`No module named 'flask'`:** the environment isn't active. Activate it and run `pip install -r backend/requirements.txt` again.
- **Python version is older than 3.11:** install a newer Python, then create the environment with `py -3.11 -m venv .venv` (Windows) or `python3.11 -m venv .venv` (Mac).
- **Port 5000 already in use:** stop the other program, or stop the old server with `Ctrl+C`.
