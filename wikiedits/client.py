from typing import Any, Dict, List, Optional

from .api import edits_aggregate, edits_per_page, bytes_diff_abs_aggregate, bytes_diff_abs_per_page, bytes_diff_net_aggregate, bytes_diff_net_per_page


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

  response = "";

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

  response = "";

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