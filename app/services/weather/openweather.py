from datetime import datetime
from typing import Dict, List

from .base import WeatherServiceBase

class OpenWeatherService(WeatherServiceBase):
    """OpenWeather service implementation."""
    
    def __init__(self, api_key: str):
        """
        Initialize the OpenWeather service.
        
        Args:
            api_key: OpenWeather API key
        """
        super().__init__(
            api_key=api_key,
            base_url="https://api.openweathermap.org/data/2.5"
        )
        
    def get_station_metadata(self, station_id: str) -> Dict:
        """
        Get metadata for a specific OpenWeather station.
        
        Args:
            station_id: OpenWeather station identifier (city ID)
            
        Returns:
            Dictionary containing station metadata
        """
        endpoint = f"weather"
        response = self._make_request(
            endpoint,
            params={
                'id': station_id,
                'appid': self.api_key
            }
        )
        
        return {
            'id': str(response['id']),
            'name': response['name'],
            'country': response['sys']['country'],
            'latitude': response['coord']['lat'],
            'longitude': response['coord']['lon']
        }
        
    def get_temperature_data(
        self,
        station_id: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = 'hourly'
    ) -> List[Dict]:
        """
        Get temperature data for a specific OpenWeather station and time period.
        
        Args:
            station_id: OpenWeather station identifier (city ID)
            start_date: Start date for the data range
            end_date: End date for the data range
            interval: Data interval ('hourly' or 'daily')
            
        Returns:
            List of dictionaries containing temperature data
        """
        if interval not in ['hourly', 'daily']:
            raise ValueError("OpenWeather API only supports hourly or daily data")
            
        # Convert dates to Unix timestamps
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        
        endpoint = f"onecall/timemachine"
        response = self._make_request(
            endpoint,
            params={
                'lat': self.get_station_metadata(station_id)['latitude'],
                'lon': self.get_station_metadata(station_id)['longitude'],
                'dt': start_timestamp,
                'appid': self.api_key,
                'units': 'metric'  # Use Celsius
            }
        )
        
        # Transform the data into our standard format
        transformed_data = []
        for entry in response['hourly']:
            timestamp = datetime.fromtimestamp(entry['dt'])
            if start_date <= timestamp <= end_date:
                transformed_data.append({
                    'timestamp': timestamp,
                    'temperature': entry['temp'],
                    'temperature_max': entry.get('temp_max', entry['temp']),
                    'temperature_min': entry.get('temp_min', entry['temp']),
                    'station_id': station_id
                })
                
        return transformed_data 