import unittest
from unittest.mock import Mock, patch

from wikiedits.api import top_by_net_diff


class TestTopByNetDiff(unittest.TestCase):
    @patch("wikiedits.api.requests.get")
    def test_top_by_net_diff_basic(self, mock_get):
        """Test basic top by net diff functionality"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "results": [
                        {
                            "top": [
                                {
                                    "project": "en.wikipedia",
                                    "page_title": "Python",
                                    "net_bytes_diff": 5000,
                                    "rank": 1,
                                },
                                {
                                    "project": "en.wikipedia",
                                    "page_title": "JavaScript",
                                    "net_bytes_diff": 4500,
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

        result = top_by_net_diff("en.wikipedia", "20240315")

        mock_get.assert_called_once_with(
            "https://wikimedia.org/api/rest_v1/metrics/edited-pages/"
            "top-by-net-bytes-difference/en.wikipedia/all-editor-types/"
            "all-page-types/2024/03/15",
            headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
            timeout=30,
        )
        self.assertEqual(result[0]["net_bytes_diff"], 5000)
        self.assertEqual(result[1]["net_bytes_diff"], 4500)

    @patch("wikiedits.api.requests.get")
    def test_top_by_net_diff_with_custom_parameters(self, mock_get):
        """Test most edited net with custom parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        top_by_net_diff(
            "fr.wikipedia", "20240415", editor_type="user", page_type="content"
        )

        mock_get.assert_called_once_with(
            "https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-net-bytes-difference/fr.wikipedia/user/content/2024/04/15",
            headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
            timeout=30,
        )

    @patch("wikiedits.api.requests.get")
    def test_top_by_net_diff_with_default_parameters(self, mock_get):
        """Test most edited net with default parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        top_by_net_diff("es.wikipedia", "20240201")

        expected_url = "https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-net-bytes-difference/es.wikipedia/all-editor-types/all-page-types/2024/02/01"
        mock_get.assert_called_once_with(
            expected_url,
            headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
            timeout=30,
        )

    @patch("wikiedits.api.requests.get")
    def test_top_by_net_diff_iso_date_format(self, mock_get):
        """Test most edited net with ISO date format"""
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        top_by_net_diff("de.wikipedia", "2024-06-20")

        mock_get.assert_called_once_with(
            "https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-net-bytes-difference/de.wikipedia/all-editor-types/all-page-types/2024/06/20",
            headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
            timeout=30,
        )

    @patch("wikiedits.api.requests.get")
    def test_top_by_net_diff_slash_date_format(self, mock_get):
        """Test most edited net with MM/DD/YYYY date format"""
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        top_by_net_diff("it.wikipedia", "07/25/2024")

        mock_get.assert_called_once_with(
            "https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-net-bytes-difference/it.wikipedia/all-editor-types/all-page-types/2024/07/25",
            headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
            timeout=30,
        )

    @patch("wikiedits.api.requests.get")
    def test_top_by_net_diff_text_date_format(self, mock_get):
        """Test most edited net with text date format"""
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        top_by_net_diff("pt.wikipedia", "August 10, 2024")

        mock_get.assert_called_once_with(
            "https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-net-bytes-difference/pt.wikipedia/all-editor-types/all-page-types/2024/08/10",
            headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
            timeout=30,
        )

    @patch("wikiedits.api.split_date")
    @patch("wikiedits.api.requests.get")
    def test_top_by_net_diff_date_splitting(self, mock_get, mock_split):
        """Test that date splitting is called correctly"""
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"results": [{"top": []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_split.return_value = ("2024", "09", "15")

        top_by_net_diff("en.wikipedia", "2024-09-15")

        mock_split.assert_called_once_with("2024-09-15")
        mock_get.assert_called_once_with(
            "https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-net-bytes-difference/en.wikipedia/all-editor-types/all-page-types/2024/09/15",
            headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
            timeout=30,
        )

    def test_top_by_net_diff_invalid_date(self):
        """Test most edited net with invalid date format"""
        with self.assertRaises(ValueError) as context:
            top_by_net_diff("en.wikipedia", "invalid-date")

        self.assertIn("Invalid date format", str(context.exception))
        self.assertIn("invalid-date", str(context.exception))

    def test_top_by_net_diff_none_date(self):
        """Test most edited net with None date"""
        with self.assertRaises(ValueError) as context:
            top_by_net_diff("en.wikipedia", None)

        self.assertIn("Invalid date format", str(context.exception))

    def test_top_by_net_diff_empty_date(self):
        """Test most edited net with empty date string"""
        with self.assertRaises(ValueError) as context:
            top_by_net_diff("en.wikipedia", "")

        self.assertIn("Invalid date format", str(context.exception))


if __name__ == "__main__":
    unittest.main()
