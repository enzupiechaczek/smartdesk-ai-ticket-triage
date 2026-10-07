"""Tests for the priority rule documented in docs/priority.md.

Run from the repository root:  python -m unittest discover -s backend -p "test_*.py" -v
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from priority import compute_priority


class ComputePriorityTests(unittest.TestCase):
    def test_documented_examples(self):
        # The "Examples for Group B" table in docs/priority.md.
        cases = [
            ("Login broken", "I cannot access my account", "urgent"),
            ("Server DOWN", "Site unreachable", "urgent"),
            ("Slow report", "Everyone in finance sees delays", "urgent"),
            ("Download fails", "The download button gives an error", "normal"),
            ("Printer issue", "Paper jam on floor 2", "normal"),
            ("Reproduction", "Seen in Production last night", "urgent"),
            ("Typo", "Can't access the page", "normal"),
            ("Shutdown", "Please schedule a shutdown", "normal"),
        ]
        for subject, description, expected in cases:
            with self.subTest(subject=subject):
                self.assertEqual(compute_priority(subject, description), expected)

    def test_download_does_not_trigger_down(self):
        self.assertEqual(compute_priority("Downloads", "downloading the report is slow"), "normal")

    def test_down_as_a_whole_word_is_urgent(self):
        self.assertEqual(compute_priority("Help", "The server is down"), "urgent")

    def test_every_urgent_phrase_matches(self):
        for phrase in ["cannot access", "locked out", "outage", "down",
                       "all users", "everyone", "production", "data loss"]:
            with self.subTest(phrase=phrase):
                self.assertEqual(compute_priority("Issue", "We have " + phrase + " today"), "urgent")

    def test_phrase_in_subject_only_is_urgent(self):
        self.assertEqual(compute_priority("Outage", "Please help"), "urgent")

    def test_no_phrase_is_normal(self):
        self.assertEqual(compute_priority("Question", "How do I change my display name?"), "normal")


if __name__ == "__main__":
    unittest.main()
