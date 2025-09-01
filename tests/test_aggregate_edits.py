import unittest
from unittest.mock import patch, Mock
from wikiedits.api import aggregate_edits


class TestAggregateEdits(unittest.TestCase):
    
    @patch('wikiedits.api.requests.get')
    def test_aggregate_edits_basic(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {'project': 'en.wikipedia', 'edits': 1500, 'timestamp': '20240101'},
                {'project': 'en.wikipedia', 'edits': 1800, 'timestamp': '20240102'}
            ]
        }
        mock_get.return_value = mock_response
        
        result = aggregate_edits('en.wikipedia', '20240101', '20240102')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edits/aggregate/en.wikipedia/all-editor-types/all-page-types/daily/20240101/20240102',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
        self.assertEqual(result['items'][0]['edits'], 1500)
        self.assertEqual(result['items'][1]['edits'], 1800)

    @patch('wikiedits.api.requests.get')
    def test_aggregate_edits_with_custom_parameters(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response
        
        aggregate_edits(
            'es.wikipedia', 
            '20240101', 
            '20240105',
            editor_type='user',
            page_type='content',
            granularity='monthly'
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
    def test_aggregate_edits_with_default_parameters(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_get.return_value = mock_response
        
        aggregate_edits('fr.wikipedia', '20240201', '20240228')
        
        expected_url = 'https://wikimedia.org/api/rest_v1/metrics/edits/aggregate/fr.wikipedia/all-editor-types/all-page-types/daily/20240201/20240228'
        mock_get.assert_called_once_with(
            expected_url,
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )


if __name__ == '__main__':
    unittest.main()