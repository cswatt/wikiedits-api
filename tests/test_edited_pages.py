import unittest
from unittest.mock import Mock, patch

from wikiedits.api import edited_pages


class TestEditedPages(unittest.TestCase):
  @patch("wikiedits.api.requests.get")
  def test_edited_pages_basic(self, mock_get):
    """Test basic edited pages functionality"""
    mock_response = Mock()
    mock_response.json.return_value = {
      "items": [
        {
          "results": [
            {
              "project": "en.wikipedia.org",
              "edited_pages": 2500,
              "timestamp": "20250101",
            },
            {
              "project": "en.wikipedia.org",
              "edited_pages": 2800,
              "timestamp": "20250102",
            },
          ]
        }
      ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = edited_pages("en.wikipedia.org", "daily", "20250101", "20250102")

    expected_url = (
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "aggregate/en.wikipedia.org/all-editor-types/all-page-types/"
      "all-activity-levels/daily/20250101/20250102"
    )
    mock_get.assert_called_once_with(
      expected_url,
      headers={
        "User-Agent": "wikiedits-api/0.1.0",
        "Accept": "application/json"
      },
      timeout=30,
    )
    self.assertEqual(result[0]["edited_pages"], 2500)
    self.assertEqual(result[1]["edited_pages"], 2800)

  @patch("wikiedits.api.requests.get")
  def test_edited_pages_with_custom_parameters(self, mock_get):
    """Test edited pages with all custom parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": []}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    edited_pages(
      "de.wikipedia.org",
      "monthly",
      "20250101",
      "20250105",
      editor_type="user",
      page_type="content",
      activity_level="1..4-edits",
    )

    expected_url = (
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "aggregate/de.wikipedia.org/user/content/1..4-edits/monthly/"
      "20250101/20250105"
    )
    mock_get.assert_called_once_with(
      expected_url,
      headers={
        "User-Agent": "wikiedits-api/0.1.0",
        "Accept": "application/json"
      },
      timeout=30,
    )

  @patch("wikiedits.api.requests.get")
  def test_edited_pages_with_default_parameters(self, mock_get):
    """Test edited pages with default parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": []}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    edited_pages("fr.wikipedia.org", "daily", "20250201", "20250228")

    expected_url = (
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "aggregate/fr.wikipedia.org/all-editor-types/all-page-types/"
      "all-activity-levels/daily/20250201/20250228"
    )
    mock_get.assert_called_once_with(
      expected_url,
      headers={
        "User-Agent": "wikiedits-api/0.1.0",
        "Accept": "application/json"
      },
      timeout=30,
    )

  @patch("wikiedits.api.requests.get")
  def test_edited_pages_with_partial_custom_parameters(self, mock_get):
    """Test edited pages with some custom parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": []}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    edited_pages(
      "es.wikipedia.org",
      "daily",
      "20250301",
      "20250331",
      activity_level="5..24-edits",
    )

    expected_url = (
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "aggregate/es.wikipedia.org/all-editor-types/all-page-types/"
      "5..24-edits/daily/20250301/20250331"
    )
    mock_get.assert_called_once_with(
      expected_url,
      headers={
        "User-Agent": "wikiedits-api/0.1.0",
        "Accept": "application/json"
      },
      timeout=30,
    )

  @patch("wikiedits.api.validate_dates")
  @patch("wikiedits.api.requests.get")
  def test_edited_pages_date_validation(self, mock_get, mock_validate):
    """Test that date validation is called"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": []}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    mock_validate.return_value = ("20250101", "20250102")

    edited_pages("en.wikipedia.org", "daily", "2025-01-01", "2025-01-02")

    self.assertEqual(mock_validate.call_count, 1)
    mock_validate.assert_called_with("daily", "2025-01-01", "2025-01-02")


if __name__ == "__main__":
  unittest.main()
