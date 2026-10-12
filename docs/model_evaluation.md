# Model Evaluation Report

## Training Overview

- **Baseline dataset:** 36 synthetic support-ticket records in `ai/data/tickets.csv`, with 12 records per category.
- **Training implementation:** [`ai/train.py`](../ai/train.py).
- **Model:** TF-IDF vectorization using unigrams and bigrams, followed by Logistic Regression.
- **Test procedure:** Stratified 80/20 train/test split using `random_state=42`.
- **Test-set size:** 8 records, representing 20% of the 36-row baseline.
- **Cross-validation:** Five-fold stratified cross-validation on all 36 rows.
- **Final artifact:** After evaluation, the script retrains the pipeline on all 36 rows and saves `ai/model.joblib`.

These results apply to the documented 36-row baseline and its evaluation procedure. If [PR #47](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/47) merges its proposed 42-row dataset, coordinate a version and metrics update before attributing these figures to the new dataset.

Group B's separate six-ticket evaluation is documented in [PR #46](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/46). It is separate from the eight-record test split below. The Group B evaluation has already been exposed and is not a blind benchmark.

## Evaluation Results: 20% Test Split

The following results are the reported metrics for the eight records in the 20% test split.

| Metric | Result |
|---|---:|
| Accuracy | 0.625 (62.5%) |
| Access precision | 0.50 |
| Access recall | 1.00 |
| Billing precision | 0.67 |
| Billing recall | 0.67 |
| Technical precision | 1.00 |
| Technical recall | 0.33 |

The reported classification output was (the classification report rounds accuracy to 0.62; the unrounded test accuracy is 0.625):

```text
              precision    recall  f1-score   support

      access       0.50      1.00      0.67         2
     billing       0.67      0.67      0.67         3
   technical       1.00      0.33      0.50         3

    accuracy                           0.62         8
   macro avg       0.72      0.67      0.61         8
weighted avg       0.75      0.62      0.60         8
```

Because the test split contains only eight records, one incorrect prediction changes accuracy by 12.5 percentage points. These results should therefore be interpreted cautiously.

## Wrong Predictions on the Test Split

The following observed errors are from the eight-record test split:

```text
WRONG: technical -> billing | We updated our billing card details successfully, but the data export script hangs indefinitely at 99%
WRONG: technical -> access | Some settings are not being saved after I update them.
WRONG: billing -> access | Please send me a receipt for my most recent payment.
```

The first ticket combines billing-related wording with an export failure. Billing terms may have influenced the prediction, but this is a possible explanation rather than verified internal model reasoning.

The second ticket describes settings that are not being saved. Its wording may be ambiguous to a text classifier, but the exact reason for the prediction has not been verified.

The receipt request was also misclassified. These are observed examples, not proof of how the classifier will behave on other tickets.

## Cross-Validation: Separate Evaluation

The reported five-fold stratified cross-validation results on the 36-row baseline were:

```text
Cross-validation accuracy per fold: [0.875, 0.429, 0.429, 0.857, 0.571]
Cross-validation mean accuracy: 0.632 (+/- 0.198)
```

These results are separate from the eight-record test-split metrics. Cross-validation evaluates models fitted across different folds; it does not evaluate the final saved model as an independent, blind test.

## Final Saved Model

After the test-split and cross-validation steps, `ai/train.py` fits the pipeline on all 36 rows and saves `ai/model.joblib`.

The test-split scores describe the model fitted on the 80% training portion. The cross-validation scores summarize the five-fold evaluation procedure. Neither is an independent evaluation of the final model trained on all 36 rows.

## Limitations and Follow-up

- The dataset contains only 36 synthetic records and may not represent real support traffic.
- Technical recall was 0.33 on the eight-record test split, so human review is important.
- Group B's six-ticket evaluation in PR #46 is separate and already exposed, not a blind benchmark.
- If PR #47's proposed 42-row dataset merges, recheck the dataset version and rerun or confirm the appropriate evaluation before updating the reported metrics.
- Teammate/Group B review feedback and outcome remain pending until the review has actually occurred and its results are documented.
