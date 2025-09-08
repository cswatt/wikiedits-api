import unittest
from unittest.mock import patch

from wikiedits.client import edits


class TestEdits(unittest.TestCase):
  @patch("wikiedits.client.edits_aggregate")
  @patch("wikiedits.client.edits_per_page")
  def test_edits_calls_aggregate_without_page_title(self, mock_per_page, mock_aggregate):
    """Test that edits() calls edits_aggregate when no page title is provided"""
    # Setup
    mock_aggregate.return_value = [
    {"edits": 100, "timestamp": "20250101"},
    {"edits": 150, "timestamp": "20250102"}
    ]

    # Call function
    result = edits(
    start="2025-01-01",
    end="2025-01-02",
    project="en.wikipedia.org"
    )

    # Verify aggregate was called and per_page was not
    mock_aggregate.assert_called_once()
    mock_per_page.assert_not_called()
    self.assertEqual(result, 250)  # Sum of 100 + 150

  @patch("wikiedits.client.edits_aggregate")
  @patch("wikiedits.client.edits_per_page")
  def test_edits_calls_per_page_with_page_title(self, mock_per_page, mock_aggregate):
    """Test that edits() calls edits_per_page when page title is provided"""
    # Setup
    mock_per_page.return_value = [
    {"edits": 30, "timestamp": "20250101"},
    {"edits": 20, "timestamp": "20250102"}
    ]

    # Call function
    result = edits(
    start="2025-01-01",
    end="2025-01-02",
    project="en.wikipedia.org",
    page_title="Climate_change"
    )

    # Verify per_page was called and aggregate was not
    mock_per_page.assert_called_once()
    mock_aggregate.assert_not_called()
    self.assertEqual(result, 50)  # Sum of 30 + 20

  def test_edits_missing_required_params(self):
    """Test that edits() raises error when missing required parameters"""
    with self.assertRaises(TypeError):
      edits()

    with self.assertRaises(TypeError):
      edits(start="2025-01-01")  # Missing end parameter


if __name__ == "__main__":
  unittest.main()
