import unittest
from unittest.mock import patch, Mock
from wikiedits.api import edits_aggregate


class TestEditsAggregate(unittest.TestCase):
    
    @patch('wikiedits.api.requests.get')
    def test_edits_aggregate_basic(self, mock_get):
        """Test basic edits aggregate functionality"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {
                    'results': [
                        {'project': 'en.wikipedia', 'edits': 1000, 'timestamp': '20240101'},
                        {'project': 'en.wikipedia', 'edits': 1200, 'timestamp': '20240102'}
                    ]
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = edits_aggregate('en.wikipedia', 'daily', '20240101', '20240102')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edits/aggregate/en.wikipedia/all-editor-types/all-page-types/daily/20240101/20240102',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
        self.assertEqual(result[0]['edits'], 1000)
        self.assertEqual(result[1]['edits'], 1200)
    
    @patch('wikiedits.api.requests.get')
    def test_edits_aggregate_with_custom_parameters(self, mock_get):
        """Test edits aggregate with custom parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{'results': []}]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        edits_aggregate(
            'es.wikipedia', 
            'monthly',
            '20240101', 
            '20240105',
            editor_type='user',
            page_type='content'
        )
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edits/aggregate/es.wikipedia/user/content/monthly/20240101/20240105',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.requests.get')
    def test_edits_aggregate_with_default_parameters(self, mock_get):
        """Test edits aggregate with default parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{'results': []}]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        edits_aggregate('fr.wikipedia', 'daily', '20240201', '20240228')
        
        expected_url = 'https://wikimedia.org/api/rest_v1/metrics/edits/aggregate/fr.wikipedia/all-editor-types/all-page-types/daily/20240201/20240228'
        mock_get.assert_called_once_with(
            expected_url,
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.validate_dates')
    @patch('wikiedits.api.requests.get')
    def test_edits_aggregate_date_validation(self, mock_get, mock_validate):
        """Test that date validation is called"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{'results': []}]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_validate.return_value = ('20240101', '20240102')
        
        edits_aggregate('en.wikipedia', 'daily', '2024-01-01', '2024-01-02')
        
        self.assertEqual(mock_validate.call_count, 1)
        mock_validate.assert_called_with('daily', '2024-01-01', '2024-01-02')


if __name__ == '__main__':
    unittest.main()