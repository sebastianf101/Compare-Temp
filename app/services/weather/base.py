import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class WeatherServiceBase(ABC):
    """Base class for weather data services."""
    
    def __init__(self, api_key: str, base_url: str, max_retries: int = 3):
        """
        Initialize the weather service.
        
        Args:
            api_key: API key for the weather service
            base_url: Base URL for the weather service API
            max_retries: Maximum number of retries for failed requests
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = self._create_session(max_retries)
        
    def _create_session(self, max_retries: int) -> requests.Session:
        """
        Create a requests session with retry logic.
        
        Args:
            max_retries: Maximum number of retries
            
        Returns:
            Configured requests session
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
        
    @abstractmethod
    def get_station_metadata(self, station_id: str) -> Dict:
        """
        Get metadata for a specific weather station.
        
        Args:
            station_id: Unique identifier for the weather station
            
        Returns:
            Dictionary containing station metadata
        """
        pass
        
    @abstractmethod
    def get_temperature_data(
        self,
        station_id: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = 'hourly'
    ) -> List[Dict]:
        """
        Get temperature data for a specific station and time period.
        
        Args:
            station_id: Unique identifier for the weather station
            start_date: Start date for the data range
            end_date: End date for the data range
            interval: Data interval (e.g., 'hourly', 'daily')
            
        Returns:
            List of dictionaries containing temperature data
        """
        pass
        
    def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict:
        """
        Make a request to the weather service API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers
            
        Returns:
            JSON response from the API
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        default_headers = {
            'Accept': 'application/json',
            'User-Agent': 'Compare-Temp/1.0'
        }
        if headers:
            default_headers.update(headers)
            
        try:
            response = self.session.get(
                url,
                params=params,
                headers=default_headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to make request to {url}: {str(e)}")
            raise 