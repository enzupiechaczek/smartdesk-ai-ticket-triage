# Health-check evidence

Date: 12 October 2026, local time (UTC+07:00)

This check used a separate disposable worktree. The working checkout's model
and database were not used or changed.

## Baseline

- Disposable checkout: `C:\Users\LOQ\Desktop\smartdesk-health-check-disposable`
- `git rev-parse HEAD`: `cd03b15ee91b71c2a44ad678b3db5e705f2e8379`
- Initial `git status --short --branch`: `## HEAD (no branch)`
- Initial artifacts: `ai\model.joblib` absent; `backend\smartdesk.db` absent
- OS: Microsoft Windows 11 Home, version `10.0.26200`, build `26200`,
  64-bit
- Python executable: `C:\Users\LOQ\AppData\Local\Programs\Python\Python314\python.exe`
- Python version: `Python 3.14.8`

## Run 1: no model

The server was started from the disposable checkout with:

```powershell
python backend/app.py
```

From a separate terminal, the health check command was:

```powershell
curl.exe -i http://127.0.0.1:5000/api/health
```

Actual result:

```text
HTTP/1.1 503 SERVICE UNAVAILABLE
Server: Werkzeug/3.1.9 Python/3.14.8
Content-Type: application/json

{
  "message": "Model not trained. Run python ai/train.py",
  "status": "error"
}
```

The server was then stopped. A separate connection check returned curl exit
code `7` (`Could not connect to server`).

## Training

With the server stopped, the local training command was:

```powershell
python ai/train.py
```

Actual result: exit code `0`; `Accuracy: 0.625`; cross-validation mean
accuracy `0.632 (+/- 0.198)`; `Saved model.joblib`.

Training created only the disposable checkout's `ai\model.joblib`. The
disposable server had already created its own `backend\smartdesk.db`; neither
artifact belonged to the working checkout.

## Run 2: after training

The server was restarted with the same command:

```powershell
python backend/app.py
```

From a separate terminal, the same health check command returned:

```text
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Content-Type: application/json

{
  "service": "SmartDesk local API",
  "status": "ok"
}
```

The server was stopped after the capture. The server logs recorded
`GET /api/health` as HTTP 503 at `22:52:28` for Run 1 and HTTP 200 at
`22:52:52` for Run 2.
