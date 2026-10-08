# SmartDesk Prediction Contract

## Function

`predict_category(text)` classifies plain ticket text into one of three categories and returns a confidence score.

## Input

- `text`: a plain-text string containing the support ticket. No extra metadata is needed.
- If `text` is empty, `None`, or contains only whitespace, the function raises a `ValueError("Ticket text must not be empty")`.

## Output

A dictionary with exactly these two keys:

- `category`: a string, exactly one of `"access"`, `"billing"` or `"technical"`.
- `confidence`: a number from 0 to 1, inclusive. A higher number means more certainty.

Example:

```python
{"category": "access", "confidence": 0.95}