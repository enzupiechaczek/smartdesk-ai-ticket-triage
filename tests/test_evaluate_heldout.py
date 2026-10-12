import contextlib
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from ai import evaluate_heldout


class SeparateEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "evaluation.csv"

    def write_csv(self, content):
        self.path.write_text(content, encoding="utf-8")

    def test_cli_reports_ids_and_counts_without_private_text(self):
        self.write_csv("ticket_text,category\nPRIVATE_SYNTHETIC_SENTINEL,access\n")
        predictor = Mock(return_value={"category": "access", "confidence": 0.8})
        output = io.StringIO()
        with patch.object(evaluate_heldout, "predict_category", predictor):
            with contextlib.redirect_stdout(output):
                evaluate_heldout.main(["--csv", str(self.path)])
        text = output.getvalue()
        self.assertIn("CASE-001 | OK | expected=access", text)
        self.assertIn("Accuracy: 1/1 (100.0%)", text)
        self.assertIn(hashlib.sha256(self.path.read_bytes()).hexdigest(), text)
        self.assertNotIn("PRIVATE_SYNTHETIC_SENTINEL", text)

    def test_results_count_misclassifications_and_normalize_labels(self):
        self.write_csv("ticket_text,category\nFirst synthetic case, Access \nSecond synthetic case,billing\n")
        predictor = Mock(side_effect=[
            {"category": "ACCESS", "confidence": 0.7},
            {"category": "technical", "confidence": 0.6},
        ])
        result = evaluate_heldout.evaluate_csv(self.path, predictor)
        self.assertEqual((result["correct"], result["total"]), (1, 2))
        self.assertEqual(result["cases"][1]["case_id"], "CASE-002")
        self.assertNotIn("ticket_text", result["cases"][0])

    def test_rejects_empty_file_and_invalid_columns_before_prediction(self):
        predictor = Mock()
        for content in ("ticket_text,category\n", "text,category\nSynthetic,access\n"):
            with self.subTest(content=content):
                self.write_csv(content)
                with self.assertRaises(ValueError):
                    evaluate_heldout.evaluate_csv(self.path, predictor)
        predictor.assert_not_called()

    def test_invalid_row_errors_do_not_disclose_private_text(self):
        for content in (
            "ticket_text,category\nPRIVATE_SYNTHETIC_SENTINEL,unknown\n",
            "ticket_text,category\nPRIVATE_SYNTHETIC_SENTINEL,access,extra\n",
        ):
            with self.subTest(content=content):
                self.write_csv(content)
                with self.assertRaises(ValueError) as error:
                    evaluate_heldout.evaluate_csv(self.path, Mock())
                self.assertNotIn("PRIVATE_SYNTHETIC_SENTINEL", str(error.exception))


if __name__ == "__main__":
    unittest.main()
