import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "model.joblib"
_model = None

def predict_category(text):
    global _model
    if not text or not text.strip():
        raise ValueError("Ticket text must not be empty")
    if _model is None:
        if not MODEL_PATH.exists():
            raise RuntimeError("Run python ai/train.py first")
        _model = joblib.load(MODEL_PATH)
    probs = _model.predict_proba([text])[0]
    best = probs.argmax()
    return {"category": str(_model.classes_[best]),
            "confidence": round(float(probs[best]), 3)}
            