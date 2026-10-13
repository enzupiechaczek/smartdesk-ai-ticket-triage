# SmartDesk API Test Evidence

- Test session started: 2026-10-12T07:18:17.008+02:00
- Git commit: 005f1b57e6110d0f45c1c0bb14bfdabf4eb92a5f
- Dataset SHA-256: 525AC01B9A55B86BB69D77B17128D5529535D1844F9018CF8DCE1DB4C2F896A1
- Dataset baseline: 36 rows, subject to confirmation against the CSV

## Login ticket

Request timestamp: 2026-10-12T07:18:17.978+02:00

Exact request JSON:
```json
{"description":"I reset my password, but I still cannot access my account.","subject":"Cannot log in after password reset"}
```

PowerShell submission:
```powershell
$body = @'
{"description":"I reset my password, but I still cannot access my account.","subject":"Cannot log in after password reset"}
'@
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/tickets" -Method Post -ContentType "application/json" -Body $body
```

HTTP status: 201

Full response body:
```json
{
  "category": "access",
  "confidence": 0.893,
  "created_at": "2026-10-12T05:18:46.305221+00:00",
  "description": "I reset my password, but I still cannot access my account.",
  "id": 11,
  "priority": "urgent",
  "subject": "Cannot log in after password reset"
}

```

## Export ticket

Request timestamp: 2026-10-12T07:18:47.264+02:00

Exact request JSON:
```json
{"description":"The export script stops responding after I click Export and never finishes.","subject":"Data export hangs"}
```

PowerShell submission:
```powershell
$body = @'
{"description":"The export script stops responding after I click Export and never finishes.","subject":"Data export hangs"}
'@
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/tickets" -Method Post -ContentType "application/json" -Body $body
```

HTTP status: 201

Full response body:
```json
{
  "category": "technical",
  "confidence": 0.69,
  "created_at": "2026-10-12T05:18:47.270982+00:00",
  "description": "The export script stops responding after I click Export and never finishes.",
  "id": 12,
  "priority": "normal",
  "subject": "Data export hangs"
}

```
