# SmartDesk AI Ticket Classifier: Model Evaluation

## 1. Evaluation Scope

This report documents the evaluation of the 36-row synthetic baseline dataset in [`ai/data/tickets.csv`](../ai/data/tickets.csv), containing 12 examples for each category: `access`, `billing`, and `technical`.

The training and evaluation procedure is implemented in [`ai/train.py`](../ai/train.py).

[PR #47](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/47) proposes a 42-row dataset. The results in this report apply only to the 36-row baseline. If PR #47 merges, confirm the applicable dataset version and rerun or verify the evaluation before updating these figures.

Group B's separate six-ticket evaluation is documented in [PR #46](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/46). It is separate from the eight-record test split reported here. Those tickets and results have already been exposed and must not be described as a blind benchmark.

## 2. Training and Evaluation Procedure

- **Algorithm:** Logistic Regression with TF-IDF text features.
- **Text features:** Unigrams and bigrams.
- **Dataset:** 36 synthetic ticket records.
- **Train/test split:** Stratified 80% training and 20% testing, using `random_state=42`.
- **Test-set size:** 8 records.
- **Cross-validation:** Five-fold stratified cross-validation on the 36-row baseline.
- **Final saved model:** After the evaluation steps, the training script fits the pipeline on all 36 rows and saves it as `ai/model.joblib`.

The test-split metrics describe the model fitted on the training portion of the split. Cross-validation summarizes results across five separate folds. Neither provides an independent evaluation of the final saved model trained on all 36 rows.

## 3. Test-Split Results

The eight-record test split achieved an accuracy of **0.625 (62.5%)**.

| Metric | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Access | 0.50 | 1.00 | 0.67 | 2 |
| Billing | 0.67 | 0.67 | 0.67 | 3 |
| Technical | 1.00 | 0.33 | 0.50 | 3 |
| Macro average | 0.72 | 0.67 | 0.61 | 8 |
| Weighted average | 0.75 | 0.62 | 0.60 | 8 |

The classification report rounds the overall accuracy to 0.62. The unrounded accuracy is 0.625.

Because the test split contains only eight records, one incorrect prediction changes the accuracy by 12.5 percentage points. These results should therefore be interpreted cautiously.

## 4. Five-Fold Cross-Validation

The reported fold accuracies were:

```text
[0.875, 0.429, 0.429, 0.857, 0.571]
```

- **Mean accuracy:** 0.632 (63.2%)
- **Standard deviation:** 0.198

Five-fold cross-validation provides an additional estimate of model performance across different data splits. However, the small synthetic dataset limits the conclusions drawn from these results. The mean score is not automatically more reliable than the test-split score, and neither result establishes performance on real support tickets.

## 5. Observed Misclassifications

The following three errors were observed on the eight-record test split.

| Actual category | Predicted category | Ticket text |
|---|---|---|
| Technical | Billing | We updated our billing card details successfully, but the data export script hangs indefinitely at 99% |
| Technical | Access | Some settings are not being saved after I update them. |
| Billing | Access | Please send me a receipt for my most recent payment. |

The first ticket combines billing-related wording with an export failure. Billing terms might have influenced the prediction, but the model's internal reasoning has not been independently verified.

The second ticket describes a settings problem without an explicit technical keyword. Its wording might be ambiguous to a text classifier, but the exact reason for the prediction has not been verified.

The receipt request was also misclassified. These examples document observed errors. They do not establish how the model will behave on other tickets.

## 6. Limitations and Follow-Up

- **Small dataset:** The baseline contains only 36 synthetic records.
- **Limited test set:** Eight test records provide a limited basis for estimating performance.
- **Technical recall:** Technical recall was 0.33 on the test split. Two of the three technical tickets were misclassified.
- **Representativeness:** Synthetic tickets might not reflect the language, ambiguity, spelling, and complexity of real support requests.
- **Category overlap:** A ticket might mention multiple issues, making its primary category difficult to infer from text alone.
- **Human review:** Support staff should review predictions, particularly for ambiguous tickets and consequential account or payment decisions.
- **Group B evaluation:** The six-ticket evaluation in PR #46 is separate and already exposed. It must not be described as a blind benchmark.
- **Dataset changes:** If PR #47's proposed 42-row dataset merges, verify the applicable dataset version and rerun or verify the evaluation before updating the reported metrics.
- **Further evaluation:** Expand the dataset with more varied, representative support tickets, then rerun the evaluation to determine whether performance improves.

The final saved model is trained on all 36 baseline rows. The test-split and cross-validation results above are not an independent evaluation of that final artifact. Any claims about the final model's performance should be supported by an appropriate evaluation of the saved model on data not used for training.