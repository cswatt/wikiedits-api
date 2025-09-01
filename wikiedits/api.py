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

def _make_request(endpoint, args, api_base_url=BASE_URL):
  url = "/".join([api_base_url, endpoint, args])
  
  try:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
    response.raise_for_status()
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

def aggregate_edits(project, start, end,
                    editor_type='all-editor-types', page_type='all-page-types', granularity='daily'):

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

  return _make_request(endpoint, args)

def new_pages(project, start, end,
              editor_type='all-editor-types', page_type='all-page-types', granularity='daily'):

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
  
  return _make_request(endpoint, args)
  
