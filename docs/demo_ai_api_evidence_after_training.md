# SmartDesk API Evidence - After Fresh Training

- Session started: 2026-10-12T07:24:30.085+02:00
- Git commit: 005f1b57e6110d0f45c1c0bb14bfdabf4eb92a5f
- Dataset SHA-256: 525AC01B9A55B86BB69D77B17128D5529535D1844F9018CF8DCE1DB4C2F896A1
- Environment: Windows PowerShell 5.1, project virtual environment
- Training command: python ai/train.py
- Test-split accuracy: 0.625 across 8 test tickets
- Five-fold CV mean: 0.632; standard deviation: 0.198
- Endpoint: POST http://127.0.0.1:5000/api/tickets

## Login ticket

- Request timestamp: 2026-10-12T07:24:30.461+02:00
- Exact request JSON:
```json
{"description":"I reset my password, but I still cannot access my account.","subject":"Cannot log in after password reset"}
```

- HTTP status: 201
- Full response body:
```json
{
  "category": "access",
  "confidence": 0.893,
  "created_at": "2026-10-12T05:24:31.823807+00:00",
  "description": "I reset my password, but I still cannot access my account.",
  "id": 13,
  "priority": "urgent",
  "subject": "Cannot log in after password reset"
}

```

## Export ticket

- Request timestamp: 2026-10-12T07:24:31.936+02:00
- Exact request JSON:
```json
{"description":"The export script stops responding after I click Export and never finishes.","subject":"Data export hangs"}
```

- HTTP status: 201
- Full response body:
```json
{
  "category": "technical",
  "confidence": 0.69,
  "created_at": "2026-10-12T05:24:31.950416+00:00",
  "description": "The export script stops responding after I click Export and never finishes.",
  "id": 14,
  "priority": "normal",
  "subject": "Data export hangs"
}

```
