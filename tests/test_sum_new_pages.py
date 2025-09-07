import unittest
from unittest.mock import patch

from wikiedits.api import sum_new_pages


class TestSumNewPages(unittest.TestCase):
  @patch("wikiedits.api.new_pages")
  def test_sum_new_pages_basic(self, mock_new_pages):
    """Test basic sum_new_pages functionality"""
    mock_new_pages.return_value = [
      {"timestamp": "2024-01-01T00:00:00.000Z", "new_pages": 150},
      {"timestamp": "2024-01-02T00:00:00.000Z", "new_pages": 200},
    ]

    result = sum_new_pages("en.wikipedia", "20240101", "20240102")

    mock_new_pages.assert_called_once_with(
      "en.wikipedia",
      "daily",
      "20240101",
      "20240102",
      "all-editor-types",
      "all-page-types",
    )
    self.assertEqual(result, 350)

  @patch("wikiedits.api.new_pages")
  def test_sum_new_pages_with_custom_parameters(self, mock_new_pages):
    """Test sum_new_pages with custom parameters"""
    mock_new_pages.return_value = [
      {"timestamp": "2024-01-01T00:00:00.000Z", "new_pages": 75},
      {"timestamp": "2024-01-02T00:00:00.000Z", "new_pages": 85},
    ]

    result = sum_new_pages(
      "es.wikipedia",
      "20240201",
      "20240202",
      editor_type="user",
      page_type="content",
    )

    mock_new_pages.assert_called_once_with(
      "es.wikipedia", "daily", "20240201", "20240202", "user", "content"
    )
    self.assertEqual(result, 160)

  @patch("wikiedits.api.new_pages")
  def test_sum_new_pages_empty_response(self, mock_new_pages):
    """Test sum_new_pages with empty response"""
    mock_new_pages.return_value = []

    result = sum_new_pages("fr.wikipedia", "20240101", "20240102")

    self.assertEqual(result, 0)

  @patch("wikiedits.api.new_pages")
  def test_sum_new_pages_single_day(self, mock_new_pages):
    """Test sum_new_pages with single day"""
    mock_new_pages.return_value = [
      {"timestamp": "2024-01-01T00:00:00.000Z", "new_pages": 99}
    ]

    result = sum_new_pages("de.wikipedia", "20240101", "20240101")

    self.assertEqual(result, 99)


if __name__ == "__main__":
  unittest.main()
