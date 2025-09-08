import unittest
from unittest.mock import Mock, patch

from wikiedits.client import top


class TestTop(unittest.TestCase):
  @patch("wikiedits.client.top_by_edits")
  @patch("wikiedits.client.top_by_net_diff")
  @patch("wikiedits.client.top_by_abs_diff")
  def test_top_calls_top_by_edits_when_by_edits(
  self, mock_abs_diff, mock_net_diff, mock_edits):
    """Test that top() calls top_by_edits when by='edits'"""
    # Setup
    mock_edits.return_value = [
    {"page_title": "Python_(programming_language)", "edits": 50},
    {"page_title": "Machine_learning", "edits": 40},
    {"page_title": "Artificial_intelligence", "edits": 30},
    ]

    # Call function
    result = top(
    date="2025-03-15",
    by="edits",
    count=10,
    project="en.wikipedia.org"
    )

    # Verify top_by_edits was called and others were not
    mock_edits.assert_called_once_with(
    project="en.wikipedia.org",
    date="2025-03-15",
    editor_type="all-editor-types",
    page_type="all-page-types"
    )
    mock_net_diff.assert_not_called()
    mock_abs_diff.assert_not_called()
    self.assertEqual(len(result), 3)
    self.assertEqual(
    result[0]["page_title"], "Python_(programming_language)")

  @patch("wikiedits.client.top_by_edits")
  @patch("wikiedits.client.top_by_net_diff")
  @patch("wikiedits.client.top_by_abs_diff")
  def test_top_calls_top_by_net_diff_when_by_net_diff(
  self, mock_abs_diff, mock_net_diff, mock_edits):
    """Test that top() calls top_by_net_diff when by='net-diff'"""
    # Setup
    mock_net_diff.return_value = [
    {"page_title": "Climate_change", "net_bytes_diff": 1500},
    {"page_title": "Global_warming", "net_bytes_diff": 1200},
    ]

    # Call function
    result = top(
    date="2025-07-20",
    by="net-diff",
    project="fr.wikipedia.org"
    )

    # Verify top_by_net_diff was called and others were not
    mock_net_diff.assert_called_once_with(
    project="fr.wikipedia.org",
    date="2025-07-20",
    editor_type="all-editor-types",
    page_type="all-page-types"
    )
    mock_edits.assert_not_called()
    mock_abs_diff.assert_not_called()
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0]["page_title"], "Climate_change")

  @patch("wikiedits.client.top_by_edits")
  @patch("wikiedits.client.top_by_net_diff")
  @patch("wikiedits.client.top_by_abs_diff")
  def test_top_calls_top_by_abs_diff_when_by_absolute_diff(
  self, mock_abs_diff, mock_net_diff, mock_edits):
    """Test that top() calls top_by_abs_diff when by='absolute-diff'"""
    # Setup
    mock_abs_diff.return_value = [
    {"page_title": "Wikipedia", "abs_bytes_diff": 2000},
    {"page_title": "Technology", "abs_bytes_diff": 1800},
    {"page_title": "Science", "abs_bytes_diff": 1600},
    ]

    # Call function
    result = top(
    date="2025-12-01",
    by="absolute-diff",
    count=3,
    project="de.wikipedia.org"
    )

    # Verify top_by_abs_diff was called and others were not
    mock_abs_diff.assert_called_once_with(
    project="de.wikipedia.org",
    date="2025-12-01",
    editor_type="all-editor-types",
    page_type="all-page-types"
    )
    mock_edits.assert_not_called()
    mock_net_diff.assert_not_called()
    self.assertEqual(len(result), 3)
    self.assertEqual(result[0]["page_title"], "Wikipedia")

  @patch("wikiedits.client.top_by_edits")
  @patch("wikiedits.client.top_by_net_diff")
  @patch("wikiedits.client.top_by_abs_diff")
  def test_top_limits_results_by_count(
  self, mock_abs_diff, mock_net_diff, mock_edits):
    """Test that top() limits results to the specified count"""
    # Setup - return more results than requested
    mock_edits.return_value = [
    {"page_title": "Page1", "edits": 100},
    {"page_title": "Page2", "edits": 90},
    {"page_title": "Page3", "edits": 80},
    {"page_title": "Page4", "edits": 70},
    {"page_title": "Page5", "edits": 60},
    ]

    # Call function with count=3
    result = top(
    date="2025-06-10",
    by="edits",
    count=3,
    project="es.wikipedia.org"
    )

    # Verify only 3 results returned
    self.assertEqual(len(result), 3)
    self.assertEqual(result[0]["page_title"], "Page1")
    self.assertEqual(result[1]["page_title"], "Page2")
    self.assertEqual(result[2]["page_title"], "Page3")

  @patch("wikiedits.client.top_by_edits")
  @patch("wikiedits.client.top_by_net_diff")
  @patch("wikiedits.client.top_by_abs_diff")
  def test_top_with_custom_parameters(
  self, mock_abs_diff, mock_net_diff, mock_edits):
    """Test that top() passes custom parameters correctly"""
    # Setup
    mock_edits.return_value = [{"page_title": "Test", "edits": 25}]

    # Call function with custom parameters
    result = top(
    date="2025-09-05",
    by="edits",
    count=5,
    project="it.wikipedia.org",
    editor_type="user",
    page_type="content"
    )

    # Verify parameters were passed correctly
    mock_edits.assert_called_once_with(
    project="it.wikipedia.org",
    date="2025-09-05",
    editor_type="user",
    page_type="content"
    )
    self.assertEqual(len(result), 1)

  def test_top_raises_error_for_invalid_by_parameter(self):
    """Test that top() raises ValueError for invalid 'by' parameter"""
    with self.assertRaises(ValueError) as context:
      top(date="2025-01-01", by="invalid-metric",
      project="en.wikipedia.org")

    self.assertIn("Invalid 'by' parameter: invalid-metric",
      str(context.exception))
    self.assertIn("Must be 'edits', 'net-diff', or 'absolute-diff'",
      str(context.exception))

  def test_top_missing_required_params(self):
    """Test that top() raises error when missing required parameters"""
    with self.assertRaises(TypeError):
      top()  # Missing date parameter


if __name__ == "__main__":
  unittest.main()
