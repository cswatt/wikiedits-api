import unittest
from unittest.mock import patch, Mock
from wikiedits.api import edits_per_page


class TestEditsPerPage(unittest.TestCase):
    
    @patch('wikiedits.api.requests.get')
    def test_edits_per_page_basic(self, mock_get):
        """Test basic edits per page functionality"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{
                'results': [
                    {'project': 'en.wikipedia', 'page_title': 'Python', 'edits': 45, 'timestamp': '20240101'},
                    {'project': 'en.wikipedia', 'page_title': 'Python', 'edits': 52, 'timestamp': '20240102'}
                ]
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = edits_per_page('en.wikipedia', 'Python', 'daily', '20240101', '20240102')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edits/per-page/en.wikipedia/Python/all-editor-types/all-page-types/daily/20240101/20240102',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
        self.assertEqual(result[0]['edits'], 45)
        self.assertEqual(result[1]['edits'], 52)
    
    @patch('wikiedits.api.requests.get')
    def test_edits_per_page_with_custom_parameters(self, mock_get):
        """Test edits per page with custom parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': []}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        edits_per_page(
            'es.wikipedia',
            'Machine_learning',
            'monthly',
            '20240101',
            '20240105',
            editor_type='user',
            page_type='content'
        )
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edits/per-page/es.wikipedia/Machine_learning/user/content/monthly/20240101/20240105',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.requests.get')
    def test_edits_per_page_with_default_parameters(self, mock_get):
        """Test edits per page with default parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': []}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        edits_per_page('fr.wikipedia', 'Artificial_intelligence', 'daily', '20240201', '20240228')
        
        expected_url = 'https://wikimedia.org/api/rest_v1/metrics/edits/per-page/fr.wikipedia/Artificial_intelligence/all-editor-types/all-page-types/daily/20240201/20240228'
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
    def test_edits_per_page_date_validation(self, mock_get, mock_validate):
        """Test that date validation is called"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': []}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_validate.side_effect = ['20240101', '20240102']
        
        edits_per_page('en.wikipedia', 'Test_page', 'daily', '2024-01-01', '2024-01-02')
        
        self.assertEqual(mock_validate.call_count, 2)
        mock_validate.assert_any_call('2024-01-01')
        mock_validate.assert_any_call('2024-01-02')


if __name__ == '__main__':
    unittest.main()