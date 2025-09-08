import unittest
from unittest.mock import Mock, patch

from wikiedits.api import edits_per_page


class TestEditsPerPage(unittest.TestCase):
  @patch("wikiedits.api.requests.get")
  def test_edits_per_page_basic(self, mock_get):
    """Test basic edits per page functionality"""
    mock_response = Mock()
    mock_response.json.return_value = {
    "items": [
    {
    "results": [
    {
      "project": "en.wikipedia.org",
      "page_title": "Python",
      "edits": 45,
      "timestamp": "20250101",
    },
    {
      "project": "en.wikipedia.org",
      "page_title": "Python",
      "edits": 52,
      "timestamp": "20250102",
    },
    ]
    }
    ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = edits_per_page(
    "en.wikipedia.org", "Python", "daily", "20250101", "20250102"
    )

    expected_url = (
    "https://wikimedia.org/api/rest_v1/metrics/edits/per-page/"
    "en.wikipedia.org/Python/all-editor-types/daily/20250101/20250102"
    )
    mock_get.assert_called_once_with(
    expected_url,
    headers={
    "User-Agent": "wikiedits-api/0.1.0",
    "Accept": "application/json"
    },
    timeout=30,
    )
    self.assertEqual(result[0]["edits"], 45)
    self.assertEqual(result[1]["edits"], 52)

  @patch("wikiedits.api.requests.get")
  def test_edits_per_page_with_custom_parameters(self, mock_get):
    """Test edits per page with custom parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": []}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    edits_per_page(
    "es.wikipedia.org",
    "Machine_learning",
    "monthly",
    "20250101",
    "20250105",
    editor_type="user",
    )

    expected_url = (
    "https://wikimedia.org/api/rest_v1/metrics/edits/per-page/"
    "es.wikipedia.org/Machine_learning/user/monthly/20250101/20250105"
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
  def test_edits_per_page_with_default_parameters(self, mock_get):
    """Test edits per page with default parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": []}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    edits_per_page(
    "fr.wikipedia.org", "Artificial_intelligence", "daily",
    "20250201", "20250228"
    )

    expected_url = (
    "https://wikimedia.org/api/rest_v1/metrics/edits/per-page/"
    "fr.wikipedia.org/Artificial_intelligence/all-editor-types/"
    "daily/20250201/20250228"
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
  def test_edits_per_page_date_validation(self, mock_get, mock_validate):
    """Test that date validation is called"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": []}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    mock_validate.return_value = ("20250101", "20250102")

    edits_per_page("en.wikipedia.org", "Test_page", "daily",
      "2025-01-01", "2025-01-02")

    self.assertEqual(mock_validate.call_count, 1)
    mock_validate.assert_called_with("daily", "2025-01-01", "2025-01-02")


if __name__ == "__main__":
  unittest.main()

