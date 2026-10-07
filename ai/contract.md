# SmartDesk Prediction Contract

## Function

`predict_category(text)` classifies plain ticket text into one of three categories and returns a confidence score.

## Input

- `text`: a plain-text string containing the support ticket. No extra metadata is needed.

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

## Temporary stub

Until the trained model replaces it on Day 2, `predict_category` always returns `technical` with confidence `0.5`.