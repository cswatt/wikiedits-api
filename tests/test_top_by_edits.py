import unittest
from unittest.mock import Mock, patch

from wikiedits.api import top_by_edits


class TestTopByEdits(unittest.TestCase):
  @patch("wikiedits.api.requests.get")
  def test_top_by_edits_basic(self, mock_get):
    """Test basic top by edits functionality"""
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
      "edits": 150,
      "rank": 1,
      },
      {
      "project": "en.wikipedia.org",
      "page_title": "JavaScript",
      "edits": 145,
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

    result = top_by_edits("en.wikipedia.org", "20250315")

    expected_url = (
    "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
    "top-by-edits/en.wikipedia.org/all-editor-types/all-page-types/"
    "2025/03/15"
    )
    mock_get.assert_called_once_with(
    expected_url,
    headers={
    "User-Agent": "wikiedits-api/0.1.0",
    "Accept": "application/json"
    },
    timeout=30,
    )
    self.assertEqual(result[0]["edits"], 150)
    self.assertEqual(result[1]["edits"], 145)

  @patch("wikiedits.api.requests.get")
  def test_top_by_edits_with_custom_parameters(self, mock_get):
    """Test top by edits with custom parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    top_by_edits(
    "fr.wikipedia.org", "20250415", editor_type="user", page_type="content"
    )

    expected_url = (
    "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
    "top-by-edits/fr.wikipedia.org/user/content/2025/04/15"
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
  def test_top_by_edits_with_default_parameters(self, mock_get):
    """Test top by edits with default parameters"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    top_by_edits("es.wikipedia.org", "20250201")

    expected_url = (
    "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
    "top-by-edits/es.wikipedia.org/all-editor-types/all-page-types/"
    "2025/02/01"
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
  def test_top_by_edits_iso_date_format(self, mock_get):
    """Test top by edits with ISO date format"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    top_by_edits("de.wikipedia.org", "2025-06-20")

    expected_url = (
    "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
    "top-by-edits/de.wikipedia.org/all-editor-types/all-page-types/"
    "2025/06/20"
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
  def test_top_by_edits_slash_date_format(self, mock_get):
    """Test top by edits with MM/DD/YYYY date format"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    top_by_edits("it.wikipedia.org", "07/25/2025")

    expected_url = (
    "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
    "top-by-edits/it.wikipedia.org/all-editor-types/all-page-types/"
    "2025/07/25"
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
  def test_top_by_edits_text_date_format(self, mock_get):
    """Test top by edits with text date format"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    top_by_edits("pt.wikipedia.org", "August 10, 2025")

    expected_url = (
    "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
    "top-by-edits/pt.wikipedia.org/all-editor-types/all-page-types/"
    "2025/08/10"
    )
    mock_get.assert_called_once_with(
    expected_url,
    headers={
    "User-Agent": "wikiedits-api/0.1.0",
    "Accept": "application/json"
    },
    timeout=30,
    )

  @patch("wikiedits.api.split_date")
  @patch("wikiedits.api.requests.get")
  def test_top_by_edits_date_splitting(self, mock_get, mock_split):
    """Test that date splitting is called correctly"""
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    mock_split.return_value = ("2025", "09", "15")

    top_by_edits("en.wikipedia.org", "2025-09-15")

    mock_split.assert_called_once_with("2025-09-15")
    expected_url = (
    "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
    "top-by-edits/en.wikipedia.org/all-editor-types/all-page-types/"
    "2025/09/15"
    )
    mock_get.assert_called_once_with(
    expected_url,
    headers={
    "User-Agent": "wikiedits-api/0.1.0",
    "Accept": "application/json"
    },
    timeout=30,
    )

  def test_top_by_edits_invalid_date(self):
    """Test top by edits with invalid date format"""
    with self.assertRaises(ValueError) as context:
      top_by_edits("en.wikipedia.org", "invalid-date")

    self.assertIn("Invalid date format", str(context.exception))
    self.assertIn("invalid-date", str(context.exception))

  def test_top_by_edits_none_date(self):
    """Test top by edits with None date"""
    with self.assertRaises(ValueError) as context:
      top_by_edits("en.wikipedia.org", None)

    self.assertIn("Invalid date format", str(context.exception))

  def test_top_by_edits_empty_date(self):
    """Test top by edits with empty date string"""
    with self.assertRaises(ValueError) as context:
      top_by_edits("en.wikipedia.org", "")

    self.assertIn("Invalid date format", str(context.exception))


if __name__ == "__main__":
  unittest.main()

