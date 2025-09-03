from dateutil.parser import parse as date_parse
from typing import Tuple


def validate_date(date_string: str) -> str:
    """
    Validate and normalize date string to YYYYMMDD format.
    """
    try:
        if len(date_string) == 8 and date_string.isdigit():
            # if already in YYYYMMDD format, return
            return date_string

        # otherwise, parse and return normalized date string
        parsed_date = date_parse(date_string)
        return parsed_date.strftime("%Y%m%d")
    except (ValueError, TypeError):
        raise ValueError(f"Invalid date format: {date_string}. Expected YYYYMMDD or parseable date string.")


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
        return (parsed_date.strftime("%Y"), parsed_date.strftime("%m"), parsed_date.strftime("%d"))
    except (ValueError, TypeError):
        raise ValueError(f"Invalid date format: {date_string}. Expected YYYYMMDD or parseable date string.")