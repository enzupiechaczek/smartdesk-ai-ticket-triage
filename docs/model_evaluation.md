# Model Evaluation Report

## 1. Training Overview

* **Algorithm:** Logistic Regression with TF-IDF Vectorizer (unigrams and bigrams)
* **Training and validation split:** 80% training / 20% validation, stratified
* **Training dataset size:** 36 synthetic ticket samples
* **Evaluation tasks:** Day 2 validation and cross-validation (baseline), followed by Day 3 held-out evaluation (Task 2930)

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

## 3. Day 3 — Held-Out Ticket Evaluation (Task 2930)

### Evaluation Method

The saved model (`ai/model.joblib`) was evaluated against the six held-out tickets supplied by Group B in `tests/held_out_tickets.csv`. The evaluation script (`ai/evaluate_heldout.py`) passed each ticket to the existing prediction function and compared the predicted category with the expected category.

The script normalizes category labels by converting them to lowercase and removing surrounding whitespace before comparison. The held-out tickets were kept separate from the training dataset, and the existing saved model was used without retraining during this evaluation.

### Fresh Held-Out Results

#### Reproducibility Evidence

* **Run date:** 2026-10-12
* **Checkout commit:** `f0c684a4cc0ea78c254eeb932314cf3bc603e1a5`
* **Evaluator SHA-256:** `99dec36583039c9344d0a910c97c40fee6d6bbe09880f0e3edab5275254c664b`
  The evaluator was a staged working-tree change during this run, so this hash identifies the exact tested evaluator source; it is not part of the checkout commit above.
* **Evaluation CSV:** `tests/held_out_tickets.csv`
* **Evaluation CSV SHA-256:** `994997e3f47ae53eef85e38d344c6a9ae726f2df5bcbd2b18a3daa65e270ebaf`
* **Model artifact:** local, Git-ignored `ai/model.joblib`; SHA-256 `bddcbfa2781a0bdb5b2a3ba0a99a8d9d4d965001603c79025ecf2e8113696a92`
* **Training script:** `ai/train.py`; SHA-256 `60ab4a8dacc05d06da053c2a75c75cbe20e85d3b92150b27b84b6877da35af01`
* **Training CSV:** `ai/data/tickets.csv` (36 rows); SHA-256 `f3eea6dcfca3bd7786a04874ca00f7041ab169ba752653e9e703e071e29a4b71`
* **Model provenance:** The recorded training recipe builds a lowercase unigram/bigram TF-IDF and Logistic Regression (`C=10`, `max_iter=1000`) pipeline, evaluates it, refits it on all 36 training rows, and saves it with `joblib`. That script was not run for this evaluation; the pre-existing local artifact was used. Because the artifact is ignored and carries no recorded training metadata, its creation history cannot be independently verified from the repository.
* **Exact command:** `.venv/bin/python ai/evaluate_heldout.py`

Captured output from that command:

```text
MISS | case-01 | expected=access | predicted=billing | confidence=0.413
OK | case-02 | expected=access | predicted=access | confidence=0.814
OK | case-03 | expected=billing | predicted=billing | confidence=0.682
OK | case-04 | expected=billing | predicted=billing | confidence=0.69
MISS | case-05 | expected=technical | predicted=access | confidence=0.465
OK | case-06 | expected=technical | predicted=technical | confidence=0.763

Accuracy: 4/6 (66.7%)
```

**Correct predictions:** 4 out of 6

**Held-out accuracy:** 66.7%

### Comparison with Day 2

The Day 3 held-out accuracy was 66.7%, compared with 62.5% on the Day 2 validation split and a 63.2% mean accuracy in Day 2 cross-validation. Although the held-out score was higher than both Day 2 figures, the six-ticket sample is too small to establish that the model has improved or will perform similarly on future tickets.

### Day 3 Error Analysis

Two of the six held-out tickets were misclassified:

1. **Access predicted as billing:** The request concerned updating the registered email address on a workspace account. The model predicted billing with a confidence of 0.413.
2. **Technical predicted as access:** The request stated that the user was unable to update their email. The model predicted access with a confidence of 0.465.

Both errors involved email updates, suggesting that short requests about account settings may be difficult to classify consistently. The model may benefit from more varied training examples that distinguish account-access requests from technical problems involving settings or profile updates.

### Comparison Summary

| Metric                          |                     Day 2 |              Day 3 |
| ------------------------------- | ------------------------: | -----------------: |
| Validation or held-out accuracy |                     62.5% |              66.7% |
| Dataset evaluated               | 8-ticket validation split | 6 held-out tickets |
| Cross-validation mean accuracy  |                     63.2% |     Not calculated |

The Day 2 validation and Day 3 held-out scores come from different ticket sets and should be treated as separate measurements. The Day 3 result provides an additional check on the saved model, rather than proof of a performance improvement.

## 4. Limitations and Next Steps

* **Small datasets:** The original training dataset contains 36 synthetic samples, and the held-out evaluation contains only six tickets.
* **Sensitivity to individual errors:** Each incorrect prediction changes the Day 3 accuracy by approximately 16.7 percentage points.
* **Category overlap:** Short requests involving email updates, account settings, and access may contain similar language across categories.
* **Confidence interpretation:** Prediction confidence is the model's reported probability for its selected category; it should not automatically be treated as a guarantee that the prediction is correct.
* **Future improvements:** Add more varied, accurately labelled training examples, particularly for ambiguous account-setting and technical requests, then evaluate changes using a separate held-out dataset.
* **Evaluation integrity:** Keep held-out tickets separate from training data so that the evaluation remains meaningful.

## 5. Conclusion

The saved ticket-classification model correctly classified four of the six held-out tickets, achieving an accuracy of 66.7%. The evaluation identified confusion between access and technical requests involving email updates, providing a concrete area for future improvement while highlighting the need for a larger evaluation dataset.
