import unittest
from unittest.mock import patch

from wikiedits.api import sum_edits_aggregate


class TestSumEditsAggregate(unittest.TestCase):
  @patch("wikiedits.api.edits_aggregate")
  def test_sum_edits_aggregate_basic(self, mock_edits_aggregate):
    """Test basic sum_edits_aggregate functionality"""
    mock_edits_aggregate.return_value = [
      {"timestamp": "2024-01-01T00:00:00.000Z", "edits": 177370},
      {"timestamp": "2024-01-02T00:00:00.000Z", "edits": 185367},
    ]

    result = sum_edits_aggregate("en.wikipedia", "20240101", "20240102")

    mock_edits_aggregate.assert_called_once_with(
      "en.wikipedia",
      "daily",
      "20240101",
      "20240102",
      "all-editor-types",
      "all-page-types",
    )
    self.assertEqual(result, 362737)

  @patch("wikiedits.api.edits_aggregate")
  def test_sum_edits_aggregate_with_custom_parameters(self, mock_edits_aggregate):
    """Test sum_edits_aggregate with custom parameters"""
    mock_edits_aggregate.return_value = [
      {"timestamp": "2024-01-01T00:00:00.000Z", "edits": 50000},
      {"timestamp": "2024-01-02T00:00:00.000Z", "edits": 60000},
    ]

    result = sum_edits_aggregate(
      "es.wikipedia",
      "20240201",
      "20240202",
      editor_type="user",
      page_type="content",
    )

    mock_edits_aggregate.assert_called_once_with(
      "es.wikipedia", "daily", "20240201", "20240202", "user", "content"
    )
    self.assertEqual(result, 110000)

  @patch("wikiedits.api.edits_aggregate")
  def test_sum_edits_aggregate_empty_response(self, mock_edits_aggregate):
    """Test sum_edits_aggregate with empty response"""
    mock_edits_aggregate.return_value = []

    result = sum_edits_aggregate("fr.wikipedia", "20240101", "20240102")

    self.assertEqual(result, 0)

  @patch("wikiedits.api.edits_aggregate")
  def test_sum_edits_aggregate_single_day(self, mock_edits_aggregate):
    """Test sum_edits_aggregate with single day"""
    mock_edits_aggregate.return_value = [
      {"timestamp": "2024-01-01T00:00:00.000Z", "edits": 123456}
    ]

    result = sum_edits_aggregate("de.wikipedia", "20240101", "20240101")

    self.assertEqual(result, 123456)


if __name__ == "__main__":
  unittest.main()
