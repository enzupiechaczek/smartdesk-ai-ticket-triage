# Placeholder. Group A2 writes the stub in task A2-1.2 and the real predictor in task A2-2.3.
import csv
rows = list(csv.DictReader(open("ai/data/tickets.csv", encoding="utf-8")))
texts = [r["ticket_text"].strip().lower() for r in rows]
print("rows:", len(texts), "unique:", len(set(texts)))