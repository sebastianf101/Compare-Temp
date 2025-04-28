import requests
import pandas as pd
from datetime import datetime, timedelta
import random
import os
import logging
from typing import List, Dict, Optional
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SMNDownloader:
    def __init__(self):
        self.base_url = "https://ssl.smn.gob.ar/dpd/descarga_opendata.php"
        self.stations = {
            'BUENOS AIRES OBSERVATORIO': {'lat': -34.58, 'lon': -58.48},
            'TANDIL AERO': {'lat': -37.23, 'lon': -59.25}
        }
        
    def _generate_url(self, date: datetime) -> str:
        """Generate the SMN data URL for a specific date."""
        date_str = date.strftime('%Y%m%d')
        return f"{self.base_url}?file=observaciones/datohorario{date_str}.txt"
    
    def _download_file(self, url: str) -> Optional[str]:
        """Download a file from the SMN server."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to download {url}: {str(e)}")
            return None
    
    def _parse_data(self, content: str, date: datetime) -> List[Dict]:
        """Parse the raw SMN data into a structured format."""
        data = []
        for line in content.split('\n'):
            if not line.strip():
                continue
            try:
                # Example format: "BUENOS AIRES OBSERVATORIO,20200101,0,25.4,75,1012.5"
                parts = line.strip().split(',')
                if len(parts) >= 5 and parts[0] in self.stations:
                    data.append({
                        'station': parts[0],
                        'date': date.strftime('%Y%m%d'),
                        'hour': int(parts[2]),
                        'temperature': float(parts[3]),
                        'humidity': float(parts[4]),
                        'pressure': float(parts[5]) if len(parts) > 5 else None
                    })
            except (ValueError, IndexError) as e:
                logger.warning(f"Failed to parse line: {line}. Error: {str(e)}")
        return data
    
    def download_month(self, year: int, month: int) -> pd.DataFrame:
        """Download data for a specific month."""
        all_data = []
        start_date = datetime(year, month, 1)
        
        # Handle end of month correctly
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        current_date = start_date
        while current_date <= end_date:
            url = self._generate_url(current_date)
            logger.info(f"Downloading data for {current_date.strftime('%Y-%m-%d')}")
            
            content = self._download_file(url)
            if content:
                daily_data = self._parse_data(content, current_date)
                all_data.extend(daily_data)
            
            current_date += timedelta(days=1)
            time.sleep(1)  # Be nice to the server
        
        return pd.DataFrame(all_data)

def main():
    # Create output directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Choose a random month in 2020
    month = random.randint(1, 12)
    logger.info(f"Selected month: {month}/2020")
    
    # Download the data
    downloader = SMNDownloader()
    df = downloader.download_month(2020, month)
    
    if not df.empty:
        # Save to CSV
        output_file = f'data/smn_data_2020_{month:02d}.csv'
        df.to_csv(output_file, index=False)
        logger.info(f"Data saved to {output_file}")
        
        # Print some statistics
        print("\nDownload Statistics:")
        print(f"Total records: {len(df)}")
        print("\nRecords by station:")
        print(df['station'].value_counts())
        print("\nTemperature statistics by station:")
        print(df.groupby('station')['temperature'].agg(['mean', 'min', 'max']).round(1))
    else:
        logger.error("No data was downloaded")

if __name__ == "__main__":
    main() 