from typing import Tuple

from dateutil.parser import parse as date_parse
from dateutil.relativedelta import relativedelta


def validate_dates(granularity: str, start: str, end: str) -> Tuple[str, str]:
  """
  Validate and normalize start and end dates based on granularity.

  Args:
    granularity: "daily" or "monthly"
    start: Start date in any parseable format
    end: End date in any parseable format

  Returns:
    tuple: (start_date, end_date) in YYYYMMDD format

  Raises:
    ValueError: If end date is before start date or invalid granularity
  """
  # Validate and parse the dates
  start_parsed = date_parse(start)
  end_parsed = date_parse(end)

  # Check if end is before start
  if end_parsed < start_parsed:
    raise ValueError(f"End date ({end}) cannot be before start date ({start})")

  # Handle equal dates based on granularity
  if start_parsed == end_parsed:
    if granularity == "daily":
      # Add one day to end date
      end_parsed = start_parsed + relativedelta(days=1)
      return (start_parsed.strftime("%Y%m%d"), end_parsed.strftime("%Y%m%d"))
    elif granularity == "monthly":
      # Set start to beginning of month, end to first day of next month
      start_parsed = start_parsed.replace(day=1)
      end_parsed = start_parsed + relativedelta(months=1)
      return (start_parsed.strftime("%Y%m%d"), end_parsed.strftime("%Y%m%d"))
    else:
      raise ValueError(
        f"Invalid granularity: {granularity}. Expected 'daily' or 'monthly'"
      )

  return (start_parsed.strftime("%Y%m%d"), end_parsed.strftime("%Y%m%d"))


def split_date(date_string: str) -> Tuple[str, str, str]:
  """
  Split date string into year, month, day tuple.

  Args:
    date_string: Date in any parseable format

  Returns:
    tuple: (year, month, day) in YYYY, MM, DD format
  """
  try:
    if len(date_string) == 8 and date_string.isdigit():
      # if already in YYYYMMDD format, split directly
      return (date_string[:4], date_string[4:6], date_string[6:8])

    # otherwise, parse and return formatted components
    parsed_date = date_parse(date_string)
    return (
      parsed_date.strftime("%Y"),
      parsed_date.strftime("%m"),
      parsed_date.strftime("%d"),
    )
  except (ValueError, TypeError):
    raise ValueError(
      f"Invalid date format: {date_string}. Expected YYYYMMDD or "
      f"parseable date string."
    )
