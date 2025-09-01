import unittest
from unittest.mock import patch, Mock
from wikiedits.api import new_pages


class TestNewPages(unittest.TestCase):
    
    @patch('wikiedits.api.requests.get')
    def test_new_pages_basic(self, mock_get):
        """Test basic new pages functionality"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{
                'results': [
                    {'project': 'en.wikipedia', 'new_pages': 150, 'timestamp': '20240101'},
                    {'project': 'en.wikipedia', 'new_pages': 175, 'timestamp': '20240102'}
                ]
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = new_pages('en.wikipedia', 'daily', '20240101', '20240102')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/new/en.wikipedia/all-editor-types/all-page-types/daily/20240101/20240102',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
        self.assertEqual(result[0]['new_pages'], 150)
        self.assertEqual(result[1]['new_pages'], 175)
    
    @patch('wikiedits.api.requests.get')
    def test_new_pages_with_custom_parameters(self, mock_get):
        """Test new pages with custom parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': []}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        new_pages(
            'de.wikipedia',
            'monthly',
            '20240101',
            '20240105',
            editor_type='user',
            page_type='content'
        )
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/new/de.wikipedia/user/content/monthly/20240101/20240105',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.requests.get')
    def test_new_pages_with_default_parameters(self, mock_get):
        """Test new pages with default parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': []}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        new_pages('fr.wikipedia', 'daily', '20240201', '20240228')
        
        expected_url = 'https://wikimedia.org/api/rest_v1/metrics/edited-pages/new/fr.wikipedia/all-editor-types/all-page-types/daily/20240201/20240228'
        mock_get.assert_called_once_with(
            expected_url,
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api._validate_date')
    @patch('wikiedits.api.requests.get')
    def test_new_pages_date_validation(self, mock_get, mock_validate):
        """Test that date validation is called"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': []}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_validate.side_effect = ['20240101', '20240102']
        
        new_pages('en.wikipedia', 'daily', '2024-01-01', '2024-01-02')
        
        self.assertEqual(mock_validate.call_count, 2)
        mock_validate.assert_any_call('2024-01-01')
        mock_validate.assert_any_call('2024-01-02')


if __name__ == '__main__':
    unittest.main()