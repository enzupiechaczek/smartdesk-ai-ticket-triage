# SmartDesk AI Ticket Classifier — Demo Script

## Objective

Demonstrate how the SmartDesk API classifies support tickets, show two verified API responses, and explain why human review remains necessary.

**Planned duration:** 105 seconds (1 minute 45 seconds). This is a planned walkthrough, not a recorded rehearsal.

## Preparation checklist

Complete these steps before the timed presentation:

- [ ] Activate the project virtual environment.
- [ ] Confirm the dataset version (see [Dataset change to watch](#dataset-change-to-watch)) and review the latest training output.
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

These commands create new local ticket records each time they run. The responses captured on 12 October 2026 in the session after fresh training were:

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
- Dataset SHA-256: `525AC01B9A55B86BB69D77B17128D5529535D1844F9018CF8DCE1DB4C2F896A1`. This is the hash of a Windows checkout, where Git (`core.autocrlf=true`) writes CRLF line endings. The same file as committed in Git has LF line endings and the SHA-256 `f3eea6dcfca3bd7786a04874ca00f7041ab169ba752653e9e703e071e29a4b71`, the value [PR #47](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/47) reports for the 36-row baseline. Both hashes were reproduced on 12 October 2026 and describe the same 36 rows.
- Dataset size: 36 synthetic rows; 12 per category.
- Command: `python ai/train.py`.
- Test-split accuracy: `0.625` (8 test tickets).
- Five-fold cross-validation mean: `0.632`; standard deviation: `0.198`.
- Model artifact: `ai/model.joblib` (local, ignored by Git).
- Exact training start time and Python version were not separately recorded.

The test-split accuracy describes the held-out split used during this training run. The cross-validation mean describes the folds used by the training process. Neither is an independent evaluation of the final model trained on all 36 rows.

### API captures on 12 October 2026

Two capture sessions sent the same subjects and descriptions as the commands above, at Git commit `005f1b57e6110d0f45c1c0bb14bfdabf4eb92a5f`. Both recorded HTTP 201 for every request and the same categories, confidences and priorities. They are kept as separate sessions.

**First session (ticket IDs 11 and 12)**

- API capture session started: `2026-10-12T07:18:17.008+02:00`.
- Login ticket, ID 11: category `access`, confidence `0.893`, priority `urgent`.
- Export ticket, ID 12: category `technical`, confidence `0.690`, priority `normal`.
- Full request JSON, timestamps, HTTP statuses and response bodies: [API evidence, first session](demo_ai_api_evidence.md).
- The file does not record the environment, or whether the model was retrained just before this session. Its header lists the 36-row baseline as "subject to confirmation". On 12 October 2026 the dataset at commit `005f1b5` was confirmed to contain 36 rows, 12 per category.

**Fresh-training session (ticket IDs 13 and 14)**

- API capture session started: `2026-10-12T07:24:30.085+02:00`, after a fresh `python ai/train.py` run.
- Environment: Windows PowerShell 5.1 with the project `.venv`.
- Endpoint: `POST http://127.0.0.1:5000/api/tickets`.
- Full request JSON, timestamps, HTTP statuses and response bodies: [API evidence after fresh training](demo_ai_api_evidence_after_training.md).

### Earlier observations (historical)

These results were recorded in commit `005f1b5` (11 October 2026) and in the original pull request description. They come from earlier sessions whose run date, tested commit and environment were not recorded, and no full responses were captured. They are kept as historical results and are not combined with the 12 October captures.

- Training: test-split accuracy `0.625`, cross-validation mean `0.632`, standard deviation `0.198`. These match the 12 October training run.
- Predictor only, run with this command:

  ```text
  python -c "from ai.predictor import predict_category; print('TEST 1 - Login issue:'); print(predict_category('I cannot log in after resetting my password')); print('TEST 2 - Export issue:'); print(predict_category('The data export hangs after I click export'))"
  ```

  - `I cannot log in after resetting my password`: category `access`, confidence `0.859`.
  - `The data export hangs after I click export`: category `technical`, confidence `0.664`.
- API, two requests sent with PowerShell `Invoke-RestMethod`. The HTTP status was not recorded.
  - Ticket 9, subject `Cannot log in`: category `access`, confidence `0.852`, priority `normal`.
  - Ticket 10, subject `Data export hangs`: category `technical`, confidence `0.667`, priority `normal`.
  - The descriptions sent with these two requests were not recorded.
- One earlier result appears only in the first version of this script (commit `35efb06`, 11 October 2026): a login ticket was classified as `access` with confidence `0.844`. Its exact input text, date and method were not recorded.

### How the API input differs from the predictor-only input

The API builds its predictor input from both fields as `subject + ". " + description` (see `create_ticket` in [backend/app.py](../backend/app.py)). For example, the 12 October login request was classified from this text:

```text
Cannot log in after password reset. I reset my password, but I still cannot access my account.
```

The predictor-only examples were single sentences, and the descriptions for tickets 9 and 10 are unknown. The confidence scores therefore come from different input strings and should not be compared as if the same text had been submitted. The cause of any particular score difference has not been investigated.

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

Status on 12 October 2026: no rehearsal has taken place, and the 105-second timing above is planned, not measured. Replace each pending item with the actual result after it happens.

| Item | Status |
| --- | --- |
| Presenter | Pending confirmation |
| Rehearsal date and time | Pending |
| Tested commit and environment | Pending |
| Participants | Pending |
| Measured duration | Pending |
| Outcome and issues found | Pending |

### Related documents

- Evaluation report: [Model Evaluation Report](model_evaluation.md). It covers the 36-row baseline.
- Data quality report: [Data Quality Report](data_quality_report.md).
- Model card: pending. It is proposed as `docs/model_card.md` in [PR #49](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/49), which has not been merged, so this script does not link the file yet.

### Dataset change to watch

[PR #47](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/47) proposes expanding the training data from 36 to 42 rows. It has not been merged. Every figure in this script describes the 36-row baseline: the dataset size, the `0.625` split accuracy, the `0.632` cross-validation mean and `0.198` standard deviation, the three test-split errors, and the confidences captured on 12 October. If PR #47 merges before the demo, `python ai/train.py` will train on the merged data, so these figures must be revised from a recorded run on that data before presenting. This revision has not been done and still needs to be agreed with the PR #47 owner.

### Handoffs with the other demo segments

As of 12 October 2026, no handoff has been confirmed with Group A1 or Group B.

- From Group A1: A1's script, `docs/demo_script.md` in [PR #44](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/44) (not yet merged), ends by handing over to the AI team and links to this file. A1's moment 5 already explains category, confidence and priority. Still to agree with A1: which segment explains confidence, and whether the AI segment reuses A1's running server and database. If it does, the two requests above will receive the next ticket IDs after A1's tickets, not 13 and 14.
- To Group B: A1's script links the QA segment as `docs/demo_qa.md`. No branch in the repository contains a written QA script at that path yet. The handoff to Group B's QA segment still needs to be agreed.
