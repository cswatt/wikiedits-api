# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python client library for Wikipedia editor analytics from the Wikimedia Analytics API. The library provides comprehensive access to Wikipedia editing metrics, page statistics, and top pages data.

## Project Structure

- `wikiedits/` - Main package directory
  - `__init__.py` - Package initialization, exports all public API functions
  - `api.py` - Core API client with 14 endpoint functions
  - `date_utils.py` - Date validation and formatting utilities
- `tests/` - Comprehensive test suite with 13 test modules
- `.venv/` - Python virtual environment (gitignored)
- `pyproject.toml` - Modern Python packaging configuration
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies

## Development Environment

### Setup
```bash
source .venv/bin/activate  # Activate virtual environment
pip install -r requirements-dev.txt  # Install dev dependencies
```

### Dependencies
- **Production**: `requests>=2.25.0`, `python-dateutil>=2.8.0`
- **Development**: pytest, black, flake8, isort, mypy, pre-commit, pytest-mock

### Code Quality Tools
```bash
black .           # Format code
flake8           # Lint code  
isort .          # Sort imports
mypy wikiedits   # Type checking
pytest           # Run tests
```

## Architecture

### API Client (`api.py`)
- **Core Functions**: `_make_request()`, `_build_*_args()` helper functions
- **14 Public Functions** covering all Wikimedia Analytics endpoints:
  - Aggregate metrics: `edits_aggregate`, `net_bytes_diff_aggregate`, `abs_change_aggregate`
  - Per-page metrics: `edits_per_page`, `net_bytes_diff_per_page`, `abs_change_per_page` 
  - Page counts: `new_pages`, `edited_pages`
  - Summation helpers: `sum_*` functions for totaling data
  - Top pages: `top_by_edits`, `top_by_net_diff`, `top_by_abs_diff`

### Date Utilities (`date_utils.py`)
- `validate_dates()`: Normalizes dates to YYYYMMDD format, handles granularity logic
- `split_date()`: Parses dates for top-by endpoints

### Package Interface (`__init__.py`)
Exports all 14 public functions with proper `__all__` declaration.

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

Comprehensive test coverage with 13 test modules covering:
- All API functions individually
- Date utility functions  
- Request building and error handling

Run tests: `pytest`

## Packaging

Modern Python packaging with `pyproject.toml`:
- Package name: `wikiedits-api` 
- Version: `0.1.0` (from `api.__version__`)
- Python support: >=3.8
- Includes build system, tool configurations for black/flake8/mypy/isort

## Wikimedia REST API v1
- This API requires dates to be in YYYYMMDD format
