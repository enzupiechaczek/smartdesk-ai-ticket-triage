# Day 3 Integration Check

## Objective
Verify the end-to-end integration between the Flask backend (`backend/app.py`) and the trained machine learning model (`ai/model.joblib`). Confirm that the server loads the model, generates predictions with confidence scores, persists ticket records across restarts, and serves accurate payloads via GET endpoints.

## Environment
- **Branch**: `a2-day3-integration`
- **Local API Address**: `http://127.0.0.1:5000/api/tickets`
- **Model Path**: `ai/model.joblib` (existing model reused without retraining)

### Testing Sessions & Attribution
- **Historical team testing**:
  - **Date**: 2026-10-08
  - **Recorded commit**: `48ba094`
  - **Scope**: Historical team testing capturing IDs 6, 10, 11, and 12.
- **Captured POST session**:
  - **Timestamps**: 2026-10-10, approximately 23:25–23:27 UTC
  - **IDs created**: 5, 6, 7, 8
  - **Tested commit**: Not recorded at execution time.
- **GET/restart session**:
  - **Date & Times**: 2026-10-11, before 04:01:07 +02:00 and after 04:03:06 +02:00
  - **Tested commit**: `72f0f56`
  - **Scope**: Verification of GET responses and restart persistence; existing model reused without retraining.

## Commands and procedure

### 1. Historical Team Testing (2026-10-08)
- Exact commands: Not recorded at execution time.

### 2. Captured POST Session (2026-10-10)
- Exact commands: Submitted four POST requests with ticket payloads to `http://127.0.0.1:5000/api/tickets`, generating IDs 5 through 8.

### 3. GET and Restart Verification (2026-10-11)
1. **Pre-restart verification (04:01:07 +02:00)**: Queried `GET http://127.0.0.1:5000/api/tickets` and captured the raw output in [Before-restart GET capture](get-pre-restart.txt).
2. **Server stop**: Terminated running server process via `Ctrl+C`.
3. **Server restart**: Launched server via `python backend/app.py` from repository root.
4. **Post-restart verification (04:03:06 +02:00)**: Queried `GET http://127.0.0.1:5000/api/tickets` and captured the raw output in [After-restart GET capture](get-post-restart.txt).

## Results

| Ticket | Exact subject and description | Expected category | Actual category | Confidence | Priority | POST status | ID | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Subject: "I cannot sign in to the portal, even though my password appears to be correct." - Description: "Tried multiple times to sign in but the portal is not responding properly." | access | access | 0.855 | normal | 201 Created | 5 | Pass |
| 2 | Subject: "The system displays an error when I open the activity section." - Description: "The system displays an error when I open the activity section." | technical | technical | 0.866 | normal | 201 Created | 6 | Pass |
| 3 | Subject: "I can sign into the workspace without issue, but the system billed our company credit card twice for this month" - Description: "I can sign into the workspace without issue, but the system billed our company credit card twice for this month" | billing | billing | 0.831 | normal | 201 Created | 7 | Pass |
| 4 | Subject: "The downlaod botton throwss a 500 internal serer errror" - Description: "The downlaod botton throwss a 500 internal serer errror" | technical | technical | 0.854 | normal | 201 Created | 8 | Pass |

## GET verification
Both captured responses recorded an `HTTP/1.1 200 OK` status and preserved all eight records (IDs 1 through 8) in storage.

Inspectable raw captures:
- [Before-restart GET capture](get-pre-restart.txt)
- [After-restart GET capture](get-post-restart.txt)

Every record across both captures preserves identical fields: `id`, `subject`, `description`, `category`, `confidence`, `priority`, and `created_at`.

## Restart persistence
- **Before-restart IDs**: 1, 2, 3, 4, 5, 6, 7, 8
- **After-restart IDs**: 1, 2, 3, 4, 5, 6, 7, 8
- **Result**: Pass. All eight records survived server restart with identical IDs, timestamps, categories, and confidence scores.

## Findings and limits
- **API & Persistence Integration**: Ticket submission via `POST /api/tickets`, retrieval via `GET /api/tickets`, and persistence of eight records across server restarts were verified.
- **Model Inference**: The four reported test cases matched their expected categories (`access`, `billing`, and two `technical` cases), correctly handling typos and multi-topic tickets.
- **Limits**: An existing model artifact was reused without retraining. These four successful example predictions demonstrate functional endpoint integration and routing; they do not represent a comprehensive model-accuracy evaluation or general accuracy benchmark across wider production distributions.
