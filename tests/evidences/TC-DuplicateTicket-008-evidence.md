Tested commit: 757cda875c1df13133ea66569f0bda9fd0d33187
Tested at: 2026-10-10T18:03:22+04:00
Server: python backend/app.py on http://127.0.0.1:5000

## Submission 1

Request:
```http
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Unable to access my account","description":"I cannot log into my account using my correct credentials."}
```

Response status: **201**

```json
{
    "category":  "access",
    "confidence":  0.785,
    "created_at":  "2026-10-10T14:03:24.937538+00:00",
    "description":  "I cannot log into my account using my correct credentials.",
    "id":  13,
    "priority":  "normal",
    "subject":  "Unable to access my account"
}
```

## Submission 2

Request:
```http
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Unable to access my account","description":"I cannot log into my account using my correct credentials."}
```

Response status: **201**

```json
{
    "category":  "access",
    "confidence":  0.785,
    "created_at":  "2026-10-10T14:03:25.086009+00:00",
    "description":  "I cannot log into my account using my correct credentials.",
    "id":  14,
    "priority":  "normal",
    "subject":  "Unable to access my account"
}
```

## Readback through GET /api/tickets

Full response is long, so only the two tickets under test are listed. The rest of the dashboard is unchanged.

```json
[
    {
        "category":  "access",
        "confidence":  0.785,
        "created_at":  "2026-10-10T14:03:25.086009+00:00",
        "description":  "I cannot log into my account using my correct credentials.",
        "id":  14,
        "priority":  "normal",
        "subject":  "Unable to access my account"
    },
    {
        "category":  "access",
        "confidence":  0.785,
        "created_at":  "2026-10-10T14:03:24.937538+00:00",
        "description":  "I cannot log into my account using my correct credentials.",
        "id":  13,
        "priority":  "normal",
        "subject":  "Unable to access my account"
    }
]
```

## Checks

- Both submissions returned status 201
- Submission 1 id: 13
- Submission 2 id: 14
- Ids differ: True
- Subject identical in both: True
- Description identical in both: True
- Subject value: 'Unable to access my account'
- Description value: 'I cannot log into my account using my correct credentials.'
- Both tickets are stored, neither overwrote the other: True

## Dashboard

See TC-DuplicateTicket-008.png for the two cards on the dashboard. The dashboard does not print ids, which is why this file records them.
