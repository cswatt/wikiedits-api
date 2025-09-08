from typing import Any, Dict, List, Optional

from .api import (edits_aggregate, edits_per_page, bytes_diff_abs_aggregate,
                  bytes_diff_abs_per_page, bytes_diff_net_aggregate,
                  bytes_diff_net_per_page, new_pages, edited_pages,
                  top_by_edits, top_by_net_diff, top_by_abs_diff)


def edits(
  start: str,
  end: str,
  project: str = "all-projects",
  page_title: Optional[str] = None,
  editor_type: str = "all-editor-types",
) -> int:
  """
  Get summed edit counts for a project or specific page.

  Routes to either edits_aggregate() or edits_per_page() based on whether
  page_title is provided. Then sums results.

  Args:
    start: Start date
    end: End date
    project: Domain and subdomain of Wikimedia project.
    page_title: Optional page title. If provided, gets per-page stats
    editor_type: Editor type filter

  Returns:
    Integer sum of edit counts.
  """

  response = ""

  if page_title:
    response = edits_per_page(
      project=project,
      page_title=page_title,
      granularity="daily",
      start=start,
      end=end,
      editor_type=editor_type,
    )
  else:
    response = edits_aggregate(
      project=project,
      granularity="daily",
      start=start,
      end=end,
      editor_type=editor_type,
    )

  return sum(item["edits"] for item in response)


def bytes(
  start: str,
  end: str,
  diff_type: str = "absolute",
  project: str = "all-projects",
  page_title: Optional[str] = None,
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types"
) -> int:
  """
  Get summed byte difference counts for a project or specific page.

  Routes to appropriate bytes_diff_*_* function based on page_title and diff_type.
  Then sums results.

  Args:
    start: Start date
    end: End date
    diff_type: Either "absolute" or "net"
    project: Domain and subdomain of Wikimedia project
    page_title: Optional page title. If provided, gets per-page stats
    editor_type: Editor type filter
    page_type: Page type filter

  Returns:
    Integer sum of byte difference counts.
  """

  response = ""

  if page_title:
    if diff_type == "absolute":
      response = bytes_diff_abs_per_page(
        project=project,
        page_title=page_title,
        granularity="daily",
        start=start,
        end=end,
        editor_type=editor_type,
      )
    else:  # diff_type == "net"
      response = bytes_diff_net_per_page(
        project=project,
        page_title=page_title,
        granularity="daily",
        start=start,
        end=end,
        editor_type=editor_type,
      )
  else:
    if diff_type == "absolute":
      response = bytes_diff_abs_aggregate(
        project=project,
        granularity="daily",
        start=start,
        end=end,
        editor_type=editor_type,
        page_type=page_type,
      )
    else:  # diff_type == "net"
      response = bytes_diff_net_aggregate(
        project=project,
        granularity="daily",
        start=start,
        end=end,
        editor_type=editor_type,
        page_type=page_type,
      )

  # Sum the appropriate field based on diff_type
  field_name = "abs_bytes_diff" if diff_type == "absolute" else "net_bytes_diff"
  return sum(item[field_name] for item in response)


def pages(
  start: str,
  end: str,
  change_type: str = "edited",
  project: str = "all-projects",
  editor_type: str = "all-editor-types",
  activity_level: str = "all-activity-levels",
  page_type: str = "all-page-types"
) -> int:
  """
  Get summed page counts for a project.

  Routes to either new_pages() or edited_pages() based on change_type.
  Then sums results.

  Args:
    start: Start date
    end: End date
    change_type: Either "new" or "edited"
    project: Domain and subdomain of Wikimedia project
    editor_type: Editor type filter
    page_type: Page type filter

  Returns:
    Integer sum of page counts.
  """

  response = ""

  if change_type == "new":
    response = new_pages(
      project=project,
      granularity="daily",
      start=start,
      end=end,
      editor_type=editor_type,
      page_type=page_type,
    )
    return sum(item["new_pages"] for item in response)
  else:  # change_type == "edited"
    response = edited_pages(
      project=project,
      granularity="daily",
      start=start,
      end=end,
      editor_type=editor_type,
      page_type=page_type,
      activity_level=activity_level,
    )
    return sum(item["edited_pages"] for item in response)


def top(
  date: str,
  by: str = "edits",
  count: int = 10,
  project: str = "all-projects",
  editor_type: str = "all-editor-types",
  page_type: str = "all-page-types"
) -> List[Dict[str, Any]]:
  """
  Get top pages for a project on a specific date.

  Routes to appropriate top_by_* function based on the 'by' parameter.
  Returns the top 'count' results.

  Args:
    date: Date in YYYY-MM-DD format
    by: Metric to sort by - "edits", "net-diff", or "absolute-diff"
    count: Number of results to return (1-100)
    project: Domain and subdomain of Wikimedia project
    editor_type: Editor type filter
    page_type: Page type filter

  Returns:
    List of dictionaries containing top pages data.
  """

  if by == "edits":
    response = top_by_edits(
      project=project,
      date=date,
      editor_type=editor_type,
      page_type=page_type,
    )
  elif by == "net-diff":
    response = top_by_net_diff(
      project=project,
      date=date,
      editor_type=editor_type,
      page_type=page_type,
    )
  elif by == "absolute-diff":
    response = top_by_abs_diff(
      project=project,
      date=date,
      editor_type=editor_type,
      page_type=page_type,
    )
  else:
    raise ValueError(f"Invalid 'by' parameter: {by}. Must be 'edits', "
                     f"'net-diff', or 'absolute-diff'")

  return response[:count]
