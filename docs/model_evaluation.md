# Model Evaluation Report

Historical author-reported results from the original PR #47; original run timestamps, tested revisions, and captured outputs were not supplied. These values are not a fresh verification of the updated 42-row model. The six evaluation cases were previously exposed in Git history, so this is a separate evaluation set rather than a blind benchmark. Versioned fresh-run evidence is being prepared locally.

## 1. Training Overview

* **Algorithm:** Logistic Regression with TF-IDF Vectorizer (unigrams and bigrams)
* **Training and validation split:** 80% training / 20% validation, stratified
* **Training dataset size:** 36 synthetic ticket samples
* **Evaluation tasks:** Day 2 validation and cross-validation (baseline), followed by Day 3 separate-set evaluation (Task 2930)

## 2. Day 2 — Validation Results

### Validation Performance

```text
Accuracy: 0.625

              precision    recall  f1-score   support

      access       0.50      1.00      0.67         2
     billing       0.67      0.67      0.67         3
   technical       1.00      0.33      0.50         3

    accuracy                           0.62         8
   macro avg       0.72      0.67      0.61         8
weighted avg       0.75      0.62      0.60         8
```

### Incorrect Predictions on the Validation Split

```text
WRONG: technical -> billing | We updated our billing card details successfully, but the data export script hangs indefinitely at 99%
WRONG: technical -> access | Some settings are not being saved after I update them.
WRONG: billing -> access | Please send me a receipt for my most recent payment.
```

### Five-Fold Stratified Cross-Validation

```text
Cross-validation accuracy per fold: [0.875, 0.429, 0.429, 0.857, 0.571]
Cross-validation mean accuracy: 0.632 (+/- 0.198)
```

### Interpretation of Day 2 Results

* The validation split contained only eight tickets. One additional incorrect prediction would change its accuracy by 12.5 percentage points.
* The technical category had the lowest recall (0.33). Two of the three technical tickets in the validation split were misclassified.
* One misclassified ticket combined billing-related wording with a technical issue involving a data export that stopped progressing. The model predicted billing, likely because of the billing-related terms.
* Another technical ticket described settings that would not save. The model predicted access, suggesting difficulty distinguishing account-access issues from technical problems.
* A billing ticket requesting a receipt was classified as access. The short text may not have provided enough distinctive billing-related language.
* The cross-validation mean accuracy was 63.2%, with a standard deviation of 19.8 percentage points. The variation between folds indicates that the small dataset produces inconsistent results across different splits.

## 3. Day 3 — Separate-Set Ticket Evaluation (Task 2930)

### Evaluation Method

The saved model (`ai/model.joblib`) was evaluated against the six separate-set tickets supplied by Group B in `tests/held_out_tickets.csv`. The evaluation script (`ai/evaluate_heldout.py`) passed each ticket to the existing prediction function and compared the predicted category with the expected category.

The script normalizes category labels by converting them to lowercase and removing surrounding whitespace before comparison. The separate-set tickets were kept separate from the training dataset, and the existing saved model was used without retraining during this evaluation.

### Separate-Set Results

|  # | Expected Category | Predicted Category | Confidence | Result    |
| -: | ----------------- | ------------------ | ---------: | --------- |
|  1 | access            | billing            |      0.413 | Incorrect |
|  2 | access            | access             |      0.814 | Correct   |
|  3 | billing           | billing            |      0.682 | Correct   |
|  4 | billing           | billing            |      0.690 | Correct   |
|  5 | technical         | access             |      0.465 | Incorrect |
|  6 | technical         | technical          |      0.763 | Correct   |

**Correct predictions:** 4 out of 6

**Separate-set accuracy:** 66.7%

### Comparison with Day 2

The Day 3 separate-set accuracy was 66.7%, compared with 62.5% on the Day 2 validation split and a 63.2% mean accuracy in Day 2 cross-validation. Although the separate-set score was higher than both Day 2 figures, the six-ticket sample is too small to establish that the model has improved or will perform similarly on future tickets.

### Day 3 Error Analysis

Two of the six separate-set tickets were misclassified:

1. **Access predicted as billing:** The request concerned updating the registered email address on a workspace account. The model predicted billing with a confidence of 0.413.
2. **Technical predicted as access:** The request stated that the user was unable to update their email. The model predicted access with a confidence of 0.465.

Both errors involved email updates, suggesting that short requests about account settings may be difficult to classify consistently. The model may benefit from more varied training examples that distinguish account-access requests from technical problems involving settings or profile updates.

### Comparison Summary

| Metric                          |                     Day 2 |              Day 3 |
| ------------------------------- | ------------------------: | -----------------: |
| Validation or separate-set accuracy |                     62.5% |              66.7% |
| Dataset evaluated               | 8-ticket validation split | 6 separate-set tickets |
| Cross-validation mean accuracy  |                     63.2% |     Not calculated |

The Day 2 validation and Day 3 separate-set scores come from different ticket sets and should be treated as separate measurements. The Day 3 result provides an additional check on the saved model, rather than proof of a performance improvement.

## 4. Limitations and Next Steps

* **Small datasets:** The original training dataset contains 36 synthetic samples, and the separate-set evaluation contains only six tickets.
* **Sensitivity to individual errors:** Each incorrect prediction changes the Day 3 accuracy by approximately 16.7 percentage points.
* **Category overlap:** Short requests involving email updates, account settings, and access may contain similar language across categories.
* **Confidence interpretation:** Prediction confidence is the model's reported probability for its selected category; it should not automatically be treated as a guarantee that the prediction is correct.
* **Future improvements:** Add more varied, accurately labelled training examples, particularly for ambiguous account-setting and technical requests, then evaluate changes using a separate separate-set dataset.
* **Evaluation integrity:** Keep separate-set tickets separate from training data so that the evaluation remains meaningful.

## 5. Conclusion

The saved ticket-classification model correctly classified four of the six separate-set tickets, achieving an accuracy of 66.7%. The evaluation identified confusion between access and technical requests involving email updates, providing a concrete area for future improvement while highlighting the need for a larger evaluation dataset.
