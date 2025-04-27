import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.services.weather.openweather import OpenWeatherService

@pytest.fixture
def openweather_service():
    return OpenWeatherService(api_key="test_key")

@patch('app.services.weather.openweather.OpenWeatherService._make_request')
def test_get_station_metadata(mock_request):
    """Test station metadata retrieval."""
    service = OpenWeatherService(api_key="test_key")
    
    mock_request.return_value = {
        'id': 1234,
        'name': 'Test City',
        'sys': {'country': 'AR'},
        'coord': {
            'lat': -34.6,
            'lon': -58.4
        }
    }
    
    metadata = service.get_station_metadata("1234")
    assert metadata == {
        'id': '1234',
        'name': 'Test City',
        'country': 'AR',
        'latitude': -34.6,
        'longitude': -58.4
    }

@patch('app.services.weather.openweather.OpenWeatherService._make_request')
def test_get_temperature_data(mock_request):
    """Test temperature data retrieval."""
    service = OpenWeatherService(api_key="test_key")
    
    # Mock the two-step process: first get metadata, then get temperature data
    mock_request.side_effect = [
        {  # First call: get station metadata
            'id': 1234,
            'name': 'Test City',
            'sys': {'country': 'AR'},
            'coord': {
                'lat': -34.6,
                'lon': -58.4
            }
        },
        {  # Second call: get temperature data
            'hourly': [
                {
                    'dt': 1713571200,  # 2024-04-20 00:00:00 UTC
                    'temp': 20.5,
                    'temp_max': 25.0,
                    'temp_min': 15.0
                },
                {
                    'dt': 1713574800,  # 2024-04-20 01:00:00 UTC
                    'temp': 21.0,
                    'temp_max': 26.0,
                    'temp_min': 16.0
                }
            ]
        }
    ]
    
    start_date = datetime(2024, 4, 20)
    end_date = datetime(2024, 4, 20, 1)
    data = service.get_temperature_data("1234", start_date, end_date)
    
    assert len(data) == 2
    assert data[0]['timestamp'] == datetime(2024, 4, 20, 0, 0)
    assert data[0]['temperature'] == 20.5
    assert data[0]['temperature_max'] == 25.0
    assert data[0]['temperature_min'] == 15.0
    assert data[0]['station_id'] == '1234'

@patch('app.services.weather.openweather.OpenWeatherService._make_request')
def test_get_temperature_data_invalid_interval(mock_request):
    """Test temperature data retrieval with invalid interval."""
    service = OpenWeatherService(api_key="test_key")
    start_date = datetime(2024, 4, 20)
    end_date = datetime(2024, 4, 21)
    
    with pytest.raises(ValueError, match="OpenWeather API only supports hourly or daily data"):
        service.get_temperature_data("1234", start_date, end_date, interval='weekly')

@patch('app.services.weather.openweather.OpenWeatherService._make_request')
def test_get_temperature_data_no_data_in_range(mock_request):
    """Test temperature data retrieval when no data is available in the specified range."""
    service = OpenWeatherService(api_key="test_key")
    
    # Mock the two-step process
    mock_request.side_effect = [
        {  # First call: get station metadata
            'id': 1234,
            'name': 'Test City',
            'sys': {'country': 'AR'},
            'coord': {
                'lat': -34.6,
                'lon': -58.4
            }
        },
        {  # Second call: get temperature data
            'hourly': [
                {
                    'dt': 1713571200,  # 2024-04-20 00:00:00 UTC
                    'temp': 20.5,
                    'temp_max': 25.0,
                    'temp_min': 15.0
                }
            ]
        }
    ]
    
    # Request data for a different time range
    start_date = datetime(2024, 4, 21)
    end_date = datetime(2024, 4, 22)
    data = service.get_temperature_data("1234", start_date, end_date)
    
    assert len(data) == 0

@patch('app.services.weather.openweather.OpenWeatherService._make_request')
def test_get_temperature_data_daily_interval(mock_request):
    """Test temperature data retrieval with daily interval."""
    service = OpenWeatherService(api_key="test_key")
    
    # Mock the two-step process
    mock_request.side_effect = [
        {  # First call: get station metadata
            'id': 1234,
            'name': 'Test City',
            'sys': {'country': 'AR'},
            'coord': {
                'lat': -34.6,
                'lon': -58.4
            }
        },
        {  # Second call: get temperature data
            'daily': [
                {
                    'dt': 1713571200,  # 2024-04-20 00:00:00 UTC
                    'temp': {'day': 20.5, 'max': 25.0, 'min': 15.0}
                },
                {
                    'dt': 1713657600,  # 2024-04-21 00:00:00 UTC
                    'temp': {'day': 21.0, 'max': 26.0, 'min': 16.0}
                }
            ]
        }
    ]
    
    start_date = datetime(2024, 4, 20)
    end_date = datetime(2024, 4, 21)
    data = service.get_temperature_data("1234", start_date, end_date, interval='daily')
    
    assert len(data) == 2
    assert data[0]['timestamp'] == datetime(2024, 4, 20)
    assert data[0]['temperature'] == 20.5
    assert data[0]['temperature_max'] == 25.0
    assert data[0]['temperature_min'] == 15.0
    assert data[0]['station_id'] == '1234' 