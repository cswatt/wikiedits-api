import unittest
from unittest.mock import patch

from wikiedits.api import sum_edited_pages


class TestSumEditedPages(unittest.TestCase):
  @patch("wikiedits.api.edited_pages")
  def test_sum_edited_pages_basic(self, mock_edited_pages):
    """Test basic sum_edited_pages functionality"""
    mock_edited_pages.return_value = [
      {"timestamp": "2024-01-01T00:00:00.000Z", "edited_pages": 1250},
      {"timestamp": "2024-01-02T00:00:00.000Z", "edited_pages": 1400},
    ]

    result = sum_edited_pages("en.wikipedia", "20240101", "20240102")

    mock_edited_pages.assert_called_once_with(
      "en.wikipedia",
      "daily",
      "20240101",
      "20240102",
      "all-editor-types",
      "all-page-types",
    )
    self.assertEqual(result, 2650)

  @patch("wikiedits.api.edited_pages")
  def test_sum_edited_pages_with_custom_parameters(self, mock_edited_pages):
    """Test sum_edited_pages with custom parameters"""
    mock_edited_pages.return_value = [
      {"timestamp": "2024-01-01T00:00:00.000Z", "edited_pages": 500},
      {"timestamp": "2024-01-02T00:00:00.000Z", "edited_pages": 600},
    ]

    result = sum_edited_pages(
      "es.wikipedia",
      "20240201",
      "20240202",
      editor_type="user",
      page_type="content",
      activity_level="25-99-edits",
    )

    mock_edited_pages.assert_called_once_with(
      "es.wikipedia", "daily", "20240201", "20240202", "user", "content"
    )
    self.assertEqual(result, 1100)

  @patch("wikiedits.api.edited_pages")
  def test_sum_edited_pages_empty_response(self, mock_edited_pages):
    """Test sum_edited_pages with empty response"""
    mock_edited_pages.return_value = []

    result = sum_edited_pages("fr.wikipedia", "20240101", "20240102")

    self.assertEqual(result, 0)

  @patch("wikiedits.api.edited_pages")
  def test_sum_edited_pages_single_day(self, mock_edited_pages):
    """Test sum_edited_pages with single day"""
    mock_edited_pages.return_value = [
      {"timestamp": "2024-01-01T00:00:00.000Z", "edited_pages": 888}
    ]

    result = sum_edited_pages("de.wikipedia", "20240101", "20240101")

    self.assertEqual(result, 888)


if __name__ == "__main__":
  unittest.main()
