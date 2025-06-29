# FRED API MCP Server

A Model Context Protocol (MCP) server that provides access to the Federal Reserve Economic Data (FRED) API from the St. Louis Federal Reserve.

## Features

- **Search Economic Data**: Search for economic data series by keywords
- **Get Series Data**: Retrieve time series data for specific economic indicators
- **Series Information**: Get detailed metadata about economic data series
- **Browse Categories**: Explore FRED data categories
- **Get Releases**: Access information about FRED data releases
- **Release Series**: Get all series associated with a specific release
- **Release Dates**: Get release dates and schedules
- **Popular Series Resource**: Quick access to commonly used economic indicators
- **Popular Releases Resource**: Quick access to commonly used releases

## Setup

### 1. Get a FRED API Key

1. Visit [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Create a free account if you don't have one
3. Request an API key (it's free and approved instantly)

### 2. Install the Server with Claude Desktop

Install the server using uv:

```bash
uv run mcp install src/server.py
```

### 3. Add API Key Configuration

Add the following configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "fred_mcp_server": {
      "command": "/path/.local/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/path/to/dev/fred-mcp/src/server.py"
      ],
      "env": {
        "FRED_API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## Popular Series IDs

Here are some commonly used FRED series IDs:

- **GDP** - Gross Domestic Product
- **UNRATE** - Unemployment Rate
- **CPIAUCSL** - Consumer Price Index for All Urban Consumers
- **FEDFUNDS** - Federal Funds Rate
- **DGS10** - 10-Year Treasury Constant Maturity Rate
- **DEXUSEU** - US/Euro Foreign Exchange Rate
- **PAYEMS** - All Employees, Total Nonfarm
- **HOUST** - Housing Starts
- **INDPRO** - Industrial Production Index
- **CPILFESL** - Core CPI (excluding food and energy)

## Popular Release IDs

Here are some commonly used FRED release IDs:

- **53** - Gross Domestic Product
- **10** - Employment Situation
- **24** - Consumer Price Index
- **62** - Federal Reserve Economic Data
- **18** - Industrial Production and Capacity Utilization
- **20** - Housing Starts
- **25** - Personal Income and Outlays
- **50** - Flow of Funds
- **13** - G.17 Industrial Production and Capacity Utilization
- **21** - New Residential Construction

## Rate Limits

FRED API has the following rate limits:
- 120 requests per 60 seconds
- Be respectful of the API and cache results when possible

## Usage with MCP Clients

This server follows the Model Context Protocol specification and can be used with any MCP-compatible client. The server communicates via stdin/stdout and provides tools for querying economic data.

## Documentation

For detailed information about available tools and server implementation, see [SERVER.md](SERVER.md).