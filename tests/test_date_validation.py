import unittest
from wikiedits.api import _validate_date


class TestDateValidation(unittest.TestCase):
    
    def test_validate_date_yyyymmdd_format(self):
        """Test date already in YYYYMMDD format"""
        result = _validate_date('20240315')
        self.assertEqual(result, '20240315')
    
    def test_validate_date_iso_format(self):
        """Test ISO date format conversion"""
        result = _validate_date('2024-03-15')
        self.assertEqual(result, '20240315')
    
    def test_validate_date_slash_format(self):
        """Test MM/DD/YYYY format conversion"""
        result = _validate_date('03/15/2024')
        self.assertEqual(result, '20240315')
    
    def test_validate_date_dot_format(self):
        """Test DD.MM.YYYY format conversion"""
        result = _validate_date('15.03.2024')
        self.assertEqual(result, '20240315')
    
    def test_validate_date_text_format(self):
        """Test text date format conversion"""
        result = _validate_date('March 15, 2024')
        self.assertEqual(result, '20240315')
    
    def test_validate_date_invalid_format(self):
        """Test invalid date format raises ValueError"""
        with self.assertRaises(ValueError) as context:
            _validate_date('invalid-date')
        
        self.assertIn('Invalid date format', str(context.exception))
        self.assertIn('invalid-date', str(context.exception))
    
    def test_validate_date_none_input(self):
        """Test None input raises ValueError"""
        with self.assertRaises(ValueError) as context:
            _validate_date(None)
        
        self.assertIn('Invalid date format', str(context.exception))
    
    def test_validate_date_empty_string(self):
        """Test empty string raises ValueError"""
        with self.assertRaises(ValueError) as context:
            _validate_date('')
        
        self.assertIn('Invalid date format', str(context.exception))
    
    def test_validate_date_partial_yyyymmdd_invalid(self):
        """Test partial YYYYMMDD format (not 8 digits) that's invalid"""
        with self.assertRaises(ValueError) as context:
            _validate_date('2024031')
        
        self.assertIn('Invalid date format', str(context.exception))
    
    def test_validate_date_with_time(self):
        """Test date with time component"""
        result = _validate_date('2024-03-15T10:30:00')
        self.assertEqual(result, '20240315')


if __name__ == '__main__':
    unittest.main()