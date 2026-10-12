# Day 4 API evidence, fresh run

Captured 2026-10-12 06:00:21 +0300, against commit `57a7fae` with the model trained by `ai/train.py`.
The local database was emptied first (`DELETE FROM tickets`, 0 rows remained), so the ids and
positions below come from this run and nothing here is reconstructed from an earlier session.

Every request below was sent to `POST http://127.0.0.1:5000/api/tickets` with
`Content-Type: application/json`. The response shown is the complete response body.

## TC-Priority-021, dashboard ordering

The case submits the urgent ticket TC-Priority-013 first, then the normal ticket TC-Priority-015,
then reads `GET /api/tickets` to compare their positions.

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject": "Server DOWN", "description": "Site unreachable"}
```

Response: **HTTP 201**

```json
{
  "category": "technical",
  "confidence": 0.477,
  "created_at": "2026-10-12T03:00:21.738225+00:00",
  "description": "Site unreachable",
  "id": 25,
  "priority": "urgent",
  "subject": "Server DOWN"
}
```

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject": "Printer issue", "description": "Paper jam on floor 2"}
```

Response: **HTTP 201**

```json
{
  "category": "billing",
  "confidence": 0.445,
  "created_at": "2026-10-12T03:00:21.751422+00:00",
  "description": "Paper jam on floor 2",
  "id": 26,
  "priority": "normal",
  "subject": "Printer issue"
}
```

Both creation timestamps, as returned by the API:

| Ticket | id | created_at | priority |
| --- | --- | --- | --- |
| Server DOWN | 25 | 2026-10-12T03:00:21.738225+00:00 | urgent |
| Printer issue | 26 | 2026-10-12T03:00:21.751422+00:00 | normal |

`GET /api/tickets` then returned 2 tickets in this order:

```
 0  id 25  urgent    Server DOWN
 1  id 26  normal    Printer issue
```

| Ticket | id | created_at | priority | position in GET |
| --- | --- | --- | --- | --- |
| Server DOWN, older | 25 | 2026-10-12T03:00:21.738225+00:00 | urgent | 0 |
| Printer issue, newer | 26 | 2026-10-12T03:00:21.751422+00:00 | normal | 1 |

The urgent ticket was created first and carries the lower id, so it is the older of the two,
and it appears at position 0, above the newer normal ticket at position 1.
Ordering therefore does not follow creation order alone; it puts urgent above normal.

The browser reload observation is recorded separately in `day4_regression_results.md` section 6,
because it is a different kind of evidence from the API responses above.


## Complete `GET /api/tickets` response, observation C

Captured 2026-10-12 14:03:33 +0300, against commit `57a7fae`. This is the complete JSON body, not a
summary. It is the third of three observations of the same two tickets from TC-Priority-021; see
the table in `day4_regression_results.md` section 6 that distinguishes them.

State at capture: the four unsafe-input tickets, both duplicate tickets and TC-Priority-024 (id 32)
had been submitted after the original two-ticket check, so the list holds 8 tickets.
`Server DOWN` (id 25) is at position 1 and `Printer issue` (id 26) at position 7.
The urgent ticket is still above the normal one. `Production issue` (id 32) is a newer urgent
ticket, which is why id 25 is no longer at position 0.

Response: **HTTP 200**

```json
[
  {
    "category": "billing",
    "confidence": 0.493,
    "created_at": "2026-10-12T03:46:26.672306+00:00",
    "description": "Please investigate",
    "id": 32,
    "priority": "urgent",
    "subject": "Production issue"
  },
  {
    "category": "technical",
    "confidence": 0.477,
    "created_at": "2026-10-12T03:00:21.738225+00:00",
    "description": "Site unreachable",
    "id": 25,
    "priority": "urgent",
    "subject": "Server DOWN"
  },
  {
    "category": "access",
    "confidence": 0.785,
    "created_at": "2026-10-12T03:00:21.826917+00:00",
    "description": "I cannot log into my account using my correct credentials.",
    "id": 31,
    "priority": "normal",
    "subject": "Unable to access my account"
  },
  {
    "category": "access",
    "confidence": 0.785,
    "created_at": "2026-10-12T03:00:21.814433+00:00",
    "description": "I cannot log into my account using my correct credentials.",
    "id": 30,
    "priority": "normal",
    "subject": "Unable to access my account"
  },
  {
    "category": "technical",
    "confidence": 0.382,
    "created_at": "2026-10-12T03:00:21.797388+00:00",
    "description": "<img src=x>",
    "id": 29,
    "priority": "normal",
    "subject": "Image test"
  },
  {
    "category": "technical",
    "confidence": 0.488,
    "created_at": "2026-10-12T03:00:21.783968+00:00",
    "description": "<script>alert(1)</script>",
    "id": 28,
    "priority": "normal",
    "subject": "Script test"
  },
  {
    "category": "technical",
    "confidence": 0.382,
    "created_at": "2026-10-12T03:00:21.770587+00:00",
    "description": "<b>bold</b>",
    "id": 27,
    "priority": "normal",
    "subject": "HTML bold test"
  },
  {
    "category": "billing",
    "confidence": 0.445,
    "created_at": "2026-10-12T03:00:21.751422+00:00",
    "description": "Paper jam on floor 2",
    "id": 26,
    "priority": "normal",
    "subject": "Printer issue"
  }
]
```

## Unsafe input, API responses

These four were sent to the API directly, bypassing the browser form, so the server response is
observed rather than inferred from what the form allowed.

### TC-HTMLBold-001

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject": "HTML bold test", "description": "<b>bold</b>"}
```

Response: **HTTP 201**

```json
{
  "category": "technical",
  "confidence": 0.382,
  "created_at": "2026-10-12T03:00:21.770587+00:00",
  "description": "<b>bold</b>",
  "id": 27,
  "priority": "normal",
  "subject": "HTML bold test"
}
```

### TC-Script-002

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject": "Script test", "description": "<script>alert(1)</script>"}
```

Response: **HTTP 201**

```json
{
  "category": "technical",
  "confidence": 0.488,
  "created_at": "2026-10-12T03:00:21.783968+00:00",
  "description": "<script>alert(1)</script>",
  "id": 28,
  "priority": "normal",
  "subject": "Script test"
}
```

### TC-Image-003

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject": "Image test", "description": "<img src=x>"}
```

Response: **HTTP 201**

```json
{
  "category": "technical",
  "confidence": 0.382,
  "created_at": "2026-10-12T03:00:21.797388+00:00",
  "description": "<img src=x>",
  "id": 29,
  "priority": "normal",
  "subject": "Image test"
}
```

### TC-Spaces-004

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject": "Spaces test", "description": " "}
```

Response: **HTTP 400**

```json
{
  "error": "Description is required (max 500 characters)"
}
```

## TC-DuplicateTicket-008, both responses

Request:

```
{"subject": "Unable to access my account", "description": "I cannot log into my account using my correct credentials."}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.785,
  "created_at": "2026-10-12T03:00:21.814433+00:00",
  "description": "I cannot log into my account using my correct credentials.",
  "id": 30,
  "priority": "normal",
  "subject": "Unable to access my account"
}
```

Request:

```
{"subject": "Unable to access my account", "description": "I cannot log into my account using my correct credentials."}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.785,
  "created_at": "2026-10-12T03:00:21.826917+00:00",
  "description": "I cannot log into my account using my correct credentials.",
  "id": 31,
  "priority": "normal",
  "subject": "Unable to access my account"
}
```

Both submissions returned 201 with different ids, 30 then 31. `GET /api/tickets` afterwards
returns 2 tickets whose subject is 'Unable to access my account', ids 31, 30, so neither submission overwrote the other.

| id | subject | description |
| --- | --- | --- |
| 30 | Unable to access my account | I cannot log into my account using my correct credentials. |
| 31 | Unable to access my account | I cannot log into my account using my correct credentials. |

## The 24 main-run cases, full requests and full responses

These were captured on 2026-10-12 against commit `57a7fae` with the model trained by `ai/train.py`.
The request bodies are the inputs from `tests/test_cases.md`. The response shown is the complete
body returned by the API. The database was emptied immediately before this batch, so ids start at 1.

| Test ID | HTTP | id | category | confidence | priority | result |
| --- | --- | --- | --- | --- | --- | --- |
| TC-ValidAccess-001 | 201 | 1 | access | 0.768 | normal | Pass |
| TC-ValidBilling-002 | 201 | 2 | billing | 0.642 | normal | Pass |
| TC-ValidTechnical-003 | 201 | 3 | technical | 0.661 | normal | Pass |
| TC-BlankSubject-004 | 400 | - | - | - | - | Pass |
| TC-BlankDescription-005 | 400 | - | - | - | - | Pass |
| TC-101CharacterSubject-006 | 400 | - | - | - | - | Pass |
| TC-501CharacterDescription-007 | 400 | - | - | - | - | Pass |
| TC-DuplicateTicket-008 | 201 | 5 | access | 0.785 | normal | Pass |
| TC-HTMLLikeText-009 | 201 | 6 | access | 0.69 | normal | Pass |
| TC-AmbiguousTicket-010 | 201 | 7 | access | 0.51 | normal | Pass |
| TC-MalformedJson-011 | 400 | - | - | - | - | Pass |
| TC-Priority-012 | 201 | 8 | access | 0.737 | urgent | Pass |
| TC-Priority-013 | 201 | 9 | technical | 0.477 | urgent | Pass |
| TC-Priority-014 | 201 | 10 | technical | 0.778 | normal | Pass |
| TC-Priority-015 | 201 | 11 | billing | 0.445 | normal | Pass |
| TC-Priority-016 | 201 | 12 | access | 0.481 | urgent | Pass |
| TC-Priority-017 | 201 | 13 | technical | 0.491 | urgent | Pass |
| TC-Priority-018 | 201 | 14 | access | 0.619 | urgent | Pass |
| TC-Priority-019 | 201 | 15 | access | 0.528 | normal | Pass |
| TC-Priority-020 | 201 | 16 | access | 0.813 | normal | Pass |
| TC-Priority-022 | 201 | 17 | access | 0.378 | urgent | Pass |
| TC-Priority-023 | 201 | 18 | access | 0.429 | urgent | Pass |
| TC-Priority-024 | 201 | 19 | billing | 0.493 | urgent | Pass |
| TC-Priority-021 | 201 | - | - | - | - | Pass |

### Full request and response per case

#### TC-ValidAccess-001

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Unable to access my account","description":"I cannot log into my account"}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.768,
  "created_at": "2026-10-11T23:30:36.506748+00:00",
  "description": "I cannot log into my account",
  "id": 1,
  "priority": "normal",
  "subject": "Unable to access my account"
}
```

#### TC-ValidBilling-002

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Billing inquiry regarding invoice #12345","description":"I would like to request an itemized breakdown for my latest invoice."}
```

Response: **HTTP 201**

```json
{
  "category": "billing",
  "confidence": 0.642,
  "created_at": "2026-10-11T23:30:36.524453+00:00",
  "description": "I would like to request an itemized breakdown for my latest invoice.",
  "id": 2,
  "priority": "normal",
  "subject": "Billing inquiry regarding invoice #12345"
}
```

#### TC-ValidTechnical-003

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"PDF upload failed","description":"The app freezes when I upload a PDF"}
```

Response: **HTTP 201**

```json
{
  "category": "technical",
  "confidence": 0.661,
  "created_at": "2026-10-11T23:30:36.536290+00:00",
  "description": "The app freezes when I upload a PDF",
  "id": 3,
  "priority": "normal",
  "subject": "PDF upload failed"
}
```

#### TC-BlankSubject-004

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"","description":"Need help with my account settings"}
```

Response: **HTTP 400**

```json
{
  "error": "Subject is required (max 100 characters)"
}
```

#### TC-BlankDescription-005

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Need help with my account settings","description":""}
```

Response: **HTTP 400**

```json
{
  "error": "Description is required (max 500 characters)"
}
```

#### TC-101CharacterSubject-006

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
     xxxxxxxxxxxx", "description": "I need help logging in"}
  subject length 101, description length 22, verified 2026-10-12.
  Built by the command in the steps column of tests/test_cases.md:
  python -c "import json; print(json.dumps({'subject': 'x' * 101, 'description': 'I need help logging in'}))"
```

Response: **HTTP 400**

```json
{
  "error": "Subject is required (max 100 characters)"
}
```

#### TC-501CharacterDescription-007

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject": "Technical support request", "description": "<501 characters, all y>"}
  subject length 25, description length 501, verified 2026-10-12.
  Built by the command in the steps column of tests/test_cases.md:
  python -c "import json; print(json.dumps({'subject': 'Technical support request', 'description': 'y' * 501}))"
  The literal request is 560 characters long, so it is described rather than pasted in full.
  The generation command above produces it exactly, and the response returned for it is below.
```

Response: **HTTP 400**

```json
{
  "error": "Description is required (max 500 characters)"
}
```

#### TC-DuplicateTicket-008

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Unable to access my account","description":"I cannot log into my account using my correct credentials."}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.785,
  "created_at": "2026-10-11T23:30:36.576432+00:00",
  "description": "I cannot log into my account using my correct credentials.",
  "id": 5,
  "priority": "normal",
  "subject": "Unable to access my account"
}
```

#### TC-HTMLLikeText-009

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"<b>Login Problem</b>","description":"I cannot login to my account. <b>Please help.</b>"}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.69,
  "created_at": "2026-10-11T23:30:36.587452+00:00",
  "description": "I cannot login to my account. <b>Please help.</b>",
  "id": 6,
  "priority": "normal",
  "subject": "<b>Login Problem</b>"
}
```

#### TC-AmbiguousTicket-010

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Help needed","description":"i need help"}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.51,
  "created_at": "2026-10-11T23:30:36.597132+00:00",
  "description": "i need help",
  "id": 7,
  "priority": "normal",
  "subject": "Help needed"
}
```

#### TC-MalformedJson-011

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Help needed","description":}
```

Response: **HTTP 400**

```json
{
  "error": "Request body must be a JSON object"
}
```

#### TC-Priority-012

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Login broken","description":"I cannot access my account"}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.737,
  "created_at": "2026-10-11T23:30:36.611905+00:00",
  "description": "I cannot access my account",
  "id": 8,
  "priority": "urgent",
  "subject": "Login broken"
}
```

#### TC-Priority-013

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Server DOWN","description":"Site unreachable"}
```

Response: **HTTP 201**

```json
{
  "category": "technical",
  "confidence": 0.477,
  "created_at": "2026-10-11T23:30:36.623796+00:00",
  "description": "Site unreachable",
  "id": 9,
  "priority": "urgent",
  "subject": "Server DOWN"
}
```

#### TC-Priority-014

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Download fails","description":"The download button gives an error"}
```

Response: **HTTP 201**

```json
{
  "category": "technical",
  "confidence": 0.778,
  "created_at": "2026-10-11T23:30:36.633250+00:00",
  "description": "The download button gives an error",
  "id": 10,
  "priority": "normal",
  "subject": "Download fails"
}
```

#### TC-Priority-015

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Printer issue","description":"Paper jam on floor 2"}
```

Response: **HTTP 201**

```json
{
  "category": "billing",
  "confidence": 0.445,
  "created_at": "2026-10-11T23:30:36.656627+00:00",
  "description": "Paper jam on floor 2",
  "id": 11,
  "priority": "normal",
  "subject": "Printer issue"
}
```

#### TC-Priority-016

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Outage","description":"Please help"}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.481,
  "created_at": "2026-10-11T23:30:36.667157+00:00",
  "description": "Please help",
  "id": 12,
  "priority": "urgent",
  "subject": "Outage"
}
```

#### TC-Priority-017

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Report problem","description":"We had data loss after saving"}
```

Response: **HTTP 201**

```json
{
  "category": "technical",
  "confidence": 0.491,
  "created_at": "2026-10-11T23:30:36.677883+00:00",
  "description": "We had data loss after saving",
  "id": 13,
  "priority": "urgent",
  "subject": "Report problem"
}
```

#### TC-Priority-018

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Password reset","description":"I am locked out since this morning"}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.619,
  "created_at": "2026-10-11T23:30:36.687843+00:00",
  "description": "I am locked out since this morning",
  "id": 14,
  "priority": "urgent",
  "subject": "Password reset"
}
```

#### TC-Priority-019

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Slow laptop","description":"Everything is slow after the breakdown of my laptop"}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.528,
  "created_at": "2026-10-11T23:30:36.698269+00:00",
  "description": "Everything is slow after the breakdown of my laptop",
  "id": 15,
  "priority": "normal",
  "subject": "Slow laptop"
}
```

#### TC-Priority-020

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Cannot log in","description":"I can't access my account"}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.813,
  "created_at": "2026-10-11T23:30:36.708573+00:00",
  "description": "I can't access my account",
  "id": 16,
  "priority": "normal",
  "subject": "Cannot log in"
}
```

#### TC-Priority-022

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Login issue","description":"This affects all users"}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.378,
  "created_at": "2026-10-11T23:30:36.719327+00:00",
  "description": "This affects all users",
  "id": 17,
  "priority": "urgent",
  "subject": "Login issue"
}
```

#### TC-Priority-023

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Login issue","description":"Everyone is affected"}
```

Response: **HTTP 201**

```json
{
  "category": "access",
  "confidence": 0.429,
  "created_at": "2026-10-11T23:30:36.729900+00:00",
  "description": "Everyone is affected",
  "id": 18,
  "priority": "urgent",
  "subject": "Login issue"
}
```

#### TC-Priority-024

Request:

```
POST /api/tickets HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{"subject":"Production issue","description":"Please investigate"}
```

Response: **HTTP 201**

```json
{
  "category": "billing",
  "confidence": 0.493,
  "created_at": "2026-10-11T23:30:36.742262+00:00",
  "description": "Please investigate",
  "id": 19,
  "priority": "urgent",
  "subject": "Production issue"
}
```

## Note on the two images captured later

`day4-TC-Priority-024.png` and `day4-TC-HTMLBold-001.png` were captured after the runs above, on the
same clone and the same commit. They are dashboard images, so the ticket id shown can differ from the
id in the response recorded above. The two are reconciled here so the records do not silently
disagree.

| Case | id in the recorded response | id shown in the image | created_at | confidence | how the image was matched |
| --- | --- | --- | --- | --- | --- |
| TC-Priority-024 | 19 (main run, 2026-10-11) | 32 (submitted later, for the image) | 2026-10-12T03:46:26.672306+00:00 | 0.493 | card subject "Production issue", Priority: urgent |
| TC-HTMLBold-001 | 27 | 27 (same ticket, not resubmitted) | 2026-10-12T03:00:21.770587+00:00 | 0.382 | card subject "HTML bold test", shown as Category: technical (38%) |

TC-Priority-024 was resubmitted specifically to produce the image, so it carries a new id. It returned
`priority: urgent` on both runs, and the image shows that card at the top of the dashboard.

TC-HTMLBold-001 was already on the dashboard and was **not** resubmitted, so its id is unchanged at 27.
The image shows `Category: technical (38%)`, which matches the recorded confidence 0.382 rounded to a
percentage, and the visible time 6:00:21 AM local matches the recorded `created_at`. The bold image
incidentally also shows the `<img src=x>` and `<script>alert(1)</script>` cards rendered as literal
text, which corroborates those two cases as well.

The ids recorded for the four unsafe cases are **27 bold, 28 script, 29 image**, and TC-Spaces-004 was
rejected so it received no id. An earlier revision of this note labelled the bold ticket as id 28; that
was wrong, 28 is TC-Script-002.
