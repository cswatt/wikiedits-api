from typing import Any, Dict, List, Optional

from .api import edits_aggregate, edits_per_page


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