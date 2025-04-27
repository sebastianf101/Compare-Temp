import pytest
from datetime import datetime
from app.db.models import Station
from app.repositories.base import BaseRepository

def test_create(db_session):
    """Test creating a record."""
    repo = BaseRepository(Station, db_session)
    station_data = {
        'name': 'Test Station',
        'code': 'TEST001',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    station = repo.create(station_data)
    assert station.id is not None
    assert station.name == 'Test Station'
    assert station.code == 'TEST001'

def test_get(db_session):
    """Test getting a record by ID."""
    repo = BaseRepository(Station, db_session)
    station_data = {
        'name': 'Test Station',
        'code': 'TEST001',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    station = repo.create(station_data)
    retrieved = repo.get(station.id)
    assert retrieved is not None
    assert retrieved.name == 'Test Station'

def test_get_all(db_session):
    """Test getting all records."""
    repo = BaseRepository(Station, db_session)
    station_data = {
        'name': 'Test Station',
        'code': 'TEST001',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    repo.create(station_data)
    stations = repo.get_all()
    assert len(stations) == 1
    assert stations[0].name == 'Test Station'

def test_update(db_session):
    """Test updating a record."""
    repo = BaseRepository(Station, db_session)
    station_data = {
        'name': 'Test Station',
        'code': 'TEST001',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    station = repo.create(station_data)
    updated = repo.update(station.id, {'name': 'Updated Station'})
    assert updated.name == 'Updated Station'

def test_delete(db_session):
    """Test deleting a record."""
    repo = BaseRepository(Station, db_session)
    station_data = {
        'name': 'Test Station',
        'code': 'TEST001',
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    station = repo.create(station_data)
    assert repo.delete(station.id) is True
    assert repo.get(station.id) is None

def test_bulk_create(db_session):
    """Test creating multiple records in bulk."""
    repo = BaseRepository(Station, db_session)
    stations_data = [
        {
            'name': 'Station 1',
            'code': 'ST001',
            'latitude': 40.7128,
            'longitude': -74.0060
        },
        {
            'name': 'Station 2',
            'code': 'ST002',
            'latitude': 40.7129,
            'longitude': -74.0061
        }
    ]
    stations = repo.bulk_create(stations_data)
    assert len(stations) == 2
    assert stations[0].name == 'Station 1'
    assert stations[1].name == 'Station 2' 