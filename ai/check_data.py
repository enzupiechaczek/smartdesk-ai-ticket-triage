import csv
from collections import Counter
from pathlib import Path

PATH = Path(__file__).parent / "data" / "tickets.csv"
VALID = {"access", "billing", "technical"}

with open(PATH, encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

texts = [r["ticket_text"].strip().lower() for r in rows]
labels = [r["category"].strip() for r in rows]
counts = Counter(labels)

print("rows:", len(rows), "unique:", len(set(texts)))
print("per category:", dict(counts))

problems = []
if any(label not in VALID for label in labels):
    problems.append("invalid label found")
if any(not text for text in texts):
    problems.append("empty ticket text found")
if len(set(texts)) != len(texts):
    problems.append("duplicate ticket text found")
if len(set(counts.values())) != 1:
    problems.append("categories are not balanced")

print("PROBLEMS: " + "; ".join(problems) if problems else "OK: no problems found")
