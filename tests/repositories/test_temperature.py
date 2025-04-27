import pytest
from datetime import datetime, timedelta
from app.repositories.station import StationRepository
from app.repositories.temperature import TemperatureRepository

@pytest.fixture
def station(db_session):
    """Create a test station."""
    repo = StationRepository(db_session)
    station_data = {
        'name': 'Test Station',
        'code': 'TEST001',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    return repo.create(station_data)

def test_get_by_station(db_session, station):
    """Test getting temperatures by station."""
    temp_repo = TemperatureRepository(db_session)
    temps_data = [
        {
            'station_id': station.id,
            'temperature': 20.5,
            'timestamp': datetime.utcnow()
        },
        {
            'station_id': station.id,
            'temperature': 21.0,
            'timestamp': datetime.utcnow() + timedelta(hours=1)
        }
    ]
    temp_repo.bulk_create_temperatures(temps_data)
    temps = temp_repo.get_by_station(station.id)
    assert len(temps) == 2
    assert {t.temperature for t in temps} == {20.5, 21.0}

def test_get_by_station_and_date_range(db_session, station):
    """Test getting temperatures by station and date range."""
    temp_repo = TemperatureRepository(db_session)
    now = datetime.utcnow()
    temps_data = [
        {
            'station_id': station.id,
            'temperature': 20.5,
            'timestamp': now
        },
        {
            'station_id': station.id,
            'temperature': 21.0,
            'timestamp': now + timedelta(hours=1)
        },
        {
            'station_id': station.id,
            'temperature': 22.0,
            'timestamp': now + timedelta(days=1)
        }
    ]
    temp_repo.bulk_create_temperatures(temps_data)
    
    # Get temperatures for the first day
    temps = temp_repo.get_by_station_and_date_range(
        station.id,
        now,
        now + timedelta(hours=2)
    )
    assert len(temps) == 2
    assert {t.temperature for t in temps} == {20.5, 21.0}

def test_get_latest_by_station(db_session, station):
    """Test getting the latest temperature for a station."""
    temp_repo = TemperatureRepository(db_session)
    now = datetime.utcnow()
    temps_data = [
        {
            'station_id': station.id,
            'temperature': 20.5,
            'timestamp': now
        },
        {
            'station_id': station.id,
            'temperature': 21.0,
            'timestamp': now + timedelta(hours=1)
        }
    ]
    temp_repo.bulk_create_temperatures(temps_data)
    latest = temp_repo.get_latest_by_station(station.id)
    assert latest is not None
    assert latest.temperature == 21.0

def test_bulk_create_temperatures(db_session, station):
    """Test bulk creating temperature readings."""
    temp_repo = TemperatureRepository(db_session)
    now = datetime.utcnow()
    temps_data = [
        {
            'station_id': station.id,
            'temperature': 20.5,
            'timestamp': now
        },
        {
            'station_id': station.id,
            'temperature': 21.0,
            'timestamp': now + timedelta(hours=1)
        }
    ]
    temps = temp_repo.bulk_create_temperatures(temps_data)
    assert len(temps) == 2
    assert {t.temperature for t in temps} == {20.5, 21.0} 