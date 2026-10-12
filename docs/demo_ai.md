# SmartDesk AI Ticket Classifier — Demo Script

## Objective

Demonstrate how the SmartDesk API classifies support tickets, show two verified API responses, and explain why human review remains necessary.

**Planned duration:** 105 seconds (1 minute 45 seconds). This is a planned walkthrough, not a recorded rehearsal.

## Preparation checklist

Complete these steps before the timed presentation:

- [ ] Activate the project virtual environment.
- [ ] Confirm the dataset version and review the latest training output.
- [ ] Run `python ai/train.py` before the presentation; training is outside the timed demo.
- [ ] Start the API with `python backend\app.py` and confirm `/api/health` returns `ok`.
- [ ] Confirm the two example requests below work.
- [ ] Record the actual rehearsal date, tested commit, participants, duration and outcome after a rehearsal has taken place.
- [ ] Record the presenter name before presenting.

## Timed walkthrough

### 1. Introduction — 15 seconds

"SmartDesk helps support teams classify incoming tickets into access, billing and technical categories. It is intended to assist ticket routing, not replace human support staff."

### 2. Explain the model — 20 seconds

"The training pipeline uses TF-IDF to convert ticket text into numerical features and Logistic Regression to predict a category. The predictor returns the selected category and a confidence score. That score is an estimate, not a guarantee that the prediction is correct."

### 3. Demonstrate the API — 30 seconds

The API accepts a subject and description. It constructs the prediction input as `subject + ". " + description`.

With the API running, paste these commands into a second PowerShell window from the repository root.

**Example 1 — login issue**

```powershell
$body = '{"subject":"Cannot log in after password reset","description":"I reset my password, but I still cannot access my account."}'
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/tickets" -Method Post -ContentType "application/json" -Body $body -UseBasicParsing
"HTTP status: $([int]$response.StatusCode)"
$response.Content
```

**Example 2 — export issue**

```powershell
$body = '{"subject":"Data export hangs","description":"The export script stops responding after I click Export and never finishes."}'
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/tickets" -Method Post -ContentType "application/json" -Body $body -UseBasicParsing
"HTTP status: $([int]$response.StatusCode)"
$response.Content
```

These commands create new local ticket records each time they run. The verified responses from the 12 October 2026 capture were:

- Login ticket, ID 13: HTTP 201, category `access`, confidence `0.893`, priority `urgent`.
- Export ticket, ID 14: HTTP 201, category `technical`, confidence `0.690`, priority `normal`.

New requests may receive different ticket IDs and timestamps. Confirm the live responses rather than presenting these historical IDs as new results.

### 4. Explain a limitation — 25 seconds

"The dataset contains only 36 synthetic tickets. The training run reported 0.625 accuracy on an eight-ticket test split and a five-fold cross-validation mean of 0.632, with a standard deviation of 0.198. Three test-split examples were misclassified. These small-sample results do not establish production readiness."

### 5. Conclusion — 15 seconds

"The API successfully returned predictions for the two demonstrated requests. More representative data, further evaluation and human oversight are needed before relying on the classifier for real support decisions."

## Verification record

### Training

- Date: 12 October 2026.
- Git commit: `005f1b57e6110d0f45c1c0bb14bfdabf4eb92a5f`.
- Dataset: `ai/data/tickets.csv`.
- Dataset SHA-256: `525AC01B9A55B86BB69D77B17128D5529535D1844F9018CF8DCE1DB4C2F896A1`.
- Dataset size: 36 synthetic rows; 12 per category.
- Command: `python ai/train.py`.
- Test-split accuracy: `0.625` (8 test tickets).
- Five-fold cross-validation mean: `0.632`; standard deviation: `0.198`.
- Model artifact: `ai/model.joblib` (local, ignored by Git).
- Exact training start time and Python version were not separately recorded.

The test-split accuracy describes the held-out split used during this training run. The cross-validation mean describes the folds used by the training process. Neither is an independent evaluation of the final model trained on all 36 rows.

### Fresh API capture

- Date: 12 October 2026.
- API capture session started: `2026-10-12T07:24:30.085+02:00`.
- Git commit: `005f1b57e6110d0f45c1c0bb14bfdabf4eb92a5f`.
- Environment: Windows PowerShell 5.1 with the project `.venv`.
- Endpoint: `POST http://127.0.0.1:5000/api/tickets`.
- Full request JSON, timestamps, HTTP statuses and response bodies: [API evidence after fresh training](demo_ai_api_evidence_after_training.md).

The API calls use both the subject and description joined with a period and a space. Earlier predictor-only examples used different input strings. Their confidence scores should not be compared as if the exact same text had been submitted.

### Known test-split errors

The training output recorded these incorrect predictions:

- A technical ticket about billing-card updates and an export script hanging was classified as billing.
- A ticket about settings not being saved was classified as access rather than technical.
- A request for a receipt for a recent payment was classified as access rather than billing.

These examples illustrate the need to evaluate the model on more representative data.

## Limitations and responsible use

- The dataset is small and synthetic.
- Test and cross-validation metrics are limited evidence of generalisation.
- Confidence scores are not guarantees of correctness.
- The API's successful response means the request was processed; it does not prove the category is correct.
- Human review is necessary, especially for ambiguous or high-impact tickets.
- Do not use the two successful demo requests as proof of overall model quality.

## Rehearsal and handoff record

- Presenter: pending confirmation.
- Rehearsal date and time: pending; not yet recorded.
- Tested commit and environment for rehearsal: pending.
- Participants, actual duration and outcome: pending.
- Evaluation report: [Model Evaluation Report](model_evaluation.md).
- Data quality report: [Data Quality Report](data_quality_report.md).
- Separate model card: not found in the current documentation files.
- Coordination with the related demo and QA work: pending verification.
