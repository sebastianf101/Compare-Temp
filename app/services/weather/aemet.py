from datetime import datetime
from typing import Dict, List

from .base import WeatherServiceBase

class AEMETService(WeatherServiceBase):
    """AEMET weather service implementation."""
    
    def __init__(self, api_key: str):
        """
        Initialize the AEMET weather service.
        
        Args:
            api_key: AEMET API key
        """
        super().__init__(
            api_key=api_key,
            base_url="https://opendata.aemet.es/opendata/api"
        )
        
    def get_station_metadata(self, station_id: str) -> Dict:
        """
        Get metadata for a specific AEMET weather station.
        
        Args:
            station_id: AEMET station identifier
            
        Returns:
            Dictionary containing station metadata
        """
        endpoint = f"valores/climatologicos/inventarioestaciones/todasestaciones"
        response = self._make_request(
            endpoint,
            params={'api_key': self.api_key}
        )
        
        # Get the actual data URL from the response
        data_url = response['datos']
        station_data = self._make_request(data_url)
        
        # Find the specific station
        for station in station_data:
            if station['indicativo'] == station_id:
                return {
                    'id': station['indicativo'],
                    'name': station['nombre'],
                    'province': station['provincia'],
                    'altitude': station['altitud'],
                    'latitude': station['latitud'],
                    'longitude': station['longitud']
                }
                
        raise ValueError(f"Station {station_id} not found")
        
    def get_temperature_data(
        self,
        station_id: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = 'hourly'
    ) -> List[Dict]:
        """
        Get temperature data for a specific AEMET station and time period.
        
        Args:
            station_id: AEMET station identifier
            start_date: Start date for the data range
            end_date: End date for the data range
            interval: Data interval (must be 'daily' for AEMET)
            
        Returns:
            List of dictionaries containing temperature data
        """
        if interval != 'daily':
            raise ValueError("AEMET API only supports daily data")
            
        # Format dates for AEMET API
        start_str = start_date.strftime('%Y-%m-%dT00:00:00UTC')
        end_str = end_date.strftime('%Y-%m-%dT23:59:59UTC')
        
        endpoint = f"valores/climatologicos/diarios/datos/fechaini/{start_str}/fechafin/{end_str}/estacion/{station_id}"
        response = self._make_request(
            endpoint,
            params={'api_key': self.api_key}
        )
        
        # Get the actual data URL from the response
        data_url = response['datos']
        temperature_data = self._make_request(data_url)
        
        # Transform the data into our standard format
        transformed_data = []
        for entry in temperature_data:
            transformed_data.append({
                'timestamp': datetime.strptime(entry['fecha'], '%Y-%m-%d'),
                'temperature': float(entry['tmed']),  # Average temperature
                'temperature_max': float(entry['tmax']),  # Maximum temperature
                'temperature_min': float(entry['tmin']),  # Minimum temperature
                'station_id': station_id
            })
            
        return transformed_data 