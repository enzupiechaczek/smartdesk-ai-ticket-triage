"""Validation tests for POST /api/tickets.

Run from the repository root:  python -m unittest discover -s backend -p "test_*.py" -v
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

import database

# Point the app at a throwaway database before it is imported (app.py calls init_db() on import).
_tmp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
database.DB_PATH = Path(_tmp_dir.name) / "test.db"

from app import app

class CreateTicketValidationTests(unittest.TestCase):
    def setUp(self):
        if database.DB_PATH.exists():
            database.DB_PATH.unlink()
        database.init_db()
        self.client = app.test_client()

    def post_json(self, body):
        return self.client.post("/api/tickets", json=body)

    def assert_rejected(self, response, error):
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": error})

    def test_valid_ticket_is_created(self):
        response = self.post_json(
            {"subject": "Cannot log in", "description": "My reset link expired."}
        )
        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertEqual(body["subject"], "Cannot log in")
        self.assertIn(body["category"], {"access", "billing", "technical"})

    def test_body_must_be_a_json_object(self):
        for body in ([], [{"subject": "a", "description": "b"}], "text", 42, True):
            with self.subTest(body=body):
                self.assert_rejected(
                    self.post_json(body), "Request body must be a JSON object"
                )

    def test_null_body_is_rejected(self):
        response = self.client.post(
            "/api/tickets", data="null", content_type="application/json"
        )
        self.assert_rejected(response, "Request body must be a JSON object")

    def test_missing_or_invalid_json_is_rejected(self):
        self.assert_rejected(
            self.client.post("/api/tickets"), "Request body must be a JSON object"
        )
        response = self.client.post(
            "/api/tickets", data="{not json", content_type="application/json"
        )
        self.assert_rejected(response, "Request body must be a JSON object")

    def test_subject_must_be_a_string(self):
        for subject in (None, 123, 1.5, True, ["a"], {"a": 1}):
            with self.subTest(subject=subject):
                response = self.post_json(
                    {"subject": subject, "description": "Valid description"}
                )
                self.assert_rejected(response, "Subject must be a string")

    def test_missing_subject_is_rejected(self):
        self.assert_rejected(
            self.post_json({"description": "Valid description"}),
            "Subject must be a string",
        )

    def test_description_must_be_a_string(self):
        for description in (None, 123, 1.5, False, ["a"], {"a": 1}):
            with self.subTest(description=description):
                response = self.post_json(
                    {"subject": "Valid subject", "description": description}
                )
                self.assert_rejected(response, "Description must be a string")

    def test_missing_description_is_rejected(self):
        self.assert_rejected(
            self.post_json({"subject": "Valid subject"}), "Description must be a string"
        )

    def test_blank_or_too_long_subject_is_rejected(self):
        for subject in ("", "   ", "x" * 101):
            with self.subTest(length=len(subject)):
                response = self.post_json(
                    {"subject": subject, "description": "Valid description"}
                )
                self.assert_rejected(
                    response, "Subject is required (max 100 characters)"
                )

    def test_blank_or_too_long_description_is_rejected(self):
        for description in ("", "   ", "x" * 501):
            with self.subTest(length=len(description)):
                response = self.post_json(
                    {"subject": "Valid subject", "description": description}
                )
                self.assert_rejected(
                    response, "Description is required (max 500 characters)"
                )

    def test_rejected_tickets_are_not_saved(self):
        before = len(self.client.get("/api/tickets").get_json())
        self.post_json({"subject": None, "description": "Valid description"})
        self.post_json([])
        after = len(self.client.get("/api/tickets").get_json())
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
