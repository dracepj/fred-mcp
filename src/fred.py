
from typing import Any, Dict, Optional
import httpx

class FREDAPIClient:
    """Client for interacting with the FRED API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.stlouisfed.org/fred"
        self.client = httpx.AsyncClient()
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the FRED API"""
        params.update({
            'api_key': self.api_key,
            'file_type': 'json'
        })
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
    
    async def get_series(self, series_id: str, **kwargs) -> Dict[str, Any]:
        """Get data for a specific series"""
        params = {'series_id': series_id}
        params.update(kwargs)
        return await self._make_request('series/observations', params)
    
    async def search_series(self, search_text: str, limit: int = 10, **kwargs) -> Dict[str, Any]:
        """Search for series"""
        params = {
            'search_text': search_text,
            'limit': limit
        }
        params.update(kwargs)
        return await self._make_request('series/search', params)
    
    async def get_series_info(self, series_id: str) -> Dict[str, Any]:
        """Get information about a series"""
        params = {'series_id': series_id}
        return await self._make_request('series', params)
    
    async def get_categories(self, category_id: Optional[int] = None) -> Dict[str, Any]:
        """Get categories"""
        params = {}
        if category_id:
            params['category_id'] = category_id
        endpoint = 'category' if category_id else 'category'
        return await self._make_request(endpoint, params)
    
    async def get_releases(self, limit: int = 100, **kwargs) -> Dict[str, Any]:
        """Get all releases"""
        params = {'limit': limit}
        params.update(kwargs)
        return await self._make_request('releases', params)
    
    async def get_release(self, release_id: int) -> Dict[str, Any]:
        """Get information about a specific release"""
        params = {'release_id': release_id}
        return await self._make_request('release', params)
    
    async def get_release_series(self, release_id: int, limit: int = 100, **kwargs) -> Dict[str, Any]:
        """Get series for a specific release"""
        params = {'release_id': release_id, 'limit': limit}
        params.update(kwargs)
        return await self._make_request('release/series', params)
    
    async def get_release_dates(self, release_id: int, limit: int = 100, **kwargs) -> Dict[str, Any]:
        """Get release dates for a specific release"""
        params = {'release_id': release_id, 'limit': limit}
        params.update(kwargs)
        return await self._make_request('release/dates', params)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
