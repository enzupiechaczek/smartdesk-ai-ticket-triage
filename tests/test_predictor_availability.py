"""Model-loading boundary tests using mocks, not real model artifacts."""
import unittest
from unittest.mock import Mock, patch

from ai import predictor


class PredictorAvailabilityTests(unittest.TestCase):
    def setUp(self):
        cache_patch = patch.object(predictor, "_model", None)
        cache_patch.start()
        self.addCleanup(cache_patch.stop)

    def test_missing_file_raises_specific_error_without_loading(self):
        path = Mock()
        path.exists.return_value = False
        with patch.object(predictor, "MODEL_PATH", path), patch.object(predictor.joblib, "load") as load:
            with self.assertRaises(predictor.ModelUnavailableError):
                predictor.predict_category("Synthetic ticket")
            load.assert_not_called()

    def test_file_disappearing_during_load_has_same_specific_error(self):
        path = Mock()
        path.exists.return_value = True
        with patch.object(predictor, "MODEL_PATH", path), patch.object(predictor.joblib, "load", side_effect=FileNotFoundError("private path")):
            with self.assertRaises(predictor.ModelUnavailableError) as error:
                predictor.predict_category("Synthetic ticket")
        self.assertEqual(str(error.exception), "Run python ai/train.py first")

    def test_unexpected_load_error_is_not_reclassified(self):
        path = Mock()
        path.exists.return_value = True
        with patch.object(predictor, "MODEL_PATH", path), patch.object(predictor.joblib, "load", side_effect=RuntimeError("Unexpected fault")):
            with self.assertRaisesRegex(RuntimeError, "Unexpected fault"):
                predictor.predict_category("Synthetic ticket")

    def test_blank_text_still_raises_validation_error(self):
        with self.assertRaises(ValueError):
            predictor.predict_category("   ")


if __name__ == "__main__":
    unittest.main()
