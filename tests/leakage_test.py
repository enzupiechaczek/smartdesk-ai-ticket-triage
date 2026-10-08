import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAIN = ROOT / "ai" / "data" / "tickets.csv"
HELD_OUT = ROOT / "tests" / "held_out_tickets.csv"


def normalise(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def load(path):
    with open(path, encoding="utf-8", newline="") as f:
        return {normalise(r["ticket_text"]) for r in csv.DictReader(f)}


if not HELD_OUT.exists():
    print("Missing", HELD_OUT, "- copy the real held-out file there first.")
    sys.exit(2)

train = load(TRAIN)
held_out = load(HELD_OUT)
overlap = train & held_out
print("Training rows (unique):", len(train))
print("Held-out rows (unique):", len(held_out))
print("Overlap:", overlap)
sys.exit(1 if overlap else 0)
