import csv
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

BASE = Path(__file__).parent

# 1. Load the synthetic ticket dataset
with open(BASE / "data" / "tickets.csv", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

texts = [r["ticket_text"] for r in rows]
labels = [r["category"] for r in rows]

# 2. Split dataset into train (80%) and validation test (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

# 3. Build text-classification pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
    ("clf", LogisticRegression(C=10, max_iter=1000)),
])

# 4. Train and evaluate on held-out test split
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))
print("Wrong predictions on the test split:")
for text, true, guess in zip(X_test, y_test, pred):
    if true != guess:
        print("WRONG:", true, "->", guess, "|", text)

# 4b. More reliable estimate: 5-fold stratified cross-validation on all rows
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, texts, labels, cv=cv, scoring="accuracy")
print("Cross-validation accuracy per fold:", [round(s, 3) for s in scores])
print("Cross-validation mean accuracy: %.3f (+/- %.3f)" % (scores.mean(), scores.std()))


# 5. Retrain on all available data and export artifacts
model.fit(texts, labels)  # retrain on all data after evaluating
joblib.dump(model, BASE / "model.joblib")
print("Saved model.joblib")
