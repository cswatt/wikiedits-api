import unittest
from unittest.mock import Mock, patch

from wikiedits.api import top_by_abs_diff


class TestTopByAbsDiff(unittest.TestCase):
  @patch("wikiedits.api.requests.get")
  def test_top_by_abs_diff_basic(self, mock_get):
    """Test basic top by absolute diff functionality"""
    mock_response = Mock()
    mock_response.json.return_value = {
      "items": [
        {
          "results": [
            {
              "top": [
                {
                  "project": "en.wikipedia.org",
                  "page_title": "Python",
                  "abs_bytes_diff": 5000,
                  "rank": 1,
                },
                {
                  "project": "en.wikipedia.org",
                  "page_title": "JavaScript",
                  "abs_bytes_diff": 4500,
                  "rank": 2,
                },
              ]
            }
          ]
        }
      ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = top_by_abs_diff("en.wikipedia.org", "20250315")

    mock_get.assert_called_once_with(
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "top-by-absolute-bytes-difference/en.wikipedia.org/"
      "all-editor-types/all-page-types/2025/03/15",
      headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
      timeout=30,
    )
    self.assertEqual(result[0]["abs_bytes_diff"], 5000)
    self.assertEqual(result[1]["abs_bytes_diff"], 4500)

  @patch("wikiedits.api.requests.get")
  def test_top_by_abs_diff_with_custom_parameters(self, mock_get):
    """Test top by absolute diff with custom parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    top_by_abs_diff(
      "fr.wikipedia.org", "20250415", editor_type="user", page_type="content"
    )

    mock_get.assert_called_once_with(
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "top-by-absolute-bytes-difference/fr.wikipedia.org/user/content/2025/04/15",
      headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
      timeout=30,
    )

  @patch("wikiedits.api.requests.get")
  def test_top_by_abs_diff_with_default_parameters(self, mock_get):
    """Test top by absolute diff with default parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    top_by_abs_diff("es.wikipedia.org", "20250201")

    expected_url = (
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "top-by-absolute-bytes-difference/es.wikipedia.org/"
      "all-editor-types/all-page-types/2025/02/01"
    )
    mock_get.assert_called_once_with(
      expected_url,
      headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
      timeout=30,
    )

  @patch("wikiedits.api.requests.get")
  def test_top_by_abs_diff_iso_date_format(self, mock_get):
    """Test top by absolute diff with ISO date format"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    top_by_abs_diff("de.wikipedia.org", "2025-06-20")

    mock_get.assert_called_once_with(
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "top-by-absolute-bytes-difference/de.wikipedia.org/"
      "all-editor-types/all-page-types/2025/06/20",
      headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
      timeout=30,
    )

  @patch("wikiedits.api.requests.get")
  def test_top_by_abs_diff_slash_date_format(self, mock_get):
    """Test top by absolute diff with MM/DD/YYYY date format"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    top_by_abs_diff("it.wikipedia.org", "07/25/2025")

    mock_get.assert_called_once_with(
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "top-by-absolute-bytes-difference/it.wikipedia.org/"
      "all-editor-types/all-page-types/2025/07/25",
      headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
      timeout=30,
    )

  @patch("wikiedits.api.requests.get")
  def test_top_by_abs_diff_text_date_format(self, mock_get):
    """Test top by absolute diff with text date format"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    top_by_abs_diff("pt.wikipedia.org", "August 10, 2025")

    mock_get.assert_called_once_with(
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "top-by-absolute-bytes-difference/pt.wikipedia.org/"
      "all-editor-types/all-page-types/2025/08/10",
      headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
      timeout=30,
    )

  @patch("wikiedits.api.split_date")
  @patch("wikiedits.api.requests.get")
  def test_top_by_abs_diff_date_splitting(self, mock_get, mock_split):
    """Test that date splitting is called correctly"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    mock_split.return_value = ("2025", "09", "15")

    top_by_abs_diff("en.wikipedia.org", "2025-09-15")

    mock_split.assert_called_once_with("2025-09-15")
    mock_get.assert_called_once_with(
      "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
      "top-by-absolute-bytes-difference/en.wikipedia.org/"
      "all-editor-types/all-page-types/2025/09/15",
      headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
      timeout=30,
    )

  def test_top_by_abs_diff_invalid_date(self):
    """Test top by absolute diff with invalid date format"""
    with self.assertRaises(ValueError) as context:
      top_by_abs_diff("en.wikipedia.org", "invalid-date")

    self.assertIn("Invalid date format", str(context.exception))
    self.assertIn("invalid-date", str(context.exception))

  def test_top_by_abs_diff_none_date(self):
    """Test top by absolute diff with None date"""
    with self.assertRaises(ValueError) as context:
      top_by_abs_diff("en.wikipedia.org", None)

    self.assertIn("Invalid date format", str(context.exception))

  def test_top_by_abs_diff_empty_date(self):
    """Test top by absolute diff with empty date string"""
    with self.assertRaises(ValueError) as context:
      top_by_abs_diff("en.wikipedia.org", "")

    self.assertIn("Invalid date format", str(context.exception))


if __name__ == "__main__":
  unittest.main()
