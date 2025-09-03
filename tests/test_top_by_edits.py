import unittest
from unittest.mock import patch, Mock
from wikiedits.api import top_by_edits


class TestTopByEdits(unittest.TestCase):
    
    @patch('wikiedits.api.requests.get')
    def test_top_by_edits_basic(self, mock_get):
        """Test basic top by edits functionality"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{
                'results': [{
                    'top': [
                        {'project': 'en.wikipedia', 'page_title': 'Python', 'edits': 150, 'rank': 1},
                        {'project': 'en.wikipedia', 'page_title': 'JavaScript', 'edits': 145, 'rank': 2}
                    ]
                }]
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = top_by_edits('en.wikipedia', '20240315')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-edits/en.wikipedia/all-editor-types/all-page-types/2024/03/15',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
        self.assertEqual(result[0]['edits'], 150)
        self.assertEqual(result[1]['edits'], 145)
    
    @patch('wikiedits.api.requests.get')
    def test_top_by_edits_with_custom_parameters(self, mock_get):
        """Test top by edits with custom parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': [{'top': []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        top_by_edits(
            'fr.wikipedia',
            '20240415',
            editor_type='user',
            page_type='content'
        )
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-edits/fr.wikipedia/user/content/2024/04/15',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.requests.get')
    def test_top_by_edits_with_default_parameters(self, mock_get):
        """Test top by edits with default parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': [{'top': []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        top_by_edits('es.wikipedia', '20240201')
        
        expected_url = 'https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-edits/es.wikipedia/all-editor-types/all-page-types/2024/02/01'
        mock_get.assert_called_once_with(
            expected_url,
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.requests.get')
    def test_top_by_edits_iso_date_format(self, mock_get):
        """Test top by edits with ISO date format"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': [{'top': []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        top_by_edits('de.wikipedia', '2024-06-20')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-edits/de.wikipedia/all-editor-types/all-page-types/2024/06/20',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.requests.get')
    def test_top_by_edits_slash_date_format(self, mock_get):
        """Test top by edits with MM/DD/YYYY date format"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': [{'top': []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        top_by_edits('it.wikipedia', '07/25/2024')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-edits/it.wikipedia/all-editor-types/all-page-types/2024/07/25',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.requests.get')
    def test_top_by_edits_text_date_format(self, mock_get):
        """Test top by edits with text date format"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': [{'top': []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        top_by_edits('pt.wikipedia', 'August 10, 2024')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-edits/pt.wikipedia/all-editor-types/all-page-types/2024/08/10',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.split_date')
    @patch('wikiedits.api.requests.get')
    def test_top_by_edits_date_splitting(self, mock_get, mock_split):
        """Test that date splitting is called correctly"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': [{'top': []}]}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_split.return_value = ('2024', '09', '15')
        
        top_by_edits('en.wikipedia', '2024-09-15')
        
        mock_split.assert_called_once_with('2024-09-15')
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/edited-pages/top-by-edits/en.wikipedia/all-editor-types/all-page-types/2024/09/15',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    def test_top_by_edits_invalid_date(self):
        """Test top by edits with invalid date format"""
        with self.assertRaises(ValueError) as context:
            top_by_edits('en.wikipedia', 'invalid-date')
        
        self.assertIn('Invalid date format', str(context.exception))
        self.assertIn('invalid-date', str(context.exception))
    
    def test_top_by_edits_none_date(self):
        """Test top by edits with None date"""
        with self.assertRaises(ValueError) as context:
            top_by_edits('en.wikipedia', None)
        
        self.assertIn('Invalid date format', str(context.exception))
    
    def test_top_by_edits_empty_date(self):
        """Test top by edits with empty date string"""
        with self.assertRaises(ValueError) as context:
            top_by_edits('en.wikipedia', '')
        
        self.assertIn('Invalid date format', str(context.exception))


if __name__ == '__main__':
    unittest.main()