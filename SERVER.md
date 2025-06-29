# FRED MCP Server Documentation

This document provides detailed information about the FRED MCP Server implementation, available tools, and development guidelines.

## Available Tools

### search_economic_data
Search for economic data series in the FRED database.

**Parameters:**
- `search_text` (required): Text to search for in series titles and descriptions
- `limit` (optional): Maximum number of results to return (default: 10)

**Example:**
```json
{
  "search_text": "unemployment rate",
  "limit": 5
}
```

### get_economic_series
Get data for a specific economic data series.

**Parameters:**
- `series_id` (required): FRED series ID (e.g., 'GDP', 'UNRATE', 'CPIAUCSL')
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `limit` (optional): Maximum number of observations to return (default: 100)

**Example:**
```json
{
  "series_id": "UNRATE",
  "start_date": "2020-01-01",
  "end_date": "2023-12-31"
}
```

### get_series_info
Get detailed information about an economic data series.

**Parameters:**
- `series_id` (required): FRED series ID

**Example:**
```json
{
  "series_id": "GDP"
}
```

### get_categories
Get FRED data categories.

**Parameters:**
- `category_id` (optional): Category ID (returns root categories if not specified)

**Example:**
```json
{
  "category_id": 32991
}
```

### get_releases
Get all FRED data releases or information about a specific release.

**Parameters:**
- `release_id` (optional): Specific release ID to get detailed information
- `limit` (optional): Maximum number of releases to return (default: 100)

**Examples:**
```json
{
  "limit": 50
}
```

```json
{
  "release_id": 53
}
```

### get_release_series
Get all series for a specific FRED release.

**Parameters:**
- `release_id` (required): Release ID to get series for
- `limit` (optional): Maximum number of series to return (default: 100)

**Example:**
```json
{
  "release_id": 53,
  "limit": 20
}
```

### get_release_dates
Get release dates for a specific FRED release.

**Parameters:**
- `release_id` (required): Release ID to get dates for
- `limit` (optional): Maximum number of dates to return (default: 100)
- `start_date` (optional): Start date for release dates in YYYY-MM-DD format
- `end_date` (optional): End date for release dates in YYYY-MM-DD format

**Example:**
```json
{
  "release_id": 53,
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```
## API Reference

For complete FRED API documentation, refer to:
- [FRED API Documentation](https://fred.stlouisfed.org/docs/api/)