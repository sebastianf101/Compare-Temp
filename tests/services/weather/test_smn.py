import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
import zipfile
from io import BytesIO

from app.services.weather.smn import SMNService

@pytest.fixture
def smn_service():
    return SMNService()

def test_generate_data_url():
    """Test URL generation for SMN data files."""
    service = SMNService()
    date = datetime(2024, 4, 20)
    
    expected_url = "https://ssl.smn.gob.ar/dpd/descarga_opendata.php?file=observaciones/datohorario20240420.txt"
    assert service._generate_data_url(date) == expected_url

def test_generate_metadata_url():
    """Test URL generation for SMN metadata file."""
    service = SMNService()
    expected_url = "https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=estaciones"
    assert service._generate_metadata_url() == expected_url

@patch('requests.get')
def test_download_file(mock_get):
    """Test file download functionality."""
    service = SMNService()
    mock_response = MagicMock()
    mock_response.content = b"test content"
    mock_get.return_value = mock_response
    
    content = service._download_file("https://test.url")
    assert content == b"test content"
    mock_get.assert_called_once_with("https://test.url")

@patch('app.services.weather.smn.SMNService._download_file')
def test_download_and_extract_metadata(mock_download):
    """Test metadata file download and extraction."""
    service = SMNService()
    
    # Create a mock zip file with the correct format
    metadata_content = """NOMBRE                          PROVINCIA                        LATITUD LONGITUD ALTURA  INDICATIVO
texto                          texto                           grados  grados    m       texto
BASE BELGRANO II               ANTARTIDA                            -77      52       -34      37        256  89034 SAYB
LABOULAYE AERO                 CORDOBA                              -31      33       -63      22        137  87534 SAYB
"""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr('estaciones.txt', metadata_content)
    
    mock_download.return_value = zip_buffer.getvalue()
    
    content = service._download_and_extract_metadata()
    assert content.decode('utf-8') == metadata_content

@patch('app.services.weather.smn.SMNService._download_and_extract_metadata')
def test_get_station_metadata(mock_download):
    """Test station metadata retrieval."""
    service = SMNService()
    mock_download.return_value = b"""NOMBRE                          PROVINCIA                        LATITUD LONGITUD ALTURA  INDICATIVO
texto                          texto                           grados  grados    m       texto
BASE BELGRANO II               ANTARTIDA                            -77      52       -34      37        256  89034 SAYB
LABOULAYE AERO                 CORDOBA                              -31      33       -63      22        137  87534 SAYB
"""
    
    # Test BASE BELGRANO II
    metadata = service.get_station_metadata("89034")
    assert metadata == {
        'id': '89034',
        'name': 'BASE BELGRANO II',
        'province': 'ANTARTIDA',
        'latitude': -77.8667,  # -77° 52'
        'longitude': -34.6167,  # -34° 37'
        'altitude': 256
    }
    
    # Test LABOULAYE AERO
    metadata = service.get_station_metadata("87534")
    assert metadata == {
        'id': '87534',
        'name': 'LABOULAYE AERO',
        'province': 'CORDOBA',
        'latitude': -31.55,  # -31° 33'
        'longitude': -63.3667,  # -63° 22'
        'altitude': 137
    }

@patch('app.services.weather.smn.SMNService._download_file')
def test_get_temperature_data(mock_download):
    """Test temperature data retrieval."""
    service = SMNService()
    mock_download.return_value = b"""Fecha    Hora    Temp    Hum    Pres    Viento  Dir     Estacion
ddmmyyyy hh      C       %      hPa     km/h    grados  texto
20042025     0  14.7   71  1021.8  990    4     AEROPARQUE AERO
"""
    
    start_date = datetime(2024, 4, 20)
    end_date = datetime(2024, 4, 20, 1)
    data = service.get_temperature_data("1234", start_date, end_date)
    
    assert len(data) == 2
    assert data[0]['timestamp'] == datetime(2024, 4, 20, 0, 0)
    assert data[0]['temperature'] == 20.5
    assert data[0]['station_id'] == '1234'

@patch('app.services.weather.smn.SMNService._download_file')
def test_parse_2025_data(mock_download):
    """Test parsing of specific data format from April 20, 2025."""
    service = SMNService()
    mock_download.return_value = b"""Fecha    Hora    Temp    Hum    Pres    Viento  Dir     Estacion
ddmmyyyy hh      C       %      hPa     km/h    grados  texto
20042025     0  14.7   71  1021.8  990    4     AEROPARQUE AERO
"""
    
    start_date = datetime(2025, 4, 20)
    end_date = datetime(2025, 4, 20, 1)
    data = service.get_temperature_data("AEROPARQUE AERO", start_date, end_date)
    
    assert len(data) == 1
    assert data[0]['timestamp'] == datetime(2025, 4, 20, 0, 0)
    assert data[0]['temperature'] == 14.7
    assert data[0]['station_id'] == 'AEROPARQUE AERO' 