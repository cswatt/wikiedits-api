import unittest
from unittest.mock import Mock, patch

from wikiedits.client import pages


class TestPages(unittest.TestCase):
  @patch("wikiedits.client.new_pages")
  @patch("wikiedits.client.edited_pages")
  def test_pages_calls_new_pages_when_change_type_new(self, mock_edited_pages, mock_new_pages):
    """Test that pages() calls new_pages when change_type is 'new'"""
    # Setup
    mock_new_pages.return_value = [
      {"new_pages": 50, "timestamp": "20250101"},
      {"new_pages": 75, "timestamp": "20250102"}
    ]
    
    # Call function
    result = pages(
      start="2025-01-01", 
      end="2025-01-02",
      change_type="new",
      project="en.wikipedia.org"
    )
    
    # Verify new_pages was called and edited_pages was not
    mock_new_pages.assert_called_once_with(
      project="en.wikipedia.org",
      granularity="daily",
      start="2025-01-01",
      end="2025-01-02",
      editor_type="all-editor-types",
      page_type="all-page-types"
    )
    mock_edited_pages.assert_not_called()
    self.assertEqual(result, 125)  # Sum of 50 + 75

  @patch("wikiedits.client.new_pages")
  @patch("wikiedits.client.edited_pages")
  def test_pages_calls_edited_pages_when_change_type_edited(self, mock_edited_pages, mock_new_pages):
    """Test that pages() calls edited_pages when change_type is 'edited'"""
    # Setup
    mock_edited_pages.return_value = [
      {"edited_pages": 200, "timestamp": "20250101"},
      {"edited_pages": 300, "timestamp": "20250102"}
    ]
    
    # Call function
    result = pages(
      start="2025-01-01",
      end="2025-01-02",
      change_type="edited",
      project="fr.wikipedia.org"
    )
    
    # Verify edited_pages was called and new_pages was not
    mock_edited_pages.assert_called_once_with(
      project="fr.wikipedia.org",
      granularity="daily",
      start="2025-01-01",
      end="2025-01-02",
      editor_type="all-editor-types",
      page_type="all-page-types",
      activity_level="all-activity-levels"
    )
    mock_new_pages.assert_not_called()
    self.assertEqual(result, 500)  # Sum of 200 + 300

  @patch("wikiedits.client.new_pages")
  @patch("wikiedits.client.edited_pages")
  def test_pages_defaults_to_edited_when_no_change_type(self, mock_edited_pages, mock_new_pages):
    """Test that pages() defaults to edited_pages when no change_type is provided"""
    # Setup
    mock_edited_pages.return_value = [
      {"edited_pages": 100, "timestamp": "20250101"}
    ]
    
    # Call function (no change_type parameter)
    result = pages(
      start="2025-01-01",
      end="2025-01-01",
      project="de.wikipedia.org"
    )
    
    # Verify edited_pages was called
    mock_edited_pages.assert_called_once()
    mock_new_pages.assert_not_called()
    self.assertEqual(result, 100)

  @patch("wikiedits.client.new_pages")
  @patch("wikiedits.client.edited_pages")
  def test_pages_with_custom_parameters(self, mock_edited_pages, mock_new_pages):
    """Test that pages() passes through custom parameters correctly"""
    # Setup
    mock_new_pages.return_value = [
      {"new_pages": 25, "timestamp": "20250101"}
    ]
    
    # Call function with custom parameters
    result = pages(
      start="2025-03-15",
      end="2025-03-15",
      change_type="new",
      project="es.wikipedia.org",
      editor_type="user",
      page_type="content",
      activity_level="5..99-edits"
    )
    
    # Verify parameters were passed correctly
    mock_new_pages.assert_called_once_with(
      project="es.wikipedia.org",
      granularity="daily",
      start="2025-03-15",
      end="2025-03-15",
      editor_type="user",
      page_type="content"
    )
    self.assertEqual(result, 25)

  def test_pages_missing_required_params(self):
    """Test that pages() raises error when missing required parameters"""
    with self.assertRaises(TypeError):
      pages()
    
    with self.assertRaises(TypeError):
      pages(start="2025-01-01")  # Missing end parameter


if __name__ == "__main__":
  unittest.main()