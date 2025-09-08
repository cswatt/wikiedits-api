# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python client library for Wikipedia editor analytics from the Wikimedia Analytics API. The library provides comprehensive access to Wikipedia editing metrics, page statistics, and top pages data.

## Development practices

### Code style

- Use 2-space indentation.

## Project Structure

- `wikiedits/` - Main package directory
  - `__init__.py` - Package initialization, exports all public API functions
  - `client.py` - High-level convenience functions (edits, bytes, pages, top)
  - `api.py` - Core API client with 10 endpoint functions
  - `date_utils.py` - Date validation and formatting utilities
- `tests/` - Comprehensive test suite with 17 test modules
- `.venv/` - Python virtual environment (gitignored)
- `pyproject.toml` - Modern Python packaging configuration
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies

## Development Environment

### Setup
If no .venv exists, first create a virtual envieronment:

```bash
python3 -m venv .venv
```

Activate .venv and install requirements:

```bash
source .venv/bin/activate  # Activate virtual environment
pip install -r requirements-dev.txt  # Install dev dependencies
```

### Dependencies
- **Production**: `requests>=2.25.0`, `python-dateutil>=2.8.0`
- **Development**: pytest, flake8, isort, mypy, pre-commit, pytest-mock

### Code Quality Tools
```bash
flake8           # Lint code  
isort .          # Sort imports
mypy wikiedits   # Type checking
pytest           # Run tests
```

## Architecture

### API Client (`api.py`)
- **Core Functions**: `_make_request()`, `_build_*_args()` helper functions
- **10 Public Functions** covering all Wikimedia Analytics endpoints:
  - Aggregate metrics: `edits_aggregate`, `bytes_diff_net_aggregate`, `bytes_diff_abs_aggregate`
  - Per-page metrics: `edits_per_page`, `bytes_diff_net_per_page`, `bytes_diff_abs_per_page` 
  - Page counts: `new_pages`, `edited_pages`
  - Top pages: `top_by_edits`, `top_by_net_diff`, `top_by_abs_diff`

### Date Utilities (`date_utils.py`)
- `validate_dates()`: Normalizes dates to YYYYMMDD format, handles granularity logic
- `split_date()`: Parses dates for top-by endpoints

### Client Interface (`client.py`)
- **4 High-level Functions** for common use cases:
  - `edits()`: Get summed edit counts, routes to aggregate or per-page endpoints
  - `bytes()`: Get summed byte changes (absolute or net), routes to appropriate endpoints
  - `pages()`: Get summed page counts (new or edited), routes to appropriate endpoints
  - `top()`: Get top pages by metric (edits, net-diff, or absolute-diff)

### Package Interface (`__init__.py`)
Exports all 10 API functions and 4 client functions with proper `__all__` declaration.

## API Endpoints

Base URL: `https://wikimedia.org/api/rest_v1/metrics`

**Supported Endpoints:**
- `edits/aggregate` & `edits/per-page` - Edit counts
- `bytes-difference/net/aggregate` & `bytes-difference/net/per-page` - Net byte changes
- `bytes-difference/absolute/aggregate` & `bytes-difference/absolute/per-page` - Absolute byte changes  
- `edited-pages/new` - New page creation metrics
- `edited-pages/aggregate` - Edited pages counts
- `edited-pages/top-by-*` - Daily top pages by various metrics

## Testing

Comprehensive test coverage with 17 test modules covering:
- All 10 API functions individually
- All 4 client functions individually
- Date utility functions  
- Request building and error handling

Run tests: `pytest`

## Packaging

Modern Python packaging with `pyproject.toml`:
- Package name: `wikiedits-api` 
- Version: `0.1.0` (from `api.__version__`)
- Python support: >=3.8
- Includes build system, tool configurations for flake8/mypy/isort

## Wikimedia REST API v1
- This API requires dates to be in YYYYMMDD format