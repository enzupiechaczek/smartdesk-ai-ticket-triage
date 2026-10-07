# Model Evaluation Report

## Training Overview
- **Algorithm**: Logistic Regression with TF-IDF Vectorizer (unigrams + bigrams)
- **Train/Test Split**: 80% train / 20% validation split (stratified)
- **Dataset Size**: 36 synthetic samples

## Evaluation Results

```text
Accuracy: 0.625

              precision    recall  f1-score   support

      access       0.50      1.00      0.67         2
     billing       0.67      0.67      0.67         3
   technical       1.00      0.33      0.50         3

    accuracy                           0.62         8
   macro avg       0.72      0.67      0.61         8
weighted avg       0.75      0.62      0.60         8


## Wrong predictions on the test split
  Wrong predictions on the test split:
  WRONG: technical -> billing | We updated our billing card details successfully, but the data export script hangs indefinitely at 99%
  WRONG: technical -> access | Some settings are not being saved after I update them.
  WRONG: billing -> access | Please send me a receipt for my most recent payment.

## Cross-validation (5-fold,stratifield)
  Cross-validation accuracy per fold: [np.float64(0.875), np.float64(0.429), np.float64(0.429), np.float64(0.857), np.float64(0.571)]
  Cross-validation mean accuracy: 0.632 (+/- 0.198)
  Saved model.joblib

## How to read these result
 - The test split has only 8 tickets, so one wrong prediction changes accuracy by 12.5 points. The cross-validation mean is the more reliable number.
- The technical class had the lowest recall (0.33) on the test split. WRITE ONE OR TWO SENTENCES: which technical tickets were wrong, and what they look like (very short, mixed topics, typos?).
- The saved model (ai/model.joblib) is trained on all 36 rows after the evaluation, so these scores describe the 80% model, not the final one.
- The dataset is small (36 synthetic rows). More and more varied rows are the most likely way to improve the scores.
- Next step: ai/predictor.py will load model.joblib to replace the temporary stub (task A2-2.3).