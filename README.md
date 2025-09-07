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

## Changelog

### v0.1.0 (2025-09-01)
- Initial release with full API coverage
- Type hints and comprehensive error handling
- Support for flexible date formats
- Complete test suite
- Added sum functions for aggregating metrics over time periods
