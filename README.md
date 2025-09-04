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

### number of edits over time, aggregated
`edits_aggregate(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Aggregated edit counts over time.

```python
# Daily edit counts for English Wikipedia
edits = wikiedits.edits_aggregate(
    project="en.wikipedia.org",
    granularity="daily",
    start="20240101",
    end="20240131"
)
```

Returns something like:

```
[{'timestamp': '2024-01-01T00:00:00.000Z', 'edits': 177370}, 
 {'timestamp': '2024-01-02T00:00:00.000Z', 'edits': 185367}, 
 {'timestamp': '2024-01-03T00:00:00.000Z', 'edits': 185573}, 
 ...
 {'timestamp': '2024-01-30T00:00:00.000Z', 'edits': 465599}]
```

### sum of edits over time, aggregated
`sum_edits_aggregate(project, start, end, editor_type = 'all-editor-types', page_type = 'all-page-types')`

```
edits = wikiedits.sum_edits_aggregate(
    project="en.wikipedia.org",
    start="20250101",
    end="20250201"
)
```

Returns `6468782`.

### number of edits over time, per page

`edits_per_page(project, page_title, granularity, start, end, editor_type='all-editor-types')`

Edit counts over time, for a specific page.

```python
# Edits to "Climate change" article
edits = wikiedits.edits_per_page(
    project="en.wikipedia.org",
    page_title="Climate_change",
    granularity="daily", 
    start="20240101",
    end="20240131"
)
```

Returns something like:

```
[{'timestamp': '2024-01-03T00:00:00.000Z', 'edits': 1}, 
 {'timestamp': '2024-01-04T00:00:00.000Z', 'edits': 1}, 
 {'timestamp': '2024-01-05T00:00:00.000Z', 'edits': 1}, 
 ... , 
 {'timestamp': '2024-01-29T00:00:00.000Z', 'edits': 2}]
```

### net change, in bytes, aggregated

`net_change_aggregate(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Net byte changes (additions minus deletions) over time.

```python
# Net content changes across all pages
changes = wikiedits.net_change_aggregate(
    project="en.wikipedia.org",
    granularity="daily",
    start="2024-01-01", 
    end="2024-01-31"
)
```

Returns something like:

```
[{'timestamp': '2024-01-01T00:00:00.000Z', 'net_bytes_diff': 4113808}, 
{'timestamp': '2024-01-02T00:00:00.000Z', 'net_bytes_diff': 10456087}, 
{'timestamp': '2024-01-03T00:00:00.000Z', 'net_bytes_diff': 12598440}, 
...
{'timestamp': '2024-01-30T00:00:00.000Z', 'net_bytes_diff': 27934337}]
```

### net change, in bytes, per page 

`net_change_per_page(project, page_title, granularity, start, end, editor_type='all-editor-types')`

Get net byte changes for a specific page.

```
changes = wikiedits.net_change_per_page(
    project="en.wikipedia.org",
    page_title="Climate_change",
    granularity="daily",
    start="2024-01-01", 
    end="2024-01-31")
```

Returns something like:

```
[{'timestamp': '2024-01-03T00:00:00.000Z', 'net_bytes_diff': 236}, 
 {'timestamp': '2024-01-04T00:00:00.000Z', 'net_bytes_diff': 294}, 
 {'timestamp': '2024-01-05T00:00:00.000Z', 'net_bytes_diff': 232}, 
 ...
 {'timestamp': '2024-01-29T00:00:00.000Z', 'net_bytes_diff': -191}]
```

### absolute change, in bytes, aggregated 
`abs_change_aggregate(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Get absolute byte changes (total additions + deletions) over time.

### absolute change, in bytes, per page
`abs_change_per_page(project, page_title, granularity, start, end, editor_type='all-editor-types')`

Get absolute byte changes for a specific page.

### number of new pages
`new_pages(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types')`

Get counts of newly created pages.

```python
# New articles created each day
new_pages = wikiedits.new_pages(
    project="en.wikipedia.org",
    granularity="daily",
    start="2024-01-01",
    end="2024-01-31",
    page_type="content"  # Only content pages (articles)
)
```

Returns something like:

```
[{'timestamp': '2024-01-01T00:00:00.000Z', 'new_pages': 493}, 
 {'timestamp': '2024-01-02T00:00:00.000Z', 'new_pages': 648}, 
 {'timestamp': '2024-01-03T00:00:00.000Z', 'new_pages': 648}, 
 ...
 {'timestamp': '2024-01-30T00:00:00.000Z', 'new_pages': 488}]
```

### number of edited pages
`edited_pages(project, granularity, start, end, editor_type='all-editor-types', page_type='all-page-types', activity_level='all-activity-levels')`

Get counts of pages that were edited.

```python
# Pages edited each day
edited = wikiedits.edited_pages(
    project="en.wikipedia.org",
    granularity="daily",
    start="2024-01-01", 
    end="2024-01-31"
)
```

Returns something like:

```
[{'timestamp': '2024-01-01T00:00:00.000Z', 'edited_pages': 106507},
 {'timestamp': '2024-01-02T00:00:00.000Z', 'edited_pages': 112384},
 {'timestamp': '2024-01-03T00:00:00.000Z', 'edited_pages': 111012},
 ...
 {'timestamp': '2024-01-30T00:00:00.000Z', 'edited_pages': 384863}]
```
### top edited pages, by edits 
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

### top edited pages, by net content change
`top_by_net_diff(project, date, editor_type='all-editor-types', page_type='all-page-types')`

Get pages with the largest net content changes.

### top edited pages, by absolute content change 
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
- Installed anyio dependency for async support
- Fixed PostToolUse hook dependency issues
- Added claude-code-sdk dependency for hook functionality
- Added typing-extensions dependency for better type support