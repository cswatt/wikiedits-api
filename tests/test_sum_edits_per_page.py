import unittest
from unittest.mock import patch

from wikiedits.api import sum_edits_per_page


class TestSumEditsPerPage(unittest.TestCase):
    @patch("wikiedits.api.edits_per_page")
    def test_sum_edits_per_page_basic(self, mock_edits_per_page):
        """Test basic sum_edits_per_page functionality"""
        mock_edits_per_page.return_value = [
            {"timestamp": "2024-01-01T00:00:00.000Z", "edits": 25},
            {"timestamp": "2024-01-02T00:00:00.000Z", "edits": 30},
        ]

        result = sum_edits_per_page(
            "en.wikipedia", "Python_(programming_language)", "20240101", "20240102"
        )

        mock_edits_per_page.assert_called_once_with(
            "en.wikipedia",
            "Python_(programming_language)",
            "daily",
            "20240101",
            "20240102",
            "all-editor-types",
        )
        self.assertEqual(result, 55)

    @patch("wikiedits.api.edits_per_page")
    def test_sum_edits_per_page_with_custom_parameters(self, mock_edits_per_page):
        """Test sum_edits_per_page with custom parameters"""
        mock_edits_per_page.return_value = [
            {"timestamp": "2024-01-01T00:00:00.000Z", "edits": 10},
            {"timestamp": "2024-01-02T00:00:00.000Z", "edits": 15},
        ]

        result = sum_edits_per_page(
            "es.wikipedia", "Madrid", "20240201", "20240202", editor_type="user"
        )

        mock_edits_per_page.assert_called_once_with(
            "es.wikipedia", "Madrid", "daily", "20240201", "20240202", "user"
        )
        self.assertEqual(result, 25)

    @patch("wikiedits.api.edits_per_page")
    def test_sum_edits_per_page_empty_response(self, mock_edits_per_page):
        """Test sum_edits_per_page with empty response"""
        mock_edits_per_page.return_value = []

        result = sum_edits_per_page("fr.wikipedia", "Paris", "20240101", "20240102")

        self.assertEqual(result, 0)

    @patch("wikiedits.api.edits_per_page")
    def test_sum_edits_per_page_single_day(self, mock_edits_per_page):
        """Test sum_edits_per_page with single day"""
        mock_edits_per_page.return_value = [
            {"timestamp": "2024-01-01T00:00:00.000Z", "edits": 42}
        ]

        result = sum_edits_per_page("de.wikipedia", "Berlin", "20240101", "20240101")

        self.assertEqual(result, 42)


if __name__ == "__main__":
    unittest.main()
