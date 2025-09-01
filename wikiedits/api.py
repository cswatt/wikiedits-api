import requests
from dateutil.parser import parse as date_parse

__version__ = "0.1.0"

BASE_URL = "https://wikimedia.org/api/rest_v1/metrics"

DEFAULT_HEADERS = {
  "User-Agent": "wikiedits-api/{version}".format(version=__version__),
  "Accept": "application/json"
}

def _validate_date(date_string):
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

def _split_date(date_string):
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
  
def _make_request(endpoint, args, api_base_url=BASE_URL):
  """
  Make HTTP request to Wikimedia API endpoint with error handling.
  
  Args:
    endpoint: API endpoint path (e.g. 'edits/aggregate')
    args: Formatted URL path arguments
    api_base_url: Base URL for the API (defaults to Wikimedia REST API)
    
  Returns:
    dict: JSON response from the API
    
  Raises:
    requests.exceptions.RequestException: For all request-related errors
  """
  # Construct full URL by joining base URL, endpoint, and arguments
  url = "/".join([api_base_url, endpoint, args])
  
  try:
    # Make GET request with default headers and 30 second timeout
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
    response.raise_for_status()  # Raise exception for HTTP error status codes
    return response.json()
  except requests.exceptions.Timeout:
    raise requests.exceptions.RequestException(f"Request timed out for URL: {url}")
  except requests.exceptions.ConnectionError:
    raise requests.exceptions.RequestException(f"Failed to connect to API: {url}")
  except requests.exceptions.HTTPError as e:
    raise requests.exceptions.RequestException(f"HTTP error {response.status_code}: {response.text}")
  except requests.exceptions.JSONDecodeError:
    raise requests.exceptions.RequestException(f"Invalid JSON response from: {url}")
  except requests.exceptions.RequestException as e:
    raise requests.exceptions.RequestException(f"Request failed: {str(e)}")

def edits_aggregate(project, granularity, start, end,
                    editor_type='all-editor-types', page_type='all-page-types'):

  start = _validate_date(start)
  end = _validate_date(end)

  endpoint = "edits/aggregate"
  _args = "{project}/{editor_type}/{page_type}/{granularity}/{start}/{end}"

  args = _args.format(project=project,
                      editor_type=editor_type,
                      page_type=page_type,
                      granularity=granularity,
                      start=start,
                      end=end)

  response = _make_request(endpoint, args)
  return response['items'][0]['results']

def edits_per_page(project, page_title, granularity, start, end,
                   editor_type='all-editor-types', page_type='all-page-types'):

  start = _validate_date(start)
  end = _validate_date(end)

  endpoint = "edits/per-page"
  _args = "{project}/{page_title}/{editor_type}/{page_type}/{granularity}/{start}/{end}"

  args = _args.format(project=project,
                      page_title=page_title,
                      editor_type=editor_type,
                      page_type=page_type,
                      granularity=granularity,
                      start=start,
                      end=end)

  response = _make_request(endpoint, args)
  return response['items'][0]['results']

def net_change_aggregate(project, granularity, start, end,
                         editor_type='all-editor-types', page_type='all-page-types'):

  start = _validate_date(start)
  end = _validate_date(end)

  endpoint = "bytes-difference/net/aggregate"
  _args = "{project}/{editor_type}/{page_type}/{granularity}/{start}/{end}"

  args = _args.format(project=project,
                      editor_type=editor_type,
                      page_type=page_type,
                      granularity=granularity,
                      start=start,
                      end=end)

  response = _make_request(endpoint, args)
  return response['items'][0]['results']

def net_change_per_page(project, page_title, granularity, start, end,
                        editor_type='all-editor-types', page_type='all-page-types'):

  start = _validate_date(start)
  end = _validate_date(end)

  endpoint = "bytes-difference/net/per-page"
  _args = "{project}/{page_title}/{editor_type}/{page_type}/{granularity}/{start}/{end}"

  args = _args.format(project=project,
                      page_title=page_title,
                      editor_type=editor_type,
                      page_type=page_type,
                      granularity=granularity,
                      start=start,
                      end=end)

  response = _make_request(endpoint, args)
  return response['items'][0]['results']

def abs_change_aggregate(project, granularity, start, end,
                         editor_type='all-editor-types', page_type='all-page-types'):

  start = _validate_date(start)
  end = _validate_date(end)

  endpoint = "bytes-difference/absolute/aggregate"
  _args = "{project}/{editor_type}/{page_type}/{granularity}/{start}/{end}"

  args = _args.format(project=project,
                      editor_type=editor_type,
                      page_type=page_type,
                      granularity=granularity,
                      start=start,
                      end=end)

  response = _make_request(endpoint, args)
  return response['items'][0]['results']

def abs_change_per_page(project, page_title, granularity, start, end,
                        editor_type='all-editor-types', page_type='all-page-types'):

  start = _validate_date(start)
  end = _validate_date(end)

  endpoint = "bytes-difference/absolute/per-page"
  _args = "{project}/{page_title}/{editor_type}/{page_type}/{granularity}/{start}/{end}"

  args = _args.format(project=project,
                      page_title=page_title,
                      editor_type=editor_type,
                      page_type=page_type,
                      granularity=granularity,
                      start=start,
                      end=end)

  response = _make_request(endpoint, args)
  return response['items'][0]['results']
  
def new_pages(project, granularity, start, end,
              editor_type='all-editor-types', page_type='all-page-types'):

  start = _validate_date(start)
  end = _validate_date(end)

  endpoint = "edited-pages/new"
  _args = "{project}/{editor_type}/{page_type}/{granularity}/{start}/{end}"

  args = _args.format(project=project,
                      editor_type=editor_type,
                      page_type=page_type,
                      granularity=granularity,
                      start=start,
                      end=end)
  
  response = _make_request(endpoint, args)
  return response['items'][0]['results']

def edited_pages(project, granularity, start, end,
                 editor_type='all-editor-types', page_type='all-page-types', activity_level='all-activity-levels'):

  start = _validate_date(start)
  end = _validate_date(end)

  endpoint = "edited-pages/aggregate"
  _args = "{project}/{editor_type}/{page_type}/{activity_level}/{granularity}/{start}/{end}"

  args = _args.format(project=project,
                      editor_type=editor_type,
                      page_type=page_type,
                      activity_level=activity_level,
                      granularity=granularity,
                      start=start,
                      end=end)
  
  response = _make_request(endpoint, args)
  return response['items'][0]['results']

def top_by_net_diff(project, date,
                    editor_type='all-editor-types', page_type='all-page-types'):

  year, month, day = _split_date(date)

  endpoint = "edited-pages/top-by-net-bytes-difference"
  _args = "{project}/{editor_type}/{page_type}/{year}/{month}/{day}"

  args = _args.format(project=project,
                      editor_type=editor_type,
                      page_type=page_type,
                      year=year,
                      month=month,
                      day=day)
  
  response = _make_request(endpoint, args)
  return response['items'][0]['results'][0]['top']

def top_by_abs_diff(project, date,
                    editor_type='all-editor-types', page_type='all-page-types'):

  year, month, day = _split_date(date)

  endpoint = "edited-pages/top-by-absolute-bytes-difference"
  _args = "{project}/{editor_type}/{page_type}/{year}/{month}/{day}"

  args = _args.format(project=project,
                      editor_type=editor_type,
                      page_type=page_type,
                      year=year,
                      month=month,
                      day=day)
  
  response = _make_request(endpoint, args)
  return response['items'][0]['results'][0]['top']

def top_by_edits(project, date,
                    editor_type='all-editor-types', page_type='all-page-types'):

  year, month, day = _split_date(date)

  endpoint = "edited-pages/top-by-edits"
  _args = "{project}/{editor_type}/{page_type}/{year}/{month}/{day}"

  args = _args.format(project=project,
                      editor_type=editor_type,
                      page_type=page_type,
                      year=year,
                      month=month,
                      day=day)
  
  response = _make_request(endpoint, args)
  return response['items'][0]['results'][0]['top']