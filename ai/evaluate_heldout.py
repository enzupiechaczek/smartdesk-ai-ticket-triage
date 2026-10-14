import argparse
import csv
import hashlib
import io
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai.predictor import predict_category

CSV_PATH = ROOT / "tests" / "held_out_tickets.csv"
VALID_CATEGORIES = {"access", "billing", "technical"}


def evaluate_csv(path, predictor):
    """Evaluate a local CSV and return results without retaining ticket text."""
    data = Path(path).read_bytes()
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")), strict=True)
    if reader.fieldnames != ["ticket_text", "category"]:
        raise ValueError("Evaluation CSV must have ticket_text,category columns.")
    rows = list(reader)
    if not rows:
        raise ValueError("The separate evaluation CSV contains no tickets.")

    cases = []
    for index, row in enumerate(rows, 1):
        case_id = f"CASE-{index:03d}"
        if set(row) != {"ticket_text", "category"} or not row["ticket_text"]:
            raise ValueError(f"Invalid evaluation row: {case_id}.")
        if not row["ticket_text"].strip() or not row["category"]:
            raise ValueError(f"Empty evaluation value: {case_id}.")
        expected = row["category"].strip().lower()
        if expected not in VALID_CATEGORIES:
            raise ValueError(f"Invalid expected category: {case_id}.")

        result = predictor(row["ticket_text"])
        predicted = result["category"].strip().lower()
        confidence = result["confidence"]
        if predicted not in VALID_CATEGORIES:
            raise ValueError(f"Invalid predicted category: {case_id}.")
        if not isinstance(confidence, (int, float)) or not math.isfinite(confidence):
            raise ValueError(f"Invalid confidence: {case_id}.")
        if not 0 <= confidence <= 1:
            raise ValueError(f"Confidence outside 0..1: {case_id}.")
        cases.append({
            "case_id": case_id,
            "expected": expected,
            "predicted": predicted,
            "confidence": confidence,
            "correct": expected == predicted,
        })

    return {
        "csv_sha256": hashlib.sha256(data).hexdigest(),
        "cases": cases,
        "correct": sum(case["correct"] for case in cases),
        "total": len(cases),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Count-only separate-set evaluation.")
    parser.add_argument("--csv", type=Path, default=CSV_PATH,
                        help="Path to the local-only evaluation CSV.")
    args = parser.parse_args(argv)
    try:
        results = evaluate_csv(args.csv, predict_category)
    except OSError:
        print("Error: Cannot read the local evaluation CSV.", file=sys.stderr)
        return 1
    except (UnicodeError, csv.Error, ValueError):
        print("Error: Invalid evaluation CSV or prediction data.", file=sys.stderr)
        return 1
    print("Separate evaluation set; ticket text is omitted.")
    print("Evaluation CSV SHA-256:", results["csv_sha256"])
    for case in results["cases"]:
        status = "OK" if case["correct"] else "MISS"
        print(f"{case['case_id']} | {status} | expected={case['expected']} | "
              f"predicted={case['predicted']} | confidence={case['confidence']:.3f}")
    correct, total = results["correct"], results["total"]
    print(f"Accuracy: {correct}/{total} ({correct / total:.1%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
