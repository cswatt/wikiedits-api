import unittest
from unittest.mock import patch, Mock
from wikiedits.api import new_pages, _make_request


class TestNewPages(unittest.TestCase):
    
    @patch('wikiedits.api.requests.get')
    def test_new_pages_basic(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {'project': 'en.wikipedia', 'new_pages': 100, 'timestamp': '20240101'},
                {'project': 'en.wikipedia', 'new_pages': 120, 'timestamp': '20240102'}
            ]
        }
        mock_get.return_value = mock_response
        
        result = new_pages('en.wikipedia', '20240101', '20240102')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/new/en.wikipedia/all-editor-types/all-page-types/daily/20240101/20240102',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
        self.assertEqual(result['items'][0]['new_pages'], 100)
        self.assertEqual(result['items'][1]['new_pages'], 120)

    @patch('wikiedits.api.requests.get')
    def test_new_pages_with_custom_parameters(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response
        
        new_pages(
            'es.wikipedia', 
            '20240101', 
            '20240105',
            editor_type='user',
            page_type='content',
            granularity='monthly'
        )
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/new/es.wikipedia/user/content/monthly/20240101/20240105',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )

    @patch('wikiedits.api.requests.get')
    def test_new_pages_with_default_parameters(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response
        
        new_pages('fr.wikipedia', '20240201', '20240228')
        
        expected_url = 'https://wikimedia.org/api/rest_v1/metrics/edited-pages/new/fr.wikipedia/all-editor-types/all-page-types/daily/20240201/20240228'
        mock_get.assert_called_once_with(
            expected_url,
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )

    @patch('wikiedits.api.requests.get')
    def test_make_request_function(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'test': 'data'}
        mock_get.return_value = mock_response
        
        result = _make_request('test-endpoint', 'test/args')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/test-endpoint/test/args',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
        self.assertEqual(result, {'test': 'data'})


if __name__ == '__main__':
    unittest.main()