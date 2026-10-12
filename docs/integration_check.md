# Day 3 Integration Check

## Objective

Verify the end-to-end integration between the Flask backend (`backend/app.py`) and the trained machine learning model (`ai/model.joblib`). Confirm that the server loads the model, generates predictions with confidence scores, persists ticket records across restarts, and serves accurate payloads via GET endpoints.

## Environment

- **Branch**: `a2-day3-integration`
- **Local API Address**: `http://127.0.0.1:5000/api/tickets`
- **Model Path**: `ai/model.joblib` (existing model reused without retraining)

### Testing Sessions & Attribution

- **Session 1: Historical team testing**
  - **Date**: 2026-10-08
  - **Recorded commit**: `48ba094`
  - **Scope**: Historical team testing capturing IDs 6, 10, 11, and 12.

- **Session 2: Captured POST session**
  - **Timestamps**: 2026-10-10, approximately 23:25–23:27 UTC
  - **IDs created**: 5, 6, 7, 8
  - **Tested commit**: Not recorded at execution time.

- **Session 3: GET/restart session**
  - **Date & Times**: 2026-10-11
  - **Tested commit**: `72f0f56`
  - **Scope**: Verification of GET responses and restart persistence; existing model reused without retraining.

## Commands and Procedure

### 1. Historical Team Testing (2026-10-08)

- **Recorded procedure**: Not recorded at execution time.

### 2. Captured POST Session (2026-10-10)

- **Recorded procedure**: Submitted four POST requests with ticket payloads to `http://127.0.0.1:5000/api/tickets`, generating IDs 5 through 8.

### 3. GET and Restart Verification (2026-10-11)

1. **Pre-restart verification**: Queried `GET http://127.0.0.1:5000/api/tickets` and captured the raw output in [Before-restart GET capture](docs/get-pre-restart.txt).
2. **Server stop**: Terminated running server process via `Ctrl+C`.
3. **Server restart**: Launched server via `python backend/app.py` from repository root.
4. **Post-restart verification**: Queried `GET http://127.0.0.1:5000/api/tickets` and captured the raw output in [After-restart GET capture](docs/get-post-restart.txt).

## Results

| Ticket | Exact subject and description | Expected category | Actual category | Confidence | Priority | POST status | ID | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Subject: "I cannot sign in to the portal, even though my password appears to be correct." - Description: "Tried multiple times to sign in but the portal is not responding properly." | access | access | 0.855 | normal | 201 Created | 5 | Pass |
| 2 | Subject: "The system displays an error when I open the activity section." - Description: "The system displays an error when I open the activity section." | technical | technical | 0.866 | normal | 201 Created | 6 | Pass |
| 3 | Subject: "I can sign into the workspace without issue, but the system billed our company credit card twice for" - Description: "I can sign into the workspace without issue, but the system billed our company credit card twice for this month" | billing | billing | 0.831 | normal | 201 Created | 7 | Pass |
| 4 | Subject: "The downlaod botton throwss a 500 internal serer errror" - Description: "The downlaod botton throwss a 500 internal serer errror" | technical | technical | 0.854 | normal | 201 Created | 8 | Pass |

### POST Evidence

#### Ticket 1: Login issue

**Request body:**

```json
{
  "subject": "I cannot sign in to the portal, even though my password appears to be correct.",
  "description": "Tried multiple times to sign in but the portal is not responding properly."
}
```

**HTTP status:** `201 Created`

**Response body:**

```json
{
  "category": "access",
  "confidence": 0.855,
  "created_at": "2026-10-10T23:25:38.397139+00:00",
  "description": "Tried multiple times to sign in but the portal is not responding properly.",
  "id": 5,
  "priority": "normal",
  "subject": "I cannot sign in to the portal, even though my password appears to be correct."
}
```

#### Ticket 2: Activity-section error

**Request body:**

```json
{
  "subject": "The system displays an error when I open the activity section.",
  "description": "The system displays an error when I open the activity section."
}
```

**HTTP status:** `201 Created`

**Response body:**

```json
{
  "category": "technical",
  "confidence": 0.866,
  "created_at": "2026-10-10T23:26:24.003590+00:00",
  "description": "The system displays an error when I open the activity section.",
  "id": 6,
  "priority": "normal",
  "subject": "The system displays an error when I open the activity section."
}
```

#### Ticket 3: Duplicate charge

**Request body:**

```json
{
  "subject": "I can sign into the workspace without issue, but the system billed our company credit card twice for",
  "description": "I can sign into the workspace without issue, but the system billed our company credit card twice for this month"
}
```

**HTTP status:** `201 Created`

**Response body:**

```json
{
  "category": "billing",
  "confidence": 0.831,
  "created_at": "2026-10-10T23:26:53.598451+00:00",
  "description": "I can sign into the workspace without issue, but the system billed our company credit card twice for this month",
  "id": 7,
  "priority": "normal",
  "subject": "I can sign into the workspace without issue, but the system billed our company credit card twice for"
}
```

#### Ticket 4: Download error

**Request body:**

```json
{
  "subject": "The downlaod botton throwss a 500 internal serer errror",
  "description": "The downlaod botton throwss a 500 internal serer errror"
}
```

**HTTP status:** `201 Created`

**Response body:**

```json
{
  "category": "technical",
  "confidence": 0.854,
  "created_at": "2026-10-10T23:27:22.827058+00:00",
  "description": "The downlaod botton throwss a 500 internal serer errror",
  "id": 8,
  "priority": "normal",
  "subject": "The downlaod botton throwss a 500 internal serer errror"
}
```

### GET Verification

Both captured responses recorded an `HTTP/1.1 200 OK` status and preserved all eight records (IDs 1 through 8) in storage.

**Inspectable raw captures:**

- [Before-restart GET capture](docs/get-pre-restart.txt)
- [After-restart GET capture](docs/get-post-restart.txt)

Every record across both captures preserves identical fields: `id`, `subject`, `description`, `category`, `confidence`, `priority`, and `created_at`.

### Restart Persistence

- **Before-restart IDs**: 1, 2, 3, 4, 5, 6, 7, 8
- **After-restart IDs**: 1, 2, 3, 4, 5, 6, 7, 8
- **Result**: Pass. Both files reflect all eight records.

**Chronology Limitation**: The file metadata for the captures is chronologically inverted (pre-restart recorded at 04:03:06 and post-restart at 04:01:07). Since the original exact sequence cannot be definitively established from the file metadata alone, we are disclosing this limitation. However, the response bodies match perfectly across both captures, establishing that all eight records persist regardless of order.

## Findings and Limits

**API & Persistence Integration**: Ticket submission via `POST /api/tickets`, retrieval via `GET /api/tickets`, and persistence of eight records across server restarts were verified.

**Model Inference**: The four reported test cases matched their expected categories (access, billing, and two technical cases), correctly handling typos and multi-topic tickets.

**Limits:**

- An existing model artifact was reused without retraining. These four successful example predictions demonstrate functional endpoint integration and routing; they do not represent a comprehensive model-accuracy evaluation or general accuracy benchmark across wider production distributions.
- The four pre-existing records (IDs 1–4) had a confidence of 0.5 and were not part of the live prediction test. Their stored results should not be treated as predictions from the current live test.
- All four new tickets received normal priority. This test did not establish urgent-priority behavior.
- The observed ticket IDs are local database IDs. They may differ from IDs in other team environments because database histories can differ.
- The evidence records the command-line results observed during this test. It does not claim that a separate reviewer independently repeated the test.
