# wikiedits-api

A Python client library for accessing Wikipedia editor analytics from the Wikimedia Analytics API. 

## Installation

```bash
pip install wikiedits-api
```

Or install from source:

```bash
git clone https://github.com/cswatt/wikiedits-api.git
cd wikiedits-api
pip install -e .
```

## Example usage

```python
import wikiedits

# Get edit counts for English Wikipedia in the last 30 days
edits = wikiedits.edits_aggregate(
    project="en.wikipedia.org",
    granularity="daily",
    start="2024-01-01",
    end="2024-01-31"
)

print(edits)
```

## Functions

### edits_aggregate
`edits_aggregate(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Aggregated edit counts over time.

Returns something like:

```
[{'timestamp': '2024-01-01T00:00:00.000Z', 'edits': 177370}, 
 {'timestamp': '2024-01-02T00:00:00.000Z', 'edits': 185367}, 
 {'timestamp': '2024-01-03T00:00:00.000Z', 'edits': 185573}, 
 ...
 {'timestamp': '2024-01-30T00:00:00.000Z', 'edits': 465599}]
```

### sum_edits_aggregate
`sum_edits_aggregate(project, start, end, editor_type = 'all-editor-types', page_type = 'all-page-types')`

A sum of all edits over a period of time.

Returns an integer like `6468782`.

### edits_per_page
`edits_per_page(project, page_title, granularity, start, end, editor_type='all-editor-types')`

Edit counts over time, for a specific page.

Returns something like:

```
[{'timestamp': '2024-01-03T00:00:00.000Z', 'edits': 1}, 
 {'timestamp': '2024-01-04T00:00:00.000Z', 'edits': 1}, 
 {'timestamp': '2024-01-05T00:00:00.000Z', 'edits': 1}, 
 ... , 
 {'timestamp': '2024-01-29T00:00:00.000Z', 'edits': 2}]
```

### sum_edits_per_page
`sum_edits_per_page(project, page_title, start, end, editor_type = 'all-editor-types', page_type = 'all-page-types')`

Summed edit counts of a page over a period of time.

Returns an integer.

### net_bytes_diff_aggregate
`net_bytes_diff_aggregate(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Net byte changes (additions minus deletions) over time.

Returns something like:

```
[{'timestamp': '2024-01-01T00:00:00.000Z', 'net_bytes_diff': 4113808}, 
{'timestamp': '2024-01-02T00:00:00.000Z', 'net_bytes_diff': 10456087}, 
{'timestamp': '2024-01-03T00:00:00.000Z', 'net_bytes_diff': 12598440}, 
...
{'timestamp': '2024-01-30T00:00:00.000Z', 'net_bytes_diff': 27934337}]
```

### net_bytes_diff_per_page

`net_bytes_diff_per_page(project, page_title, granularity, start, end, editor_type='all-editor-types')`

Net byte changes (additions minus deletions) for a specific page, over time.

Returns something like:

```
[{'timestamp': '2024-01-03T00:00:00.000Z', 'net_bytes_diff': 236}, 
 {'timestamp': '2024-01-04T00:00:00.000Z', 'net_bytes_diff': 294}, 
 {'timestamp': '2024-01-05T00:00:00.000Z', 'net_bytes_diff': 232}, 
 ...
 {'timestamp': '2024-01-29T00:00:00.000Z', 'net_bytes_diff': -191}]
```

### abs_change_aggregate 
`abs_change_aggregate(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Get absolute byte changes (total additions + deletions) over time.

### abs_change_per_page
`abs_change_per_page(project, page_title, granularity, start, end, editor_type='all-editor-types')`

Get absolute byte changes (additions + deletions) for a specific page.

### new_pages
`new_pages(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Get counts of newly created pages.

Returns something like:

```
[{'timestamp': '2024-01-01T00:00:00.000Z', 'new_pages': 493}, 
 {'timestamp': '2024-01-02T00:00:00.000Z', 'new_pages': 648}, 
 {'timestamp': '2024-01-03T00:00:00.000Z', 'new_pages': 648}, 
 ...
 {'timestamp': '2024-01-30T00:00:00.000Z', 'new_pages': 488}]
```

### sum_new_pages
`sum_new_pages(project, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Sum of all new pages in a provided time frame.

Returns an integer.

### edited_pages
`edited_pages(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types', activity_level='all-activity-levels')`

Get counts of pages that were edited.

Returns something like:

```
[{'timestamp': '2024-01-01T00:00:00.000Z', 'edited_pages': 106507},
 {'timestamp': '2024-01-02T00:00:00.000Z', 'edited_pages': 112384},
 {'timestamp': '2024-01-03T00:00:00.000Z', 'edited_pages': 111012},
 ...
 {'timestamp': '2024-01-30T00:00:00.000Z', 'edited_pages': 384863}]
```

### sum_edited_pages
`sum_edited_pages(project, start, endeditor_type='all-editor-types', page_type='all-page-types', activity_level='all-activity-levels')`

Sum of edited pages in a provided time frame. Use `activity_level` to specify a certain number of edits.

### top_by_edits
`top_by_edits(project, date, editor_type='all-editor-types', page_type='all-page-types')`

Get pages with the most edits on a specific day.

```python
# Most edited pages on January 1st, 2024
top_pages = wikiedits.top_by_edits(
    project="en.wikipedia.org",
    date="2025-06-01",
    page_type="content"
)
```

Returns something like:

```
[{'page_title': 'List_of_people_named_Peter', 'edits': 293, 'rank': 1},
 {'page_title': 'Operation_Spiderweb', 'edits': 173, 'rank': 2},
 {'page_title': '1993_in_the_United_States', 'edits': 116, 'rank': 3},
 ...
 {'page_title': '2023_Terengganu_FC_season', 'edits': 26, 'rank': 100}]
```

### top_by_net_diff
`top_by_net_diff(project, date, editor_type='all-editor-types', page_type='all-page-types')`

Get pages with the largest net content changes.

### top_by_abs_diff
`top_by_abs_diff(project, date, editor_type='all-editor-types', page_type='all-page-types')`

Get pages with the largest absolute content changes.

## Parameters

### Common Parameters

- **`project`** (str): Wikipedia project (e.g., "en.wikipedia.org", "fr.wikipedia.org")
- **`granularity`** (str): Time granularity - "daily" or "monthly" 
- **`start`** (str): Start date - YYYYMMDD, ISO format, or human-readable
- **`end`** (str): End date - YYYYMMDD, ISO format, or human-readable
- **`date`** (str): Specific date for top-by functions

### Optional Filters

- **`editor_type`** (str): 
  - `"all-editor-types"` (default) - All editors
  - `"anonymous"` - Anonymous/IP editors  
  - `"group-bot"` - Bot accounts
  - `"name-bot"` - Named bot accounts
  - `"user"` - Registered users

- **`page_type`** (str):
  - `"all-page-types"` (default) - All page types
  - `"content"` - Content pages (articles)
  - `"non-content"` - Non-content pages (talk, user, etc.)

- **`activity_level`** (str): For `edited_pages()` only
  - `"all-activity-levels"` (default)
  - `"1..4-edits"` - Pages with 1-4 edits
  - `"5..24-edits"` - Pages with 5-24 edits  
  - `"25..99-edits"` - Pages with 25-99 edits
  - `"100..-edits"` - Pages with 100+ edits

## Date formats

The library accepts flexible date formats:

```python
# YYYYMMDD format
wikiedits.edits_aggregate("en.wikipedia.org", "daily", "20240101", "20240131")

# ISO format
wikiedits.edits_aggregate("en.wikipedia.org", "daily", "2024-01-01", "2024-01-31") 

# Human readable
wikiedits.edits_aggregate("en.wikipedia.org", "daily", "January 1, 2024", "January 31, 2024")
```

## Error Handling

The library provides informative error messages for common issues:

```python
import wikiedits
from requests.exceptions import RequestException

try:
    edits = wikiedits.edits_aggregate(
        project="en.wikipedia.org",
        granularity="daily", 
        start="invalid-date",
        end="2024-01-31"
    )
except ValueError as e:
    print(f"Date format error: {e}")
except RequestException as e:
    print(f"API request failed: {e}")
```

## Rate Limits

The Wikimedia API has rate limits. The library includes a 30-second timeout for requests. For high-volume usage, consider implementing delays between requests.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `python -m pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Wikimedia Analytics API Documentation](https://wikimedia.org/api/rest_v1/#/)
- [GitHub Repository](https://github.com/cswatt/wikiedits-api)

## Changelog

### v0.1.0 (2025-09-01)
- Initial release with full API coverage
- Type hints and comprehensive error handling
- Support for flexible date formats
- Complete test suite
- Added sum functions for aggregating metrics over time periods
