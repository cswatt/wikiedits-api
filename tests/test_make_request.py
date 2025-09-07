import unittest
from unittest.mock import Mock, patch

import requests

from wikiedits.api import _make_request


class TestMakeRequest(unittest.TestCase):
  @patch("wikiedits.api.requests.get")
  def test_make_request_success(self, mock_get):
    """Test successful request"""
    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "data": "test"}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = _make_request("test-endpoint", "test/args")

    mock_get.assert_called_once_with(
      "https://wikimedia.org/api/rest_v1/metrics/test-endpoint/test/args",
      headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
      timeout=30,
    )
    self.assertEqual(result, {"success": True, "data": "test"})

  @patch("wikiedits.api.requests.get")
  def test_make_request_with_custom_base_url(self, mock_get):
    """Test request with custom base URL"""
    mock_response = Mock()
    mock_response.json.return_value = {"data": "custom"}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    custom_base = "https://custom-api.example.com/v1"
    result = _make_request("endpoint", "args", api_base_url=custom_base)

    mock_get.assert_called_once_with(
      "https://custom-api.example.com/v1/endpoint/args",
      headers={"User-Agent": "wikiedits-api/0.1.0", "Accept": "application/json"},
      timeout=30,
    )
    self.assertEqual(result, {"data": "custom"})

  @patch("wikiedits.api.requests.get")
  def test_make_request_timeout_error(self, mock_get):
    """Test timeout error handling"""
    mock_get.side_effect = requests.exceptions.Timeout()

    with self.assertRaises(requests.exceptions.RequestException) as context:
      _make_request("test-endpoint", "test/args")

    self.assertIn("Request timed out", str(context.exception))
    self.assertIn(
      "https://wikimedia.org/api/rest_v1/metrics/test-endpoint/test/args",
      str(context.exception),
    )

  @patch("wikiedits.api.requests.get")
  def test_make_request_connection_error(self, mock_get):
    """Test connection error handling"""
    mock_get.side_effect = requests.exceptions.ConnectionError()

    with self.assertRaises(requests.exceptions.RequestException) as context:
      _make_request("test-endpoint", "test/args")

    self.assertIn("Failed to connect to API", str(context.exception))
    self.assertIn(
      "https://wikimedia.org/api/rest_v1/metrics/test-endpoint/test/args",
      str(context.exception),
    )

  @patch("wikiedits.api.requests.get")
  def test_make_request_http_error(self, mock_get):
    """Test HTTP error handling"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_get.return_value = mock_response

    with self.assertRaises(requests.exceptions.RequestException) as context:
      _make_request("test-endpoint", "test/args")

    self.assertIn("HTTP error 404", str(context.exception))
    self.assertIn("Not Found", str(context.exception))

  @patch("wikiedits.api.requests.get")
  def test_make_request_json_decode_error(self, mock_get):
    """Test JSON decode error handling"""
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
      "msg", "doc", 0
    )
    mock_get.return_value = mock_response

    with self.assertRaises(requests.exceptions.RequestException) as context:
      _make_request("test-endpoint", "test/args")

    self.assertIn("Invalid JSON response", str(context.exception))
    self.assertIn(
      "https://wikimedia.org/api/rest_v1/metrics/test-endpoint/test/args",
      str(context.exception),
    )

  @patch("wikiedits.api.requests.get")
  def test_make_request_generic_request_exception(self, mock_get):
    """Test generic request exception handling"""
    mock_get.side_effect = requests.exceptions.RequestException("Generic error")

    with self.assertRaises(requests.exceptions.RequestException) as context:
      _make_request("test-endpoint", "test/args")

    self.assertIn("Request failed", str(context.exception))
    self.assertIn("Generic error", str(context.exception))


if __name__ == "__main__":
  unittest.main()
