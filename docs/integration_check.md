# Day 3 Integration Check

## Objective

Verify that the SmartDesk API loads the ticket-classification model, accepts valid ticket submissions, stores the resulting tickets, returns them through the GET endpoint, and preserves them after the API process restarts.

## Environment

* **Verification date:** 2026-10-11 (South African Standard Time, UTC+02:00)
* **Verification branch:** `a2-day3-integration-review`
* **Tested Git commit:** `72f0f56194fabc6d097518eb179f4ba2ce7be2eb`
* **Operating environment:** Windows PowerShell
* **API address:** `http://127.0.0.1:5000`
* **API implementation:** `backend/app.py`
* **Local model file used by the API:** `ai/model.joblib`
* **Database:** `backend/smartdesk.db`
* **Database engine:** SQLite
* **Python dependencies checked:** Flask 3.1.3, joblib 1.6.0, scikit-learn 1.9.1

The existing database initially contained four tickets (IDs 1–4). These records were preserved. The four new tickets created during this test received IDs 5–8.

## Commands and procedure

1. Recorded the tested Git commit using `git rev-parse HEAD`. The result was `72f0f56194fabc6d097518eb179f4ba2ce7be2eb`.
2. Checked the existing database in read-only mode before testing. It contained four tickets, IDs 1–4.
3. Checked that Flask, joblib, and scikit-learn were importable.
4. Loaded the model through `ai.predictor.predict_category`. A sample login problem was classified as `access` with confidence `0.837`.
5. Started the API using `python backend\app.py`.
6. Checked the health endpoint using `Invoke-RestMethod http://127.0.0.1:5000/api/health`.
7. Submitted four tickets to `POST http://127.0.0.1:5000/api/tickets` with JSON request bodies. Captured the HTTP status and response body for each request.
8. Retrieved the saved tickets using `GET http://127.0.0.1:5000/api/tickets`.
9. Stopped the Flask process with Ctrl+C, restarted it using `python backend\app.py`, and repeated the GET request.
10. Captured the actual HTTP status and complete GET response body before and after the API restart. Both captures recorded the tested Git commit.

## Results

| Test                   | Expected category | Actual category | Confidence | Priority | POST status | Actual ID | Result |
| ---------------------- | ----------------- | --------------- | ---------: | -------- | ----------- | --------: | ------ |
| Login issue            | access            | access          |      0.855 | normal   | 201 Created |         5 | Pass   |
| Activity-section error | technical         | technical       |      0.866 | normal   | 201 Created |         6 | Pass   |
| Duplicate charge       | billing           | billing         |      0.831 | normal   | 201 Created |         7 | Pass   |
| Download error         | technical         | technical       |      0.854 | normal   | 201 Created |         8 | Pass   |

All four POST requests returned HTTP `201 Created`. For these four test inputs, the predicted categories matched the expected categories. The recorded confidence values were 0.855, 0.866, 0.831, and 0.854.

### POST evidence

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

## GET verification

The health endpoint returned the following response:

```json
{
  "service": "SmartDesk local API",
  "status": "ok"
}
```

The GET endpoint, `http://127.0.0.1:5000/api/tickets`, returned eight records: the four pre-existing records (IDs 1-4) and the four newly created records (IDs 5-8).

The GET response for the four new records matched their POST responses for ticket ID, subject, description, category, confidence, and priority. The total number of records was eight.

## Restart persistence

The API was stopped using Ctrl+C and restarted with `python backend\app.py`. The GET endpoint was then called again to verify that the stored records remained available.

Both the pre-restart and post-restart GET requests returned HTTP `200 OK`. Both responses contained the same eight ticket records, with IDs 1-8. Tickets 5-8 remained available with their recorded subjects, categories, confidence values, and priorities.

### Captured GET evidence

**Before restart**

* **Evidence file:** `get-before-restart-20261011-040105.txt`
* **Verification time:** 2026-10-11 04:01:07 +02:00
* **HTTP status:** `200`
* **Tested Git commit:** `72f0f56194fabc6d097518eb179f4ba2ce7be2eb`

**After restart**

* **Evidence file:** `get-after-restart-20261011-040306.txt`
* **Verification time:** 2026-10-11 04:03:06 +02:00
* **HTTP status:** `200`
* **Tested Git commit:** `72f0f56194fabc6d097518eb179f4ba2ce7be2eb`

Both evidence files contain the captured response bodies, including the ticket IDs, subjects, descriptions, categories, confidence values, and priorities. The matching responses demonstrate that the records remained retrievable across an API process restart using the existing SQLite database. This test did not evaluate persistence after deleting or replacing the database.

## Findings and limits

* The model loaded successfully and produced a category prediction for the sample login problem.
* All four valid POST requests returned `201 Created`.
* All four predictions matched the expected categories for these test cases.
* GET returned the four newly created records and the four pre-existing records.
* All eight records remained retrievable after the API process restarted.
* The four pre-existing records had category `technical` and confidence `0.5`. They were created before this test and were not changed. Their stored results should not be treated as predictions from the current live test.
* Four successful examples demonstrate integration behavior for these inputs; they do not establish general model accuracy or performance across unseen tickets.
* All four new tickets received `normal` priority. This test did not establish urgent-priority behavior.
* The observed ticket IDs are local database IDs. They may differ from IDs in other team environments because database histories can differ.
* The API used the existing local `ai/model.joblib` file during this integration verification. The model file is ignored by Git and is not included in this submission. No model-training command was run during this verification session.
* The evidence records the command-line results observed during this test. It does not claim that a separate reviewer independently repeated the test.
