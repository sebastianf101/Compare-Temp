import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.services.weather.aemet import AEMETService

@pytest.fixture
def aemet_service():
    return AEMETService(api_key="test_key")

def test_generate_metadata_url():
    """Test URL generation for AEMET metadata."""
    service = AEMETService(api_key="test_key")
    expected_url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"
    assert service._generate_metadata_url() == expected_url

def test_generate_data_url():
    """Test URL generation for AEMET data."""
    service = AEMETService(api_key="test_key")
    start_date = datetime(2024, 4, 20)
    end_date = datetime(2024, 4, 21)
    station_id = "1234"
    
    expected_url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2024-04-20T00:00:00UTC/fechafin/2024-04-21T23:59:59UTC/estacion/1234"
    assert service._generate_data_url(station_id, start_date, end_date) == expected_url

@patch('requests.get')
def test_download_file(mock_get):
    """Test file download functionality."""
    service = AEMETService(api_key="test_key")
    mock_response = MagicMock()
    mock_response.content = b"test content"
    mock_get.return_value = mock_response
    
    content = service._download_file("https://test.url")
    assert content == b"test content"
    mock_get.assert_called_once_with("https://test.url")

@patch('app.services.weather.aemet.AEMETService._make_request')
def test_get_station_metadata(mock_request):
    """Test station metadata retrieval."""
    service = AEMETService(api_key="test_key")
    
    # Mock the two-step process of AEMET API
    mock_request.side_effect = [
        {'datos': 'https://data.url'},  # First call returns data URL
        [  # Second call returns actual data
            {
                'indicativo': '1234',
                'nombre': 'Test Station',
                'provincia': 'Test Province',
                'altitud': '25.0',
                'latitud': '-34.6',
                'longitud': '-58.4'
            }
        ]
    ]
    
    metadata = service.get_station_metadata("1234")
    assert metadata == {
        'id': '1234',
        'name': 'Test Station',
        'province': 'Test Province',
        'latitude': -34.6,
        'longitude': -58.4,
        'altitude': 25.0
    }

@patch('app.services.weather.aemet.AEMETService._make_request')
def test_get_temperature_data(mock_request):
    """Test temperature data retrieval."""
    service = AEMETService(api_key="test_key")
    
    # Mock the two-step process of AEMET API
    mock_request.side_effect = [
        {'datos': 'https://data.url'},  # First call returns data URL
        [  # Second call returns actual data
            {
                'fecha': '2024-04-20',
                'tmed': '20.5',
                'tmax': '25.0',
                'tmin': '15.0'
            },
            {
                'fecha': '2024-04-21',
                'tmed': '21.0',
                'tmax': '26.0',
                'tmin': '16.0'
            }
        ]
    ]
    
    start_date = datetime(2024, 4, 20)
    end_date = datetime(2024, 4, 21)
    data = service.get_temperature_data("1234", start_date, end_date)
    
    assert len(data) == 2
    assert data[0]['timestamp'] == datetime(2024, 4, 20)
    assert data[0]['temperature'] == 20.5
    assert data[0]['temperature_max'] == 25.0
    assert data[0]['temperature_min'] == 15.0
    assert data[0]['station_id'] == '1234'

@patch('app.services.weather.aemet.AEMETService._make_request')
def test_get_temperature_data_invalid_interval(mock_request):
    """Test temperature data retrieval with invalid interval."""
    service = AEMETService(api_key="test_key")
    start_date = datetime(2024, 4, 20)
    end_date = datetime(2024, 4, 21)
    
    with pytest.raises(ValueError, match="AEMET API only supports daily data"):
        service.get_temperature_data("1234", start_date, end_date, interval='hourly')

@patch('app.services.weather.aemet.AEMETService._make_request')
def test_get_station_metadata_not_found(mock_request):
    """Test station metadata retrieval when station is not found."""
    service = AEMETService(api_key="test_key")
    
    # Mock the two-step process of AEMET API
    mock_request.side_effect = [
        {'datos': 'https://data.url'},  # First call returns data URL
        [  # Second call returns actual data
            {
                'indicativo': '5678',  # Different station ID
                'nombre': 'Other Station',
                'provincia': 'Other Province',
                'altitud': '30.0',
                'latitud': '-35.0',
                'longitud': '-59.0'
            }
        ]
    ]
    
    with pytest.raises(ValueError, match="Station 1234 not found"):
        service.get_station_metadata("1234") 