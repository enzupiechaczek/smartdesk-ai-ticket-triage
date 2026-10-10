# Current-model API evidence

- Tested commit: 04dcb2ce188cce5fc027d871ac86de1b231208f1
- Date run: 2026-10-11
- Run at: 2026-10-11T01:02:39+04:00
- Command: the app was started with `python backend/app.py` after `python ai/train.py`, then each body below was sent to POST /api/tickets
- Base URL: http://127.0.0.1:5000

Every response below is the full body returned by the API, not an excerpt.

## TC-ValidAccess-001

Request body:

```json
{"subject":"Unable to access my account","description":"I cannot log into my account"}
```

HTTP status: **201**

Full response:

```json
{
  "category": "access",
  "confidence": 0.768,
  "created_at": "2026-10-10T21:02:39.140407+00:00",
  "description": "I cannot log into my account",
  "id": 22,
  "priority": "normal",
  "subject": "Unable to access my account"
}
```


## TC-ValidBilling-002

Request body:

```json
{"subject":"Billing inquiry regarding invoice #12345","description":"I would like to request an itemized breakdown for my latest invoice."}
```

HTTP status: **201**

Full response:

```json
{
  "category": "billing",
  "confidence": 0.642,
  "created_at": "2026-10-10T21:02:39.156060+00:00",
  "description": "I would like to request an itemized breakdown for my latest invoice.",
  "id": 23,
  "priority": "normal",
  "subject": "Billing inquiry regarding invoice #12345"
}
```


## TC-ValidTechnical-003

Request body:

```json
{"subject":"PDF upload failed","description":"The app freezes when I upload a PDF"}
```

HTTP status: **201**

Full response:

```json
{
  "category": "technical",
  "confidence": 0.661,
  "created_at": "2026-10-10T21:02:39.169160+00:00",
  "description": "The app freezes when I upload a PDF",
  "id": 24,
  "priority": "normal",
  "subject": "PDF upload failed"
}
```


## TC-BlankSubject-004

Request body:

```json
{"subject":"","description":"Need help with my account settings"}
```

HTTP status: **400**

Full response:

```json
{
  "error": "Subject is required (max 100 characters)"
}
```


## TC-BlankDescription-005

Request body:

```json
{"subject":"Need help with my account settings","description":""}
```

HTTP status: **400**

Full response:

```json
{
  "error": "Description is required (max 500 characters)"
}
```


## TC-101CharacterSubject-006

Request body:

```json
{"subject":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx","description":"I need help logging in"}
```

HTTP status: **400**

Full response:

```json
{
  "error": "Subject is required (max 100 characters)"
}
```


## TC-501CharacterDescription-007

Request body:

```json
{"subject":"Technical support request","description":"yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"}
```

HTTP status: **400**

Full response:

```json
{
  "error": "Description is required (max 500 characters)"
}
```


## TC-DuplicateTicket-008 submission 1

Request body:

```json
{"subject":"Unable to access my account","description":"I cannot log into my account using my correct credentials."}
```

HTTP status: **201**

Full response:

```json
{
  "category": "access",
  "confidence": 0.785,
  "created_at": "2026-10-10T21:02:39.199372+00:00",
  "description": "I cannot log into my account using my correct credentials.",
  "id": 25,
  "priority": "normal",
  "subject": "Unable to access my account"
}
```


## TC-DuplicateTicket-008 submission 2

Request body:

```json
{"subject":"Unable to access my account","description":"I cannot log into my account using my correct credentials."}
```

HTTP status: **201**

Full response:

```json
{
  "category": "access",
  "confidence": 0.785,
  "created_at": "2026-10-10T21:02:39.214266+00:00",
  "description": "I cannot log into my account using my correct credentials.",
  "id": 26,
  "priority": "normal",
  "subject": "Unable to access my account"
}
```


## TC-HTMLLikeText-009

Request body:

```json
{"subject":"<b>Login Problem</b>","description":"I cannot login to my account. <b>Please help.</b>"}
```

HTTP status: **201**

Full response:

```json
{
  "category": "access",
  "confidence": 0.69,
  "created_at": "2026-10-10T21:02:39.228032+00:00",
  "description": "I cannot login to my account. <b>Please help.</b>",
  "id": 27,
  "priority": "normal",
  "subject": "<b>Login Problem</b>"
}
```


## TC-AmbiguousTicket-010

Request body:

```json
{"subject":"Help needed","description":"i need help"}
```

HTTP status: **201**

Full response:

```json
{
  "category": "access",
  "confidence": 0.51,
  "created_at": "2026-10-10T21:02:39.240606+00:00",
  "description": "i need help",
  "id": 28,
  "priority": "normal",
  "subject": "Help needed"
}
```


## TC-MalformedJson-011

Request body:

```json
{"subject":"Help needed","description":}
```

HTTP status: **400**

Full response:

```json
{
  "error": "Request body must be a JSON object"
}
```


## TC-DuplicateTicket-008 readback through GET /api/tickets

The dashboard does not print ids, so both stored tickets were read back:

```json
[
  {
    "category": "access",
    "confidence": 0.785,
    "created_at": "2026-10-10T21:02:39.199372+00:00",
    "description": "I cannot log into my account using my correct credentials.",
    "id": 25,
    "priority": "normal",
    "subject": "Unable to access my account"
  },
  {
    "category": "access",
    "confidence": 0.785,
    "created_at": "2026-10-10T21:02:39.214266+00:00",
    "description": "I cannot log into my account using my correct credentials.",
    "id": 26,
    "priority": "normal",
    "subject": "Unable to access my account"
  }
]
```

## Checks against the Expected column

| Test ID | Check | Result |
| --- | --- | --- |
| TC-ValidAccess-001 | 201, subject unchanged | PASS — sent 'Unable to access my account', stored 'Unable to access my account' |
| TC-ValidAccess-001 | 201, description unchanged | PASS — stored 'I cannot log into my account'... |
| TC-ValidAccess-001 | 201, id present | PASS — id=22 |
| TC-ValidAccess-001 | 201, category is one of access/billing/technical | PASS — category=access |
| TC-ValidAccess-001 | 201, confidence between 0 and 1 | PASS — confidence=0.768 |
| TC-ValidAccess-001 | 201, priority present | PASS — priority=normal |
| TC-ValidAccess-001 | 201, created_at present | PASS — created_at=2026-10-10T21:02:39.140407+00:00 |
| TC-ValidBilling-002 | 201, subject unchanged | PASS — sent 'Billing inquiry regarding invoice #12345', stored 'Billing inquiry regarding invoice #12345' |
| TC-ValidBilling-002 | 201, description unchanged | PASS — stored 'I would like to request an itemized brea'... |
| TC-ValidBilling-002 | 201, id present | PASS — id=23 |
| TC-ValidBilling-002 | 201, category is one of access/billing/technical | PASS — category=billing |
| TC-ValidBilling-002 | 201, confidence between 0 and 1 | PASS — confidence=0.642 |
| TC-ValidBilling-002 | 201, priority present | PASS — priority=normal |
| TC-ValidBilling-002 | 201, created_at present | PASS — created_at=2026-10-10T21:02:39.156060+00:00 |
| TC-ValidTechnical-003 | 201, subject unchanged | PASS — sent 'PDF upload failed', stored 'PDF upload failed' |
| TC-ValidTechnical-003 | 201, description unchanged | PASS — stored 'The app freezes when I upload a PDF'... |
| TC-ValidTechnical-003 | 201, id present | PASS — id=24 |
| TC-ValidTechnical-003 | 201, category is one of access/billing/technical | PASS — category=technical |
| TC-ValidTechnical-003 | 201, confidence between 0 and 1 | PASS — confidence=0.661 |
| TC-ValidTechnical-003 | 201, priority present | PASS — priority=normal |
| TC-ValidTechnical-003 | 201, created_at present | PASS — created_at=2026-10-10T21:02:39.169160+00:00 |
| TC-BlankSubject-004 | 400 with documented error | PASS — Subject is required (max 100 characters) |
| TC-BlankDescription-005 | 400 with documented error | PASS — Description is required (max 500 characters) |
| TC-101CharacterSubject-006 | 400 with documented error | PASS — Subject is required (max 100 characters) |
| TC-501CharacterDescription-007 | 400 with documented error | PASS — Description is required (max 500 characters) |
| TC-DuplicateTicket-008 | 201, subject unchanged | PASS — sent 'Unable to access my account', stored 'Unable to access my account' |
| TC-DuplicateTicket-008 | 201, description unchanged | PASS — stored 'I cannot log into my account using my co'... |
| TC-DuplicateTicket-008 | 201, id present | PASS — id=25 |
| TC-DuplicateTicket-008 | 201, category is one of access/billing/technical | PASS — category=access |
| TC-DuplicateTicket-008 | 201, confidence between 0 and 1 | PASS — confidence=0.785 |
| TC-DuplicateTicket-008 | 201, priority present | PASS — priority=normal |
| TC-DuplicateTicket-008 | 201, created_at present | PASS — created_at=2026-10-10T21:02:39.199372+00:00 |
| TC-HTMLLikeText-009 | 201, subject unchanged | PASS — sent '<b>Login Problem</b>', stored '<b>Login Problem</b>' |
| TC-HTMLLikeText-009 | 201, description unchanged | PASS — stored 'I cannot login to my account. <b>Please '... |
| TC-HTMLLikeText-009 | 201, id present | PASS — id=27 |
| TC-HTMLLikeText-009 | 201, category is one of access/billing/technical | PASS — category=access |
| TC-HTMLLikeText-009 | 201, confidence between 0 and 1 | PASS — confidence=0.69 |
| TC-HTMLLikeText-009 | 201, priority present | PASS — priority=normal |
| TC-HTMLLikeText-009 | 201, created_at present | PASS — created_at=2026-10-10T21:02:39.228032+00:00 |
| TC-AmbiguousTicket-010 | 201, subject unchanged | PASS — sent 'Help needed', stored 'Help needed' |
| TC-AmbiguousTicket-010 | 201, description unchanged | PASS — stored 'i need help'... |
| TC-AmbiguousTicket-010 | 201, id present | PASS — id=28 |
| TC-AmbiguousTicket-010 | 201, category is one of access/billing/technical | PASS — category=access |
| TC-AmbiguousTicket-010 | 201, confidence between 0 and 1 | PASS — confidence=0.51 |
| TC-AmbiguousTicket-010 | 201, priority present | PASS — priority=normal |
| TC-AmbiguousTicket-010 | 201, created_at present | PASS — created_at=2026-10-10T21:02:39.240606+00:00 |
| TC-MalformedJson-011 | 400 with documented error | PASS — Request body must be a JSON object |
| TC-DuplicateTicket-008 | both submissions returned 201 | PASS — first 201, second 201 |
| TC-DuplicateTicket-008 | the two ids differ | PASS — id 25 then id 26 |
| TC-DuplicateTicket-008 | subject and description identical in both | PASS — both store the same subject and description |

## Not verified here

This file covers the API responses only. Browser rendering is not evidenced here;
the HTML rendering observation is recorded separately with its own screenshot.
