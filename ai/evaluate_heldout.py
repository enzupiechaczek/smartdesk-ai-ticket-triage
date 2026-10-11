import csv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ai.predictor import predict_category

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "tests" / "held_out_tickets.csv"


def main():
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise ValueError("The held-out CSV contains no tickets.")

    correct = 0

    for row in rows:
        expected = row["category"].strip().lower()
        result = predict_category(row["ticket_text"])
        predicted = result["category"].strip().lower()
        matched = expected == predicted

        if matched:
            correct += 1

        status = "OK" if matched else "MISS"
        print(
            f"{status} | expected={expected} | "
            f"predicted={predicted} | "
            f"confidence={result['confidence']} | "
            f"ticket={row['ticket_text']}"
        )

    accuracy = correct / len(rows) * 100
    print(f"\nAccuracy: {correct}/{len(rows)} ({accuracy:.1f}%)")


if __name__ == "__main__":
    main()