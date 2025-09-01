# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python client library for editor analytics from the Wikimedia Analytics API. The library provides access to Wikipedia editing metrics and statistics.

## Project Structure

- `wikiedits/` - Main package directory
  - `__init__.py` - Package initialization, exports `new_pages` function
  - `api.py` - Core API client implementation
- `myenv/` - Python virtual environment (gitignored)
- `README.md` - Basic project description
- `tests` - where tests live

## Development Environment

The project uses a Python virtual environment (`myenv`) for dependency isolation. 

### Setup
```bash
source myenv/bin/activate  # Activate virtual environment
```

### Dependencies
Currently minimal dependencies (only `requests` imported in api.py for HTTP requests).

## Architecture

The library follows a simple modular design:

- **API Client** (`api.py`): Contains the core HTTP client functionality
  - `_make_request()`: Generic request handler for Wikimedia API endpoints
  - `new_pages()`: Specific function for fetching new page creation metrics
  - Constants define API base URL and endpoint patterns

- **Package Interface** (`__init__.py`): Exports public API functions for consumers

## API Endpoints

The library interfaces with the Wikimedia REST API v1 metrics endpoints:
- Base URL: `https://wikimedia.org/api/rest_v1/metrics`
- Current endpoint: `edited-pages/new` for new page creation data

## Current Limitations
- No build/packaging configuration (no setup.py, pyproject.toml, etc.)


## Wikimedia REST API v1
- This API requires dates to be in YYYYMMDD format