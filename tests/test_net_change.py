import unittest
from unittest.mock import patch, Mock
from wikiedits.api import net_change_aggregate, net_change_per_page


class TestNetChange(unittest.TestCase):
    
    @patch('wikiedits.api.requests.get')
    def test_net_change_aggregate_basic(self, mock_get):
        """Test basic net change aggregate functionality"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{
                'results': [
                    {'project': 'en.wikipedia', 'net_bytes_diff': 15000, 'timestamp': '20240101'},
                    {'project': 'en.wikipedia', 'net_bytes_diff': 18000, 'timestamp': '20240102'}
                ]
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = net_change_aggregate('en.wikipedia', 'daily', '20240101', '20240102')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/bytes-difference/net/aggregate/en.wikipedia/all-editor-types/all-page-types/daily/20240101/20240102',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
        self.assertEqual(result[0]['net_bytes_diff'], 15000)
        self.assertEqual(result[1]['net_bytes_diff'], 18000)
    
    @patch('wikiedits.api.requests.get')
    def test_net_change_aggregate_custom_parameters(self, mock_get):
        """Test net change aggregate with custom parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': []}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        net_change_aggregate(
            'de.wikipedia',
            'monthly',
            '20240101',
            '20240105',
            editor_type='user',
            page_type='content'
        )
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/bytes-difference/net/aggregate/de.wikipedia/user/content/monthly/20240101/20240105',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.requests.get')
    def test_net_change_per_page_basic(self, mock_get):
        """Test basic net change per page functionality"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{
                'results': [
                    {'project': 'en.wikipedia', 'page_title': 'Python', 'net_bytes_diff': 500, 'timestamp': '20240101'},
                    {'project': 'en.wikipedia', 'page_title': 'Python', 'net_bytes_diff': -200, 'timestamp': '20240102'}
                ]
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = net_change_per_page('en.wikipedia', 'Python', 'daily', '20240101', '20240102')
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/bytes-difference/net/per-page/en.wikipedia/Python/all-editor-types/daily/20240101/20240102',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
        self.assertEqual(result[0]['net_bytes_diff'], 500)
        self.assertEqual(result[1]['net_bytes_diff'], -200)
    
    @patch('wikiedits.api.requests.get')
    def test_net_change_per_page_custom_parameters(self, mock_get):
        """Test net change per page with custom parameters"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': []}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        net_change_per_page(
            'es.wikipedia',
            'Machine_learning',
            'monthly',
            '20240101',
            '20240105',
            editor_type='user'
        )
        
        mock_get.assert_called_once_with(
            'https://wikimedia.org/api/rest_v1/metrics/bytes-difference/net/per-page/es.wikipedia/Machine_learning/user/monthly/20240101/20240105',
            headers={
                'User-Agent': 'wikiedits-api/0.1.0',
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    @patch('wikiedits.api.validate_date')
    @patch('wikiedits.api.requests.get')
    def test_net_change_date_validation(self, mock_get, mock_validate):
        """Test that date validation is called for both functions"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': [{'results': []}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_validate.side_effect = ['20240101', '20240102', '20240101', '20240102']
        
        net_change_aggregate('en.wikipedia', 'daily', '2024-01-01', '2024-01-02')
        net_change_per_page('en.wikipedia', 'Test_page', 'daily', '2024-01-01', '2024-01-02')
        
        self.assertEqual(mock_validate.call_count, 4)


if __name__ == '__main__':
    unittest.main()