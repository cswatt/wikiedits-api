from typing import Any, Dict, List, cast

import requests

from .date_utils import split_date, validate_dates

__version__ = "0.1.0"

BASE_URL = "https://wikimedia.org/api/rest_v1/metrics"

DEFAULT_HEADERS = {
  "User-Agent": "wikiedits-api/{version}".format(version=__version__),
  "Accept": "application/json",
}


def _make_request(
  endpoint: str, args: str, api_base_url: str = BASE_URL
) -> Dict[str, object]:
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
    return cast(Dict[str, object], response.json())
  except requests.exceptions.Timeout:
    raise requests.exceptions.RequestException(f"Request timed out for URL: {url}")
  except requests.exceptions.ConnectionError:
    raise requests.exceptions.RequestException(f"Failed to connect to API: {url}")
  except requests.exceptions.HTTPError:
    raise requests.exceptions.RequestException(
      f"HTTP error {response.status_code}: {response.text}"
    )
  except requests.exceptions.JSONDecodeError:
    raise requests.exceptions.RequestException(f"Invalid JSON response from: {url}")
  except requests.exceptions.RequestException as e:
    raise requests.exceptions.RequestException(f"Request failed: {str(e)}")


def _build_standard_args(
  project: str,
  editor_type: str,
  page_type: str,
  granularity: str,
  start: str,
  end: str,
) -> str:
  """
  Build URL arguments for standard aggregate API endpoints.
  """
  return f"{project}/{editor_type}/{page_type}/{granularity}/{start}/{end}"


def _build_per_page_args(
  project: str,
  page_title: str,
  editor_type: str,
  granularity: str,
  start: str,
  end: str,
) -> str:
  """
  Build URL arguments for per-page API endpoints.
  """
  return f"{project}/{page_title}/{editor_type}/{granularity}/{start}/{end}"


def _build_top_by_args(
  project: str, editor_type: str, page_type: str, year: str, month: str, day: str
) -> str:
  """
  Build URL arguments for top-by API endpoints.
  """
  return f"{project}/{editor_type}/{page_type}/{year}/{month}/{day}"


def _make_standard_request(
  endpoint: str,
  project: str,
  granularity: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> List[Dict[str, object]]:
  """
  Make a standard API request for aggregate endpoints.
  """
  start, end = validate_dates(granularity, start, end)
  args = _build_standard_args(
    project, editor_type, page_type, granularity, start, end
  )
  response = _make_request(endpoint, args)
  items = cast(List[Dict[str, Any]], response["items"])
  results = cast(List[Dict[str, object]], items[0]["results"])
  return results


def _make_per_page_request(
  endpoint: str,
  project: str,
  page_title: str,
  granularity: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
) -> List[Dict[str, Any]]:
  """
  Make a per-page API request for specific page endpoints.
  """
  start, end = validate_dates(granularity, start, end)
  args = _build_per_page_args(
    project, page_title, editor_type, granularity, start, end
  )
  response = _make_request(endpoint, args)
  items = cast(List[Dict[str, Any]], response["items"])
  results = cast(List[Dict[str, Any]], items[0]["results"])
  return results


def _make_top_by_request(
  endpoint: str,
  project: str,
  date: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> List[Dict[str, object]]:
  """
  Make a top-by API request for daily top pages endpoints.
  """
  year, month, day = split_date(date)
  args = _build_top_by_args(project, editor_type, page_type, year, month, day)
  response = _make_request(endpoint, args)
  items = cast(List[Dict[str, Any]], response["items"])
  results = cast(List[Dict[str, Any]], items[0]["results"])
  top = cast(List[Dict[str, object]], results[0]["top"])
  return top


def edits_aggregate(
  project: str,
  granularity: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> List[Dict[str, Any]]:
  return _make_standard_request(
    "edits/aggregate", project, granularity, start, end, editor_type, page_type
  )


def sum_edits_aggregate(
  project: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> int:
  response = edits_aggregate(project, "daily", start, end, editor_type, page_type)
  return sum(item["edits"] for item in response)


def edits_per_page(
  project: str,
  page_title: str,
  granularity: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
) -> List[Dict[str, Any]]:
  return _make_per_page_request(
    "edits/per-page", project, page_title, granularity, start, end, editor_type
  )


def sum_edits_per_page(
  project: str,
  page_title: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
) -> int:
  response = edits_per_page(project, page_title, "daily", start, end, editor_type)
  return sum(item["edits"] for item in response)


def net_bytes_diff_aggregate(
  project: str,
  granularity: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> List[Dict[str, Any]]:
  return _make_standard_request(
    "bytes-difference/net/aggregate",
    project,
    granularity,
    start,
    end,
    editor_type,
    page_type,
  )


def net_bytes_diff_per_page(
  project: str,
  page_title: str,
  granularity: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
) -> List[Dict[str, Any]]:
  return _make_per_page_request(
    "bytes-difference/net/per-page",
    project,
    page_title,
    granularity,
    start,
    end,
    editor_type,
  )


def abs_change_aggregate(
  project: str,
  granularity: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> List[Dict[str, Any]]:
  return _make_standard_request(
    "bytes-difference/absolute/aggregate",
    project,
    granularity,
    start,
    end,
    editor_type,
    page_type,
  )


def abs_change_per_page(
  project: str,
  page_title: str,
  granularity: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
) -> List[Dict[str, Any]]:
  return _make_per_page_request(
    "bytes-difference/absolute/per-page",
    project,
    page_title,
    granularity,
    start,
    end,
    editor_type,
  )


def new_pages(
  project: str,
  granularity: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> List[Dict[str, Any]]:
  return _make_standard_request(
    "edited-pages/new", project, granularity, start, end, editor_type, page_type
  )


def sum_new_pages(
  project: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> int:
  response = new_pages(project, "daily", start, end, editor_type, page_type)
  return sum(item["new_pages"] for item in response)


def edited_pages(
  project: str,
  granularity: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
  activity_level: str = "all-activity-levels",
) -> List[Dict[str, object]]:
  start, end = validate_dates(granularity, start, end)
  args = (
    f"{project}/{editor_type}/{page_type}/{activity_level}/"
    f"{granularity}/{start}/{end}"
  )
  response = _make_request("edited-pages/aggregate", args)
  items = cast(List[Dict[str, Any]], response["items"])
  results = cast(List[Dict[str, object]], items[0]["results"])
  return results


def sum_edited_pages(
  project: str,
  start: str,
  end: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
  activity_level: str = "all-activity-levels",
) -> int:
  response = edited_pages(project, "daily", start, end, editor_type, page_type)
  return sum(cast(int, item["edited_pages"]) for item in response)


def top_by_net_diff(
  project: str,
  date: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> List[Dict[str, Any]]:
  return _make_top_by_request(
    "edited-pages/top-by-net-bytes-difference",
    project,
    date,
    editor_type,
    page_type,
  )


def top_by_abs_diff(
  project: str,
  date: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> List[Dict[str, Any]]:
  return _make_top_by_request(
    "edited-pages/top-by-absolute-bytes-difference",
    project,
    date,
    editor_type,
    page_type,
  )


def top_by_edits(
  project: str,
  date: str,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types",
) -> List[Dict[str, Any]]:
  return _make_top_by_request(
    "edited-pages/top-by-edits", project, date, editor_type, page_type
  )
