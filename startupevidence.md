# Startup Evidence

Tested commit: 3030606b93ff7fac7cc4b901b53f03a37461d5b4
Date: 12/10/2026 (DD/MM/YYYY)
Checkout: disposable clone (`smartdesk-test`); no prior .venv, model or database

## Session covered by this file

One manual session at commit 3030606 (everything below), run by hand on
Windows 11 and on Ubuntu 24.04 under WSL. It exercised the startup path as it
was at that commit: `start.sh` (environment creation and reuse, requirements
install, model training, launch from another directory), the manual Windows
startup commands, and the `/api/health` response.

No automated runs are recorded. Changes made after 3030606 are not covered by
this session.

## Environments

| Environment            | OS                                     | Python                            | Shell      |
| ---------------------- | -------------------------------------- | --------------------------------- | ---------- |
| Windows manual startup | Windows 11 (build number not recorded) | 3.14.8                            | PowerShell |
| Bash runs A-C          | Ubuntu 24.04 under WSL on Windows 11   | 3.12 (patch version not recorded) | Bash       |

The Linux Python version comes from the tester's note, not from captured
command output.

## Bash (WSL, Ubuntu 24.04, Python 3.12)

**Run A: first launch, no environment/model**

- Command: `./start.sh`
- Outcome: `.venv` created, `backend/requirements.txt` installed, model
  trained (`ai/model.joblib` created), server started on
  http://127.0.0.1:5000.
- GET /api/health: HTTP 200, body `{"service": "SmartDesk local API", "status": "ok"}`

**Run B: second launch, environment present**

- Command: `./start.sh`
- Outcome: existing `.venv` reused (not recreated), requirements installed,
  model retrained, server started on http://127.0.0.1:5000.
- GET /api/health: HTTP 200, body `{"service": "SmartDesk local API", "status": "ok"}`

**Run C: invoked from outside the repo**

- Command: `cd /tmp && bash /mnt/c/Users/LOQ/Desktop/EarTechInternShip/smartdesk-test/start.sh`
- Outcome: script changed into the repository folder itself and started the
  server normally.

## Windows manual startup (PowerShell, Windows 11, Python 3.14.8)

Windows build number was not recorded. `start.sh` was not run here; these are
the manual commands.

**First-time setup**

- Commands: `python -m venv .venv`, `. .\.venv\Scripts\Activate.ps1`,
  `pip install -r .\backend\requirements.txt`, `python ai/train.py`,
  `python backend/app.py`
- Outcome: environment created, requirements installed, model trained,
  server started on http://127.0.0.1:5000.

**New terminal, environment present**

- Commands: `. .\.venv\Scripts\Activate.ps1`, `python backend/app.py`
- Outcome: environment activated (prompt shows `(.venv)`), server started.
- GET /api/health: HTTP 200, body `{"service": "SmartDesk local API", "status": "ok"}`
  (Mon, 12 Oct 2026 14:03:03 GMT, Werkzeug/3.1.9)

## Not tested

- **macOS**: untested. No result here is evidence for macOS, and the Linux
  (WSL) runs are not treated as equivalent to it.
- **Native Linux (non-WSL)**: untested. The Bash runs were on WSL only, from a
  checkout on the Windows filesystem (`/mnt/c/...`).
- **`start.sh` on native Windows**: not run; Windows used the manual commands.
