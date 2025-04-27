import csv
from datetime import datetime, timedelta
from io import StringIO, BytesIO
from typing import Dict, List
import requests
import re
import zipfile

from .base import WeatherServiceBase

class SMNService(WeatherServiceBase):
    """SMN (Servicio Meteorológico Nacional) Argentina service implementation."""
    
    def __init__(self):
        """
        Initialize the SMN service.
        """
        super().__init__(
            api_key="",  # SMN doesn't require an API key
            base_url="https://ssl.smn.gob.ar/dpd"
        )
        
    def _generate_data_url(self, date: datetime) -> str:
        """
        Generate URL for daily data file.
        
        Args:
            date: Date for which to generate the URL
            
        Returns:
            URL string
        """
        date_str = date.strftime("%Y%m%d")
        return f"{self.base_url}/descarga_opendata.php?file=observaciones/datohorario{date_str}.txt"
        
    def _generate_metadata_url(self) -> str:
        """
        Generate URL for stations metadata file.
        
        Returns:
            URL string
        """
        return f"{self.base_url}/zipopendata.php?dato=estaciones"
        
    def _download_file(self, url: str) -> bytes:
        """
        Download a file from the given URL.
        
        Args:
            url: URL to download from
            
        Returns:
            File content as bytes
            
        Raises:
            requests.exceptions.RequestException: If download fails
        """
        response = requests.get(url)
        response.raise_for_status()
        return response.content
        
    def _download_and_extract_metadata(self) -> bytes:
        """
        Download and extract the stations metadata file from the zip archive.
        
        Returns:
            Content of the metadata file as bytes
            
        Raises:
            ValueError: If the metadata file cannot be found in the zip archive
        """
        zip_content = self._download_file(self._generate_metadata_url())
        
        with zipfile.ZipFile(BytesIO(zip_content)) as zip_file:
            # Look for the metadata file in the zip
            metadata_files = [f for f in zip_file.namelist() if f.endswith('.txt')]
            if not metadata_files:
                raise ValueError("No metadata file found in the zip archive")
                
            # Use the first .txt file found
            with zip_file.open(metadata_files[0]) as metadata_file:
                return metadata_file.read()
        
    def _parse_metadata_line(self, line: str) -> Dict:
        """
        Parse a line from the metadata file.
        
        Args:
            line: Line to parse
            
        Returns:
            Dictionary containing parsed metadata
            
        Raises:
            ValueError: If the line cannot be parsed
        """
        # Example line: "BASE BELGRANO II               ANTARTIDA                            -77      52       -34      37        256  89034 SAYB"
        pattern = r"(.{30})\s+(.{30})\s+(-?\d+)\s+(\d+)\s+(-?\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*)"
        match = re.match(pattern, line.strip())
        
        if not match:
            return None
            
        name, province, lat_deg, lat_min, lon_deg, lon_min, altitude, station_id, _ = match.groups()
        
        # Convert degrees and minutes to decimal degrees
        latitude = float(lat_deg) + float(lat_min) / 60
        longitude = float(lon_deg) + float(lon_min) / 60
        
        return {
            'id': station_id.strip(),
            'name': name.strip(),
            'province': province.strip(),
            'latitude': latitude,
            'longitude': longitude,
            'altitude': float(altitude)
        }
        
    def _parse_data_line(self, line: str) -> Dict:
        """
        Parse a line of data from the SMN file.
        
        Args:
            line: Line of data to parse
            
        Returns:
            Dictionary containing parsed data
        """
        # Example line: "20042025     0  14.7   71  1021.8  990    4     AEROPARQUE AERO"
        pattern = r"(\d{8})\s+(\d{1,2})\s+(-?\d+\.\d+)\s+\d+\s+\d+\.\d+\s+\d+\s+\d+\s+(.*)"
        match = re.match(pattern, line.strip())
        
        if not match:
            return None
            
        date_str, hour_str, temp_str, station = match.groups()
        date = datetime.strptime(date_str, "%d%m%Y")
        hour = int(hour_str)
        timestamp = datetime.combine(date.date(), datetime.min.time()) + timedelta(hours=hour)
        
        return {
            'timestamp': timestamp,
            'temperature': float(temp_str),
            'station_id': station.strip()
        }
        
    def get_station_metadata(self, station_id: str) -> Dict:
        """
        Get metadata for a specific SMN weather station.
        
        Args:
            station_id: SMN station identifier
            
        Returns:
            Dictionary containing station metadata
            
        Raises:
            ValueError: If station is not found
        """
        content = self._download_and_extract_metadata()
        lines = content.decode('utf-8').split('\n')
        
        # Skip header rows (first two rows)
        for line in lines[2:]:
            if not line.strip():
                continue
                
            metadata = self._parse_metadata_line(line)
            if metadata and metadata['id'] == station_id:
                return metadata
                
        raise ValueError(f"Station {station_id} not found")
        
    def get_temperature_data(
        self,
        station_id: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = 'hourly'
    ) -> List[Dict]:
        """
        Get temperature data for a specific SMN station and time period.
        
        Args:
            station_id: SMN station identifier
            start_date: Start date for the data range
            end_date: End date for the data range
            interval: Data interval (must be 'hourly' for SMN)
            
        Returns:
            List of dictionaries containing temperature data
            
        Raises:
            ValueError: If interval is not 'hourly'
        """
        if interval != 'hourly':
            raise ValueError("SMN API only supports hourly data")
            
        # Get data for each day in the range
        current_date = start_date.date()
        end_date_date = end_date.date()
        all_data = []
        
        while current_date <= end_date_date:
            url = self._generate_data_url(datetime.combine(current_date, datetime.min.time()))
            try:
                content = self._download_file(url)
                lines = content.decode('utf-8').split('\n')
                
                # Skip header rows (first two rows)
                for line in lines[2:]:
                    if not line.strip():
                        continue
                        
                    data = self._parse_data_line(line)
                    if data and data['station_id'] == station_id:
                        if start_date <= data['timestamp'] <= end_date:
                            all_data.append(data)
            except requests.exceptions.RequestException:
                # Skip days with no data
                pass
                
            current_date = datetime.combine(current_date, datetime.min.time()) + timedelta(days=1)
            current_date = current_date.date()
            
        return all_data 