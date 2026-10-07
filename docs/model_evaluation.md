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
```

## Wrong predictions on the test split

```text
WRONG: technical -> billing | We updated our billing card details successfully, but the data export script hangs indefinitely at 99%
WRONG: technical -> access | Some settings are not being saved after I update them.
WRONG: billing -> access | Please send me a receipt for my most recent payment.
```

## Cross-validation (5-fold, stratified)

```text
Cross-validation accuracy per fold: [0.875, 0.429, 0.429, 0.857, 0.571]
Cross-validation mean accuracy: 0.632 (+/- 0.198)
```

## How to read these results

- The test split has only 8 tickets, so one wrong prediction changes accuracy by 12.5 points. The cross-validation mean is the more reliable number.
- The technical class had the lowest recall (0.33) on the test split. Two of the three technical tickets were wrong. One mixes a billing topic (updating a billing card) with a technical problem (an export script that hangs), so the model followed the billing words. The other ("Some settings are not being saved after I update them.") is short and has no clear technical keyword, so the model guessed access.
- One billing ticket ("Please send me a receipt for my most recent payment.") was predicted as access. It is short and has no strong billing word such as invoice or charge.
- The saved model (ai/model.joblib) is trained on all 36 rows after the evaluation, so these scores describe the 80% model, not the final one.
- The dataset is small (36 synthetic rows). More and more varied rows are the most likely way to improve the scores.
- Next step: ai/predictor.py will load model.joblib to replace the temporary stub (task A2-2.3).
