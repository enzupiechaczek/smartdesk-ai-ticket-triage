"""API contract tests isolated from trained models and development data."""
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))
import database

with patch.object(database, "init_db"):
    import app as app_module

from ai.predictor import ModelUnavailableError


class CreateTicketValidationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        db_patch = patch.object(database, "DB_PATH", Path(directory.name) / "test.db")
        db_patch.start()
        self.addCleanup(db_patch.stop)
        database.init_db()
        config_patch = patch.dict(app_module.app.config, TESTING=True)
        config_patch.start()
        self.addCleanup(config_patch.stop)
        prediction_patch = patch.object(app_module, "predict_category", return_value={"category": "access", "confidence": 0.8})
        self.predictor = prediction_patch.start()
        self.addCleanup(prediction_patch.stop)
        self.client = app_module.app.test_client()

    def post_json(self, body):
        return self.client.post("/api/tickets", json=body)

    def assert_rejected(self, response, error):
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": error})
        self.predictor.assert_not_called()

    def stored_tickets(self):
        response = self.client.get("/api/tickets")
        self.assertEqual(response.status_code, 200)
        return response.get_json()

    def test_valid_ticket_is_created(self):
        response = self.post_json({"subject": "Cannot log in", "description": "My reset link expired."})
        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertEqual(set(body), {"id", "subject", "description", "category", "confidence", "priority", "created_at"})
        self.assertIsInstance(body["id"], int)
        self.assertGreater(body["id"], 0)
        self.assertEqual(body["subject"], "Cannot log in")
        self.assertEqual(body["description"], "My reset link expired.")
        self.assertEqual(body["category"], "access")
        self.assertEqual(body["confidence"], 0.8)
        self.assertEqual(body["priority"], "normal")
        self.assertIsNotNone(datetime.fromisoformat(body["created_at"]).tzinfo)
        self.predictor.assert_called_once_with("Cannot log in. My reset link expired.")
        self.assertEqual(self.stored_tickets(), [body])
        self.assertEqual(self.stored_tickets(), [body])

    def test_body_must_be_a_json_object(self):
        for body in ([], [{"subject": "a", "description": "b"}], "text", 42, True):
            with self.subTest(body=body):
                self.assert_rejected(self.post_json(body), "Request body must be a JSON object")

    def test_null_body_is_rejected(self):
        response = self.client.post("/api/tickets", data="null", content_type="application/json")
        self.assert_rejected(response, "Request body must be a JSON object")

    def test_missing_or_invalid_json_is_rejected(self):
        self.assert_rejected(self.client.post("/api/tickets"), "Request body must be a JSON object")
        response = self.client.post("/api/tickets", data="{not json", content_type="application/json")
        self.assert_rejected(response, "Request body must be a JSON object")

    def test_subject_must_be_a_string(self):
        for subject in (None, 123, 1.5, True, ["a"], {"a": 1}):
            with self.subTest(subject=subject):
                self.assert_rejected(self.post_json({"subject": subject, "description": "Valid description"}), "Subject must be a string")

    def test_missing_subject_is_rejected(self):
        self.assert_rejected(self.post_json({"description": "Valid description"}), "Subject must be a string")

    def test_description_must_be_a_string(self):
        for description in (None, 123, 1.5, False, ["a"], {"a": 1}):
            with self.subTest(description=description):
                self.assert_rejected(self.post_json({"subject": "Valid subject", "description": description}), "Description must be a string")

    def test_missing_description_is_rejected(self):
        self.assert_rejected(self.post_json({"subject": "Valid subject"}), "Description must be a string")

    def test_blank_or_too_long_subject_is_rejected(self):
        for subject in ("", "   ", "x" * 101):
            with self.subTest(length=len(subject)):
                self.assert_rejected(self.post_json({"subject": subject, "description": "Valid description"}), "Subject is required (max 100 characters)")

    def test_blank_or_too_long_description_is_rejected(self):
        for description in ("", "   ", "x" * 501):
            with self.subTest(length=len(description)):
                self.assert_rejected(self.post_json({"subject": "Valid subject", "description": description}), "Description is required (max 500 characters)")

    def test_rejected_tickets_are_not_saved(self):
        self.assertEqual(self.stored_tickets(), [])
        self.post_json({"subject": None, "description": "Valid description"})
        self.post_json([])
        self.assertEqual(self.stored_tickets(), [])
        self.predictor.assert_not_called()

    def test_missing_model_returns_safe_503_and_saves_nothing(self):
        self.predictor.side_effect = ModelUnavailableError("PRIVATE_SENTINEL /private/model.joblib")
        response = self.post_json({"subject": "PRIVATE_TICKET", "description": "Synthetic case"})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json(), {"error": "Model not trained. Run python ai/train.py"})
        self.assertNotIn("PRIVATE", response.get_data(as_text=True))
        self.predictor.assert_called_once()
        self.assertEqual(self.stored_tickets(), [])

    def test_unexpected_runtime_error_is_not_hidden_as_model_unavailable(self):
        self.predictor.side_effect = RuntimeError("Unexpected implementation fault")
        with self.assertRaisesRegex(RuntimeError, "Unexpected implementation fault"):
            self.post_json({"subject": "Synthetic subject", "description": "Synthetic description"})
        self.assertEqual(self.stored_tickets(), [])

    def test_invalid_input_is_rejected_even_when_model_unavailable(self):
        self.predictor.side_effect = ModelUnavailableError("Unavailable")
        self.assert_rejected(self.post_json({"subject": "", "description": "Synthetic"}), "Subject is required (max 100 characters)")
        self.assertEqual(self.stored_tickets(), [])

    def test_duplicate_submissions_have_distinct_persisted_ids(self):
        payload = {"subject": "Synthetic subject", "description": "Synthetic description"}
        first = self.post_json(payload)
        second = self.post_json(payload)
        self.assertEqual((first.status_code, second.status_code), (201, 201))
        a, b = first.get_json(), second.get_json()
        self.assertNotEqual(a["id"], b["id"])
        self.assertEqual(self.stored_tickets(), [b, a])

    def test_urgent_priority_and_trimmed_values_are_persisted(self):
        response = self.post_json({"subject": "  Outage  ", "description": "  Synthetic service issue  "})
        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertEqual(body["subject"], "Outage")
        self.assertEqual(body["description"], "Synthetic service issue")
        self.assertEqual(body["priority"], "urgent")
        self.assertEqual(self.stored_tickets(), [body])


if __name__ == "__main__":
    unittest.main()
