# Day 3 Integration Check

## Objective

Verify that the trained ticket-classification model works when called through the live Flask API and that submitted tickets are stored and returned correctly.

## Environment

* Branch: `a2-day3-integration`
* API: Flask local API
* Endpoint: `http://127.0.0.1:5000`
* Model: trained using `python ai/train.py`
* Model artifact: `model.joblib`

## Integration Steps Completed

1. Trained the model successfully using:

   `python ai/train.py`

2. The training process completed successfully and saved `model.joblib`.

3. Started the Flask server from the repository root using:

   `python backend\app.py`

4. Verified the API health endpoint:

   `GET /api/health`

   Result: `status = ok`

5. Submitted four tickets through:

   `POST /api/tickets`

6. Retrieved the stored results through:

   `GET /api/tickets`

## Test Results

| ID | Test Case                   | Expected Category | Actual Category | Confidence | Result    |
| -- | --------------------------- | ----------------- | --------------- | ---------: | --------- |
| 1  | Cannot log in to my account | access            | technical       |       0.50 | Incorrect |
| 2  | I was charged twice         | billing           | technical       |       0.50 | Incorrect |
| 3  | Application keeps crashing  | technical         | technical       |       0.50 | Correct   |
| 4  | Payment receipt needed      | billing           | technical       |       0.50 | Incorrect |

## Integration Verification

The server and API integration worked successfully.

* Flask server started successfully.
* Health endpoint returned `ok`.
* All four POST requests were accepted successfully.
* All four tickets were assigned IDs and stored successfully.
* `GET /api/tickets` returned all four records.
* No changes were made to `backend/app.py`.

## Finding

The integration pipeline is functioning, but the trained model produced `technical` with `0.50` confidence for all four new test tickets.

The technical ticket was classified correctly. However, the access ticket and both billing tickets were classified incorrectly.

This indicates a model prediction/classification issue rather than an API or database integration failure.

## Action Required

The classification issue should be reported to the AI/model team for investigation.

Recommended areas to investigate:

* Training dataset coverage and wording diversity
* Model training and feature extraction
* Prediction behavior for access and billing terminology
* Whether additional representative training examples are required

No changes were made to the backend API during this integration check.
