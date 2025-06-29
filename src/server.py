#!/usr/bin/env python3
"""
FRED API FastMCP Server

A FastMCP server that provides access to the Federal Reserve Economic Data (FRED) API.
This server allows querying economic data from the St. Louis Federal Reserve.
"""

import asyncio
import logging
import os
from typing import Optional
from fred import FREDAPIClient

from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fred-fastmcp-server")

# Initialize FastMCP server
mcp = FastMCP("fred_mcp_server")

# Initialize FRED client
fred_client = None

async def get_fred_client() -> FREDAPIClient:
    """Get or create FRED client"""
    global fred_client
    if fred_client is None:
        api_key = os.getenv('FRED_API_KEY')
        if not api_key:
            raise ValueError("FRED_API_KEY environment variable is required. "
                           "Get your free API key from: https://fred.stlouisfed.org/docs/api/api_key.html")
        fred_client = FREDAPIClient(api_key)
    return fred_client

@mcp.tool()
async def search_economic_data(
    search_text: str,
    limit: int = 10
) -> str:
    """
    Search for economic data series in FRED database.
    
    Args:
        search_text: Text to search for in series titles and descriptions
        limit: Maximum number of results to return (default: 10)
    """
    client = await get_fred_client()
    result = await client.search_series(search_text, limit=limit)
    
    if 'seriess' in result:
        series_list = result['seriess']
        response = f"Found {len(series_list)} series matching '{search_text}':\n\n"
        
        for series in series_list:
            response += f"**{series.get('id', 'N/A')}**: {series.get('title', 'N/A')}\n"
            response += f"  Units: {series.get('units', 'N/A')}\n"
            response += f"  Frequency: {series.get('frequency', 'N/A')}\n"
            response += f"  Last Updated: {series.get('last_updated', 'N/A')}\n\n"
    else:
        response = f"No series found matching '{search_text}'"
    
    return response

@mcp.tool()
async def get_economic_series(
    series_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100
) -> str:
    """
    Get data for a specific economic data series.
    
    Args:
        series_id: FRED series ID (e.g., 'GDP', 'UNRATE', 'CPIAUCSL')
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        limit: Maximum number of observations to return
    """
    client = await get_fred_client()
    params = {}
    
    if start_date:
        params["observation_start"] = start_date
    if end_date:
        params["observation_end"] = end_date
    params["limit"] = limit
    
    result = await client.get_series(series_id, **params)
    
    if 'observations' in result:
        observations = result['observations']
        response = f"Data for series {series_id}:\n\n"
        
        for obs in observations[-20:]:  # Show last 20 observations
            date = obs.get('date', 'N/A')
            value = obs.get('value', 'N/A')
            response += f"{date}: {value}\n"
        
        if len(observations) > 20:
            response += f"\n... and {len(observations) - 20} more observations"
    else:
        response = f"No data found for series {series_id}"
    
    return response

@mcp.tool()
async def get_series_info(series_id: str) -> str:
    """
    Get detailed information about an economic data series.
    
    Args:
        series_id: FRED series ID
    """
    client = await get_fred_client()
    result = await client.get_series_info(series_id)
    
    if 'seriess' in result and result['seriess']:
        series = result['seriess'][0]
        response = f"Series Information for {series_id}:\n\n"
        response += f"**Title**: {series.get('title', 'N/A')}\n"
        response += f"**Units**: {series.get('units', 'N/A')}\n"
        response += f"**Frequency**: {series.get('frequency', 'N/A')}\n"
        response += f"**Seasonal Adjustment**: {series.get('seasonal_adjustment', 'N/A')}\n"
        response += f"**Last Updated**: {series.get('last_updated', 'N/A')}\n"
        response += f"**Notes**: {series.get('notes', 'N/A')}\n"
    else:
        response = f"Series {series_id} not found"
    
    return response

@mcp.tool()
async def get_categories(category_id: Optional[int] = None) -> str:
    """
    Get FRED data categories.
    
    Args:
        category_id: Category ID (optional, returns root categories if not specified)
    """
    client = await get_fred_client()
    result = await client.get_categories(category_id)
    
    if 'categories' in result:
        categories = result['categories']
        response = "FRED Categories:\n\n"
        
        for cat in categories:
            response += f"**{cat.get('id', 'N/A')}**: {cat.get('name', 'N/A')}\n"
            if cat.get('parent_id'):
                response += f"  Parent ID: {cat.get('parent_id')}\n"
            response += "\n"
    else:
        response = "No categories found"
    
    return response

@mcp.tool()
async def get_releases(
    release_id: Optional[int] = None,
    limit: int = 100
) -> str:
    """
    Get all FRED data releases or information about a specific release.
    
    Args:
        release_id: Specific release ID to get detailed information (optional)
        limit: Maximum number of releases to return (default: 100)
    """
    client = await get_fred_client()
    
    if release_id:
        # Get specific release information
        result = await client.get_release(release_id)
        
        if 'releases' in result and result['releases']:
            release = result['releases'][0]
            response = f"Release Information for ID {release_id}:\n\n"
            response += f"**Name**: {release.get('name', 'N/A')}\n"
            response += f"**Press Release**: {release.get('press_release', 'N/A')}\n"
            response += f"**Link**: {release.get('link', 'N/A')}\n"
            response += f"**Notes**: {release.get('notes', 'N/A')}\n"
            response += f"**Real Time Start**: {release.get('realtime_start', 'N/A')}\n"
            response += f"**Real Time End**: {release.get('realtime_end', 'N/A')}\n"
        else:
            response = f"Release {release_id} not found"
    else:
        # Get all releases
        result = await client.get_releases(limit=limit)
        
        if 'releases' in result:
            releases = result['releases']
            response = f"FRED Releases (showing {len(releases)} releases):\n\n"
            
            for release in releases:
                response += f"**{release.get('id', 'N/A')}**: {release.get('name', 'N/A')}\n"
                if release.get('press_release') == 'true':
                    response += "  📰 Has Press Release\n"
                if release.get('link'):
                    response += f"  🔗 Link: {release.get('link')}\n"
                response += "\n"
        else:
            response = "No releases found"
    
    return response

@mcp.tool()
async def get_release_series(
    release_id: int,
    limit: int = 100
) -> str:
    """
    Get all series for a specific FRED release.
    
    Args:
        release_id: Release ID to get series for
        limit: Maximum number of series to return (default: 100)
    """
    client = await get_fred_client()
    result = await client.get_release_series(release_id, limit=limit)
    
    if 'seriess' in result:
        series_list = result['seriess']
        response = f"Series for Release {release_id} (showing {len(series_list)} series):\n\n"
        
        for series in series_list:
            response += f"**{series.get('id', 'N/A')}**: {series.get('title', 'N/A')}\n"
            response += f"  Units: {series.get('units', 'N/A')}\n"
            response += f"  Frequency: {series.get('frequency', 'N/A')}\n"
            response += f"  Last Updated: {series.get('last_updated', 'N/A')}\n\n"
    else:
        response = f"No series found for release {release_id}"
    
    return response

@mcp.tool()
async def get_release_dates(
    release_id: int,
    limit: int = 100,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """
    Get release dates for a specific FRED release.
    
    Args:
        release_id: Release ID to get dates for
        limit: Maximum number of dates to return (default: 100)
        start_date: Start date for release dates in YYYY-MM-DD format (optional)
        end_date: End date for release dates in YYYY-MM-DD format (optional)
    """
    client = await get_fred_client()
    params = {}
    
    if start_date:
        params["realtime_start"] = start_date
    if end_date:
        params["realtime_end"] = end_date
    
    result = await client.get_release_dates(release_id, limit=limit, **params)
    
    if 'release_dates' in result:
        release_dates = result['release_dates']
        response = f"Release Dates for Release {release_id} (showing {len(release_dates)} dates):\n\n"
        
        for date_info in release_dates:
            response += f"**{date_info.get('date', 'N/A')}**\n"
            if date_info.get('release_name'):
                response += f"  Release: {date_info.get('release_name')}\n"
            if date_info.get('release_id'):
                response += f"  Release ID: {date_info.get('release_id')}\n"
            response += "\n"
    else:
        response = f"No release dates found for release {release_id}"
    
    return response

@mcp.resource("fred://popular-series")
async def popular_series() -> str:
    """List of popular economic data series"""
    return """Popular FRED Economic Data Series:

GDP - Gross Domestic Product
UNRATE - Unemployment Rate
CPIAUCSL - Consumer Price Index for All Urban Consumers
FEDFUNDS - Federal Funds Rate
DGS10 - 10-Year Treasury Constant Maturity Rate
DEXUSEU - US/Euro Foreign Exchange Rate
PAYEMS - All Employees, Total Nonfarm
HOUST - Housing Starts
INDPRO - Industrial Production Index
CPILFESL - Core CPI (excluding food and energy)"""

@mcp.resource("fred://popular-releases")
async def popular_releases() -> str:
    """List of popular economic data releases"""
    return """Popular FRED Economic Data Releases:

53 - Gross Domestic Product
10 - Employment Situation
24 - Consumer Price Index
62 - Federal Reserve Economic Data
18 - Industrial Production and Capacity Utilization
20 - Housing Starts
25 - Personal Income and Outlays
50 - Flow of Funds
13 - G.17 Industrial Production and Capacity Utilization
21 - New Residential Construction
17 - Productivity and Costs
51 - Senior Loan Officer Opinion Survey
52 - Survey of Terms of Business Lending"""

# async def cleanup():
#     """Cleanup resources"""
#     global fred_client
#     if fred_client:
#         await fred_client.close()

# if __name__ == "__main__":
#     import atexit
    
#     # Register cleanup function
#     atexit.register(lambda: asyncio.run(cleanup()))
    
#     # Run the server
#     mcp.run()