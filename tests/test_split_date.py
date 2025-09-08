import unittest

from wikiedits.date_utils import split_date


class TestSplitDate(unittest.TestCase):
  def test_split_date_yyyymmdd_format(self):
    """Test date already in YYYYMMDD format"""
    result = split_date("20250315")
    self.assertEqual(result, ("2025", "03", "15"))

  def test_split_date_iso_format(self):
    """Test ISO date format conversion"""
    result = split_date("2025-03-15")
    self.assertEqual(result, ("2025", "03", "15"))

  def test_split_date_slash_format(self):
    """Test MM/DD/YYYY format conversion"""
    result = split_date("03/15/2025")
    self.assertEqual(result, ("2025", "03", "15"))

  def test_split_date_dot_format(self):
    """Test DD.MM.YYYY format conversion"""
    result = split_date("15.03.2025")
    self.assertEqual(result, ("2025", "03", "15"))

  def test_split_date_text_format(self):
    """Test text date format conversion"""
    result = split_date("March 15, 2025")
    self.assertEqual(result, ("2025", "03", "15"))

  def test_split_date_single_digit_components(self):
    """Test date with single digit month and day"""
    result = split_date("2025-01-05")
    self.assertEqual(result, ("2025", "01", "05"))

  def test_split_date_december_format(self):
    """Test date in December (month 12)"""
    result = split_date("2025-12-31")
    self.assertEqual(result, ("2025", "12", "31"))

  def test_split_date_with_time_component(self):
    """Test date with time component"""
    result = split_date("2025-03-15T10:30:00")
    self.assertEqual(result, ("2025", "03", "15"))

  def test_split_date_yyyymmdd_edge_cases(self):
    """Test YYYYMMDD format with different months and days"""
    test_cases = [
    ("20250101", ("2025", "01", "01")),
    ("20251231", ("2025", "12", "31")),
    ("20250630", ("2025", "06", "30")),
    ("20250229", ("2025", "02", "29")),  # Leap year
    ]

    for date_input, expected in test_cases:
      with self.subTest(date=date_input):
        result = split_date(date_input)
        self.assertEqual(result, expected)

  def test_split_date_invalid_format(self):
    """Test invalid date format raises ValueError"""
    with self.assertRaises(ValueError) as context:
      split_date("invalid-date")

    self.assertIn("Invalid date format", str(context.exception))
    self.assertIn("invalid-date", str(context.exception))

  def test_split_date_none_input(self):
    """Test None input raises ValueError"""
    with self.assertRaises(ValueError) as context:
      split_date(None)

    self.assertIn("Invalid date format", str(context.exception))

  def test_split_date_empty_string(self):
    """Test empty string raises ValueError"""
    with self.assertRaises(ValueError) as context:
      split_date("")

    self.assertIn("Invalid date format", str(context.exception))

  def test_split_date_partial_yyyymmdd_invalid(self):
    """Test partial YYYYMMDD format (not 8 digits) that's invalid"""
    with self.assertRaises(ValueError) as context:
      split_date("2025031")

    self.assertIn("Invalid date format", str(context.exception))

  def test_split_date_too_long_numeric_string(self):
    """Test numeric string longer than 8 digits"""
    with self.assertRaises(ValueError) as context:
      split_date("202503151")

    self.assertIn("Invalid date format", str(context.exception))


if __name__ == "__main__":
  unittest.main()

