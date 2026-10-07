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