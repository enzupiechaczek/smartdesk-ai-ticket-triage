# Model contract

## Function

Import `predict_category` from `ai.predictor` and call `predict_category(text)`.

- **Input:** `text`, a Python `str` containing plain ticket text.
- **Output:** a Python `dict` with these fields:
  - `category`: one of `"access"`, `"billing"`, or `"technical"`.
  - `confidence`: a number from `0` to `1`, inclusive, indicating confidence in the predicted category.

Callers should pass a string. Input validation and handling of other input types are outside this contract.

## Runtime rules

1. The predictor works offline.
2. It never calls Azure, OpenAI, or any paid service.
3. It never needs an API key or any other key.

## Day 1 temporary stub

The stub always returns `{"category": "technical", "confidence": 0.5}` regardless of the text. This is a fixed placeholder, not a trained prediction or a measured confidence score. It needs only Python, with no model files or extra packages.

On Day 2, the trained model replaces the stub while preserving the import path, function name, input, output fields, allowed categories, confidence range, and runtime rules. The predicted values may change.

## A1 import check

Run Python from the repository root:

```python
from ai.predictor import predict_category

result = predict_category("The application crashes when I upload a file")
assert result == {"category": "technical", "confidence": 0.5}
print(result)
```

Expected output for the Day 1 stub:

```text
{'category': 'technical', 'confidence': 0.5}
```

An A1 member should run this check and leave a comment on the pull request confirming that the import and call succeeded. A local check by A2 does not replace A1's confirmation.
