import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from app.dashboard.app import create_app
from datetime import datetime

@pytest.fixture
def app():
    """Create a test Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()

@pytest.fixture
def mock_db_session():
    """Create a mock database session."""
    with patch('app.dashboard.app.init_db') as mock_init:
        mock_session = MagicMock()
        mock_init.return_value = mock_session
        yield mock_session

def test_get_cities_success(client, mock_db_session):
    """Test successful retrieval of cities."""
    # Mock station repository
    mock_stations = [
        MagicMock(
            id=1,
            name="Test Station",
            code="TEST001",
            latitude=40.7128,
            longitude=-74.0060
        ),
        MagicMock(
            id=2,
            name="Another Station",
            code="TEST002",
            latitude=34.0522,
            longitude=-118.2437
        )
    ]
    
    mock_repo = MagicMock()
    mock_repo.get_all.return_value = mock_stations
    mock_db_session.return_value = mock_repo
    
    response = client.get('/api/cities')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['name'] == "Test Station"
    assert data[0]['code'] == "TEST001"
    assert data[0]['latitude'] == 40.7128
    assert data[0]['longitude'] == -74.0060
    assert data[1]['name'] == "Another Station"
    assert data[1]['code'] == "TEST002"
    assert data[1]['latitude'] == 34.0522
    assert data[1]['longitude'] == -118.2437

def test_get_cities_database_error(client, mock_db_session):
    """Test handling of database errors."""
    mock_repo = MagicMock()
    mock_repo.get_all.side_effect = Exception("Database error")
    mock_db_session.return_value = mock_repo
    
    response = client.get('/api/cities')
    assert response.status_code == 500
    
    data = response.get_json()
    assert data['error'] == 'Database error occurred'

def test_get_cities_unexpected_error(client, mock_db_session):
    """Test handling of unexpected errors."""
    mock_repo = MagicMock()
    mock_repo.get_all.side_effect = ValueError("Unexpected error")
    mock_db_session.return_value = mock_repo
    
    response = client.get('/api/cities')
    assert response.status_code == 500
    
    data = response.get_json()
    assert data['error'] == 'An unexpected error occurred'

def test_get_temperature_comparison_success(client, mock_db_session):
    """Test successful retrieval of temperature comparison data using real SMN data."""
    # Create SMN service instance
    from app.services.weather.smn import SMNService
    smn_service = SMNService()
    
    # Get real station metadata
    station1_metadata = smn_service.get_station_metadata("87534")  # LABOULAYE AERO
    station2_metadata = smn_service.get_station_metadata("89034")  # BASE BELGRANO II
    
    # Get real temperature data for a specific date
    start_date = datetime(2024, 4, 20)
    end_date = datetime(2024, 4, 21)
    
    station1_data = smn_service.get_temperature_data("87534", start_date, end_date)
    station2_data = smn_service.get_temperature_data("89034", start_date, end_date)
    
    # Mock the database session to return our real data
    mock_repo = MagicMock()
    mock_repo.get_by_station_and_date_range.return_value = station1_data + station2_data
    mock_db_session.return_value = mock_repo
    
    response = client.get('/api/temperature-comparison?city1_id=87534&city2_id=89034&start_date=2024-04-20&end_date=2024-04-21')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'hourly_data' in data
    assert 'min_difference' in data
    assert 'max_difference' in data
    
    # Check hourly data
    hourly_data = data['hourly_data']
    assert len(hourly_data) == 24  # 24 hours in a day
    
    # Verify the data matches our expectations
    for hour_data in hourly_data:
        hour = hour_data['hour']
        # Find corresponding data points from our real data
        station1_temp = next((d['temperature'] for d in station1_data if d['timestamp'].hour == hour), None)
        station2_temp = next((d['temperature'] for d in station2_data if d['timestamp'].hour == hour), None)
        
        if station1_temp is not None and station2_temp is not None:
            assert hour_data['city1_temperature'] == station1_temp
            assert hour_data['city2_temperature'] == station2_temp
            assert hour_data['difference'] == abs(station1_temp - station2_temp)

def test_get_temperature_comparison_missing_params(client):
    """Test handling of missing parameters."""
    response = client.get('/api/temperature-comparison')
    assert response.status_code == 400
    
    data = response.get_json()
    assert data['error'] == 'Missing required parameters'

def test_get_temperature_comparison_invalid_date(client):
    """Test handling of invalid date format."""
    response = client.get('/api/temperature-comparison?city1_id=87534&city2_id=89034&start_date=invalid&end_date=2024-04-21')
    assert response.status_code == 400
    
    data = response.get_json()
    assert data['error'] == 'Invalid date format. Use YYYY-MM-DD'

def test_get_temperature_comparison_database_error(client, mock_db_session):
    """Test handling of database errors."""
    mock_repo = MagicMock()
    mock_repo.get_by_station_and_date_range.side_effect = Exception("Database error")
    mock_db_session.return_value = mock_repo
    
    response = client.get('/api/temperature-comparison?city1_id=87534&city2_id=89034&start_date=2024-04-20&end_date=2024-04-21')
    assert response.status_code == 500
    
    data = response.get_json()
    assert data['error'] == 'Database error occurred'

def test_get_temperature_comparison_unexpected_error(client, mock_db_session):
    """Test handling of unexpected errors."""
    mock_repo = MagicMock()
    mock_repo.get_by_station_and_date_range.side_effect = ValueError("Unexpected error")
    mock_db_session.return_value = mock_repo
    
    response = client.get('/api/temperature-comparison?city1_id=87534&city2_id=89034&start_date=2024-04-20&end_date=2024-04-21')
    assert response.status_code == 500
    
    data = response.get_json()
    assert data['error'] == 'An unexpected error occurred' 