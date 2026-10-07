# Model contract

# SmartDesk Prediction Contract

## Function

`predict_category(text)`

The function takes plain ticket text as input and returns a dictionary containing the predicted category and confidence score.

### Input

- `text`: Plain text string representing the support ticket.

### Output

A dictionary with:

- `category`: String, strictly one of `"access"`, `"billing"`, or `"technical"`.
- `confidence`: Float from `0.0` to `1.0` representing prediction confidence.

Example:

```python
{
    "category": "technical",
    "confidence": 0.5
}