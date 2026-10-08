# SmartDesk Prediction Contract

## Function

`predict_category(text)` classifies plain ticket text into one of three categories and returns a confidence score.

## Input

- If `text` is empty, `None`, or contains only whitespace, the function raises a `ValueError("Ticket text must not be empty")`.

## Output

A dictionary with exactly these two keys:

- `category`: a string, exactly one of `"access"`, `"billing"` or `"technical"`.
- `confidence`: a number from 0 to 1, inclusive. A higher number means more certainty.

Example:

```python
{"category": "access", "confidence": 0.95}
```

## Categories

- access: login, password, authentication, verification or account recovery problems.
- billing: payments, invoices, charges, subscriptions, receipts or refunds.
- technical: software errors, application behaviour, performance, uploads, downloads or other technical problems.

## Rules

- It works fully offline.
- It never calls Azure, OpenAI or any paid service.
- It never requires an API key.

## Trained model

`predict_category` loads the trained model from `ai/model.joblib`, which is created by `python ai/train.py`. If the file does not exist it raises `RuntimeError("Run python ai/train.py first")`. The confidence is the highest class probability, rounded to 3 decimals.