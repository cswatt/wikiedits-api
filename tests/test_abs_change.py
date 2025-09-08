import unittest
from unittest.mock import Mock, patch

from wikiedits.api import bytes_diff_abs_aggregate, bytes_diff_abs_per_page


class TestAbsChange(unittest.TestCase):
  @patch("wikiedits.api.requests.get")
  def test_bytes_diff_abs_aggregate_basic(self, mock_get):
    """Test basic absolute change aggregate functionality"""
    mock_response = Mock()
    mock_response.json.return_value = {
    "items": [
    {
    "results": [
    {
      "project": "en.wikipedia.org",
      "abs_bytes_diff": 25000,
      "timestamp": "20250101",
    },
    {
      "project": "en.wikipedia.org",
      "abs_bytes_diff": 28000,
      "timestamp": "20250102",
    },
    ]
    }
    ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = bytes_diff_abs_aggregate("en.wikipedia.org", "daily", "20250101", "20250102")

    mock_get.assert_called_once_with(
    "https://wikimedia.org/api/rest_v1/metrics/bytes-difference/"
    "absolute/aggregate/en.wikipedia.org/all-editor-types/all-page-types/"
    "daily/20250101/20250102",
    headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
    timeout=30,
    )
    self.assertEqual(result[0]["abs_bytes_diff"], 25000)
    self.assertEqual(result[1]["abs_bytes_diff"], 28000)

  @patch("wikiedits.api.requests.get")
  def test_bytes_diff_abs_aggregate_custom_parameters(self, mock_get):
    """Test absolute change aggregate with custom parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": []}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    bytes_diff_abs_aggregate(
    "de.wikipedia.org",
    "monthly",
    "20250101",
    "20250105",
    editor_type="user",
    page_type="content",
    )

    mock_get.assert_called_once_with(
    "https://wikimedia.org/api/rest_v1/metrics/bytes-difference/"
    "absolute/aggregate/de.wikipedia.org/user/content/monthly/"
    "20250101/20250105",
    headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
    timeout=30,
    )

  @patch("wikiedits.api.requests.get")
  def test_bytes_diff_abs_per_page_basic(self, mock_get):
    """Test basic absolute change per page functionality"""
    mock_response = Mock()
    mock_response.json.return_value = {
    "items": [
    {
    "results": [
    {
      "project": "en.wikipedia.org",
      "page_title": "Climate_change",
      "abs_bytes_diff": 750,
      "timestamp": "20250101",
    },
    {
      "project": "en.wikipedia.org",
      "page_title": "Climate_change",
      "abs_bytes_diff": 620,
      "timestamp": "20250102",
    },
    ]
    }
    ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = bytes_diff_abs_per_page(
    "en.wikipedia.org", "Climate_change", "daily", "20250101", "20250102"
    )

    mock_get.assert_called_once_with(
    "https://wikimedia.org/api/rest_v1/metrics/bytes-difference/absolute/per-page/en.wikipedia.org/Climate_change/all-editor-types/daily/20250101/20250102",
    headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
    timeout=30,
    )
    self.assertEqual(result[0]["abs_bytes_diff"], 750)
    self.assertEqual(result[1]["abs_bytes_diff"], 620)

  @patch("wikiedits.api.requests.get")
  def test_bytes_diff_abs_per_page_custom_parameters(self, mock_get):
    """Test absolute change per page with custom parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": []}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    bytes_diff_abs_per_page(
    "fr.wikipedia.org",
    "Changement_climatique",
    "monthly",
    "20250101",
    "20250105",
    editor_type="user",
    )

    mock_get.assert_called_once_with(
    "https://wikimedia.org/api/rest_v1/metrics/bytes-difference/absolute/per-page/fr.wikipedia.org/Changement_climatique/user/monthly/20250101/20250105",
    headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
    timeout=30,
    )

  @patch("wikiedits.api.validate_dates")
  @patch("wikiedits.api.requests.get")
  def test_abs_change_date_validation(self, mock_get, mock_validate):
    """Test that date validation is called for both functions"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": []}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    mock_validate.side_effect = [("20250101", "20250102"), ("20250101", "20250102")]

    bytes_diff_abs_aggregate("en.wikipedia.org", "daily", "2025-01-01", "2025-01-02")
    bytes_diff_abs_per_page(
    "en.wikipedia.org", "Test_page", "daily", "2025-01-01", "2025-01-02"
    )

    self.assertEqual(mock_validate.call_count, 2)


if __name__ == "__main__":
  unittest.main()

