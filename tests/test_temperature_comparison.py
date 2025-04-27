import pytest
from datetime import datetime, timedelta
from app.dashboard.app import create_app
from app.db.models import Station, Temperature
from app.db.init_db import init_db

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
def db_session():
    """Create a test database session."""
    session = init_db('sqlite:///:memory:')
    yield session
    session.close()

@pytest.fixture
def test_data(db_session):
    """Create test data in the database."""
    # Create stations
    station1 = Station(
        name="Test Station 1",
        code="TEST001",
        latitude=40.7128,
        longitude=-74.0060
    )
    station2 = Station(
        name="Test Station 2",
        code="TEST002",
        latitude=34.0522,
        longitude=-118.2437
    )
    db_session.add_all([station1, station2])
    db_session.commit()

    # Create temperature data
    base_date = datetime(2024, 1, 1)
    temps = []
    for day in range(7):  # One week of data
        for hour in range(24):
            date = base_date + timedelta(days=day, hours=hour)
            # Station 1: 20°C ± 5°C
            temps.append(Temperature(
                station_id=station1.id,
                temperature=20 + (hour - 12) / 2,  # Varies with hour
                timestamp=date
            ))
            # Station 2: 25°C ± 5°C
            temps.append(Temperature(
                station_id=station2.id,
                temperature=25 + (hour - 12) / 2,  # Varies with hour
                timestamp=date
            ))
    
    db_session.add_all(temps)
    db_session.commit()

    return {
        'station1_id': station1.id,
        'station2_id': station2.id,
        'start_date': base_date.strftime('%Y-%m-%d'),
        'end_date': (base_date + timedelta(days=6)).strftime('%Y-%m-%d')
    }

def test_get_temperature_comparison_success(client, test_data):
    """Test successful temperature comparison request."""
    response = client.get('/api/temperature-comparison', query_string={
        'city1_id': test_data['station1_id'],
        'city2_id': test_data['station2_id'],
        'start_date': test_data['start_date'],
        'end_date': test_data['end_date']
    })
    
    assert response.status_code == 200
    data = response.get_json()
    
    # Check response structure
    assert 'hourly_data' in data
    assert 'min_difference' in data
    assert 'max_difference' in data
    
    # Check hourly data
    assert len(data['hourly_data']) == 24
    for hour_data in data['hourly_data']:
        assert 'hour' in hour_data
        assert 'city1_temperature' in hour_data
        assert 'city2_temperature' in hour_data
        assert 'difference' in hour_data
    
    # Check min/max differences
    assert data['min_difference']['hour'] is not None
    assert data['min_difference']['difference'] is not None
    assert data['max_difference']['hour'] is not None
    assert data['max_difference']['difference'] is not None

def test_get_temperature_comparison_missing_params(client):
    """Test temperature comparison request with missing parameters."""
    response = client.get('/api/temperature-comparison')
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_get_temperature_comparison_invalid_dates(client, test_data):
    """Test temperature comparison request with invalid dates."""
    response = client.get('/api/temperature-comparison', query_string={
        'city1_id': test_data['station1_id'],
        'city2_id': test_data['station2_id'],
        'start_date': 'invalid-date',
        'end_date': 'invalid-date'
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_get_temperature_comparison_no_data(client, test_data):
    """Test temperature comparison request with no data in the date range."""
    future_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    response = client.get('/api/temperature-comparison', query_string={
        'city1_id': test_data['station1_id'],
        'city2_id': test_data['station2_id'],
        'start_date': future_date,
        'end_date': future_date
    })
    assert response.status_code == 200
    data = response.get_json()
    
    # Check that all differences are None
    assert all(hour['difference'] is None for hour in data['hourly_data'])
    assert data['min_difference']['hour'] is None
    assert data['min_difference']['difference'] is None
    assert data['max_difference']['hour'] is None
    assert data['max_difference']['difference'] is None 