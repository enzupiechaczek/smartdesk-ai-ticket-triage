
import csv
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

BASE = Path(__file__).parent
with open(BASE / "data" / "tickets.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
texts = [r["ticket_text"] for r in rows]
labels = [r["category"] for r in rows]

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels)

model = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
    ("clf", LogisticRegression(C=10, max_iter=1000)),
])
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))

model.fit(texts, labels)  # retrain on all data after evaluating
joblib.dump(model, BASE / "model.joblib")
print("Saved model.joblib")