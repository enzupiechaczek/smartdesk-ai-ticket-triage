# SmartDesk AI Ticket Classifier — Demo Script

## Objective

Demonstrate the SmartDesk AI ticket classifier through the running API, show two verified predictions, and explain the model's limitations.

**Duration:** Under 2 minutes

## Demo walkthrough

### 1. Introduction (15 seconds)

"SmartDesk AI helps support teams classify incoming tickets into three categories: access, billing, and technical. The goal is to assist ticket routing, while keeping human support staff responsible for reviewing decisions."

### 2. Explain the model (20 seconds)

"The training process uses TF-IDF to convert ticket text into numerical features. A Logistic Regression classifier uses those features to predict the category and return a confidence score. The trained model is saved locally and loaded by the predictor."

### 3. Demonstrate the API (30 seconds)

"I started the application with `python backend\app.py` and submitted two test tickets to `POST /api/tickets`.

The login ticket was classified as `access` with confidence 0.852. The data export ticket was classified as `technical` with confidence 0.667. Both API requests succeeded and returned created ticket records."

### 4. Explain a limitation (25 seconds)

"The training evaluation achieved 0.625 test accuracy, while the five-fold cross-validation mean was 0.632 with a standard deviation of 0.198. One technical ticket about an export script hanging was incorrectly classified as billing during evaluation. This shows that successful demonstration examples do not guarantee that every ticket will be classified correctly."

### 5. Conclusion (15 seconds)

"The API and predictor are working for the tested examples. However, the training dataset contains only 36 synthetic tickets, so further evaluation with more representative data is necessary before relying on this model in a real support environment."

## Verified test evidence

### Training

Command: `python ai/train.py`

Observed:
- Test accuracy: 0.625
- Cross-validation mean accuracy: 0.632
- Cross-validation standard deviation: 0.198
- Model artifact saved as `ai/model.joblib`

### Predictor tests

Command: `python -c "from ai.predictor import predict_category; print('TEST 1 - Login issue:'); print(predict_category('I cannot log in after resetting my password')); print('TEST 2 - Export issue:'); print(predict_category('The data export hangs after I click export'))"`

Observed:
- Login issue: `access`, confidence 0.859
- Export issue: `technical`, confidence 0.664

### API tests

Started the application using `python backend\app.py`.

Submitted two POST requests to `http://127.0.0.1:5000/api/tickets` using PowerShell `Invoke-RestMethod`.

Observed:
- Ticket 9, "Cannot log in": `access`, confidence 0.852, priority `normal`
- Ticket 10, "Data export hangs": `technical`, confidence 0.667, priority `normal`

Both requests returned ticket records successfully.

## Limitations and responsible use

- The dataset contains 36 synthetic tickets, with 12 examples per category.
- Test accuracy and cross-validation results indicate that performance is not yet reliable enough to assume correct classification of all tickets.
- Confidence scores are model estimates, not guarantees of correctness.
- Human review remains necessary, particularly for ambiguous or high-impact tickets.
