import unittest
from unittest.mock import patch, Mock
from wikiedits.api import edited_pages


class TestEditedPages(unittest.TestCase):
    
    @patch('wikiedits.api.requests.get')
    def test_edited_pages_basic(self, mock_get):
        """Test basic edited pages functionality"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {'project': 'en.wikipedia', 'edited_pages': 2500, 'timestamp': '20240101'},
                {'project': 'en.wikipedia', 'edited_pages': 2800, 'timestamp': '20240102'}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = edited_pages('en.wikipedia', '20240101', '20240102')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/aggregate/en.wikipedia/all-editor-types/all-page-types/all-activity-levels/daily/20240101/20240102',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
        self.assertEqual(result['items'][0]['edited_pages'], 2500)
        self.assertEqual(result['items'][1]['edited_pages'], 2800)
    
    @patch('wikiedits.api.requests.get')
    def test_edited_pages_with_custom_parameters(self, mock_get):
        """Test edited pages with all custom parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        edited_pages(
            'de.wikipedia',
            '20240101',
            '20240105',
            editor_type='user',
            page_type='content',
            activity_level='1..4-edits',
            granularity='monthly'
        )
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/aggregate/de.wikipedia/user/content/1..4-edits/monthly/20240101/20240105',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.requests.get')
    def test_edited_pages_with_default_parameters(self, mock_get):
        """Test edited pages with default parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        edited_pages('fr.wikipedia', '20240201', '20240228')
        
        expected_url = 'https://wikimedia.org/api/rest_v1/metrics/edited-pages/aggregate/fr.wikipedia/all-editor-types/all-page-types/all-activity-levels/daily/20240201/20240228'
        mock_get.assert_called_once_with(
            expected_url,
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.requests.get')
    def test_edited_pages_with_partial_custom_parameters(self, mock_get):
        """Test edited pages with some custom parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        edited_pages(
            'es.wikipedia',
            '20240301',
            '20240331',
            activity_level='5..24-edits'
        )
        
        expected_url = 'https://wikimedia.org/api/rest_v1/metrics/edited-pages/aggregate/es.wikipedia/all-editor-types/all-page-types/5..24-edits/daily/20240301/20240331'
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
    def test_edited_pages_date_validation(self, mock_get, mock_validate):
        """Test that date validation is called"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_validate.side_effect = ['20240101', '20240102']
        
        edited_pages('en.wikipedia', '2024-01-01', '2024-01-02')
        
        self.assertEqual(mock_validate.call_count, 2)
        mock_validate.assert_any_call('2024-01-01')
        mock_validate.assert_any_call('2024-01-02')


if __name__ == '__main__':
    unittest.main()