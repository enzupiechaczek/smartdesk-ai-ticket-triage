# Model Evaluation Report

## 1. Training Overview

* **Algorithm:** Logistic Regression with TF-IDF Vectorizer (unigrams and bigrams)
* **Training dataset:** 36 synthetic ticket samples in `ai/data/tickets.csv` (12 access, 12 billing, 12 technical)
* **Training script:** `ai/train.py`
* **Evaluation tasks:** Day 2 validation and cross-validation, followed by Day 3 held-out evaluation (Task 2930)

### Model Versions

`ai/train.py` describes several models built from the same 36-row dataset, and each result in this report belongs to a specific one:

* **Split model:** trained on the 28-row stratified training split (80%). Produces the Day 2 validation result.
* **Cross-validation fold models:** five pipelines, each trained on four of the five folds (28 or 29 rows). Produce the Day 2 cross-validation result.
* **Final model (training recipe):** the recorded training script refits a final model on all 36 rows after the split and cross-validation steps and saves it as `ai/model.joblib`, the file the application loads.
* **Day 3 evaluated artifact:** a pre-existing local `ai/model.joblib`, identified by its recorded SHA-256 (`bddcbfa2…`, full hash under Reproducibility Evidence). Its original training session and dataset association were not independently verified from recorded artifact metadata. The recipe above describes intended model construction, not independently established provenance of this particular artifact. This artifact is the only model evaluated in Day 3.

None of the Day 2 figures were measured on the Day 3 artifact. A model trained on changed data (such as the 42-row dataset proposed in PR #47), or a newly trained 36-row artifact, is a different version and needs its own separately identified training session and results.

## 2. Day 2 — Validation Results

These results come from the split model and the cross-validation fold models, not from the Day 3 evaluated artifact.

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

A pre-existing local model artifact at `ai/model.joblib`, identified by its recorded SHA-256 (`bddcbfa2…`), was evaluated against the six held-out tickets supplied by Group B in the local-only, Git-ignored `tests/held_out_tickets.csv`. The recorded training script refits a final model on all 36 rows and saves it to that path, but this artifact's original training session and dataset association were not independently verified from recorded artifact metadata. The evaluation script (`ai/evaluate_heldout.py`) passed each ticket to the existing prediction function and compared the predicted category with the expected category.

The script normalizes category labels by converting them to lowercase and removing surrounding whitespace before comparison. None of the six ticket texts appear in the recorded 36-row training CSV. Because the artifact's training data was not independently verified, this check covers the recorded dataset, not the artifact itself. The artifact was used as found, without retraining, during this evaluation.

### Fresh Held-Out Results

#### Reproducibility Evidence

* **Run date:** 2026-10-12
* **Checkout commit:** `f0c684a4cc0ea78c254eeb932314cf3bc603e1a5`
* **Evaluator SHA-256:** `99dec36583039c9344d0a910c97c40fee6d6bbe09880f0e3edab5275254c664b`
  The evaluator was a staged working-tree change during this run, so this hash identifies the exact tested evaluator source; it is not part of the checkout commit above. The same source (identical SHA-256) was later committed in `375f997`.
* **Evaluation CSV:** `tests/held_out_tickets.csv` (local-only and Git-ignored; not tracked in this branch)
* **Evaluation CSV SHA-256:** `994997e3f47ae53eef85e38d344c6a9ae726f2df5bcbd2b18a3daa65e270ebaf`
* **Model artifact:** local, Git-ignored `ai/model.joblib`; SHA-256 `bddcbfa2781a0bdb5b2a3ba0a99a8d9d4d965001603c79025ecf2e8113696a92`
* **Training script:** `ai/train.py`; SHA-256 `60ab4a8dacc05d06da053c2a75c75cbe20e85d3b92150b27b84b6877da35af01`
* **Training CSV:** `ai/data/tickets.csv` (36 rows); SHA-256 `f3eea6dcfca3bd7786a04874ca00f7041ab169ba752653e9e703e071e29a4b71`
* **Model provenance:** The recorded training script builds a lowercase unigram/bigram TF-IDF and Logistic Regression (`C=10`, `max_iter=1000`) pipeline, evaluates it, refits a final model on all 36 rows and saves `ai/model.joblib`. That script was not run for this evaluation. This evaluation used a pre-existing local artifact identified by the SHA-256 above. Its original training session and dataset association were not independently verified from recorded artifact metadata. The recipe describes intended model construction, not independently established provenance of this particular artifact.
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

### Day 3 Error Analysis

Two of the six held-out tickets were misclassified:

1. **Access predicted as billing:** The request concerned updating the registered email address on a workspace account. The model predicted billing with a confidence of 0.413.
2. **Technical predicted as access:** The request stated that the user was unable to update their email. The model predicted access with a confidence of 0.465.

Both errors involved email updates, suggesting that short requests about account settings may be difficult to classify consistently. The model may benefit from more varied training examples that distinguish account-access requests from technical problems involving settings or profile updates.

### Relationship to Day 2 Results

The three accuracy figures in this report measure different models on different cases:

| Measurement                      | Model evaluated                                                                                          | Cases evaluated                                                                   |    Accuracy |
| -------------------------------- | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ----------: |
| Day 2 validation split           | Split model (28 training rows)                                                                           | 8 tickets held back from the training dataset                                     | 62.5% (5/8) |
| Day 2 five-fold cross-validation | Five fold models (28 or 29 rows each)                                                                    | All 36 training rows, each scored by the fold model that excluded it              |  63.2% mean |
| Day 3 held-out set               | Pre-existing `ai/model.joblib` (`bddcbfa2…`); recipe: all 36 rows, provenance not independently verified | 6 Group B tickets, separate from the recorded training CSV but previously exposed | 66.7% (4/6) |

Because the models and evaluation cases differ, these figures are not a controlled comparison and should not be read as evidence that the model improved between Day 2 and Day 3. The differences between the Day 3 figure and the two Day 2 figures (4.2 and 3.5 percentage points) are smaller than the effect of a single prediction on either the validation split (12.5 points) or the held-out set (16.7 points).

## 4. Limitations and Next Steps

* **Small datasets:** The original training dataset contains 36 synthetic samples, and the held-out evaluation contains only six tickets.
* **Sensitivity to individual errors:** Each incorrect prediction changes the Day 3 accuracy by approximately 16.7 percentage points.
* **Category overlap:** Short requests involving email updates, account settings, and access may contain similar language across categories.
* **Confidence interpretation:** Prediction confidence is the model's reported probability for its selected category; it should not automatically be treated as a guarantee that the prediction is correct.
* **Future improvements:** Add more varied, accurately labelled training examples, particularly for ambiguous account-setting and technical requests, then evaluate changes using a separate held-out dataset.
* **Evaluation integrity:** This six-ticket set has already been exposed in the repository history and can no longer serve as a blind benchmark. A blind check of a future model needs a new set that is kept local-only and is not consulted when choosing training examples.
* **Model versions:** Results for any retrained model should name the training dataset and model they were measured on, and should not be combined with the 36-row results above.
* **Artifact provenance:** The Day 3 artifact carries no recorded training metadata, so its link to the 36-row recipe is intended, not verified. Future evaluations should record the training commit, dataset hash and artifact hash when the artifact is created.

## 5. Conclusion

The pre-existing `ai/model.joblib` artifact identified by SHA-256 `bddcbfa2…` correctly classified four of the six held-out tickets, achieving an accuracy of 66.7%. This is the result of that identified artifact. The recorded recipe trains the final model on all 36 rows, but this artifact's original training session and dataset association were not independently verified. Because this set was previously exposed, the result is not a blind benchmark. It is also not directly comparable with the Day 2 validation (62.5%) and cross-validation (63.2%) figures, which were measured on different models and cases. The evaluation identified confusion between access and technical requests involving email updates, providing a concrete area for future improvement while highlighting the need for a larger evaluation dataset.
